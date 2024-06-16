using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.AI;
using DefaultNamespace;
using Newtonsoft.Json;


[RequireComponent(typeof(NavMeshAgent)), Serializable]
public class AgentMovement : MonoBehaviour
{
    //[SerializeField] private Transform regions;
    public Transform currentMovingTarget;
    public Vector3 agentPosition;
    private NavMeshAgent agent;
    private readonly double MOVEMENT_ESTIMATION_ERROR = 0.1;
    [SerializeField] private bool useApi = true;
    public bool gameFrozen = false;
    private Regions regions;

    void Awake() {
        agent = GetComponent<NavMeshAgent>();
        regions = GameManager.Instance.GetComponent<Regions>();
        agent.updateRotation = false;
        agent.updateUpAxis = false;
    }

    void Start()
    {
        GameManager.Instance.OnGameStateChange += OnGameStateChange;
        if (!useApi)
        {
            demoStart();
        }
    }

    private void OnGameStateChange(GameState obj) {
        gameFrozen = obj != GameState.PLAYING;
        Debug.Log("Game frozen: " + gameFrozen);
    }

    void Update()
    {
        if (gameFrozen) return;
        
        if (!useApi)
        {
            demoMovement();
        }
        updateAgentPosition();
    }

    public void changeDestination(Transform target)
    {
        currentMovingTarget = target;
    }

    public void updateAgentPosition()
    {
        if (currentMovingTarget != null)
        {
            agent.SetDestination(new Vector3(currentMovingTarget.position.x, currentMovingTarget.position.y, transform.position.z));
        }
    }

    private bool isOnCurrentTargetPosition()
    {
        agentPosition = new Vector3(agent.transform.position.x, agent.transform.position.y, transform.position.z);
        return Mathf.Abs(agentPosition.x - currentMovingTarget.position.x + agentPosition.y - currentMovingTarget.position.y) < MOVEMENT_ESTIMATION_ERROR;
    }

    //Demo

    private void demoStart()
    {
        //Demo intialization
        
        Transform grassTransform = regions.getRandomTranformFromRegion(Constants.grassObjectName);

        if (grassTransform == null)
        {
            Debug.Log("Failed to load initial move position");

        }
        changeDestination(grassTransform);
    }
    public void demoMovement()
    {
        if (isOnCurrentTargetPosition())
        {
            Transform targetToChange;
            if (Regions.getParentName(currentMovingTarget) == Constants.houseObjectName)
            {
                Debug.Log("Switching to house");
                targetToChange = regions.getRandomTranformFromRegion(Constants.grassObjectName);
            }
            else
            {
                Debug.Log("Switching to grass");
                targetToChange = regions.getRandomTranformFromRegion(Constants.houseObjectName);
            }


            changeDestination(targetToChange);
        }

    }

    public AgentMovementState getAgentMovementState()
    {
        // String json = "";
        // json += JsonConvert.SerializeObject(agentPosition);
        // json += JsonConvert.SerializeObject(Regions.getParentName(currentMovingTarget));
        AgentMovementState state = new AgentMovementState
        {
            agentPosition = agentPosition,
            currentTargetPosition = Regions.getParentName(currentMovingTarget)
        };
        return state;
    }
    
    [Serializable]
    public struct AgentMovementState
    {
        public Vector3 agentPosition;
        public String currentTargetPosition;
    }
}
