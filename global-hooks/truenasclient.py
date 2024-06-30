#!/usr/bin/env python3

import requests
import argparse
import os
import sys
import json

def returnServices():
   api_key = os.getenv("TRUENAS_API_KEY")
   url = os.getenv("TRUENAS_URL")
   if not api_key:
      raise Exception("TRUENAS_API_KEY environment variable was not found. Exitting.....")
   if not url:
      raise Exception("TRUNAS_URL environment variable was not found. Exitting.....")
   headers = { 'Authorization' : f'Bearer {api_key}', "Content-Type": "application/json"}
   response = requests.get(url=url+"/api/v2.0/service",headers=headers)
   response = json.loads(response.text)
   return response

if __name__ == "__main__":
   if len(sys.argv)>1 and sys.argv[1] == "--config":
      hook_config = {
      "configVersion": "v1",
      "onStartup": 1,
      }
      hook_config_json = json.dumps(hook_config)
      print(f'{hook_config_json}')