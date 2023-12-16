using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.AI;

[RequireComponent(typeof(NavMeshAgent))]
public class Agent : MonoBehaviour {
    [SerializeField] private Transform currentMovingTarget;

    private NavMeshAgent agent;

    private void Awake() {
        agent = GetComponent<NavMeshAgent>();
        
        agent.updateRotation = false;
        agent.updateUpAxis = false;
    }

    void Update() {
        agent.SetDestination(new Vector3(currentMovingTarget.position.x, currentMovingTarget.position.y, transform.position.z));
    }
    
    
}
