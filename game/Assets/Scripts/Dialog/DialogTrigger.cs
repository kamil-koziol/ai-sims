using UnityEngine;

namespace Dialog {
    public class DialogTrigger : MonoBehaviour {
        [SerializeField] private Message[] messages;
        [SerializeField] private Actor[] actors;

        private Dialog IntoDialog() {
            Dialog dialog = new Dialog(messages, actors);
            return dialog;
        }
        public void StartDialog() {
            var dialog = IntoDialog();
            DialogManager.Instance.OpenDialog(dialog);
        }
    }
}