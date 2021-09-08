import app.module

import util.discord

import datetime
import dateutil

class PlantModule(app.module.Module):
    def __init__(self):
        app.module.Module.__init__(self, "plant")
        self.plants = {}
        self._registerMessageCommand("add", self.addPlant)

    def delayedUpdate(self):
        currTime = datetime.datetime.now()
        for user in self.plants:
            for plant in self.plants[user]:
                plantData = self.plants[user][plant]
                lastTime = plantData["lastWatered"]
                delta = datetime.timedelta(days=plantData["daysToWater"])
                needsWater = lastTime + delta
                if currTime > needsWater:
                    # TODO: Send a message to the channel
                    print("Plant {} needs to be watered!".format(plant))

    # COMMAND: $plant add <name> <days-to-water>
    def addPlant(self, rawMessage, tokens):
        user = util.discord.getMessageAuthorID(rawMessage)
        if len(tokens) < 2:
            # TODO: Error handling
            return
        # TODO: Token validation
        plantName = tokens[0]
        daysToWater = tokens[1]
        if user not in self.plants:
            self.plants[user] = {}
        plantData = {
            "daysToWater" : int(daysToWater),
            "lastWatered" : datetime.datetime.now()
        }
        self.plants[user][plantName] = plantData
        print(plantData)
        
    def _dateToStr(self, date):
        return str(date)
    
    def _strToDate(self, string):
        return dateutilparser.parse(string)