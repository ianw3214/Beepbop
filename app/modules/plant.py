import app.module

import app.database.database

import util.logger

import datetime
import dateutil

class PlantModule(app.module.Module):
    def __init__(self, client, eventQueue):
        app.module.Module.__init__(self, client, eventQueue, "plant")
        self.plants = {}
        self._registerMessageCommand("add", self.addPlant)
        self._registerMessageCommand("stats", self.showStats)
        self._registerReactListener(self.waterMessageReact)

    async def delayedUpdate(self):
        currTime = datetime.datetime.now()
        collection = app.database.database.getCollection("plant", "userdata")
        cursor = collection.find()
        for userDocument in cursor:
            userid = userDocument["_id"]
            dirty = False
            for plant in userDocument["plants"]:
                plantData = userDocument["plants"][plant]
                lastTime = plantData["lastWatered"]
                delta = datetime.timedelta(days=plantData["daysToWater"])
                needsWater = lastTime + delta
                if currTime > needsWater:
                    # If message is already sent, don't send again
                    if "messageID" not in plantData:
                        message = "<@{}> Plant {} needs to be watered!\nReact to this message once you've watered your plant :)".format(userid, plant)
                        util.logger.log("plant", message)
                        msgObj = await self._sendMessage(message)
                        plantData["messageID"] = msgObj.id
                        dirty = True
            if dirty:
                collection.replace_one({"_id":userid}, userDocument)


    # COMMAND: $plant add <name> <days-to-water>
    async def addPlant(self, rawMessage, tokens):
        user = rawMessage.author.id
        if len(tokens) < 2:
            # TODO: Error handling
            return
        # TODO: Token validation
        plantName = tokens[0]
        daysToWater = tokens[1]
        plantData = {
            "daysToWater" : int(daysToWater),
            "lastWatered" : datetime.datetime.now()
        }
        # Add new plant data to database
        collection = app.database.database.getCollection("plant", "userdata")
        userData = app.database.database.getDocument("plant", "userdata", user)
        if userData is None:
            userData = { "plants" : { plantName : plantData} }
            app.database.database.insertToCollection(collection, userData, user)
        else:
            userData["plants"][plantName] = plantData
            collection.replace_one({"_id" : user}, userData)
        # User feedback and logging
        message = "Added plant {} for user <@{}>".format(plantName, user)
        await self._sendMessage(message)
        util.logger.log("plant", message)

    async def showStats(self, rawMessage, tokens):
        user = rawMessage.author.id
        userData = app.database.database.getDocument("plant", "userdata", user)
        if userData is None or len(userData["plants"]) == 0:
            await self._sendMessage("<@{}> has no plants, sadge :(".format(user))
        else:
            message = "<@{}> here are your plants!\n".format(user)
            for plant in userData["plants"]:
                plantData = userData["plants"][plant]
                message += "**{}:** last watered on {} (every {} days)".format(
                    plant,
                    plantData["lastWatered"].strftime("%m/%d/%Y, %H:%M:%S"),
                    plantData["daysToWater"]
                )
            await self._sendMessage(message)


    async def waterMessageReact(self, emoji, message, user):
        userData = app.database.database.getDocument("plant", "userdata", user)
        for plant in userData["plants"]:
            plantData = userData["plants"][plant]
            if "messageID" in plantData and plantData["messageID"] == message:
                plantData["lastWatered"] = datetime.datetime.now()
                message = "<@{}> {} has been watered, updating last watered time!".format(user, plant)
                await self._sendMessage(message)
                util.logger.log("plant", message)
                del plantData["messageID"]
        collection = app.database.database.getCollection("plant", "userdata")
        collection.replace_one({"_id": user}, userData)
        # Give the user coins for watering plants
        self._postEvent("earn_coin", { "amount" : 3 , "userID" : user})

    def _dateToStr(self, date):
        return str(date)
    
    def _strToDate(self, string):
        return dateutil.parser.parse(string)