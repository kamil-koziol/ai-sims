using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class FieldOfView : MonoBehaviour
{
    public float viewRadius;
    [Range(0, 360)]
    public float viewAngle = 360;

    public LayerMask targetMask;
    public LayerMask obstacleMask;

    public List<Transform> visibleTargets = new List<Transform>();

    void Start()
    {
        StartCoroutine("FindTargetsWithDelay", 0.2f);
    }

    IEnumerator FindTargetsWithDelay(float delay)
    {
        while (true)
        {
            yield return new WaitForSeconds(delay);
            FindVisibleTargets();
        }
    }

    void FindVisibleTargets()
    {
        visibleTargets.Clear();
        Collider2D[] targetsInViewRadius = Physics2D.OverlapCircleAll(transform.position, viewRadius, targetMask);

        for (int i = 0; i < targetsInViewRadius.Length; i++)
        {
            Transform target = targetsInViewRadius[i].transform;
            Vector2 dirToTarget = (target.position - transform.position).normalized;
            if (Vector2.Angle(transform.right, dirToTarget) < viewAngle / 2)
            {
                float distToTarget = Vector2.Distance(transform.position, target.position);

                if (!Physics2D.Raycast(transform.position, dirToTarget, distToTarget, obstacleMask))
                {
                    visibleTargets.Add(target);
                }
            }
        }
    }

    public Vector2 DirFromAngle(float angleInDegrees, bool angleIsGlobal)
    {
        if (!angleIsGlobal)
        {
            angleInDegrees += transform.eulerAngles.z;
        }
        return new Vector2(Mathf.Cos(angleInDegrees * Mathf.Deg2Rad), Mathf.Sin(angleInDegrees * Mathf.Deg2Rad));
    }
    
    public Agent GetClosestTarget()
    {
        Transform closestTarget = null;
        float closestDistance = float.MaxValue;
        foreach (Transform target in visibleTargets)
        {
            if (this.gameObject == target.gameObject)
            {
                continue;
            }
            
            float distance = Vector2.Distance(transform.position, target.position);
            if (distance < closestDistance)
            {
                closestDistance = distance;
                closestTarget = target;
            }
        }
        
        if (closestTarget != null)
        {
            return closestTarget.gameObject.GetComponent<Agent>();
        }
        
        return null;
    }

    void OnDrawGizmos()
    {
        Gizmos.color = Color.red;
        Gizmos.DrawWireSphere(transform.position, viewRadius);

        if (viewAngle < 360)
        {
            Vector2 viewAngleA = DirFromAngle(-viewAngle / 2, false);
            Vector2 viewAngleB = DirFromAngle(viewAngle / 2, false);

            Gizmos.color = Color.yellow;
            Gizmos.DrawLine(transform.position, (Vector2)transform.position + viewAngleA * viewRadius);
            Gizmos.DrawLine(transform.position, (Vector2)transform.position + viewAngleB * viewRadius);
        }
        else
        {
            Gizmos.color = Color.yellow;
            for (int i = 0; i < 360; i += 10)
            {
                Vector2 angleLine = DirFromAngle(i, false);
                Gizmos.DrawLine(transform.position, (Vector2)transform.position + angleLine * viewRadius);
            }
        }

        Gizmos.color = Color.green;
        foreach (Transform visibleTarget in visibleTargets)
        {
            Gizmos.DrawLine(transform.position, visibleTarget.position);
        }
    }
}
