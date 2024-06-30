#!/usr/bin/env python3
import json
import sys
import random
import os
import sys
import pathlib as Path
from kubernetes import client, config

# Custom library imports
from truenasclient import returnServices


def load_nginx_crds ():
   try:
      config.load_incluster_config()
   except:
      config.load_kube_config()
        
   v1 = client.CustomObjectsApi()
   resp = v1.list_cluster_custom_object(group="poc.com",version="v1alpha",plural="nginxes")
   print(resp)
   return resp

if __name__ == "__main__":
   if len(sys.argv)>1 and sys.argv[1] == "--config":
      hook_config = {
      "configVersion": "v1",
      "onStartup": 1,
      "schedule":[
            {
                "crontab": "* * * * *",
                "allowFailure": True
            }
         ],
      "kubernetes":[
         {
            "apiVersion": "poc.com/v1alpha",
            "kind": "Nginx",
            "executeHookOnEvent":["Added","Deleted","Modified"]
         },
         ],
      }
      hook_config_json = json.dumps(hook_config)
      print(f'{hook_config_json}')
   else:
      print(returnServices())
      print("Python global runtime values hook.")
      runtime_patch_path = os.getenv("VALUES_JSON_PATCH_PATH")
      namespace = os.getenv("ADDON_OPERATOR_NAMESPACE")
      nginx_replica_groups = load_nginx_crds()
      nginx_replica_group_patches = []
      for nginx_replica_group in nginx_replica_groups["items"]:
         minReplicas = nginx_replica_group["spec"]["minReplicas"]
         maxReplicas = nginx_replica_group["spec"]["maxReplicas"]
         name = nginx_replica_group["metadata"]["name"]
         sub_patch = {
            "name": name,
            "replicas": random.randint(minReplicas, maxReplicas),
            "namespace": namespace
         }
         nginx_replica_group_patches.append(sub_patch)

      nginx_global_patch = {
            "op": "add",
            "path":"/global/nginxReplicaGroups",
            "value": nginx_replica_group_patches
      }

      print(nginx_global_patch)

      runtime_patch_data = json.dumps(nginx_global_patch)
      with open(runtime_patch_path, 'w') as patch_file:
         patch_file.write(runtime_patch_data)
      patch_file.close()
      print("Global runtime values were succesfully reconciled") 
