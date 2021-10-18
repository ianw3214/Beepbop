import app.module

import math


class CrystalModule(app.module.Module):
    def __init__(self, client):
        app.module.Module.__init__(self, client, "crystal", self.calculate)

    async def calculate(self, rawMessage, tokens):
        if len(tokens) == 1 and tokens[0].isnumeric() and int(tokens[0]) > 0:
            if int(tokens[0]) > 90000:
                await self._sendMessage("You have over 90000 my guy c:")
            elif int(tokens[0]) == 90000:
                await self._sendMessage("You have 90000!?!")
            else:
                await self._sendMessage("{} more to go. {}/300 pulls".format(90000 - int(tokens[0]), math.floor(int(tokens[0]) / 3000.0 * 10.0)))
        else:
            await self._sendMessage("Oops, something went wrong. Try '$crystal <number>'")
