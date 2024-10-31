using System;
using System.Collections.Generic;
using Newtonsoft.Json.Linq;

namespace BackendService.dto {
    [Serializable]
    public struct InteractionRequest
    {
        public String initializing_agent_id;
        public String target_agent_id;
        public List<String> surroundings;
        public Location location;
        public String time;
    }
    
    [Serializable]
    public struct InteractionResponse {
        public bool status;
    }

}