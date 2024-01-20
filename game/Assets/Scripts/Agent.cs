using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[RequireComponent(typeof(UnityEngine.AI.NavMeshAgent))]
public class Agent : MonoBehaviour {

    AgentMovement agentMovement;
    private bool update = true;

    private void Awake() {

        //For now it throws exception, talk about it
        if (agentMovement != null)
        {
            Debug.Log("AgentMovement works");
        } else
        {
            throw new Exception("AgentMovement is null");
        }
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
            BackendService.BackendService.Instance.GetMock();
        }
        
        if(!update) return;
        //TODO: Talk about it
        //agentMovement.updateAgentPosition();
    }
}
