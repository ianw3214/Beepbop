import json

SETTINGS_PATH = "settings.json"

def getFileData():
    rawData = open(SETTINGS_PATH, "r")
    return json.load(rawData)

def getDiscordBotToken():
    data = getFileData()
    return data["token"]