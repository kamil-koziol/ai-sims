using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public enum GameState {
    PLAYING,
    WAITING_FOR_RESULTS,
    CONVERSATION
}
public class GameManager : MonoBehaviour {
    public Guid ID;
    [SerializeField] private List<Agent> agents;
    
    public static GameManager Instance;
    public GameState GameState;
    private CoroutineQueue coroutineQueue;
    
    public event Action<GameState> OnGameStateChange;

    private void Awake() {
        Instance = this;
    }

    private void Start()
    {
        coroutineQueue = new CoroutineQueue(this);
        coroutineQueue.Enqueue(DefaultBackendService.Instance.Game());
        foreach (var agent in agents) {
            coroutineQueue.Enqueue(DefaultBackendService.Instance.Plan(agent.ID));
        }
        
        coroutineQueue.Enqueue(DefaultBackendService.Instance.Conversation(agents[0].ID, agents[1].ID));
        coroutineQueue.Enqueue(DefaultBackendService.Instance.Interaction(agents[0].ID, agents[1].ID));
    }

    public void SetGameState(GameState gameState) {
        GameState = gameState;
        OnGameStateChange?.Invoke(gameState);
    }
    
    public void registerCoroutine(IEnumerator coroutine)
    {
        coroutineQueue.Enqueue(coroutine);
    }

    public List<Agent> GetAgents() {
        return agents;
    }
    
    public Agent GetAgentById(Guid id) {
        return agents.Find(agent => agent.ID == id);
    }
}
