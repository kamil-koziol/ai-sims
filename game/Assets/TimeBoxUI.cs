using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;

public class TimeBoxUI : MonoBehaviour
{
    // Start is called before the first frame update
    [SerializeField] private TMP_Text timeText;
    void Start()
    {
       GameManager.Instance.TimeManager.OnTimeChanged += TimeManagerOnTimeChanged; 
    }

    private void TimeManagerOnTimeChanged(object sender, TimeChangedEventArgs e)
    {
        timeText.text = e.formattedTime;
    }

}
