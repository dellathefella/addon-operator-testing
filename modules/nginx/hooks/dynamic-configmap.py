#!/usr/bin/env python3
from datetime import datetime
from kubernetes import client, config
import json
import requests
import sys

def random_user():
        response = requests.get("https://randomuser.me/api")
        response = json.loads(response.text)
        return response

if __name__ == "__main__":
    if len(sys.argv)>1 and sys.argv[1] == "--config":
        hook_config = {
            "configVersion": "v1",
            "beforeHelm": 1,
            "afterHelm": 1,
            "schedule":[
                {
                "crontab": "* * * * *",
                "allowFailure": True
                }
            ]
        }
        hook_config_json = json.dumps(hook_config)
        print(f'{hook_config_json}')
    else:
        print("Python powered hook")
        
        try:
            config.load_incluster_config()
        except:
            config.load_kube_config()
        
        config_map_name = "dynamic-configmap"
        v1 = client.CoreV1Api()
        metadata = client.V1ObjectMeta(name=config_map_name)
        
        # Get current time
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        
        # Dynamic configmap
        config_map = {
            "memory": "256Gi",
            "coreCPU": f'{current_time}',
            "crap": f'{random_user()}'
        }

        config_map_body = client.V1ConfigMap(data=config_map, metadata=metadata)
        try:
            v1.create_namespaced_config_map(namespace="default", body=config_map_body)
        except:
            v1.patch_namespaced_config_map(name=config_map_name,namespace="default", body=config_map_body)
        print(f'{config_map_name} has been succesfully reconciled.')