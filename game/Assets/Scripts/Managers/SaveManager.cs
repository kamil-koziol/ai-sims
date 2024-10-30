using System;
using UnityEngine;

namespace DefaultNamespace.Managers
{
    public class SaveManager : MonoBehaviour
    {
        private void Update()
        {
            if (Input.GetKeyDown(KeyCode.F1))
            {
                //GameManager.Instance.SetGameState(GameState.WAITING_FOR_RESULTS);
                GameManager.Instance.registerCoroutine(GameManager.Instance.BackendService.GameYaml(response =>
                {
                    GameManager.Instance.restartGame();
                    GameManager.Instance.ID = Guid.Parse(response.game.id.ToString());
                    Debug.Log(response);
                      foreach (var agent in response.game.agents)
                      {
                          GameObject instance = Instantiate(GameManager.Instance.agentPrefab, new Vector3(0, 0, 0), Quaternion.identity);
                          global::Agent newAgent = instance.GetComponent<global::Agent>();
                          newAgent.setFieldsAgent(agent.age, agent.description, agent.lifestyle, agent.name, "Other_F_A", agent.id);
                          newAgent.loadRandomSprite();
                          GameManager.Instance.AddAgentToGame(newAgent);
                      }

                      GameManager.Instance.GenerateAgentsPlan();
                    Debug.Log(response.game.id.ToString());
                }));
            }
            if (Input.GetKeyDown(KeyCode.F2))
            {
                //GameManager.Instance.SetGameState(GameState.WAITING_FOR_RESULTS);
                GameManager.Instance.registerCoroutine(GameManager.Instance.BackendService.GetGameYaml());
            }
        }
    }
}