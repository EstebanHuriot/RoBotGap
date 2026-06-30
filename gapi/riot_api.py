import requests

class RiotAPI:

    def __init__(self, api_key, region):
        self.api_key = api_key
        self.region = region


    def get(self, region, endpoint, params=None):
        
        if params is None:
            params={}

        params['api_key'] = self.api_key
        url = f"https://{region}.api.riotgames.com{endpoint}"
        
        response = requests.get(url, params=params)

        if response.status_code == 200:
            return response.json()
        
        return {"error": response.status_code, "message": response.text}


    def get_puuid(self, game_name, tag_line):
        """ 
        puuid is the primary key for players in the database
        """
        endpoint = f"/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
        return self.get(self.region, endpoint)
    

    def get_match_history(self, puuid, start=0, count=20):
        endpoint = f"/lol/match/v5/matches/by-puuid/{puuid}/ids"
        params = {"start": start, "count": count}
        return self.get(self.region, endpoint, params)


    def get_match_data(self, match_id):
        endpoint = f"/lol/match/v5/matches/{match_id}"
        return self.get(self.region, endpoint)
    

    def get_match_timeline(self, match_id):
        endpoint = f"/lol/match/v5/matches/{match_id}/timeline"
        return self.get(self.region, endpoint)