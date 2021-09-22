import app.settings

# Use prefix instead of channel to differentiate models for now
# TODO: Use thread channels instead when the API is updated
class Module:
    def __init__(self, client, prefix):
        self.prefix = prefix
        self.channel = app.settings.getChannel()
        self.channelID = app.settings.getChannelID()
        self.messageCommands = {}
        self.reactListeners = {}
        self.client = client
    
    def getPrefix(self):
        return self.prefix

    def getChannel(self):
        return self.channel
    
    async def handleMessageCommand(self, rawMessage, tokens):
        head = ""
        if len(tokens) > 0:
            head = tokens[0]
        if head in self.messageCommands:
            await self.messageCommands[head](rawMessage, tokens[1:])

    async def handleReactionAdd(self, reaction, user):
        messageID = reaction.message.id
        if messageID in self.reactListeners:
            remove = await self.reactListeners[messageID](reaction, user)
            if remove:
                del self.reactListeners[messageID]

    async def delayedUpdate(self):
        pass

    def _registerMessageCommand(self, command, func):
        if command in self.messageCommands:
            raise Exception("{} is already a command".format(command))
        self.messageCommands[command] = func

    async def _sendMessage(self, message):
        return await self.client.get_channel(self.channelID).send(message)

    # TODO: Specify emoji react to listen for
    def _registerReactListener(self, message, callback):
        self.reactListeners[message.id] = callback