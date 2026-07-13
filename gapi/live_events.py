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


async def event_monitoring(crew:list, response, last_event_id, data):
    game_start = False
    player_killed = False 
    player_died = False
    player_assisted = False
    
    
    events = response['events']['Events']

    for event in events:
        if event['EventID'] <= last_event_id:
            continue

        print("New event:", event["EventID"], event["EventName"])

        event_parsing(event, data)

        if event["EventName"] == "GameStart":
            game_start = True

        if event["EventName"] == "ChampionKill":
            victim = event.get("VictimName")
            killer = event.get("KillerName")
            assisters = event.get("Assisters", [])

            if victim in crew:
                print('Player dead')
                player_died = True

            if killer in crew:
                print("A crew member has made a kill")
                player_killed = True

            if any(assister in crew for assister in assisters):
                print("A crew member has made an assist")
                player_assisted = True

        last_event_id = event["EventID"]

    return last_event_id, data, game_start, player_killed, player_died, player_assisted