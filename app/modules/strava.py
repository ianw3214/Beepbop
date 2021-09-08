import requests
import app.module

import time

TOKEN_REFRESH_ENDPOINT="https://www.strava.com/api/v3/oauth/token"
CLUB_ACTIVITIES_ENDPOINT="https://www.strava.com/api/v3/clubs/978192/activities"

def testFunc():
    print("TEST")

class StravaModule(app.module.Module):
    def __init__(self, rawData, updateSettingsCallback):
        app.module.Module.__init__(self, "strava")
        self.clientID = rawData["clientID"]
        self.clientSecret = rawData["clientSecret"]
        self.token = rawData["token"]
        self.refresh = rawData["refresh"]
        self.expires = rawData["expires"]
        # TODO: Replace this callback with a direct interface to datastore
        self.updateSettingsCallback = updateSettingsCallback
        self._registerCommand("test", testFunc)

    # OVERRIDE
    def delayedUpdate(self):
        print("Strava update")

    def _getAccessToken(self):
        currTime = round(time.time())
        # Check if we need to refresh the token
        if currTime >= self.expires:
            print("refreshing strava token")
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
            self.updateSettingsCallback(self.token, self.refresh, self.expires)
        return self.token

    def getAuthHeader(self):
        return  {
            "Content-Type": "application/json",
            "Authorization" : "Bearer " + self.token
        }

    def getActivities(self):
        print("Getting activities")
        token = self._getAccessToken()
        authHeader = self.getAuthHeader()
        response = requests.get(CLUB_ACTIVITIES_ENDPOINT, headers=authHeader)
        # TODO: Handle request failure
        return response.json()