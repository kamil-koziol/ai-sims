using System;
using System.Collections.Generic;
using Newtonsoft.Json.Linq;

namespace BackendService.dto {
    [Serializable]
    public struct ConversationRequest
    {
        public String time;
        public String initializing_agent_id;
        public String target_agent_id;
        public List<String> surroundings;
        public Location location;
    }

    [Serializable]
    public struct ConversationResponse {
        public string[] initialising_agent_conversation;
        public string[] target_agent_conversation;
    }

}