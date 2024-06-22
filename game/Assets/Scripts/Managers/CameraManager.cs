using System.Collections;
using System.Collections.Generic;
using Cinemachine;
using UnityEngine;

public class CameraManager : MonoBehaviour
{
    [SerializeField] private CinemachineVirtualCamera virtualCamera;
    [SerializeField] private Transform cameraMan;

    void Start()
    {
        GameManager.Instance.AgentSelector.OnAgentClick += AgentSelectorOnAgentClick;
        virtualCamera.Follow = cameraMan;
    }

    private void AgentSelectorOnAgentClick(Agent agent)
    {
        if (agent == null)
        {
            virtualCamera.Follow = cameraMan;
        }
        else
        {
            virtualCamera.Follow = agent.gameObject.transform;
        }
    }

}
