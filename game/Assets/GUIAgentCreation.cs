using System;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace DefaultNamespace
{
    public class GUIAgentCreation : MonoBehaviour
    {
        [SerializeField] private GameObject visual;
        [SerializeField] private TMP_InputField nameField;
        [SerializeField] private TMP_InputField ageField;
        [SerializeField] private TMP_InputField descriptionField;
        [SerializeField] private TMP_InputField lifestyleField;
        [SerializeField] private Button submitButton;
        [SerializeField] private GameObject spriteButtons;
        private String selectedSpriteName;
        
        void Start()
        {
            visual.SetActive(false);
            
            foreach (Transform child in spriteButtons.transform)
            {
                Button button = child.GetComponent<Button>();
                button.onClick.AddListener(() =>
                {
                    selectedSpriteName = child.name;
                    Debug.Log("Selected sprite: " + selectedSpriteName);
                });
            }
            
            submitButton.onClick.AddListener(() =>
            {
                GameManager.Instance.TryAddAgent(
                    Int32.Parse(ageField.text),
                    descriptionField.text,
                    lifestyleField.text, 
                    nameField.text, 
                    selectedSpriteName
                );
                visual.SetActive(false);
                resetUi();
                GameManager.Instance.SetGameState(GameState.PLAYING);
            });
        }
        void Update()
        {
            if (Input.GetKeyDown(KeyCode.UpArrow) && GameManager.Instance.GameState == GameState.PLAYING)
            {
                GameManager.Instance.SetGameState(GameState.WAITING_FOR_RESULTS);
                visual.SetActive(!visual.activeSelf);
            } else if (Input.GetKeyDown(KeyCode.UpArrow))
            {
                GameManager.Instance.SetGameState(GameState.PLAYING);
                visual.SetActive(false);
            }
        }
        
        void resetUi()
        {
            nameField.text = "";
            ageField.text = "";
            descriptionField.text = "";
            lifestyleField.text = "";
            selectedSpriteName = "";
        }
    }
}