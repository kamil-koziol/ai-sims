using System;
using System.Collections;
using System.Threading;
using DefaultNamespace;
using UnityEngine;
using UnityEngine.Networking;
using UnityEngine.UI;

namespace BackendService {
    public class BackendService: MonoBehaviour {
        
        public static BackendService Instance;
        private string URL = "http://localhost:8080";

        private void Awake() {
            Instance = this;
        }

        struct Test {
            private string text;
        }

        public void GetMock() {
            StartCoroutine(APICall.Call<Test>(URL, null));
            return;
        }
    }
}