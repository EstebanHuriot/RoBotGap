from bot.crew import Crew, CrewMember

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


async def event_monitoring(crew:Crew, response, last_event_id, data):
    game_started = False
    game_ended = False
    player_killed = False 
    player_died = False
    player_assisted = False
    crew_names = crew.show()
    
    events = response['events']['Events']
    
    for event in events:
        if event['EventID'] <= last_event_id:
            continue

        print("New event:", event["EventID"], event["EventName"])

        event_parsing(event, data)

        last_event_id = event["EventID"] # event is considered done

        if event["EventName"] == "GameStart":
            game_started = True
            
        
        if event['EventName'] == "GameEnd":
            game_ended = True
 
            
        if event["EventName"] == "ChampionKill":
            victim = event.get("VictimName")
            killer = event.get("KillerName")
            assisters = event.get("Assisters", [])

            if victim in crew_names:
                print('Player dead')
                player_died = True

            if killer in crew_names:
                print("A crew member has made a kill")
                player_killed = True

            if any(assister in crew_names for assister in assisters):
                print("A crew member has made an assist")
                player_assisted = True

    print("event_monitoring retourne :", last_event_id)
    return last_event_id, data, game_started, game_ended, player_killed, player_died, player_assisted