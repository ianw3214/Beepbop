import pymongo
from pymongo import database

import app.settings

URL_PREFIX = "mongodb+srv://root:"
URL_POSTFIX = "?retryWrites=true&w=majority"

def getDatabase(databaseName):
    client = pymongo.MongoClient(URL_PREFIX 
        + app.settings.getMongoDBPassword() 
        + app.settings.getMongoDBUrl()
        + databaseName
        + URL_POSTFIX)
    return client[databaseName]

def getCollection(databaseName, collectionName):
    return getDatabase(databaseName)[collectionName]

def insertToCollection(collectionObj, insertData):
    return collectionObj.insert_one(insertData)