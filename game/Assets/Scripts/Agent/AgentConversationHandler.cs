using System;
using System.Collections.Generic;
using BackendService.dto;
using Dialog;
using Dialog.Mappers;
using UnityEngine;

namespace DefaultNamespace.Agent
{
    public class AgentConversationHandler : MonoBehaviour
    {
        public float minTimeBetweenConversations = 90.0f;
        public float maxTimeBetweenConversations = 150.0f;
        public float cooldownBetweenInteractions = 60.0f;
        
        private static Dictionary<Guid, float> agentIdToLastConversationTime = new Dictionary<Guid, float>();
        private float interactionCooldown = 0.0f; 
        private FieldOfView fieldOfView;
        private global::Agent agent;

        private void Start()
        {
            agent = GetComponent<global::Agent>();
            fieldOfView = GetComponent<FieldOfView>();
        }

        void AddInteractionCooldown() {
            interactionCooldown = Time.time + cooldownBetweenInteractions;
        }

        void AddConversationCooldown(global::Agent initializingAgent, global::Agent targetAgent) {
            
            agentIdToLastConversationTime[initializingAgent.getId()] = Time.time + UnityEngine.Random.Range(minTimeBetweenConversations, maxTimeBetweenConversations);
            agentIdToLastConversationTime[targetAgent.getId()] = Time.time + UnityEngine.Random.Range(minTimeBetweenConversations, maxTimeBetweenConversations);
            Debug.Log("Time: " + Time.time + " Time to next convo: Initializing agent: " + agentIdToLastConversationTime[agent.getId()] + " Target agent: " + agentIdToLastConversationTime[targetAgent.getId()]);
        }

        void Interact(global::Agent targetAgent, Action<bool> _cb) {
            GameManager.Instance.registerCoroutine(
                GameManager.Instance.getBackendService().Interaction(agent.getId(), targetAgent.getId(), cb => {
                    _cb(cb.status);
                    AddInteractionCooldown();
                })
                );
        }

        void Converse(global::Agent targetAgent) {
            Debug.Log("Conversation started! Initializing agent: " + agent.getId() + " Target agent: " + targetAgent.getId());
            GameManager.Instance.registerCoroutine(
                GameManager.Instance.getBackendService().Conversation(agent.getId(), targetAgent.getId(),
                    response =>
                    {
                        Dialog.Dialog dialog = DialogMapper.Map(agent.getId(), targetAgent.getId(), response);
                        DialogManager.Instance.OpenDialog(dialog);
                        AddConversationCooldown(agent, targetAgent); 
                    })
            );

        }

        void Update()
        {

            if (GameManager.Instance.GameState != GameState.PLAYING) return;
            
            global::Agent closestAgent = fieldOfView.GetClosestTarget();
            if (closestAgent == null) return;

            bool canInteract = Time.time > interactionCooldown;
            if(!canInteract) return;

            bool canStartConversation = false;
            if (agentIdToLastConversationTime.ContainsKey(closestAgent.getId())) {
                canStartConversation = Time.time >= agentIdToLastConversationTime[closestAgent.getId()];
            }
            else {
                canStartConversation = true;
            }
            
            if(!canStartConversation) return;
           
            Interact(closestAgent, shouldInteract => {
                if(!shouldInteract) return;
                
                Converse(closestAgent);
            });
        }
    }
}