using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CoroutineQueue
{
    private MonoBehaviour owner;
    private Queue<IEnumerator> coroutines = new Queue<IEnumerator>();
    private bool isRunning = false;

    public CoroutineQueue(MonoBehaviour owner)
    {
        this.owner = owner;
    }

    public void Enqueue(IEnumerator coroutine)
    {
        coroutines.Enqueue(coroutine);
        if (!isRunning)
        {
            owner.StartCoroutine(RunQueue());
        }
    }

    private IEnumerator RunQueue()
    {
        isRunning = true;
        while (coroutines.Count > 0)
        {
            yield return owner.StartCoroutine(coroutines.Dequeue());
        }
        isRunning = false;
    }
}