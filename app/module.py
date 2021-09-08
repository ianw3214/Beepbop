DEFAULT_CHANNEL = "beepboop"

# Use prefix instead of channel to differentiate models for now
# TODO: Use thread channels instead when the API is updated
class Module:
    def __init__(self, prefix, channel=DEFAULT_CHANNEL):
        self.prefix = prefix
        self.channel = channel
        self.messageCommands = {}
    
    def getPrefix(self):
        return self.prefix

    def getChannel(self):
        return self.channel
    
    def handleMessageCommand(self, rawMessage, tokens):
        head = tokens[0]
        if head in self.messageCommands:
            self.messageCommands[head](rawMessage, tokens[1:])
    
    def delayedUpdate(self):
        pass

    def _registerMessageCommand(self, command, func):
        if command in self.messageCommands:
            raise Exception("{} is already a command".format(command))
        self.messageCommands[command] = func