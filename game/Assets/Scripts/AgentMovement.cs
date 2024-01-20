using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.AI;
using Constants;

[RequireComponent(typeof(NavMeshAgent))]
public class AgentMovement : MonoBehaviour
{
    [SerializeField] private Transform regions;
    private Transform currentMovingTarget;
    private NavMeshAgent agent;
    private readonly double MOVEMENT_ESTIMATION_ERROR = 0.1;

    void Awake() {
        agent = GetComponent<NavMeshAgent>();

        agent.updateRotation = false;
        agent.updateUpAxis = false;
    }

    void Start()
    {

        //Demo intialization
        Transform grassTransform = regions.transform.Find(Constants.Constants.grassObjectName);

        if (grassTransform == null)
        {
            Debug.Log("Failed to load initial move position");

        }
        changeDestination(grassTransform.GetChild(0).GetChild(0));
    }

    void Update()
    {
        demoMovement();
        updateAgentPosition();
    }

    public void changeDestination(Transform target)
    {
        currentMovingTarget = target;
    }

    public void updateAgentPosition()
    {
        agent.SetDestination(new Vector3(currentMovingTarget.position.x, currentMovingTarget.position.y, transform.position.z));
    }

    private bool isOnCurrentTargetPosition()
    {
        Vector3 agentPosition = new Vector3(agent.transform.position.x, agent.transform.position.y, transform.position.z);
        return Mathf.Abs(agentPosition.x - currentMovingTarget.position.x + agentPosition.y - currentMovingTarget.position.y) < MOVEMENT_ESTIMATION_ERROR;
    }

    //Demo
    public void demoMovement()
    {
        if (isOnCurrentTargetPosition())
        {
            Transform houseTransform = regions.transform.Find(Constants.Constants.houseObjectName);
            Transform grassTransform = regions.transform.Find(Constants.Constants.grassObjectName);

            Transform targetToChange;
            if (currentMovingTarget == houseTransform.GetChild(0).GetChild(0))
            {
                targetToChange = grassTransform.GetChild(0).GetChild(0);
            }
            else
            {
                targetToChange = houseTransform.GetChild(0).GetChild(0);
            }


            changeDestination(targetToChange);
        }

    }
}
