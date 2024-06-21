using System;

namespace Plan
{
    public class PlanTask
    {
        public DateTime time;
        public string location;
    }
    public class Plan
    {
        public PlanTask[] tasks;
    }
}