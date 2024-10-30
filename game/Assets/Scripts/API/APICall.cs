using System;
using System.Collections;
using Newtonsoft.Json;
using UnityEngine;
using UnityEngine.Networking;

namespace DefaultNamespace {
    public class APICall {
        public static IEnumerator Call<T>(string url, Action<T> callback) {
            var previousGameState = GameManager.Instance.GameState;
            GameManager.Instance.SetGameState(GameState.WAITING_FOR_RESULTS);
            using (UnityWebRequest request = UnityWebRequest.Get(url)) {
                yield return request.SendWebRequest();

                switch (request.result) {
                    case UnityWebRequest.Result.ProtocolError:
                    case UnityWebRequest.Result.ConnectionError:
                    case UnityWebRequest.Result.DataProcessingError:
                        Debug.LogError(request.downloadHandler.text);
                        Debug.LogError(request.error);
                        break;
                    case UnityWebRequest.Result.Success:
                        GameManager.Instance.SetGameState(previousGameState);
                        string text = request.downloadHandler.text;
                        if (callback != null)
                        {
                            T t = JsonConvert.DeserializeObject<T>(text);
                            if (t != null)
                            {
                                callback(t);
                            }
                            else 
                            {
                                Action<string> callbackString = callback as Action<string>;
                                if (typeof(T) == typeof(string) && callbackString != null)
                                {
                                    callbackString(text);
                                }
                            }
                            Debug.Log(text);
                        }
                        break;
                }
            }
        }
        
        public static IEnumerator Call<T>(string url, string data, string contentType, Action<T> callback) {
            var previousGameState = GameManager.Instance.GameState;
            GameManager.Instance.SetGameState(GameState.WAITING_FOR_RESULTS);
            using (UnityWebRequest request = UnityWebRequest.Post(url, data, contentType)) {
                yield return request.SendWebRequest();

                switch (request.result) {
                    case UnityWebRequest.Result.ProtocolError:
                    case UnityWebRequest.Result.ConnectionError:
                    case UnityWebRequest.Result.DataProcessingError:
                        Debug.LogError(request.downloadHandler.text);
                        Debug.LogError(request.error);
                        break;
                    case UnityWebRequest.Result.Success:
                        GameManager.Instance.SetGameState(previousGameState);
                        string text = request.downloadHandler.text;
                        if (callback != null)
                        {
                            if (contentType == "application/json")
                            {
                                T t = JsonConvert.DeserializeObject<T>(text);
                                callback(t);
                            }
                            else if (contentType == "application/yaml")
                            {
                                Action<string> callbackString = callback as Action<string>;
                                if (typeof(T) == typeof(string) && callbackString != null)
                                {
                                    callbackString(text);
                                }
                            }
                            Debug.Log(text);
                        }

                        break;
                }
            }
        }
    }
}