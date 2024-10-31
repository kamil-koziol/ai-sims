using System;
using System.Collections;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using BackendService.dto;
using DefaultNamespace;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;

using UnityEngine;

namespace BackendService
{
    public class DefaultBackendService: BackendService {
        
        private string URL = "http://127.0.0.1:80";
        String contentTypeJson = "application/json";
        String contentTypeYaml = "application/yaml";
        private String path = Path.Combine(Application.persistentDataPath, "config.yaml");
        
        public IEnumerator Conversation(Guid initalizingAgent, Guid targetAgentId, Action<ConversationResponse> cb = null)
        {
            Location loc = new Location();
            loc.name = GameManager.Instance.GetAgentById(initalizingAgent).getLocation();
        
            ConversationRequest rq = new ConversationRequest
            {
                time = TimeManager.getTimeISO(),
                initializing_agent_id = initalizingAgent.ToString(), 
                target_agent_id = targetAgentId.ToString(),
                surroundings = new List<String>(),
                location = loc
            };
        
            return APICall.Call<ConversationResponse>(
                URL + "/games/" + GameManager.Instance.ID +  "/conversations", 
                JsonConvert.SerializeObject(
                    rq, 
                    Formatting.Indented, 
                    new JsonSerializerSettings { ReferenceLoopHandling = ReferenceLoopHandling.Ignore }
                ), contentTypeJson, response => {
                    if(cb != null) cb(response);

                });
        }

        public IEnumerator Plan(Guid agentId, Action<PlanResponse> cb = null) {
            PlanRequest rq = new PlanRequest
            { 
                time = TimeManager.getTimeISO()
            };
            
            Debug.Log(JsonConvert.SerializeObject(
                rq,
                Formatting.Indented,
                new JsonSerializerSettings {ReferenceLoopHandling = ReferenceLoopHandling.Ignore}
            ));
            return APICall.Call<PlanResponse>(
                URL + "/games/" + GameManager.Instance.ID + "/agents/" + agentId + "/plans",
                JsonConvert.SerializeObject(
                    rq,
                    Formatting.Indented,
                    new JsonSerializerSettings {ReferenceLoopHandling = ReferenceLoopHandling.Ignore}
                ), contentTypeJson, response => {
                    if(cb != null) cb(response);
                });
        }


        public IEnumerator GetGame(Guid gameId, Action<GameResponse> cb = null)
        {
            return APICall.Call<GameResponse>(
                URL + "/games/" + gameId,
                response => {
                    if(cb != null) cb(response);
                });
        }
        
        public IEnumerator GameYaml(Action<GameResponse> cb = null)
        {
            Debug.Log(path);
            string yamlContent = "";
            if (File.Exists(path))
            {
                // Load from persistent path
                yamlContent = File.ReadAllText(path);
                Debug.Log("Loaded YAML from persistent path:\n" + yamlContent);
            }
            else
            {
                Debug.LogError("No YAML file found at " + path + "!");
                return null;
            }
            
            return APICall.Call<GameResponse>(
                URL + "/games/yaml",
                yamlContent,
                contentTypeYaml,
                response => {
                    if(cb != null) cb(response);
                });
        }
        
        public IEnumerator GetGameYaml(Action<string> cb = null)
        {
            Debug.Log(path);
            return APICall.Call<string>(
                URL + "/games/" + GameManager.Instance.ID + "/yaml",
                response => {
                    File.WriteAllText(path, response);
                    if(cb != null) cb(response);
                });
        }

        public IEnumerator Interaction(Guid initalizingAgent, Guid targetAgentId, Action<InteractionResponse> cb = null)
        {
            Location loc = new Location();
            loc.name = GameManager.Instance.GetAgentById(initalizingAgent).getLocation();
        
            InteractionRequest rq = new InteractionRequest()
            {
                initializing_agent_id = initalizingAgent.ToString(), 
                target_agent_id = targetAgentId.ToString(),
                surroundings = new List<string>(),
                location = loc,
                time = TimeManager.getTimeISO()
            };
        
            Debug.Log(JsonConvert.SerializeObject(
                rq, 
                Formatting.Indented, 
                new JsonSerializerSettings { ReferenceLoopHandling = ReferenceLoopHandling.Ignore }
            ));
            return APICall.Call<InteractionResponse>(
                URL + "/games/" + GameManager.Instance.ID + "/interactions", 
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
                locations = locations,
                agents = agentsJson
            };
            return APICall.Call<GameResponse>(
                URL + "/games",
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
            
            AddAgentRequest rq = new AddAgentRequest
            {
                name = state.agentName,
                age = state.agentAge,
                description = state.agentDescription,
                lifestyle = state.agentLifestyle
                
            };
            return APICall.Call<AddAgentResponse>(
                URL + "/games/" + GameManager.Instance.ID + "/agents",
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
