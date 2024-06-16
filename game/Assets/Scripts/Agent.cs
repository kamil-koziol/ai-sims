using System;
using System.Collections;
using System.Collections.Generic;
using Newtonsoft.Json;
using Unity.VisualScripting;
using UnityEngine;

[RequireComponent(typeof(UnityEngine.AI.NavMeshAgent)), Serializable]
public class Agent : MonoBehaviour {
    public Guid ID;
    
    [SerializeField] private Transform currentMovingTarget;
    private bool update = true;
    [SerializeField] private int age;
    [SerializeField] private String description;
    [SerializeField] private String lifestyle;
    [SerializeField] private String agentName;
    [SerializeField] private PlanEntry[] planForDay;
    private void Awake() {
        ID = Guid.NewGuid();
    }

    private void Start() {
        GameManager.Instance.OnGameStateChange += GameManagerOnOnGameStateChange;
    }

    private void GameManagerOnOnGameStateChange(GameState gameState) {
        if (gameState == GameState.WAITING_FOR_RESULTS) {
            update = false;
        }
        else {
            update = true;
        }
    }

    private void OnDestroy() {
        GameManager.Instance.OnGameStateChange -= GameManagerOnOnGameStateChange;
    }

    void Update() {
        if (Input.GetKeyDown(KeyCode.Space)) {
            BackendService.Instance.GetMock();
        }
        
        if(!update) return;
    }

    public String getLocation()
    {
        return "empty";
    }

    public struct PlanEntry
    {
        public String time;
        public String location;
    }

    public void assingPlanToAgent(PlanEntry[] newPlan)
    {
        planForDay = newPlan;
        Debug.Log(planForDay);
    }
    
    public AgentState getAgentState()
    {
        // String json = "";
        // AgentMovement agMov = GetComponent<AgentMovement>();
        // json += JsonConvert.SerializeObject(agentName);
        // json += agMov.getAgentMovementState();
        AgentMovement agentMovement = this.GetComponent<AgentMovement>();

        AgentState data = new AgentState
        {
            agentId = ID,
            agentName = agentName, 
            agentAge = age,
            agentDescription = description,
            agentLifestyle = lifestyle,
            agentMovementState = agentMovement.getAgentMovementState()
        };
        return data;
    }
    
    [Serializable]
    public struct AgentState
    {
        public Guid agentId;
        public String agentName;
        public int agentAge;
        public String agentDescription;
        public String agentLifestyle;
        public AgentMovement.AgentMovementState agentMovementState;
    }
}
