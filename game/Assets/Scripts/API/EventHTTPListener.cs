using System;
using System.Collections.Generic;
using System.Net;
using System.Threading;
using API.endpoints;
using UnityEngine;

public class EventHTTPListener : MonoBehaviour {
    private HttpListener listener;
    private Thread listenerThread;
    
    private List<IEndpoint> endpoints;
    private Dictionary<string, IEndpoint> endpointPathResolver;

    private const int PORT = 4444;
    void Start() {
        endpoints = new List<IEndpoint>();
        endpointPathResolver = new Dictionary<string, IEndpoint>();
        RegisterEndpoint(new MockEndpoint());
        RegisterEndpoint(AgentMovementEndpoint.getInstance());
        RegisterEndpoint(GameInit.getInstance());
        RegisterEndpoint(PlanEndpoint.getInstance());
        
        listener = new HttpListener ();
        listener.Prefixes.Add ($"http://localhost:{PORT}/");
        listener.Prefixes.Add ($"http://127.0.0.1:{PORT}/");
        listener.AuthenticationSchemes = AuthenticationSchemes.Anonymous;
        listener.Start ();

        listenerThread = new Thread (startListener);
        listenerThread.Start ();
        Debug.Log ($"Server Started on PORT: {PORT}");
    }

    public void RegisterEndpoint(IEndpoint endpoint) {
        endpoints.Add(endpoint);
        endpointPathResolver.Add(endpoint.GetPath(), endpoint);
    }
    
    private void startListener ()
    {
        while (true) {               
            var result = listener.BeginGetContext (ListenerCallback, listener);
            result.AsyncWaitHandle.WaitOne ();
        }
    }
    
    private void ListenerCallback (IAsyncResult result)
    {				
        var context = listener.EndGetContext (result);		

        Debug.Log ("Method: " + context.Request.HttpMethod);
        Debug.Log ("LocalUrl: " + context.Request.Url.LocalPath);
        const string JSONContentType = "application/json";
        if (context.Request.HttpMethod == "POST") {	
            if(context.Request.ContentType != JSONContentType) return;
            
            if (endpointPathResolver.TryGetValue(context.Request.Url.LocalPath, out IEndpoint endpoint)) {
                endpoint.HandleContext(context);
            }
            Debug.Log("Status code: " + context.Response.StatusCode);
            context.Response.Close ();
            return;
        }
        
        context.Response.StatusCode = 401;
        context.Response.Close ();
    }
}
