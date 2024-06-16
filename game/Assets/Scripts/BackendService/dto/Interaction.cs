using System;
using Newtonsoft.Json.Linq;

namespace BackendService.dto {
    [Serializable]
    public struct InteractionRequest
    {
        public String game_id;
        public String initializing_agent;
        public String target_agent;
        public JArray surroundings;
        public JObject location;
    }
    
    [Serializable]
    public struct InteractionResponse {
        public string[] agent1_conversation;
        public string[] agent2_conversation;
    }

}