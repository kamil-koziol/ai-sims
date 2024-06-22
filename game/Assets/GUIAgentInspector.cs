using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;

public class GUIAgentInspector : MonoBehaviour
{
    [SerializeField] private GameObject visual;

    [SerializeField] private TMP_Text agentName;
    [SerializeField] private TMP_Text agentDescription;
    [SerializeField] private TMP_Text agentAge;
    [SerializeField] private TMP_Text agentLifestyle;
    [SerializeField] private TMP_Text agentLocation;
    [SerializeField] private TMP_Text agentId;
    
    void Start()
    {
        GameManager.Instance.AgentSelector.OnAgentClick += AgentSelectorOnAgentClick;
    }

    private void AgentSelectorOnAgentClick(Agent obj)
    {
        if (obj == null)
        {
            visual.SetActive(false);
        }
        else
        {
           AssignAgentDataToVisual(obj);
           visual.SetActive(true); 
        }
    }

    public void AssignAgentDataToVisual(Agent agent)
    {
        // TODO: automatic updates to get location in inspector 
        
        Agent.AgentState state = agent.getAgentState();
        agentId.text = state.agentId.ToString();
        agentName.text = state.agentName;
        agentDescription.text = state.agentDescription;
        agentAge.text = state.agentAge.ToString();
        agentLifestyle.text = state.agentLifestyle;
    }

}
