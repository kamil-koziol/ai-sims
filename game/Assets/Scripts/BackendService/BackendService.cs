using System;
using System.Collections;
using System.Collections.Generic;
using BackendService.dto;

namespace BackendService {
    public interface BackendService {
        public IEnumerator Game();
        public IEnumerator Interaction(Guid initalizingAgentId, Guid targetAgentId);
        public IEnumerator Conversation(Guid initalizingAgentId, Guid targetAgentId);
        public IEnumerator Plan(Guid agentId);
    }
}