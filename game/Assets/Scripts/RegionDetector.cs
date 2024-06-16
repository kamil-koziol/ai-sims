using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class RegionDetector : MonoBehaviour
{
    private void OnTriggerEnter2D(Collider2D other)
    {
        if (other.CompareTag("Agent"))
        {
            Debug.Log("Object entered the region " + gameObject.tag);
        } 
    }
}
