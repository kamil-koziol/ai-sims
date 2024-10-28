using System;
using Newtonsoft.Json.Linq;

namespace BackendService.dto
{
    public struct AddAgentRequest
    {

        //public String game_id;
        public String name { get; set; }
        public int age { get; set; }
        public String description { get; set; }
        public String lifestyle { get; set; }
    }
    
    public struct AddAgentResponse
    {
        public Agent agent;
    }
}