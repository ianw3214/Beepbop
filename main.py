import asyncio

import discord
import app.settings
import app.modules.strava
import app.modules.plant
import app.modules.coin
import app.modules.crystal
import app.modules.gamble
import app.modules.sleep

import util.logger

CHANNEL = "beepbop"
CHANNEL_ID = 884636204866347048
GUILD_ID = 714213228527484928
# TODO: Let this be set by environment variable?
UPDATE_INTERVAL = 60 * 60 * 3

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)
modules = {}
eventQueue = []

def initModules():
    strava = app.modules.strava.StravaModule(client, eventQueue)
    addModule(strava)
    plant = app.modules.plant.PlantModule(client, eventQueue)
    addModule(plant)
    coin = app.modules.coin.CoinModule(client, eventQueue)
    addModule(coin)
    crystal = app.modules.crystal.CrystalModule(client, eventQueue)
    addModule(crystal)
    gamble = app.modules.gamble.GambleModule(client, eventQueue)
    addModule(gamble)
    sleep = app.modules.sleep.SleepModule(client, eventQueue)
    addModule(sleep)

def addModule(module):
    modules[module.getPrefix()] = module

async def flushEvents():
    for event in eventQueue:
        for module in modules.values():
            await module._handleEvent(event["type"], event["data"])
    eventQueue.clear()

async def delayedUpdate():
    while True:
        for module in modules.values():
            await module.delayedUpdate()
        await flushEvents()
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
    # Run any message handlers
    for module in modules.values():
        module.handleAnyMessage(message)
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
    await flushEvents()

@client.event
async def on_raw_reaction_add(payload):
    # TODO: Make this global to avoid looping through every module
    for module in modules.values():
        await module.handleReactionAdd(payload.emoji, payload.message_id, payload.user_id)
    await flushEvents()

initModules()
client.run(app.settings.getDiscordBotToken())