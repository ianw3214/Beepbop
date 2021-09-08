import asyncio

import discord
import app.settings
import app.data_interface
import app.modules.strava
import app.modules.plant

import util.logger

CHANNEL = "beepbop"
CHANNEL_ID = 884636204866347048
UPDATE_INTERVAL = 60 * 60

client = discord.Client()
interface = app.data_interface.DataInterface()

modules = {}

def initModules():
    strava = app.modules.strava.StravaModule(app.settings.getStravaData(), app.settings.updateSettingsCallback)
    addModule(strava)
    plant = app.modules.plant.PlantModule()
    addModule(plant)

def addModule(module):
    modules[module.getPrefix()] = module

async def delayedUpdate():
    while True:
        for module in modules.values():
            module.delayedUpdate()
        await asyncio.sleep(UPDATE_INTERVAL)

@client.event
async def on_ready():
    client.loop.create_task(delayedUpdate())
    util.logger.log("core", "beepbop is now online")

@client.event
async def on_message(message):
    print(message.author.id)
    # Avoid responding to own messages
    if message.author == client.user:
        return
    # only listen to our dedicated channel
    if message.channel.name != CHANNEL:
        return
    # handle bot commands
    if message.content[0] == "$":
        tokens = message.content.split(" ")
        head = tokens[0][1:]
        if head == "signup" or head == "register":
            interface.registerUser(util.getMessageAuthorID(message))
        if head == "help" or head == "command":
            await message.channel.send("Check out a list of helpful commands here! https://github.com/ianw3214/Beepbop")
        if head in modules:
            modules[head].handleMessageCommand(message, tokens[1:])

initModules()
client.run(app.settings.getDiscordBotToken())