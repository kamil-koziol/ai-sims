using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.AI;

[RequireComponent(typeof(NavMeshAgent))]
public class AgentMovement : MonoBehaviour
{
    [SerializeField] private Transform targets;
    private Transform currentMovingTarget;
    private NavMeshAgent agent;
    private readonly double MOVEMENT_ESTIMATION_ERROR = 0.1;

    void Awake() {
        agent = GetComponent<NavMeshAgent>();

        agent.updateRotation = false;
        agent.updateUpAxis = false;
    }

    // Start is called before the first frame update
    void Start()
    {
        changeDestination(targets.GetChild(0));
    }

    // Update is called once per frame
    void Update() {
        demoMovement();
        agent.SetDestination(new Vector3(currentMovingTarget.position.x, currentMovingTarget.position.y, transform.position.z));
    }


    public void changeDestination(Transform target)
    {
        currentMovingTarget = target;
    }
    

    //Demo
    void demoMovement() {
        Vector3 agentPosition = new Vector3(agent.transform.position.x, agent.transform.position.y, transform.position.z);

        //Due to nature of NavMeshAgent we have to calculate his position with error
        if (Mathf.Abs(agentPosition.x - currentMovingTarget.position.x + agentPosition.y - currentMovingTarget.position.y) < MOVEMENT_ESTIMATION_ERROR)
        {
            Transform targetToChange;
            if (currentMovingTarget == targets.GetChild(0))
            {
                targetToChange = targets.GetChild(1);
            }
            else
            {
                targetToChange = targets.GetChild(0);
            }


            changeDestination(targetToChange);
        }

    }
}
