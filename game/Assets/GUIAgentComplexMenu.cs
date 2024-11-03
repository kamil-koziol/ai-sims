using System;
using Dialog;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace DefaultNamespace
{
    public class GUIAgentComplexMenu : MonoBehaviour
    {
        public GameObject visual;
        public GameObject characterItemPrefab;
        public Transform contentPanel;
        public Button submitButton;
        public TMP_InputField textField;
        public Toggle checkbox;
        
        private global::Agent selectedAgent = null;
        private void Start()
        {
            submitButton.onClick.AddListener(() => OnSubmitButtonClick());
        }

        private void Update()
        {
            if (Input.GetKeyDown(KeyCode.F3))
            {
                GameManager.Instance.SetGameState(GameState.WAITING_FOR_RESULTS);
                foreach (global::Agent ag in GameManager.Instance.GetAgents())
                {
                    GameObject go = Instantiate(characterItemPrefab, contentPanel);
                    Button charButton = go.GetComponentInChildren<Button>();
                    TMP_Text nameText = charButton.GetComponentInChildren<TMP_Text>();
                    global::Agent.AgentState state = ag.getAgentState();
                    nameText.text = state.agentName;
                    charButton.onClick.AddListener(() => OnCharacterSelected(ag));
                }
                visual.SetActive(true);
            }
        }
        
        void OnSubmitButtonClick()
        {
            if (selectedAgent != null)
            {
                if (checkbox.isOn)
                {
                    GameManager.Instance.registerCoroutine(GameManager.Instance.BackendService.Injection(selectedAgent.getAgentState().agentId, textField.text));
                }
                else
                {
                    global::Agent.AgentState state = selectedAgent.getAgentState();
                    GameManager.Instance.registerCoroutine(GameManager.Instance.BackendService.Interview(selectedAgent.getAgentState().agentId, textField.text,
                        response =>
                        {
                            Dialog.Dialog.Builder builder = new Dialog.Dialog.Builder();
                            Actor actor = new Actor()
                            {
                                id = 0, 
                                sprite = state.agentSprite,
                                name = state.agentName
                            };
                            builder.AddActor(actor);
                            builder.AddMessage(new Message() { message = response.response });
                            DialogManager.Instance.OpenDialog(builder.Build());
                        }));
                }
                visual.SetActive(false);
                GameManager.Instance.SetGameState(GameState.PLAYING);
            }
        }
        
        void OnCharacterSelected(global::Agent ag)
        {
            Debug.Log("Selected character: " + ag.getAgentState().agentName);
            selectedAgent = ag;
        }
    }
}