from asyncio import events
import discord
import settings

CHANNEL = "beepbop"

client = discord.Client()

@client.event
async def on_ready():
    print("Beepbop is now online")

@client.event
async def on_message(message):
    # Avoid responding to own messages
    if message.author == client.user:
        return
    # only listen to our dedicated channel
    if message.channel.name != CHANNEL:
        return
    await message.channel.send(message.content)

client.run(settings.getDiscordBotToken())