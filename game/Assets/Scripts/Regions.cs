using System;
using System.Collections.Generic;
using System.Linq;
using Newtonsoft.Json;
using UnityEngine;
using Random = System.Random;

namespace DefaultNamespace
{
    public class Regions : MonoBehaviour
    {
        //If you add region make sure to add its name in Constants
        [SerializeField] private Transform regions;
        
        private static readonly Random random = new();
        public Dictionary<String, HashSet<Transform>> regionNameToSetOfPoints = new();
        private void Awake() {
            foreach (Transform child in regions)
            {
                if (!regionNameToSetOfPoints.ContainsKey(child.name))
                {
                    regionNameToSetOfPoints.Add(child.name, new HashSet<Transform>());
                }
                foreach (Transform targets in child)
                {
                    foreach (Transform point in targets)
                    {
                        regionNameToSetOfPoints[child.name].Add(point);
                    }
                }
            }
        }

        public Transform getRandomTranformFromRegion(String regionName)
        {
            return regionNameToSetOfPoints[regionName].ElementAt(random.Next(regionNameToSetOfPoints[regionName].Count - 1));
        }

        public Transform getRandomTransformFromRandomRegion()
        {
            List<String> keys = new List<String>(regionNameToSetOfPoints.Keys);
            int randomIndex = random.Next(keys.Count - 1);
            return getRandomTranformFromRegion(keys[randomIndex]);
        }

        public static String getParentName(Transform point)
        {
            if (point == null)
            {
                return "NONE";
            }
            return point.parent.parent.name;
        }

        public RegionState getRegionsState()
        {
            // String json = "";
            //
            // foreach (var keyval in regionNameToSetOfPoints)
            // {
            //     json += JsonConvert.SerializeObject( regionNameToSetOfPoints );
            // }\
            RegionState state = new RegionState();
            state.regions = new List<string>(regionNameToSetOfPoints.Keys);
            return state;
        }

        public struct RegionState
        {
            public List<String> regions;
        }
    }
}