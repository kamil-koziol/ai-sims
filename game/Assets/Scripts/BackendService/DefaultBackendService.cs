using System;
using System.Collections;
using System.Collections.Generic;
using System.Numerics;
using System.Threading;
using BackendService.dto;
using DefaultNamespace;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using UnityEngine;
using UnityEngine.Networking;
using UnityEngine.UI;

public class DefaultBackendService: MonoBehaviour, BackendService.BackendService {
    
    public static DefaultBackendService Instance;
    private static System.Guid uuid;
    private string URL = "http://127.0.0.1:8080";
    String contentTypeJson = "application/json";


    private void Awake() {
        Instance = this;
        uuid = Guid.NewGuid();
    }

    public IEnumerator Conversation(Guid initalizingAgent, Guid targetAgentId)
    {
        
        var location = new JObject();
        location["name"] = GameManager.Instance.GetAgentById(initalizingAgent).getLocation();
        
        ConversationRequest rq = new ConversationRequest
        {
            game_id = uuid.ToString(),
            initializing_agent = initalizingAgent.ToString(), 
            target_agent = targetAgentId.ToString(),
            surroundings = new JArray(),
            location = location
        };
        
        return APICall.Call<ConversationResponse>(
            URL + "/conversation", 
            JsonConvert.SerializeObject(
                rq, 
                Formatting.Indented, 
                new JsonSerializerSettings { ReferenceLoopHandling = ReferenceLoopHandling.Ignore }
            ), contentTypeJson, entries => {
                foreach(var a in entries.agent1_conversation) {
                    Debug.Log(a);
                }
            });
    }

    public IEnumerator Plan(Guid agentId) {
        var agent = GameManager.Instance.GetAgentById(agentId);
        var location = new JObject();
        location["name"] = agent.getLocation();
        PlanRequest rq = new PlanRequest
            { game_id = uuid.ToString(), agent_id = agent.ID.ToString(), location = location };

        return APICall.Call<PlanResponse>(
            URL + "/plan",
            JsonConvert.SerializeObject(
                rq,
                Formatting.Indented,
                new JsonSerializerSettings {ReferenceLoopHandling = ReferenceLoopHandling.Ignore}
            ), contentTypeJson, r => {
                foreach (var pn in r.plan) {
                    Debug.Log(pn.action);
                }
            });
    }


    public IEnumerator Interaction(Guid initalizingAgent, Guid targetAgentId)
    {
        
        var location = new JObject();
        location["name"] = GameManager.Instance.GetAgentById(initalizingAgent).getLocation();
        
        InteractionRequest rq = new InteractionRequest()
        {
            game_id = uuid.ToString(),
            initializing_agent = initalizingAgent.ToString(), 
            target_agent = targetAgentId.ToString(),
            surroundings = new JArray(),
            location = location
        };
        
        return APICall.Call<InteractionResponse>(
            URL + "/interaction", 
            JsonConvert.SerializeObject(
                rq, 
                Formatting.Indented, 
                new JsonSerializerSettings { ReferenceLoopHandling = ReferenceLoopHandling.Ignore }
            ), contentTypeJson, i => {
                Debug.Log(i.status);
            });
    }

    public IEnumerator Game() {
        
        Regions regionsObj = GameManager.Instance.GetComponent<Regions>();

        var agents = GameManager.Instance.GetAgents();

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
        
        GameRequest snapshot = new GameRequest
        {
            id = uuid.ToString(),
            locations = locations,
            agents = agentsJson
        };
        return APICall.Call<GameResponse>(
            URL + "/game",
            JsonConvert.SerializeObject(
                snapshot,
                Formatting.Indented,
                new JsonSerializerSettings {ReferenceLoopHandling = ReferenceLoopHandling.Ignore}
            ), contentTypeJson, answer => {
                Debug.Log($"INITIALISED GAME: {answer.id}");
                GameManager.Instance.ID = new Guid(answer.id);
            });
    }

}
