using System;
using System.Collections;
using BackendService.dto;
using DefaultNamespace;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;

using UnityEngine;
using UnityEngine.Networking;
using UnityEngine.UI;
using BackendService;

namespace BackendService
{
    public class DefaultBackendService: BackendService {
    
        private Guid uuid;
        private string URL = "http://127.0.0.1:80";
        String contentTypeJson = "application/json";


        public DefaultBackendService()
        {
            uuid = Guid.NewGuid();
        }
        public IEnumerator Conversation(Guid initalizingAgent, Guid targetAgentId, Action<ConversationResponse> cb = null)
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
                ), contentTypeJson, response => {
                    if(cb != null) cb(response);

                });
        }

        public IEnumerator Plan(Guid agentId, Action<PlanResponse> cb = null) {
            var agent = GameManager.Instance.GetAgentById(agentId);
            var location = new JObject();
            location["name"] = agent.getLocation();

            // TODO: This is quick fix kacper fix pls
            if (agent.getLocation() == null) {
                location["name"] = "starting_position";
            }
            PlanRequest rq = new PlanRequest
                { game_id = uuid.ToString(), agent_id = agent.ID.ToString(), location = location };

            return APICall.Call<PlanResponse>(
                URL + "/plan",
                JsonConvert.SerializeObject(
                    rq,
                    Formatting.Indented,
                    new JsonSerializerSettings {ReferenceLoopHandling = ReferenceLoopHandling.Ignore}
                ), contentTypeJson, response => {
                    if(cb != null) cb(response);
                });
        }


        public IEnumerator Interaction(Guid initalizingAgent, Guid targetAgentId, Action<InteractionResponse> cb = null)
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
                ), contentTypeJson, response => {
                    if(cb != null) cb(response);
                });
        }

        public IEnumerator Game(Action<GameResponse> cb = null) {
        
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
                ), contentTypeJson, response => {
                    if(cb != null) cb(response);
                });
        }

        public IEnumerator AddAgent(Agent agent, Action<AddAgentResponse> cb = null)
        {
            JObject agentObj = new JObject();
            var state = agent.getAgentState();
            
            agentObj["id"] = state.agentId.ToString();
            agentObj["name"] = state.agentName;
            agentObj["age"] = state.agentAge;
            agentObj["description"] = state.agentDescription;
            agentObj["lifestyle"] = state.agentLifestyle;
            AddAgentRequest rq = new AddAgentRequest
            {
                game_id = uuid.ToString(),
                agent = agentObj
            };
            
            return APICall.Call<AddAgentResponse>(
                URL + "/game/add_agent",
                JsonConvert.SerializeObject(
                    rq,
                    Formatting.Indented,
                    new JsonSerializerSettings {ReferenceLoopHandling = ReferenceLoopHandling.Ignore}
                ), contentTypeJson, response => {
                    if(cb != null) cb(response);
                });
        }

    }
}
