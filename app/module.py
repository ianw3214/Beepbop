DEFAULT_CHANNEL = "beepboop"
DEFAULT_CHANNEL_ID = 884636204866347048

# Use prefix instead of channel to differentiate models for now
# TODO: Use thread channels instead when the API is updated
class Module:
    def __init__(self, client, prefix, channel=DEFAULT_CHANNEL):
        self.prefix = prefix
        self.channel = channel
        self.messageCommands = {}
        self.client = client
    
    def getPrefix(self):
        return self.prefix

    def getChannel(self):
        return self.channel
    
    async def handleMessageCommand(self, rawMessage, tokens):
        head = tokens[0]
        if head in self.messageCommands:
            await self.messageCommands[head](rawMessage, tokens[1:])

    async def delayedUpdate(self):
        pass

    def _registerMessageCommand(self, command, func):
        if command in self.messageCommands:
            raise Exception("{} is already a command".format(command))
        self.messageCommands[command] = func

    async def _sendMessage(self, message):
        await self.client.get_channel(DEFAULT_CHANNEL_ID).send(message)