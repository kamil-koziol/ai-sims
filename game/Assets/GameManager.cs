using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public enum GameState {
    PLAYING,
    WAITING_FOR_RESULTS
}
public class GameManager : MonoBehaviour {
    public static GameManager Instance;
    public GameState GameState;
    public event Action<GameState> OnGameStateChange;

    private void Awake() {
        Instance = this;
    }

    public void SetGameState(GameState gameState) {
        GameState = gameState;
        OnGameStateChange?.Invoke(gameState);
    }
}
