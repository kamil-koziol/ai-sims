using System;
using System.Collections;
using System.Collections.Generic;
using Newtonsoft.Json;
using UnityEngine;

[RequireComponent(typeof(UnityEngine.AI.NavMeshAgent)), Serializable]
public class Agent : MonoBehaviour {
    private bool update = true;
    [SerializeField] private String agentName;
    private void Awake() {
        
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

    public AgentState getAgentState()
    {
        // String json = "";
        // AgentMovement agMov = GetComponent<AgentMovement>();
        // json += JsonConvert.SerializeObject(agentName);
        // json += agMov.getAgentMovementState();
        AgentMovement agentMovement = this.GetComponent<AgentMovement>();

        AgentState data = new AgentState { agentName = agentName, agentMovementState = agentMovement.getAgentMovementState() };
        return data;
    }
    
    [Serializable]
    public struct AgentState
    {
        public String agentName;
        public AgentMovement.AgentMovementState agentMovementState;
    }
}
