import requests
import time

TOKEN_REFRESH_ENDPOINT="https://www.strava.com/api/v3/oauth/token"
CLUB_ACTIVITIES_ENDPOINT="https://www.strava.com/api/v3/clubs/978192/activities"

class StravaModule:
    def __init__(self, rawData, updateSettingsCallback):
        self.clientID = rawData["clientID"]
        self.clientSecret = rawData["clientSecret"]
        self.token = rawData["token"]
        self.refresh = rawData["refresh"]
        self.expires = rawData["expires"]
        self.updateSettingsCallback = updateSettingsCallback

    def getAccessToken(self):
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
            self.refresh = newData["refresh"]
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
        token = self.getAccessToken()
        authHeader = self.getAuthHeader()
        response = requests.get(CLUB_ACTIVITIES_ENDPOINT, headers=authHeader)
        # TODO: Handle request failure
        return response.json()