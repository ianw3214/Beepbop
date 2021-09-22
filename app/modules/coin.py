import app.module

import util.logger

class CoinModule(app.module.Module):
    def __init__(self, client):
        app.module.Module.__init__(self, client, "coin")
        self.coins = {}
        self._registerMessageCommand("stats", self.showStats)

    async def delayedUpdate(self):
        pass

    def addCoinToUser(self, userID, numCoins):
        if userID not in self.coins:
            self.coins[userID] = numCoins
        else:
            self.coins[userID] += numCoins
        util.logger.log("coin", "Added {} coins for user{}".format(numCoins, userID))

    def takeCoinFromUser(self, userID, numCoins):
        if userID not in self.coins:
            return False
        if self.coins[userID] < numCoins:
            return False
        self.coins[userID] = self.coins[userID] - numCoins
        util.logger.log("coin", "Took {} coins from user{}".format(numCoins, userID))
        return True

    async def showStats(self, rawMessage, tokens):
        user = rawMessage.author.id
        if user not in self.coins or self.coins[user] == 0:
            await self._sendMessage("<@{}> has no coins, sadge :(".format(user))
        else:
            message = "<@{}> has {} coins!\n".format(user, self.coins[user])
            await self._sendMessage(message)