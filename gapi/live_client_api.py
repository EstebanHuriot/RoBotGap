import requests
import pandas as pd
import time
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import credentials as cr
import discord

class LiveClientAPI:

    def __init__(self):
        self.base_url = "https://127.0.0.1:2999/liveclientdata/allgamedata"


    def get_live_data_check(self):

        try:   
            response = requests.get(self.base_url, verify=False)
    
            if response.status_code == 200:
                return {"ok": True, "data": response.json()}
            
            return {"ok": False, "error": response.status_code, "message": response.text}
        
        except requests.exceptions.ConnectionError:
            return {"ok": False, "error": "local_api_unavailable", "message": "Live Client Data API unavailable. The player is probably not in game."}


    
