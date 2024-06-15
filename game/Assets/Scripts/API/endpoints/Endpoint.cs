using System.Net;

namespace API.endpoints {
    public interface IEndpoint {
        public string GetPath();
        public void HandleContext(HttpListenerContext request);
    }
}