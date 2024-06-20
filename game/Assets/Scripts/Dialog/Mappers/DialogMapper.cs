using System;
using BackendService.dto;

namespace Dialog.Mappers
{
    public class DialogMapper
    {
        public static Dialog Map(Guid initializingAgendId, Guid targetAgentId, ConversationResponse response)
        {
            var dialogBuilder = new Dialog.Builder();
            var iAgent = GameManager.Instance.GetAgentById(initializingAgendId);
            dialogBuilder.AddActor(new Actor() {
                id = 0,
                name = iAgent.getAgentState().agentName,
                sprite = iAgent.getAgentState().agentSprite
            });
                
            var tAgent = GameManager.Instance.GetAgentById(targetAgentId);
            dialogBuilder.AddActor(new Actor() {
                id = 1,
                name = tAgent.getAgentState().agentName,
                sprite = tAgent.getAgentState().agentSprite
            });


            int shorterConversationLength =
                Math.Min(response.agent1_conversation.Length, response.agent2_conversation.Length);

            int i;
            for (i = 0; i < shorterConversationLength; i++) {
                dialogBuilder.AddMessage(new Message() {
                    actorId = 0,
                    message = response.agent1_conversation[i]
                });
                    
                dialogBuilder.AddMessage(new Message() {
                    actorId = 1,
                    message = response.agent2_conversation[i]
                });
            }

            // Adding the rest of messages
            while(i < response.agent1_conversation.Length) {
                dialogBuilder.AddMessage(new Message() {
                    actorId = 0,
                    message = response.agent1_conversation[i]
                });
                i++;
            }

            var dialog =dialogBuilder.Build();
            return dialog;
        }
    }
}