#!/usr/bin/env python3
import json
import sys
import random
import os
import pathlib as Path

if __name__ == "__main__":
    values_patch = [
        {
        "op": "replace",
        "path": "/nginx/params/replicas",
        "value": random.randint(1, 9)
        }
    ]
    print(json.dumps(values_patch), end="")