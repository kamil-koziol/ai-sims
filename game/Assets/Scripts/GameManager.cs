using System;
using System.Collections;
using System.Collections.Generic;
using DefaultNamespace;
using UnityEngine;

public enum GameState {
    PLAYING,
    WAITING_FOR_RESULTS,
    CONVERSATION
}
public class GameManager : MonoBehaviour {
    public Guid ID;
    [SerializeField] private List<Agent> agents;
    [SerializeField] private bool useApi = true; 
    
    public static GameManager Instance;
    private GameState gameState;

    public GameState GameState => gameState;

    private CoroutineQueue coroutineQueue;
    
    private Regions regions;
    public Regions Regions => regions;


    public event Action<GameState> OnGameStateChange;

    private void Awake() {
        Instance = this;
        regions = GetComponent<Regions>();
    }

    private void Start()
    {
        if (useApi)
        {
            coroutineQueue = new CoroutineQueue(this);
            coroutineQueue.Enqueue(DefaultBackendService.Instance.Game());
            foreach (var agent in agents) {
                coroutineQueue.Enqueue(DefaultBackendService.Instance.Plan(agent.ID));
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
            coroutineQueue.Enqueue(DefaultBackendService.Instance.Conversation(agents[0].ID, agents[1].ID));
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
