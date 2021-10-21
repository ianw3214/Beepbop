import asyncio

import discord
import app.settings
import app.modules.strava
import app.modules.plant
import app.modules.coin
import app.modules.crystal

import util.logger

CHANNEL = "beepbop"
CHANNEL_ID = 884636204866347048
UPDATE_INTERVAL = 60 * 60

client = discord.Client()
modules = {}

def initModules():
    strava = app.modules.strava.StravaModule(client)
    addModule(strava)
    plant = app.modules.plant.PlantModule(client)
    addModule(plant)
    coin = app.modules.coin.CoinModule(client)
    addModule(coin)
    crystal = app.modules.crystal.CrystalModule(client)
    addModule(crystal)

def addModule(module):
    modules[module.getPrefix()] = module

async def delayedUpdate():
    while True:
        for module in modules.values():
            await module.delayedUpdate()
        await asyncio.sleep(UPDATE_INTERVAL)

@client.event
async def on_ready():
    client.loop.create_task(delayedUpdate())
    util.logger.log("core", "beepbop is now online")

@client.event
async def on_message(message):
    # Avoid responding to own messages
    if message.author == client.user:
        return
    # only listen to our dedicated channel
    if message.channel.name != CHANNEL:
        return
    util.logger.log("core", "message recieved: " + message.content)
    # handle bot commands
    if len(message.content) > 0 and message.content[0] == "$":
        tokens = message.content.split(" ")
        head = tokens[0][1:]
        if head == "help" or head == "command":
            await message.channel.send("Check out a list of helpful commands here! https://github.com/ianw3214/Beepbop")
        if head in modules:
            await modules[head].handleMessageCommand(message, tokens[1:])

@client.event
async def on_reaction_add(reaction, user):
    # TODO: Make this global to avoid looping through every module
    for module in modules.values():
        await module.handleReactionAdd(reaction, user)

initModules()
client.run(app.settings.getDiscordBotToken())