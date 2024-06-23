using System;
using System.Collections.Generic;
using Dialog;
using Dialog.Mappers;
using UnityEngine;

namespace DefaultNamespace.Agent
{
    public class AgentConversationHandler : MonoBehaviour
    {
        public float minTimeBetweenConversations = 30.0f;
        public float maxTimeBetweenConversations = 120.0f;
        
        private static Dictionary<Guid, float> agentIdToLastConversationTime = new Dictionary<Guid, float>();
        private FieldOfView fieldOfView;
        private global::Agent agent;

        private void Start()
        {
            agent = GetComponent<global::Agent>();
            fieldOfView = GetComponent<FieldOfView>();
        }

        void Update()
        {

            global::Agent closestAgent = fieldOfView.GetClosestTarget();
            
            if (closestAgent == null) return;

            if ( agentIdToLastConversationTime.ContainsKey(agent.getId()) && agentIdToLastConversationTime.ContainsKey(closestAgent.getId()))
            {
                if (Time.time >= agentIdToLastConversationTime[agent.getId()])
                {
                    handleConversation(closestAgent);
                }
            }
            else
            {
                handleConversation(closestAgent);
            }
        }

        private void handleConversation(global::Agent closestAgent)
        {

            if (GameManager.Instance.GameState != GameState.PLAYING) return;

            bool startConversation = false;

            GameManager.Instance.registerCoroutine(
                GameManager.Instance.getBackendService().Interaction(agent.getId(), closestAgent.getId(),
                    response =>
                    {
                        startConversation = response.status;
                    })
            );
            
            if (!startConversation) 
                return;
            
            Debug.Log("Conversation started! Initializing agent: " + agent.getId() + " Target agent: " + closestAgent.getId());
            GameManager.Instance.registerCoroutine(
                GameManager.Instance.getBackendService().Conversation(agent.getId(), closestAgent.getId(),
                    response =>
                    {
                        Dialog.Dialog dialog = DialogMapper.Map(agent.getId(), closestAgent.getId(), response);
                        DialogManager.Instance.OpenDialog(dialog);
                    })
            );
            agentIdToLastConversationTime[agent.getId()] = Time.time + UnityEngine.Random.Range(minTimeBetweenConversations, maxTimeBetweenConversations);
            agentIdToLastConversationTime[closestAgent.getId()] = Time.time + UnityEngine.Random.Range(minTimeBetweenConversations, maxTimeBetweenConversations);
            
            Debug.Log("Time: " + Time.time + " Time to next convo: Initializing agent: " + agentIdToLastConversationTime[agent.getId()] + " Target agent: " + agentIdToLastConversationTime[closestAgent.getId()]);
        }
    }
}