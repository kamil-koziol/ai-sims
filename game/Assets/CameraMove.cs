using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CameraMove : MonoBehaviour
{
    [SerializeField] private float moveSpeed = 5f;

    void Update()
    {
        if(GameManager.Instance.GameState != GameState.PLAYING) return;
        HandleCameraMovement();        
    }

    private void HandleCameraMovement()
    {
        float moveHorizontal = Input.GetAxisRaw("Horizontal");
        float moveVertical = Input.GetAxisRaw("Vertical");

        Vector3 moveDirection = new Vector3(moveHorizontal, moveVertical, 0f).normalized * (moveSpeed * Time.deltaTime);
        Vector3 newPosition = this.transform.position + moveDirection;

        // TODO: Automatic clamping now this is bad
        newPosition.x = Mathf.Clamp(newPosition.x, -3.0f, 9.8f);
        newPosition.y = Mathf.Clamp(newPosition.y, 9.10f, 20f);

        this.transform.position = newPosition;
    }

}
