using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

using UnityEngine;
using System.Collections.Generic;

namespace Dialog {
    public class Dialog {
        public Message[] messages;
        public Actor[] actors;

        public Dialog(Message[] messages, Actor[] actors) {
            this.messages = messages;
            this.actors = actors;
        }

        public class Builder {
            private List<Message> messages = new List<Message>();
            private List<Actor> actors = new List<Actor>();

            public Builder SetMessages(Message[] messages) {
                this.messages = new List<Message>(messages);
                return this;
            }

            public Builder SetActors(Actor[] actors) {
                this.actors = new List<Actor>(actors);
                return this;
            }

            public Builder AddActor(Actor actor) {
                this.actors.Add(actor);
                return this;
            }

            public Builder AddMessage(Message message) {
                this.messages.Add(message);
                return this;
            }

            public Dialog Build() {
                Dialog dialog = new Dialog(messages.ToArray(), actors.ToArray());
                return dialog;
            }
        }
    }

    public class Message {
        public int actorId;
        public string message;
    }

    public class Actor {
        public int id;
        public Sprite sprite;
    }
}
