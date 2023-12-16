using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.AI;

[RequireComponent(typeof(NavMeshAgent))]
public class Agent : MonoBehaviour {
    
    
    [SerializeField] private Transform currentMovingTarget;
    private bool update = true;
    private NavMeshAgent agent;

    private void Awake() {
        agent = GetComponent<NavMeshAgent>();
        
        agent.updateRotation = false;
        agent.updateUpAxis = false;
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
        
        agent.SetDestination(new Vector3(currentMovingTarget.position.x, currentMovingTarget.position.y, transform.position.z));
    }
    
    
}
