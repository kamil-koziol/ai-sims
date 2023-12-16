using System.IO;
using System.Net;
using UnityEngine;

namespace API.endpoints {
    public class MockEndpoint: IEndpoint{
        public MockEndpoint() {
        }

        public string GetPath() {
            return "/mock";
        }

        public void HandleRequest(HttpListenerRequest request) {
            var body = new StreamReader(request.InputStream, 
                request.ContentEncoding).ReadToEnd();
            
            Debug.Log("Mocked");
        }
    }
}