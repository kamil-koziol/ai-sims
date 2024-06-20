using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net;
using DefaultNamespace;
using UnityEngine;

namespace API.endpoints
{
    public class AgentMovementEndpoint: IEndpoint
    {
        private static AgentMovementEndpoint INSTANCE;
        private String PATH = "/agentMov";
        private AgentMovementEndpoint() {}

        public static AgentMovementEndpoint getInstance()
        {
            if (INSTANCE == null)
            {
                INSTANCE = new AgentMovementEndpoint();
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
            RequestWrapper rqWr = JsonUtility.FromJson<RequestWrapper>(body);

            if (rqWr == null)
            {
                context.Response.StatusCode = 400;
            }
            context.Response.StatusCode = 200;
        }

        public class RequestWrapper
        {
            public String agentName;
            public String fieldName;
            public int fieldPosition;
        }
    }
}