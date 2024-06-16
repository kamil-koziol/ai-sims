using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public enum GameState {
    PLAYING,
    WAITING_FOR_RESULTS
}
public class GameManager : MonoBehaviour {
    public Guid ID;
    
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
        coroutineQueue.Enqueue(BackendService.Instance.SendGameSnapshot());
        foreach (var plan in BackendService.Instance.RequestPlanForAllAgents())
        {
            coroutineQueue.Enqueue(plan);
            //StartCoroutine(plan);
        }
    }

    public void SetGameState(GameState gameState) {
        //GameState = gameState;
        OnGameStateChange?.Invoke(gameState);
    }
    
    public void registerCoroutine(IEnumerator coroutine)
    {
        coroutineQueue.Enqueue(coroutine);
    }

    public Agent[] GetAllAgents()
    {
        GameObject agentsGameObj = GameObject.Find("Agents");
        return agentsGameObj.GetComponentsInChildren<Agent>();
    }
}
