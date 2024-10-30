using System;
using System.Collections.Generic;
using Newtonsoft.Json.Linq;

namespace BackendService.dto {
    [Serializable]
    public struct PlanNode {
        public String time { get; set; }
        public String location { get; set; }
    }
    
    [Serializable]
    public struct PlanRequest {
        public String time { get; set; }
        public Location location { get; set; }
    }
    // [Serializable]
    // public struct PlanRequest {
    //     public PlanNode plan;
    // }
    
    public struct PlanResponse
    {
        public PlanNode[] plan;
    }

}