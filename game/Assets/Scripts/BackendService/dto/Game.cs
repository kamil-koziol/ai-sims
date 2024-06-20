using System;
using Newtonsoft.Json.Linq;

namespace BackendService.dto {
    [Serializable]
    public struct GameRequest
    {
        public String id;
        public JArray locations;
        public JArray agents;
    }
    
    [Serializable] 
    public struct GameResponse
    {
        public String id;
    }
}