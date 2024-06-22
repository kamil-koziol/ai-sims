using System;
using System.Collections;
using System.Collections.Generic;
using Newtonsoft.Json;
using Plan;
using Unity.VisualScripting;
using UnityEngine;


[RequireComponent(typeof(UnityEngine.AI.NavMeshAgent), typeof(AgentMovement)), Serializable]
public class Agent : MonoBehaviour {
    public Guid ID;
    private bool update = true;
    
    private Queue<PlanTask> plan;
    private PlanTask currentTask; 
    
    [SerializeField] private int age;
    [SerializeField] private String description;
    [SerializeField] private String lifestyle;
    [SerializeField] private String agentName;
    [SerializeField] private Sprite sprite;

    private AgentMovement movement;
    private FieldOfView fov;

    private void Awake() {
        ID = Guid.NewGuid();
        plan = new Queue<PlanTask>();
        movement = GetComponent<AgentMovement>();
        fov = GetComponent<FieldOfView>();
    }

    private void Start() {
        GameManager.Instance.OnGameStateChange += GameManagerOnOnGameStateChange;
        GameManager.Instance.TimeManager.OnTimeChanged += OnTimeChanged;
    }

    private void OnTimeChanged(object sender, TimeChangedEventArgs e)
    {
        if(plan.Count == 0) return;
        bool shouldStartNextTask = e.NewTime > plan.Peek().time;
        if (!shouldStartNextTask) return;

        currentTask = plan.Dequeue();
        
        // TODO: Make so that i can pass location name and it handles it
        Debug.Log(this.gameObject + " New task: " + currentTask.location);
        movement.changeDestination(GameManager.Instance.Regions.getRandomTranformFromRegion(currentTask.location));
    }

    private void GameManagerOnOnGameStateChange(GameState gameState) {
        update = gameState == GameState.PLAYING;
    }

    private void OnDestroy() {
        GameManager.Instance.OnGameStateChange -= GameManagerOnOnGameStateChange;
        GameManager.Instance.TimeManager.OnTimeChanged -= OnTimeChanged;
    }

    void Update() {
        if(!update) return;
    }

    public String getLocation()
    {
        return movement.getLocation();
    }

    public Guid getId()
    {
        return ID;
    }

    public void changeSprite(String spriteName)
    {
        const String miniProfilesPath = "MiniProfiles/";
        const String profilesPath = "Profiles/";
        var visual = GetComponentInChildren<SpriteRenderer>();
        visual.sprite = Resources.Load<Sprite>( miniProfilesPath + spriteName);
        visual.transform.localScale = new Vector3(6.0f, 6.0f, 0.0f);
        
        sprite = Resources.Load<Sprite>( profilesPath + spriteName);
    }
    
    public AgentState getAgentState()
    {
        // String json = "";
        // AgentMovement agMov = GetComponent<AgentMovement>();
        // json += JsonConvert.SerializeObject(agentName);
        // json += agMov.getAgentMovementState();
        AgentMovement agentMovement = this.GetComponent<AgentMovement>();

        AgentState data = new AgentState
        {
            agentId = ID,
            agentName = agentName, 
            agentAge = age,
            agentDescription = description,
            agentLifestyle = lifestyle,
            agentMovementState = agentMovement.getAgentMovementState(),
            agentSprite = sprite
        };
        return data;
    }
    
    [Serializable]
    public struct AgentState
    {
        public Guid agentId;
        public String agentName;
        public int agentAge;
        public String agentDescription;
        public String agentLifestyle;
        public AgentMovement.AgentMovementState agentMovementState;
        public Sprite agentSprite;
    }

    public void AssignPlan(Plan.Plan plan)
    {
        this.plan = new Queue<PlanTask>(plan.tasks);
    }
}
