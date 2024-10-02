using System;
using UnityEngine;

public class TimeChangedEventArgs : EventArgs
{
    public DateTime NewTime { get; }
    public string formattedTime { get; }
    public bool IsNewDay { get; }

    public TimeChangedEventArgs(DateTime newTime, bool isNewDay)
    {
        NewTime = newTime;
        formattedTime = newTime.ToString("MM/dd/yyyy HH:mm");
        IsNewDay = isNewDay;
    }
}

public class TimeManager : MonoBehaviour
{
    private DateTime previousTime;
    public static DateTime startingDate = new DateTime(2024, 1,1,8,0,0);
    public static DateTime time = startingDate;
    private bool update = true;

    public delegate void TimeChangedEventHandler(object sender, TimeChangedEventArgs e);
    public event TimeChangedEventHandler OnTimeChanged;

    public const int TIME_MULTIPLIER = 60 * 1;
    public const int CLOCKS_PER_S = 3;
    
    private float CLOCK_EVERY = 1.0f/CLOCKS_PER_S;

    private float timer;

    void Start()
    {
        GameManager.Instance.OnGameStateChange += OnGameStateChange;
        previousTime = startingDate;
        timer = 0f;
    }

    private void OnGameStateChange(GameState obj)
    {
        update = obj == GameState.PLAYING; 
    }

    void Update()
    {
        if (!update) return;
        
        timer += Time.deltaTime;
        if (timer >= CLOCK_EVERY)
        {
            IncrementTime();
            timer = 0f;
        }
    }

    private void IncrementTime()
    {
        previousTime = time;
        time = time.AddSeconds(TIME_MULTIPLIER);
        bool isNewDay = previousTime.Day != time.Day;
        isNewDay = isNewDay || previousTime == startingDate; // initial day 
        OnTimeChanged?.Invoke(this, new TimeChangedEventArgs(time, isNewDay));
    }
}