using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace Dialog {
    public class DialogManager : MonoBehaviour {
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
            currentDialog = dialog;
            currentMessage = 0;
            DisplayMessage();
        }

        private void DisplayMessage() {
            bool isFirstMessage = currentMessage == 0;
            if (isFirstMessage) {
                Actor firstActor = currentDialog.actors[currentDialog.messages[0].actorId];
                firstActorImage.sprite = firstActor.sprite;
                actorNameText.text = firstActor.name;
                dialogText.text = currentDialog.messages[currentMessage].message;
                
                Actor secondActor = currentDialog.actors[currentDialog.messages[1].actorId];
                secondActorImage.sprite = secondActor.sprite;
                
            }
        }

        private void NextMessage() {
            currentMessage += 1;
        }

        public void EndActiveDialog() {
            currentDialog = null;
            currentMessage = 0;
        }
    }
}