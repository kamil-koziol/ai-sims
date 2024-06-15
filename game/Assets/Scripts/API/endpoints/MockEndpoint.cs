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

        public void HandleContext(HttpListenerContext context) {
            var body = new StreamReader(context.Request.InputStream, 
                context.Request.ContentEncoding).ReadToEnd();
            
            Debug.Log("Mocked");
        }
    }
}