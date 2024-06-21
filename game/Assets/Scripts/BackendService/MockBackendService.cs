using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using BackendService.dto;

namespace BackendService
{
    public class MockBackendService: BackendService
    {
        public IEnumerator Game(Action<GameResponse> cb = null)
        {
            GameResponse gameResponse = new GameResponse()
            {
                id = Guid.NewGuid().ToString(),
            };

            cb?.Invoke(gameResponse);
            yield return null;
        }

        public IEnumerator Interaction(Guid initalizingAgentId, Guid targetAgentId, Action<InteractionResponse> cb = null)
        {
            Random rng = new Random();
            InteractionResponse interactionResponse = new InteractionResponse()
            {
                status = rng.NextDouble() > 0.5f
            };
            
            cb?.Invoke(interactionResponse);
            yield return null;
        }

        public IEnumerator Conversation(Guid initalizingAgentId, Guid targetAgentId, Action<ConversationResponse> cb = null)
        {
            ConversationResponse conversationResponse = new ConversationResponse()
            {
agent1_conversation = new string[] {"Hello", "I'm fine how are you", "This is a very long long long long long text"},
agent2_conversation = new string[] {"Hi", "I'm fine too", "This is a very long long long long long text"}

            };
            
            cb?.Invoke(conversationResponse);
            yield return null;
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
    }
}