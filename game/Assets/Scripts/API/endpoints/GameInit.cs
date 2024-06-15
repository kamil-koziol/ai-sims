using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net;
using DefaultNamespace;
using UnityEngine;

namespace API.endpoints
{
    public class GameInit: IEndpoint
    {
        private static GameInit INSTANCE;
        private String PATH = "/init";
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
            Debug.Log(body);
            BackendService.GameSnapshot rqWr = JsonUtility.FromJson<BackendService.GameSnapshot>(body);

            if (rqWr.agents == null)
            {
                context.Response.StatusCode = 400;
            }

            context.Response.StatusCode = 200;
        }
    }
}