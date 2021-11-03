import app.settings

# Use prefix instead of channel to differentiate models for now
# TODO: Use thread channels instead when the API is updated
class Module:
    def __init__(self, client, eventQueue, prefix, defaultMessageHandler=None):
        self.prefix = prefix
        self.channel = app.settings.getChannel()
        self.channelID = app.settings.getChannelID()
        self.messageCommands = {}
        self.reactListeners = []
        self.client = client
        self.eventQueue = eventQueue
        self.defaultMessageHandler = defaultMessageHandler
        self.eventHandlers = {}

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
        elif self.defaultMessageHandler:
            await self.defaultMessageHandler(rawMessage, tokens)

    async def handleReactionAdd(self, emoji, message, user):
        for listener in self.reactListeners:
            await listener(emoji, message, user)

    async def delayedUpdate(self):
        pass

    def _registerMessageCommand(self, command, func):
        if command in self.messageCommands:
            raise Exception("{} is already a command".format(command))
        self.messageCommands[command] = func

    def _registerEventHandler(self, eventType, func):
        if eventType in self.eventHandlers:
            raise Exception("Event '{}' is already handled".format(eventType))
        self.eventHandlers[eventType] = func

    async def _sendMessage(self, message):
        return await self.client.get_channel(self.channelID).send(message)

    # TODO: Specify emoji react to listen for
    # TODO: Specify messages for each listener to listen for to avoid searching
    def _registerReactListener(self, callback):
        self.reactListeners.append(callback)

    def _postEvent(self, eventType, eventData):
        self.eventQueue.append({
            "type" : eventType,
            "data" : eventData
        })

    async def _handleEvent(self, eventType, eventData):
        if eventType in self.eventHandlers:
            await self.eventHandlers[eventType](eventData)
