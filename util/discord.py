import discord

def getMessageAuthorID(message):
    return getAuthorID(message.author)

def getAuthorID(author):
    return author.name + "#" + author.discriminator