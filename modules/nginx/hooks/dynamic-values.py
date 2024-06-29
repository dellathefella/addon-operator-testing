#!/usr/bin/env python3
import json
import sys
import random
import os
import pathlib as Path
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
        print("Python values update hook")
        values_patch = [
                {
                "op": "replace",
                "path": "/nginx/params/replicas",
                "value": random.randint(1, 9)
                }
        ]
        path = Path(os.getenv("VALUES_JSON_PATCH_PATH"))
        with open(path, "w") as file:
            file.write(json.dumps(values_patch))
            file.close
        print(f'Runtime values have been succesfully reconciled.')