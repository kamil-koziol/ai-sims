using System;
using System.Collections;
using System.Collections.Generic;
using BackendService;
using BackendService.dto;
using DefaultNamespace;
using Dialog;
using Dialog.Mappers;
using UnityEngine;

public enum GameState {
    PLAYING,
    WAITING_FOR_RESULTS,
    CONVERSATION
}

[RequireComponent(typeof(TimeManager))]
public class GameManager : MonoBehaviour {
    // Fields
    public Guid ID;
    
    [SerializeField] private List<Agent> agents;
    [SerializeField] private bool useApi = true; 
    
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

    // Events
    public event Action<GameState> OnGameStateChange;

    private void Awake() {
        Instance = this;
        regions = GetComponent<Regions>();
        // backendService = new DefaultBackendService();
        backendService = new MockBackendService();
        timeManager = GetComponent<TimeManager>();
    }

    private void Start()
    {

        if (useApi)
        {

          coroutineQueue = new CoroutineQueue(this);
          coroutineQueue.Enqueue(backendService.Game(response =>
          {
              ID = Guid.Parse(response.id);
              Debug.Log(response.id);
          }));

          foreach (var agent in agents) {
              coroutineQueue.Enqueue(backendService.Plan(agent.ID, response =>
              {
                  foreach (var node in response.plan)
                  {
                      Debug.Log(node.time + " " + node.location);
                  }
                  ;
              }));

          }
        }

        agents[0].changeSprite("Other_F_A");
        agents[1].changeSprite("Other_F_E");

    }

    public void SetGameState(GameState gameState) {
        this.gameState = gameState;
        OnGameStateChange?.Invoke(gameState);
    }

    private void Update() {
        if (Input.GetKeyDown(KeyCode.C)) {
            coroutineQueue.Enqueue(this.backendService.Conversation(agents[0].ID, agents[1].ID,
                response =>
                {
                    Dialog.Dialog dialog = DialogMapper.Map(agents[0].ID, agents[1].ID, response);
                    DialogManager.Instance.OpenDialog(dialog);
                }));
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
    
    public Agent GetAgentById(Guid id) {
        return agents.Find(agent => agent.ID == id);
    }
}
