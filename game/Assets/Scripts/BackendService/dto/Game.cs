using System;
using System.Collections.Generic;
using Newtonsoft.Json.Linq;

namespace BackendService.dto {
    [Serializable]
    public struct GameRequest
    {
        public String id;
        public JArray locations;
        public JArray agents;
    }

    public struct Agent
    {
        public String id { get; set; }
        public String name { get; set; }
        public int age { get; set; }
        public String description { get; set; }
        public String lifestyle { get; set; }

    }

    public struct Location
    {
        public String name { get; set; }
    }

    [Serializable]
    public struct Game
    {
        public String id { get; set; }
        public List<Agent> agents { get; set; }
        public List<Location> locations { get; set; }
    }
    
    [Serializable] 
    public struct GameResponse
    {
        public Game game;
    }
}