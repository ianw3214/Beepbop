import os
import json

SETTINGS_PATH = "settings.json"

def getFileData():
    rawData = open(SETTINGS_PATH, "r")
    return json.load(rawData)

def getDiscordBotToken():
    token = os.getenv('DISCORD_TOKEN')
    if token is None:
        data = getFileData()
        token = data["token"]
    return token

# TODO: Get strava data from some database somewhere
# needs to be updated so can't use environment variable
def getStravaData():
    data = getFileData()
    return data["strava"]

def updateSettingsCallback(token, refresh, expires):
    jsonData = None
    with open(SETTINGS_PATH, "r") as rawFile:
        jsonData = json.load(rawFile)
        jsonData["strava"]["token"] = token
        jsonData["strava"]["refresh"] = refresh
        jsonData["strava"]["expires"] = expires
    with open(SETTINGS_PATH, "w") as rawFile:
        json.dump(jsonData, rawFile, indent=4)