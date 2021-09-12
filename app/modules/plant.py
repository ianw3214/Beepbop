import app.module

import util.logger

import datetime
import dateutil

class PlantModule(app.module.Module):
    def __init__(self, client):
        app.module.Module.__init__(self, client, "plant")
        self.plants = {}
        self._registerMessageCommand("add", self.addPlant)

    async def delayedUpdate(self):
        currTime = datetime.datetime.now()
        for user in self.plants:
            for plant in self.plants[user]:
                plantData = self.plants[user][plant]
                lastTime = plantData["lastWatered"]
                delta = datetime.timedelta(days=plantData["daysToWater"])
                needsWater = lastTime + delta
                if currTime > needsWater:
                    message = "<@{}> Plant {} needs to be watered!".format(user, plant)
                    util.logger.log("plant", message)
                    msgObj = await self._sendMessage(message)
                    self._registerReactListener(msgObj, self.waterMessageReact)

    # COMMAND: $plant add <name> <days-to-water>
    async def addPlant(self, rawMessage, tokens):
        user = rawMessage.author.id
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
        message = "Added plant {} for user <@{}>".format(plantName, user)
        self._sendMessage(message)
        util.logger.log("plant", message)

    async def waterMessageReact(self, reaction, user):
        print("Reacted!!!")

    def _dateToStr(self, date):
        return str(date)
    
    def _strToDate(self, string):
        return dateutil.parser.parse(string)