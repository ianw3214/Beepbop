import app.module

import requests

import app.database.database
import app.settings

import util.logger

RIOT_ENDPOINT="https://na1.api.riotgames.com"
SUMMONER_API = "/lol/summoner/v4/summoners/by-name/"
MATCHES_API_PREFIX = "/lol/match/v5/matches/by-puuid/"
MATCHES_API_POSTFIX = "/ids"
MATCH_API = "/lol/match/v5/matches/"

def getSummonerEndpoint(summoner_name):
    return RIOT_ENDPOINT + SUMMONER_API + summoner_name

def getMatchesEndpoint(summoner_ppuid):
    return RIOT_ENDPOINT + MATCHES_API_PREFIX + summoner_ppuid + MATCHES_API_POSTFIX

def getMatchEndpoint(match_id):
    return RIOT_ENDPOINT + MATCH_API + match_id

def appendAPIKey(endpoint):
    return endpoint + "?api_key=" + app.settings.getRiotGamesAPI()

class LeagueModule(app.module.Module):
    def __init__(self, client, eventQueue):
        app.module.Module.__init__(self, client, eventQueue, "league")
        self._registerMessageCommand("add", self.addSummoner)

    async def delayedUpdate(self):
        pass

    async def addSummoner(self, rawMessage, tokens):
        user = rawMessage.author.id
        if len(tokens) < 1:
            message = "Incorrect format for league add command\n"
            message += "> $league add 'summoner name'"
            await self._sendMessage(message)
            util.logger.log("league", message)
            return
        summonerName = " ".join(tokens)
        # get the summoner puuid as well
        endpoint = appendAPIKey(getSummonerEndpoint(summonerName))
        response = requests.get(endpoint)
        # TODO: Handle request failure
        responseData = response.json()
        puuid = responseData["puuid"]
        # Add the data to our own database
        collection = app.database.database.getCollection("league", "userdata")
        userData = app.database.database.getDocument("league", "userdata", user)
        if userData is None:
            userData = { "name" : summonerName, "puuid" : puuid }
            app.database.database.insertToCollection(collection, userData, user)
        else:
            userData = { "name" : summonerName, "puuid" : puuid }
            collection.replace_one({"_id" : user}, userData)
        # User feedback and logging
        message = "Started tracking summoner {} for user <@{}>".format(summonerName, user)
        await self._sendMessage(message)
        util.logger.log("league", message)
