from pymongo import collection
import app.module

import app.database.database

import util.logger

import datetime
import dateutil

class CoinModule(app.module.Module):
    def __init__(self, client, eventQueue):
        app.module.Module.__init__(self, client, eventQueue, "coin", self.showStats)
        self._registerMessageCommand("stats", self.showStats)
        self._registerMessageCommand("leaderboard", self.showLeaderboard)
        self._registerEventHandler("earn_coin", self.earnCoin)

    async def delayedUpdate(self, discordClient):
        currTime = datetime.datetime.now()
        WEEK_DELTA = datetime.timedelta(weeks=1)
        collection = app.database.database.getCollection("coin", "rootdata")
        rootData = app.database.database.getDocument("coin", "rootdata", 0)
        if rootData is None:
            await self.showLeaderboard()
            rootData = {
                "nextLeaderboard" : currTime + WEEK_DELTA
            }
            app.database.database.insertToCollection(collection, rootData, 0)
        else:
            nextUpdate = rootData["nextLeaderboard"]
            if currTime > nextUpdate:
                await self.showLeaderboard()
                rootData["nextLeaderboard"] = currTime + WEEK_DELTA
                collection.replace_one({"_id":0}, rootData)

    async def showStats(self, rawMessage, tokens):
        user = rawMessage.author.id
        userData = app.database.database.getDocument("coin", "userdata", user)
        if userData is None:
            await self._sendMessage("<@{}> has no coins, sadge :(".format(user))
        else:
            message = "<@{}> has {} coins!\n".format(user, userData["amount"])
            await self._sendMessage(message)

    async def showLeaderboard(self, *_):
        # TODO: Cache leaderboard so that we don't have to retrieve from database everytime
        collection = app.database.database.getCollection("coin", "userdata")
        cursor = collection.find()
        pairs = []
        for userDocument in cursor:
            userid = userDocument["_id"]
            amount = userDocument["amount"]
            pairs.append((userid, amount))
        pairs.sort(key=lambda x : x[1], reverse=True)
        message = "**Coin Leaderboard\n**"
        # TODO: Limit the number of people that show up on the leaderboard
        for pair in pairs:
            message = message + "<@{}> : {} coins\n".format(pair[0], pair[1])
        await self._sendMessage(message)
        util.logger.log("coin", "Showing leaderboard info...")

    async def earnCoin(self, data):
        if data["userID"] is None:
            util.logger.log("coin", "Invalid input data for earnCoin, missing userID")
            return
        if data["amount"] is None:
            util.logger.log("coin", "Invalid input data for earnCoin, missing amount")
            return
        collection = app.database.database.getCollection("coin", "userdata")
        userData = app.database.database.getDocument("coin", "userdata", data["userID"])
        if userData is None:
            userData = { "amount" : data["amount"] }
            app.database.database.insertToCollection(collection, userData, data["userID"])
        else:
            userData["amount"] = userData["amount"] + data["amount"]
            collection.replace_one({"_id": data["userID"]}, userData)
        util.logger.log("coin", "Added {} coins for user{}".format(data["amount"], data["userID"]))