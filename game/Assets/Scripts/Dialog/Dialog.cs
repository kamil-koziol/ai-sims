using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

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
        public void SplitLongMessages(int maxLength)
        {
            List<Message> processedMessages = new List<Message>();

            foreach (var message in messages)
            {
                if (message.message.Length <= maxLength)
                {
                    processedMessages.Add(message);
                }
                else
                {
                    string[] words = message.message.Split(' ');
                    string part = "";
                    foreach (var word in words)
                    {
                        if (part.Length + word.Length + 1 <= maxLength) // +1 for the space
                        {
                            if (part.Length > 0)
                            {
                                part += " ";
                            }
                            part += word;
                        }
                        else
                        {
                            processedMessages.Add(new Message { actorId = message.actorId, message = part + ".." });
                            part = word;
                        }
                    }
                    if (part.Length > 0)
                    {
                        processedMessages.Add(new Message { actorId = message.actorId, message = part + ".." });
                    }
                }
            }

            messages = processedMessages.ToArray();
        }
    }

    [Serializable]
    public class Message {
        public int actorId;
        public string message;
    }

    [Serializable]
    public class Actor {
        public int id;
        public Sprite sprite;
        public string name;
    }
}
