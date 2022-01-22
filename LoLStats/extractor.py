# Getting Summoner Stats by handle
import json
from riotwatcher import LolWatcher, ApiError

class RiotPlayerStatsStaging(LolWatcher,):
    f = open('lol_api_key.json')
    api_key = json.load(f)
    key=api_key['api_key']
    log = LolWatcher(key)

    """ Getting Player Stats """

    def __init__(self,player,region):
        self.player = player
        self.region = region

    def search_summoner(self):
        return self.log.summoner.by_name(self.region,self.player)

    def get_ranked_stats(self):
        player_info = self.search_summoner()
        return self.log.league.by_summoner(self.region,player_info['id'])

    """ One issue with the LolWatcher class is that methods like matchlist_by_puuid
        take different values for regions (e.g. 'americas' vs 'na1' in the search method.
        Given this I'm introducing a separate input for region in get_last_match_ids """

    def get_last_match_ids(self,region):
        puuid = self.search_summoner()['puuid']
        return LolWatcher(self.key).match.matchlist_by_puuid(region,\
               self.search_summoner()['puuid'])

class LoLStatsLoad(RiotPlayerStatsStaging):
    """ Get item/kda stats for a given player """
    def __init__(self, parent):
        self.parent = parent
        self.player = parent.player
        self.region = parent.region

    def load_game_stats_by_number(self,match_number,region):
        game = self.parent.get_last_match_ids()[match_number]
        players = []
        return self.parent.log.match.by_id(region,game)
