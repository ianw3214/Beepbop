import asyncio

import discord
import app.settings
import app.data_interface
import app.modules.strava

CHANNEL = "beepbop"
CHANNEL_ID = 884636204866347048
UPDATE_INTERVAL = 60 * 60

client = discord.Client()
interface = app.data_interface.DataInterface()
strava = app.modules.strava.StravaModule(app.settings.getStravaData(), app.settings.updateSettingsCallback)

def getFullDiscordName(author):
    return author.name + "#" + author.discriminator

async def delayedUpdate():
    while True:
        print(strava.getActivities())
        await asyncio.sleep(UPDATE_INTERVAL)

@client.event
async def on_ready():
    client.loop.create_task(delayedUpdate())
    print("Beepbop is now online")

@client.event
async def on_message(message):
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
            interface.registerUser(getFullDiscordName(message.author))
        if head == "help" or head == "command":
            await message.channel.send("Check out a list of helpful commands here! https://github.com/ianw3214/Beepbop")

client.run(app.settings.getDiscordBotToken())