using System;
using TMPro;
using UnityEngine;
using UnityEngine.UIElements;
using Image = UnityEngine.UI.Image;

namespace Dialog {
    public class DialogManager : MonoBehaviour {
        [SerializeField] private GameObject dialogBox;
        [SerializeField] private Image firstActorImage;
        [SerializeField] private Image secondActorImage;
        [SerializeField] private TMP_Text dialogText;
        [SerializeField] private TMP_Text actorNameText;
        private static DialogManager _instance;

        public static DialogManager Instance { get { return _instance; } }

        private Dialog currentDialog;
        private int currentMessage = 0;
        private void Awake()
        {
            if (_instance != null && _instance != this)
            {
                Destroy(this.gameObject);
            } else {
                _instance = this;
            }
        }

        public void OpenDialog(Dialog dialog) {
            GameManager.Instance.SetGameState(GameState.CONVERSATION);
            const int MAX_MSG_LEN = 80;
            dialog.SplitLongMessages(MAX_MSG_LEN);
            
            dialogBox.SetActive(true);
            currentDialog = dialog;
            currentMessage = 0;
            DisplayMessage();
        }


        private void DisplayMessage() {
            Message message = currentDialog.messages[currentMessage];
            Actor firstActor = currentDialog.actors[message.actorId];
            
            firstActorImage.sprite = firstActor.sprite; 
            actorNameText.text = firstActor.name;
            dialogText.text = message.message;

            if (currentMessage + 1 < currentDialog.messages.Length) {
                int nextMessageIndex = currentMessage + 1;
                Actor secondActor = null;

                // Find the next actor that is different from the current actor
                while (nextMessageIndex < currentDialog.messages.Length) {
                    Message nextMessage = currentDialog.messages[nextMessageIndex];
                    Actor potentialSecondActor = currentDialog.actors[nextMessage.actorId];
                    if (potentialSecondActor.id != firstActor.id) {
                        secondActor = potentialSecondActor;
                        break;
                    }
                    nextMessageIndex++;
                }

                if (secondActor != null) {
                    secondActorImage.sprite = secondActor.sprite;
                    secondActorImage.color = Color.grey;
                } else {
                    secondActorImage.sprite = null;
                    secondActorImage.color = new Color(0, 0, 0, 0);
                }
            }
            else {
                secondActorImage.sprite = null;
                secondActorImage.color = new Color(0, 0, 0, 0);
            }
        }

        private void NextMessage() {
            currentMessage += 1;
            if (currentMessage < currentDialog.messages.Length) {
                DisplayMessage();
            }
            else {
                EndActiveDialog();
            }
        }

        public void EndActiveDialog() {
            currentDialog = null;
            currentMessage = 0;
            dialogBox.SetActive(false);
            GameManager.Instance.SetGameState(GameState.PLAYING);

        }

        private void Update() {
            if (currentDialog == null) return;
            if (Input.GetKeyDown(KeyCode.Space) || Input.GetMouseButtonDown(0)) {
                NextMessage();
            } 
        }
    }
}