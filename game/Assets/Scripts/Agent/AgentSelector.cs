using System;
using UnityEngine;

public class AgentSelector : MonoBehaviour
{
    public event Action<Agent> OnAgentHover;
    public event Action<Agent> OnAgentClick;
    public event Action<Agent> OnHoverLeave;

    private Agent hoveredAgent = null;
    private Agent selectedAgent = null;
    
    [SerializeField] private LayerMask agentLayer;

    private void Update()
    {
        // TODO: Rate limit
        CheckForAgentHover();
        CheckForAgentClick();
    }

    private Agent RayCastAgent()
    {
        RaycastHit2D hit = Physics2D.Raycast(Camera.main.ScreenToWorldPoint(Input.mousePosition), Vector2.zero, Mathf.Infinity, agentLayer);
        if (hit.collider == null) return null;
        
        Agent agent = hit.collider.GetComponent<Agent>();
        if(agent == null) return null;

        return agent;
    }
    private void CheckForAgentHover()
    {
        var agent = RayCastAgent();
        if (agent == null)
        {
            OnHoverLeave?.Invoke(hoveredAgent);
            hoveredAgent = null;
            return;
        };

        hoveredAgent = agent;
        OnAgentHover?.Invoke(agent);
    }

    private void CheckForAgentClick()
    {
        if (Input.GetMouseButtonDown(0))
        {
            var agent = RayCastAgent();
            if (agent == null)
            {
                // If clicked elsewhere remove selection
                selectedAgent = null;
                OnAgentClick?.Invoke(null);
                return;
            };

            selectedAgent = agent;
            OnAgentClick?.Invoke(agent);
        }
    }
}