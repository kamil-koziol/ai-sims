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
        
        public IEnumerator Conversation(Guid initalizingAgent, Guid targetAgentId, Action<ConversationResponse> cb = null)
        {
            var location = new JObject();
            location["name"] = GameManager.Instance.GetAgentById(initalizingAgent).getLocation();
        
            ConversationRequest rq = new ConversationRequest
            {
                //time = TimeManager.time.ToUniversalTime().ToString("o", CultureInfo.InvariantCulture),
                initializing_agent = initalizingAgent.ToString(), 
                target_agent = targetAgentId.ToString(),
                surroundings = new JArray(),
                location = location
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
            var agent = GameManager.Instance.GetAgentById(agentId);
            var location = new JObject();
            location["name"] = agent.getLocation();

            // TODO: This is quick fix kacper fix pls
            if (agent.getLocation() == null) {
                location["name"] = "starting_position";
            }

            Location loc = new Location();
            loc.name = agent.getLocation();
            PlanRequest rq = new PlanRequest
            { 
                time = TimeManager.time.ToUniversalTime().ToString("o", CultureInfo.InvariantCulture),
                location = loc
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
            string path = Path.Combine(Application.persistentDataPath, "config.yaml");
            Debug.Log(path);
            string yamlContent = "";
            if (File.Exists(path))
            {
                // Load from persistent path
                yamlContent = File.ReadAllText(path);
                Debug.Log("Loaded YAML from persistent path:\n" + yamlContent);
            }
            
            return APICall.Call<GameResponse>(
                URL + "/games",
                yamlContent,
                contentTypeYaml,
                response => {
                    if(cb != null) cb(response);
                });
        }
        
        public IEnumerator SaveGameYaml(Action<string> cb = null)
        {
            return APICall.Call<string>(
                URL + "/games/" + GameManager.Instance.ID + "/yaml",
                response => {
                    if(cb != null) cb(response);
                });
        }

        public IEnumerator Interaction(Guid initalizingAgent, Guid targetAgentId, Action<InteractionResponse> cb = null)
        {
        
            var location = new JObject();
            location["name"] = GameManager.Instance.GetAgentById(initalizingAgent).getLocation();
        
            InteractionRequest rq = new InteractionRequest()
            {
                //game_id = gameId.ToString(),
                initializing_agent = initalizingAgent.ToString(), 
                target_agent = targetAgentId.ToString(),
                surroundings = new JArray(),
                location = location,
                //time = TimeManager.time.ToUniversalTime().ToString("o", CultureInfo.InvariantCulture)
            };
        
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
            
            //agentObj["id"] = state.agentId.ToString();
            AddAgentRequest rq = new AddAgentRequest
            {
                //game_id = uuid.ToString(),
                name = state.agentName,
                age = state.agentAge,
                description = state.agentDescription,
                lifestyle = state.agentLifestyle
                
            };
            return APICall.Call<AddAgentResponse>(
                URL + "/games/" + GameManager.Instance.ID/*.ToString().Replace("-", string.Empty)*/ + "/agents",
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
