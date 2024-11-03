using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using BackendService.dto;
using UnityEngine;
using Random = System.Random;

namespace BackendService
{
    public class MockBackendService: BackendService
    {
        public IEnumerator Game(Action<GameResponse> cb = null)
        {
            GameResponse gameResponse = new GameResponse()
            {
                //id = Guid.NewGuid().ToString(),
            };

            cb?.Invoke(gameResponse);
            yield return null;
        }

        public IEnumerator Interaction(Guid initalizingAgentId, Guid targetAgentId, Action<InteractionResponse> cb = null)
        {
            Debug.Log("MockBackendService: Interaction");
            int randomStatus = UnityEngine.Random.Range(1, 5);
            InteractionResponse interactionResponse = new InteractionResponse()
            {
                status = randomStatus == 1
            };
            
            cb?.Invoke(interactionResponse);
            yield return null;
        }

        public IEnumerator Conversation(Guid initalizingAgentId, Guid targetAgentId, Action<ConversationResponse> cb = null)
        {
            ConversationResponse conversationResponse = new ConversationResponse()
            {
                initialising_agent_conversation = new string[] {"Hello", "I'm fine how are you", "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum."},
                target_agent_conversation = new string[] {"Hi", "I'm fine too", "This is a very long long long long long text"}
            };
            
            cb?.Invoke(conversationResponse);
            yield return null;
        }

        public IEnumerator Interview(Guid agentId, string question, Action<InterviewResponse> cb = null)
        {
            throw new NotImplementedException();
        }

        public IEnumerator Injection(Guid agentId, string memory, Action<InjectionResponse> cb = null)
        {
            throw new NotImplementedException();
        }

        public IEnumerator Plan(Guid agentId, Action<PlanResponse> cb = null)
        {
            
            
            Random random = new Random();
            var locations = GameManager.Instance.Regions.regionNameToSetOfPoints.Keys.ToList();


            var planNodes = new List<PlanNode>();

            const int STARTING_HOUR = 8;
            const int END_HOUR = 24;
            for (int i = STARTING_HOUR; i < END_HOUR; i++)
            {
                int randomIndex = random.Next(locations.Count);
                DateTime gameTime = TimeManager.time;
                DateTime dateTime = new DateTime(gameTime.Year, gameTime.Month, gameTime.Day);
                dateTime = dateTime.AddHours(i);
                string formattedTime = dateTime.ToString("MM/dd/yyyy, HH:mm:ss");
                
                PlanNode planNode = new PlanNode()
                {
                    location = locations[randomIndex],
                    time = formattedTime
                };
                
                planNodes.Add(planNode);
            }

            PlanResponse planResponse = new PlanResponse()
            {
                plan = planNodes.ToArray(),
            };

            cb?.Invoke(planResponse);
            yield return null;
        }

        public IEnumerator AddAgent(Agent agent, Action<AddAgentResponse> cb = null)
        {
            
            AddAgentResponse addAgentResponse = new AddAgentResponse()
            {
            };
            
            cb?.Invoke(addAgentResponse);
            yield return null;
        }
        
        public IEnumerator GetGame(Guid gameId, Action<GameResponse> cb = null)
        {
            yield return null;
        }
        
        public IEnumerator GameYaml(Action<GameResponse> cb = null)
        {
            yield return null;
        }
        
        public IEnumerator GetGameYaml(Action<string> cb = null)
        {
            yield return null;
        }
    }
}