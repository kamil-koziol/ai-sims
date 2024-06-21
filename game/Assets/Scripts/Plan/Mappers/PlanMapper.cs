using System;
using System.Collections.Generic;
using BackendService.dto;

namespace Plan.Mappers
{
    public class PlanMapper
    {
        public static string dateFormat = "MM/dd/yyyy, HH:mm:ss";
        
        public static Plan Map(PlanResponse response)
        {

            var nodes = new List<PlanTask>();
            foreach (var node in response.plan)
            {
                nodes.Add(new PlanTask()
                {
                   time = DateTime.ParseExact(node.time, dateFormat, System.Globalization.CultureInfo.InvariantCulture),
                   location = node.location
                });
            }

            return new Plan()
            {
                tasks = nodes.ToArray()
            };
        }
    }
}