using System;
using System.Collections;
using System.Collections.Generic;
using System.Numerics;
using System.Threading;
using DefaultNamespace;
using Newtonsoft.Json;
using UnityEngine;
using UnityEngine.Networking;
using UnityEngine.UI;

public class BackendService: MonoBehaviour {
    
    public static BackendService Instance;
    private static System.Guid uuid;
    private string URL = "http://127.0.0.1:4444";

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
        public String uuid;
        public Regions.RegionState regions;
        public List<Agent.AgentState> agents;
    }
    
    public struct GameSnapshotAnswer
    {
        public int status;
    }
    
    public void SendGameSnapshot()
    {
        String contentType = "application/json";
        
        Regions regionsObj = GameManager.Instance.GetComponent<Regions>();
        
        GameObject agentsGameObj = GameObject.Find("Agents");
        List<Agent.AgentState> jsonAgents = new List<Agent.AgentState>();
        Agent[] agents = agentsGameObj.GetComponentsInChildren<Agent>();

        foreach (var agent in agents)
        {
            jsonAgents.Add( agent.getAgentState());
        }
        
        GameSnapshot snapshot = new GameSnapshot
        {
            uuid = uuid.ToString(),
            regions = regionsObj.getRegionsState(),
            agents = jsonAgents
        };
        StartCoroutine(APICall.Call<GameSnapshotAnswer>(
            URL + "/init", 
            JsonConvert.SerializeObject(
                snapshot, 
                Formatting.Indented, 
                new JsonSerializerSettings { ReferenceLoopHandling = ReferenceLoopHandling.Ignore }
        ), contentType,null));
    }
}
