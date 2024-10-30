using System;
using System.Collections.Generic;
using BackendService.dto;
using UnityEngine;

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
                   time = DateTime.Parse(node.time, null, System.Globalization.DateTimeStyles.RoundtripKind),
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