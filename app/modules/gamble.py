import app.module

import util.logger

import datetime
import dateutil

class GambleModule(app.module.Module):
    def __init__(self, client, eventQueue):
        app.module.Module.__init__(self, client, eventQueue, "gamble")

    async def delayedUpdate(self):
        currTime = datetime.datetime.now()
        collection = app.database.database.getCollection("gamble", "games")
        cursor = collection.find()
        for gameDocument in cursor:
            gameid = gameDocument["_id"]
            starttime = gameDocument["startTime"]
            gamedays = gameDocument["days"]
            delta = datetime.timedelta(days=gamedays)
            if currTime > starttime + delta:
                util.logger.log("gamble", "game ends here...")
                # Handle betting logic and rewards
                # Remove the collection here
                # Start a new game if specified
        