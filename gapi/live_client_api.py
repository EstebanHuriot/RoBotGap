import requests
import pandas as pd
import time
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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


    def get_live_data(self):
        response = self.get_live_data_check()

        if response["ok"] == False:
            return response
        
        data = response["data"]
        return data
    

    def event_monitoring(response, last_event_id):
        events = response['events']['Events']
    
        for event in events:
            if event['EventID'] <= last_event_id:
                continue
            
            print("New event:", event["EventID"], event["EventName"])
    
            last_event_id = event["EventID"]
    
        return last_event_id
    

def death_check(response): # might be useless
    check = response['allPlayers'][0]['isDead']

    if check == True:
        return print('dead')


def event_parsing(event, data):
    event_name = event['EventName']
    assisters = event.get('Assisters', [])
    killer = event.get('KillerName', None)
    victime = event.get('VictimName', None)

    data.append({"eventid": event['EventID'],
            "event_name": event_name,
            "assisters": assisters,
            "killer": killer,
            "victime": victime})
    
    return data


def event_monitoring(response, last_event_id, data):
    events = response['events']['Events']

    for event in events:
        if event['EventID'] <= last_event_id:
            continue

        print("New event:", event["EventID"], event["EventName"])

        event_parsing(event, data)

        last_event_id = event["EventID"]

    return last_event_id, data