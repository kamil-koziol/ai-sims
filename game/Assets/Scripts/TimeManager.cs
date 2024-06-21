using System;
using UnityEngine;

public class TimeChangedEventArgs : EventArgs
{
    public DateTime NewTime { get; }

    public TimeChangedEventArgs(DateTime newTime)
    {
        NewTime = newTime;
    }
}

public class TimeManager : MonoBehaviour
{
    private DateTime time;
    [SerializeField] private DateTime startingDate;

    public delegate void TimeChangedEventHandler(object sender, TimeChangedEventArgs e);
    public event TimeChangedEventHandler OnTimeChanged;

    public const int REALTIME_MULTIPLIER = 60;
    private float CLOCK_EVERY_S = 1.0f;

    private float timer;

    void Start()
    {
        time = startingDate;
        timer = 0f;
    }

    void Update()
    {
        timer += Time.deltaTime;
        if (timer >= CLOCK_EVERY_S)
        {
            IncrementTime();
            timer = 0f;
        }
    }

    private void IncrementTime()
    {
        time = time.AddSeconds(REALTIME_MULTIPLIER * CLOCK_EVERY_S);
        OnTimeChanged?.Invoke(this, new TimeChangedEventArgs(time));
    }
}