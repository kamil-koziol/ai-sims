using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net;
using DefaultNamespace;
using Newtonsoft.Json;
using UnityEngine;

namespace API.endpoints
{
    public class GameInit: IEndpoint
    {
        private static GameInit INSTANCE;
        private String PATH = "/game";
        private GameInit() {}

        public static GameInit getInstance()
        {
            if (INSTANCE == null)
            {
                INSTANCE = new GameInit();
            }
            
            return INSTANCE;
        }
        
        public string GetPath()
        {
            return PATH;
        }

        public void HandleContext(HttpListenerContext context)
        {
            var body = new StreamReader(context.Request.InputStream, 
                context.Request.ContentEncoding).ReadToEnd();
            Debug.Log("Request body");
            Debug.Log(body);
            BackendService.GameSnapshot rqWr = JsonConvert.DeserializeObject<BackendService.GameSnapshot>(body);

            if (rqWr.agents == null)
            {
                context.Response.StatusCode = 400;
                return;
            }

            var json = JsonConvert.SerializeObject(rqWr.id);
            context.Response.ContentType = "application/json";
            var writer = new StreamWriter(context.Response.OutputStream);
            writer.Write(json);
            writer.Flush();
            
            Debug.Log("Response body");
            Debug.Log(json);
            context.Response.StatusCode = 200;
        }
    }
}