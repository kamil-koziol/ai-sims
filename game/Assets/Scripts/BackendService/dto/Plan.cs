using System;
using Newtonsoft.Json.Linq;

namespace BackendService.dto {
    [Serializable]
    public struct PlanRequest
    {
        public String game_id;
        public String agent_id;
        public JObject location;
    }
    
    [Serializable]
    public struct PlanNode {
        public String action;
    }
    [Serializable]
    public struct PlanResponse {
        public PlanNode[] plan;
    }

}