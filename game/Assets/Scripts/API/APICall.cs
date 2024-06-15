using System;
using System.Collections;
using UnityEngine;
using UnityEngine.Networking;

namespace DefaultNamespace {
    public class APICall {
        public static IEnumerator Call<T>(string url, Action<T> callback) {
            GameManager.Instance.SetGameState(GameState.WAITING_FOR_RESULTS);
            using (UnityWebRequest request = UnityWebRequest.Get(url)) {
                yield return request.SendWebRequest();

                switch (request.result) {
                    case UnityWebRequest.Result.ProtocolError:
                    case UnityWebRequest.Result.ConnectionError:
                    case UnityWebRequest.Result.DataProcessingError:
                        Debug.LogError(request.error);
                        break;
                    case UnityWebRequest.Result.Success:
                        string text = request.downloadHandler.text;
                        if (callback != null)
                        {
                            T t = JsonUtility.FromJson<T>(text);
                            callback(t);
                        }
                        GameManager.Instance.SetGameState(GameState.PLAYING);
                        break;
                }
            }
        }
        
        public static IEnumerator Call<T>(string url, string data, string contentType, Action<T> callback) {
            GameManager.Instance.SetGameState(GameState.WAITING_FOR_RESULTS);
            using (UnityWebRequest request = UnityWebRequest.Post(url, data, contentType)) {
                yield return request.SendWebRequest();

                switch (request.result) {
                    case UnityWebRequest.Result.ProtocolError:
                    case UnityWebRequest.Result.ConnectionError:
                    case UnityWebRequest.Result.DataProcessingError:
                        Debug.LogError(request.error);
                        break;
                    case UnityWebRequest.Result.Success:
                        string text = request.downloadHandler.text;
                        if (callback != null)
                        {
                            T t = JsonUtility.FromJson<T>(text);
                            callback(t);
                        }
                        GameManager.Instance.SetGameState(GameState.PLAYING);
                        break;
                }
            }
        }
    }
}