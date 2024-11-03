using System;
using System.Collections;
using System.Collections.Generic;
using BackendService.dto;

namespace BackendService {
    public interface BackendService {
        public IEnumerator Game(Action<GameResponse> cb = null);
        public IEnumerator GetGame(Guid gameId, Action<GameResponse> cb = null);
        public IEnumerator GameYaml(Action<GameResponse> cb = null);
        
        public IEnumerator GetGameYaml(Action<string> cb = null);

        public IEnumerator Interaction(Guid initalizingAgentId, Guid targetAgentId, Action<InteractionResponse> cb = null);
        public IEnumerator Conversation(Guid initalizingAgentId, Guid targetAgentId, Action<ConversationResponse> cb = null);
        public IEnumerator Interview(Guid agentId, String question, Action<InterviewResponse> cb = null);
        public IEnumerator Injection(Guid agentId, String memory, Action<InjectionResponse> cb = null);
        public IEnumerator AddAgent(Agent agent, Action<AddAgentResponse> cb = null);
        public IEnumerator Plan(Guid agentId, Action<PlanResponse> cb = null);
    }
}