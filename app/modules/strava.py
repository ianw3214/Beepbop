import requests
import time

import app.module
import app.settings

import util.logger

TOKEN_REFRESH_ENDPOINT="https://www.strava.com/api/v3/oauth/token"
CLUB_ACTIVITIES_ENDPOINT="https://www.strava.com/api/v3/clubs/978192/activities"

class StravaModule(app.module.Module):
    def __init__(self, client):
        app.module.Module.__init__(self, client, "strava")
        rawData = app.settings.getStravaData()
        self.clientID = rawData["clientID"]
        self.clientSecret = rawData["clientSecret"]
        self.token = rawData["token"]
        self.refresh = rawData["refresh"]
        self.expires = rawData["expires"]

    # OVERRIDE
    async def delayedUpdate(self):
        pass

    def _getAccessToken(self):
        currTime = round(time.time())
        # Check if we need to refresh the token
        if currTime >= self.expires:
            util.logger.log("strava", "sending refresh token")
            fields = { 
                "client_id" : self.clientID,
                "client_secret" : self.clientSecret,
                "grant_type" : "refresh_token",
                "refresh_token" : self.refresh
            }
            response = requests.post(TOKEN_REFRESH_ENDPOINT, fields)
            # TODO: Handle request failure
            newData = response.json()
            self.token = newData["access_token"]
            self.refresh = newData["refresh_token"]
            self.expires = newData["expires_in"]
            # Write this all back to the file in case we need to load again
            app.settings.updateSettingsCallback(self.token, self.refresh, self.expires)
            util.logger.log("strava", "new authorization token set")
        return self.token

    def getAuthHeader(self):
        return  {
            "Content-Type": "application/json",
            "Authorization" : "Bearer " + self.token
        }

    def getActivities(self):
        token = self._getAccessToken()
        authHeader = self.getAuthHeader()
        response = requests.get(CLUB_ACTIVITIES_ENDPOINT, headers=authHeader)
        # TODO: Handle request failure
        return response.json()