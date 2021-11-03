import app.module

import app.database.database

import util.logger

class CoinModule(app.module.Module):
    def __init__(self, client, eventQueue):
        app.module.Module.__init__(self, client, eventQueue, "coin")
        self._registerMessageCommand("stats", self.showStats)
        self._registerEventHandler("earn_coin", self.earnCoin)

    async def delayedUpdate(self):
        pass

    # def takeCoinFromUser(self, userID, numCoins):
    #     if userID not in self.coins:
    #         return False
    #     if self.coins[userID] < numCoins:
    #         return False
    #     self.coins[userID] = self.coins[userID] - numCoins
    #     util.logger.log("coin", "Took {} coins from user{}".format(numCoins, userID))
    #     return True

    async def showStats(self, rawMessage, tokens):
        user = rawMessage.author.id
        userData = app.database.database.getDocument("coin", "userdata", user)
        if userData is None:
            await self._sendMessage("<@{}> has no coins, sadge :(".format(user))
        else:
            message = "<@{}> has {} coins!\n".format(user, userData["amount"])
            await self._sendMessage(message)

    async def earnCoin(self, data):
        # TODO: Data validation
        collection = app.database.database.getCollection("coin", "userdata")
        userData = app.database.database.getDocument("coin", "userdata", data["userID"])
        if userData is None:
            userData = { "amount" : data["amount"] }
            app.database.database.insertToCollection(collection, userData, data["userID"])
        else:
            userData["amount"] = userData["amount"] + data["amount"]
            collection.replace_one({"_id": data["userID"]}, userData)
        util.logger.log("coin", "Added {} coins for user{}".format(data["amount"], data["userID"]))