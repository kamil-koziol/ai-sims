using System;
using System.Collections.Generic;
using UnityEditor.UI;

namespace DefaultNamespace {
    public class AgentManager {
        private List<Agent> agents;
        public List<Agent> Agents => agents;

        public static AgentManager Instance;
        private void Awake() {
            Instance = this;
        }

        public void AddAgent(Agent agent) {
            this.agents.Add(agent);
        }

        public Agent GetAgentById(Guid id) {
            return agents.Find(agent => agent.ID == id);
        }
    }
}