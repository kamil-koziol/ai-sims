using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class AgentSelectionController : MonoBehaviour
{
    [SerializeField] private Transform border;
    private Agent agent;
    
    private bool isSelected;
    public bool IsSelected => isSelected;

    public void Select()
    {
        isSelected = true;
        border.gameObject.SetActive(true);
    }

    public void Unselect()
    {
        isSelected = false;
        border.gameObject.SetActive(false);

    }
    
    public void OnHover()
    {
        border.gameObject.SetActive(true);
    }

    public void OnHoverLeave()
    {
        if (!isSelected)
        {
            border.gameObject.SetActive(false);
        }
    }

    private void Awake()
    {
        agent = this.gameObject.GetComponent<Agent>();
    }

    private void Start()
    {
        GameManager.Instance.AgentSelector.OnAgentHover += AgentSelectorOnAgentHover; 
        GameManager.Instance.AgentSelector.OnAgentClick += AgentSelectorOnAgentClick;
        GameManager.Instance.AgentSelector.OnHoverLeave += AgentSelectorOnHoverLeave;
        
    }

    private void AgentSelectorOnHoverLeave(Agent obj)
    {
        if (obj == agent)
        {
            OnHoverLeave();
        }
    }

    private void AgentSelectorOnAgentClick(Agent obj)
    {
        if (obj == agent)
        {
            Select();
        }
        else
        {
            // Only 1 agent can be selected
            Unselect();
        }
    }

    private void AgentSelectorOnAgentHover(Agent obj)
    {
        if (obj == agent)
        {
            OnHover();
        }
    }
}
