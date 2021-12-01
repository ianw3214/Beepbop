import app.module

import discord

import app.database.database

import util.logger

import datetime
import dateutil

# THIS IS SUPER HARD CODED
# DUPLICATED FROM main.py
# TODO: PUT THIS IN A CENTRAL PLACE
#   EVEN BETTER, JUST GET RID OF IT
GUILD_ID = 714213228527484928

class SleepModule(app.module.Module):
    def __init__(self, client, eventQueue):
        app.module.Module.__init__(self, client, eventQueue, "sleep")
        self._registerMessageCommand("register", self.registerUser)

    async def delayedUpdate(self, discordClient):
        currTime = datetime.datetime.now()
        collection = app.database.database.getCollection("sleep", "userdata")
        cursor = collection.find()
        for userDocument in cursor:
            userid = userDocument["_id"]
            dirty = False
            memberData = discordClient.get_guild(GUILD_ID).get_member(userid)
            if not memberData:
                util.logger.log("sleep", "Could not find discord member {}".format(userid))
                continue
            status = memberData.status
            # Module logic
            currDay = userDocument["currDay"]
            if currDay.date() < currTime.date():
                setNewDay = False
                # If before 4am and online, we r badge
                if currTime.hour < 4 and status == discord.Status.online:
                    message = "<@{}> Go to sleep, no coin for u".format(userid)
                    util.logger.log("sleep", message)
                    await self._sendMessage(message)
                    setNewDay = True
                # Once past 4am, we r good
                if currTime.hour > 4:
                    message = "<@{}> Nice job sleeping before 12, have some coin!".format(userid)
                    util.logger.log("sleep", message)
                    await self._sendMessage(message)
                    # Give the user coins for watering plants
                    self._postEvent("earn_coin", { "amount" : 3 , "userID" : userid})
                    setNewDay = True
                if setNewDay:
                    userDocument["currDay"] = datetime.datetime.now()
                    dirty = True
            if dirty:
                collection.replace_one({"_id": userid}, userDocument)
                
    
    # COMMAND: $sleep register
    async def registerUser(self, rawMessage, tokens):
        user = rawMessage.author.id
        # Add user to the database if necessary
        userData = app.database.database.getDocument("sleep", "userdata", user)
        if userData is None:
            userData = {
                "currDay" : datetime.datetime.now()
            }
            # TODO: Some sort of user feedback here too
            collection = app.database.database.getCollection("sleep", "userdata")
            app.database.database.insertToCollection(collection, userData, user)
            util.logger.log("sleep", "<@{}> registered for sleep module")