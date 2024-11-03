using System;

namespace BackendService.dto
{
    public struct InterviewRequest
    {
        public String question;
        public Location location;
        public String time;
    }
    
    public struct InterviewResponse
    {
        public String response;
    }
}