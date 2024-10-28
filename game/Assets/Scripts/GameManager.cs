using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using BackendService;
using BackendService.dto;
using DefaultNamespace;
using Dialog;
using Dialog.Mappers;
using Plan.Mappers;
using UnityEngine;

public enum GameState {
    PLAYING,
    WAITING_FOR_RESULTS,
    CONVERSATION
}

[RequireComponent(typeof(TimeManager), typeof(AgentSelector), typeof(CameraManager))]
public class GameManager : MonoBehaviour {
    // Fields
    public Guid ID;
    
    [SerializeField] private List<Agent> agents;
    [SerializeField] private bool useApi = true;
    [SerializeField] private bool mock = false;
    public GameObject agentPrefab;
    
    public static GameManager Instance;
    private GameState gameState;

    public GameState GameState => gameState;

    private CoroutineQueue coroutineQueue;
    
    private Regions regions;
    public Regions Regions => regions;

    // Singletons

    private BackendService.BackendService backendService;
    
    private TimeManager timeManager;

    public TimeManager TimeManager => timeManager;

    private AgentSelector agentSelector;

    public AgentSelector AgentSelector => agentSelector;

    private CameraManager cameraManager;
    public CameraManager CameraManager => cameraManager;

    // Events
    public event Action<GameState> OnGameStateChange;

    private void Awake() {
        Instance = this;
        regions = GetComponent<Regions>();
        
        if (mock) {
            backendService = new MockBackendService();
        }
        else {
            backendService = new DefaultBackendService();
        }

        
        timeManager = GetComponent<TimeManager>();
        timeManager.OnTimeChanged += TimeManagerOnTimeChanged;

        agentSelector = GetComponent<AgentSelector>();
        cameraManager = GetComponent<CameraManager>();
    }

    private void TimeManagerOnTimeChanged(object sender, TimeChangedEventArgs e)
    {
        if (!e.IsNewDay) return;
        
        GenerateAgentsPlan(); 
    }

    private void GenerateAgentsPlan()
    {
          foreach (var agent in agents) {
              coroutineQueue.Enqueue(backendService.Plan(agent.ID, response =>
              {
                  var plan = PlanMapper.Map(response);
                  agent.AssignPlan(plan);
              }));

          }
    }

    public void TryAddAgent(int age, String description, String lifestyle, String agentName, String spriteName)
    {
        GameObject instance = Instantiate(agentPrefab, new Vector3(0, 0, 0), Quaternion.identity);
        Agent agent = instance.GetComponent<Agent>();
        if (agent != null)
        {
            agent.setFieldsAgent(age, description, lifestyle, agentName, spriteName);
        }
        
        coroutineQueue.Enqueue(backendService.AddAgent(agent, response =>
        {
            AddAgentToGame(agent);

            coroutineQueue.Enqueue(backendService.Plan(agent.getId(), response =>
            {
                var plan = PlanMapper.Map(response);
                agent.AssignPlan(plan);
                SetGameState(GameState.PLAYING);
            }));
        }));
        
    }
    
    private void AddAgentToGame(Agent agent)
    {
        agents.Add(agent);
    }

    private void Start()
    {
        

        if (useApi)
        {

          coroutineQueue = new CoroutineQueue(this);
          coroutineQueue.Enqueue(backendService.Game(response =>
          {
              ID = Guid.Parse(response.game.id.ToString());
              Debug.Log(response.game.id.ToString());
          }));
          
        //agents = new List<Agent>();
        
        // coroutineQueue.Enqueue(backendService.GetGame(new Guid("a0667329-4270-45af-9a28-325517279438"), response =>
        // {
        //     ID = Guid.Parse(response.game.id.ToString());
        //     Debug.Log(response);
        //       foreach (var agent in response.game.agents)
        //       {
        //           GameObject instance = Instantiate(agentPrefab, new Vector3(0, 0, 0), Quaternion.identity);
        //           Agent newAgent = instance.GetComponent<Agent>();
        //           newAgent.setFieldsAgent(agent.age, agent.description, agent.lifestyle, agent.name, "Other_F_A", agent.id);
        //           newAgent.loadRandomSprite();
        //           agents.Add(newAgent);
        //       }
        //     Debug.Log(response.game.id.ToString());
        // }));
        }

        agents[0].changeSprite("Other_F_A");
        agents[1].changeSprite("Other_F_E");

    }

    public void SetGameState(GameState gameState) {
        this.gameState = gameState;
        OnGameStateChange?.Invoke(gameState);
    }

    private bool doOnce = true;
    private void Update() {
        if (GameManager.Instance.gameState == GameState.PLAYING && doOnce)
        {
            // GameObject instance = Instantiate(agentPrefab, new Vector3(0, 0, 0), Quaternion.identity);
            // Agent agent = instance.GetComponent<Agent>();
            // agent.setFieldsAgent(10, "description", "lifestyle", "agentName", "Other_F_A");
            // coroutineQueue.Enqueue(backendService.AddAgent(agent, response =>
            // {
            //     AddAgentToGame(agent);
            // }));
            // agent.changeSprite("Other_F_A");
            
            coroutineQueue.Enqueue(backendService.SaveGameYaml(response =>
            {
                string path = Path.Combine(Application.persistentDataPath, "config.yaml");
                Debug.Log(path);
                File.WriteAllText(path, response);
            }));
            doOnce = false;
        }
    }

    public void registerCoroutine(IEnumerator coroutine)
    {
        coroutineQueue.Enqueue(coroutine);
    }

    public bool IsUsingApi()
    {
        return useApi;
    }

    public List<Agent> GetAgents() {
        return agents;
    }
    
    public BackendService.BackendService getBackendService()
    {
        return backendService;
    }
    
    public Agent GetAgentById(Guid id) {
        return agents.Find(agent => agent.ID == id);
    }
}
