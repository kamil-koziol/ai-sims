using System;
using System.Collections.Generic;
using System.IO;
using System.Net;
using Newtonsoft.Json;
using UnityEngine;

namespace API.endpoints
{
    public class PlanEndpoint: IEndpoint
    {
        private static PlanEndpoint INSTANCE;
        private String PATH = "/plan";
        private PlanEndpoint() {}
        private static PlanResponse mockResponse;
        public static PlanEndpoint getInstance()
        {
            if (INSTANCE == null)
            {
                INSTANCE = new PlanEndpoint();
            }
            mockResponse = new PlanResponse();
            mockResponse.plan = new List<Agent.PlanEntry>();
            Agent.PlanEntry planEntry = new Agent.PlanEntry { time="1632", location="Grass"};
            Agent.PlanEntry planEntry2 = new Agent.PlanEntry { time="2032", location="House"};
            mockResponse.plan.Add(planEntry);
            mockResponse.plan.Add(planEntry2);
            return INSTANCE;
        }
        
        public string GetPath()
        {
            return PATH;
        }
        
        struct PlanResponse
        {
            public List<Agent.PlanEntry> plan;
        }

        struct PlanRequest
        {
            
        }
        public void HandleContext(HttpListenerContext context)
        {
            var body = new StreamReader(context.Request.InputStream, 
                context.Request.ContentEncoding).ReadToEnd();
            Debug.Log("Request body");
            Debug.Log(body);
            BackendService.PlanRequest rqWr = JsonConvert.DeserializeObject<BackendService.PlanRequest>(body);

            if (rqWr.game_id == null)
            {
                context.Response.StatusCode = 400;
                return;
            }
            
            var json = JsonConvert.SerializeObject(mockResponse);
            context.Response.ContentType = "application/json";
            using (var writer = new StreamWriter(context.Response.OutputStream))
            {
                writer.Write(json);
                writer.Flush();
            }
            
            Debug.Log("Response body");
            Debug.Log(json);
            context.Response.StatusCode = 200;
        }
    }
}