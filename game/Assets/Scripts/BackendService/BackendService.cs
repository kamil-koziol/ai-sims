using System;
using System.Collections;
using System.Collections.Generic;
using BackendService.dto;

namespace BackendService {
    public interface BackendService {
        public IEnumerator Game(Action<GameResponse> cb = null);
        public IEnumerator Interaction(Guid initalizingAgentId, Guid targetAgentId, Action<InteractionResponse> cb = null);
        public IEnumerator Conversation(Guid initalizingAgentId, Guid targetAgentId, Action<ConversationResponse> cb = null);
        public IEnumerator Plan(Guid agentId, Action<PlanResponse> cb = null);
    }
}