using System;
using System.Collections;
using System.Collections.Generic;
using System.Numerics;
using System.Threading;
using DefaultNamespace;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using UnityEngine;
using UnityEngine.Networking;
using UnityEngine.UI;

public class BackendService: MonoBehaviour {
    
    public static BackendService Instance;
    private static System.Guid uuid;
    private string URL = "http://127.0.0.1:8080";
    String contentTypeJson = "application/json";


    private void Awake() {
        Instance = this;
        uuid = Guid.NewGuid();
    }

    struct Test {
        private string text;
    }

    public void GetMock() {
        StartCoroutine(APICall.Call<Test>(URL + "/mock", null));
    }

    [Serializable]
    public struct GameSnapshot
    {
        public String id;
        public JArray locations;
        public JArray agents;
    }
    
    public struct GameSnapshotAnswer
    {
        public String id;
    }
    
    public IEnumerator SendGameSnapshot()
    {
        
        Regions regionsObj = GameManager.Instance.GetComponent<Regions>();
        
        GameObject agentsGameObj = GameObject.Find("Agents");
        Agent[] agents = agentsGameObj.GetComponentsInChildren<Agent>();

        JArray agentsJson = new JArray();
        foreach (var agent in agents)
        {
            JObject objectAgent = new JObject();
            var state = agent.getAgentState();
            objectAgent["id"] = state.agentId.ToString();
            objectAgent["name"] = state.agentName;
            objectAgent["age"] = state.agentAge;
            objectAgent["description"] = state.agentDescription;
            objectAgent["lifestyle"] = state.agentLifestyle;
            agentsJson.Add(objectAgent);
        }
        
        JArray locations = new JArray();
        foreach (var region in regionsObj.getRegionsState().regions)
        {
            JObject objRegion = new JObject();
            objRegion["name"] = region;
            locations.Add(objRegion);
        }
        
        GameSnapshot snapshot = new GameSnapshot
        {
            id = uuid.ToString(),
            locations = locations,
            agents = agentsJson
        };
        return APICall.Call<GameSnapshotAnswer>(
            URL + "/game", 
            JsonConvert.SerializeObject(
                snapshot, 
                Formatting.Indented, 
                new JsonSerializerSettings { ReferenceLoopHandling = ReferenceLoopHandling.Ignore }
        ), contentTypeJson,null);
    }

    public struct PlanRequest
    {
        public String game_id;
        public String agent_id;
        public JObject location;
    }
    
    public List<IEnumerator> RequestPlanForAllAgents()
    {
        Agent[] agents = GameManager.Instance.GetAllAgents();
        List<IEnumerator> coroutines = new List<IEnumerator>();
        foreach (var agent in agents)
        {
            var location = new JObject();
            location["name"] = agent.getLocation();
            PlanRequest rq = new PlanRequest
                { game_id = uuid.ToString(), agent_id = agent.ID.ToString(), location = location };
            
            coroutines.Add(APICall.Call<Agent.PlanEntry[]>(
                URL + "/plan", 
                JsonConvert.SerializeObject(
                    rq, 
                    Formatting.Indented, 
                    new JsonSerializerSettings { ReferenceLoopHandling = ReferenceLoopHandling.Ignore }
                ), contentTypeJson, agent.assingPlanToAgent));
        }

        return coroutines;
    }

    public struct ConversationRequest
    {
        public String game_id;
        public String initializing_agent;
        public String target_agent;
        public JArray surroundings;
        public JObject location;
    }
    
    public IEnumerator handleConversation(Guid initalizingAgent, Guid targetAgentId)
    {
        
        var location = new JObject();
        location["name"] = AgentManager.Instance.GetAgentById(initalizingAgent).getLocation();
        
        ConversationRequest rq = new ConversationRequest
        {
            game_id = uuid.ToString(),
            initializing_agent = initalizingAgent.ToString(), 
            target_agent = targetAgentId.ToString(),
            surroundings = new JArray(),
            location = location
        };
        
        return APICall.Call<Agent.PlanEntry[]>(
            URL + "/conversation", 
            JsonConvert.SerializeObject(
                rq, 
                Formatting.Indented, 
                new JsonSerializerSettings { ReferenceLoopHandling = ReferenceLoopHandling.Ignore }
            ), contentTypeJson, null);
    }
    
    public IEnumerator handleInteraction(Guid initalizingAgent, Guid targetAgentId)
    {
        
        var location = new JObject();
        location["name"] = AgentManager.Instance.GetAgentById(initalizingAgent).getLocation();
        
        ConversationRequest rq = new ConversationRequest
        {
            game_id = uuid.ToString(),
            initializing_agent = initalizingAgent.ToString(), 
            target_agent = targetAgentId.ToString(),
            surroundings = new JArray(),
            location = location
        };
        
        return APICall.Call<Agent.PlanEntry[]>(
            URL + "/interaction", 
            JsonConvert.SerializeObject(
                rq, 
                Formatting.Indented, 
                new JsonSerializerSettings { ReferenceLoopHandling = ReferenceLoopHandling.Ignore }
            ), contentTypeJson, null);
    }
}
