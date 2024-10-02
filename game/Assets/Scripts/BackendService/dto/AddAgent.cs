using System;
using Newtonsoft.Json.Linq;

namespace BackendService.dto
{
    public struct AddAgentRequest
    {
        public String game_id;
        public JObject agent;
    }
    
    public struct AddAgentResponse
    {
        public String game_id;
    }
}