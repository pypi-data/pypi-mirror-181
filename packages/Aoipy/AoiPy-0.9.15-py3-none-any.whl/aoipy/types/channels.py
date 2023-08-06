import discord


class Channels:
    def __init__(self, channel):
        self.channel = channel
    # Gets TextChannel ID From Name
    def getTextChannelID(self) -> discord.TextChannel.name:
        return self.channel.id

    # No Setter Method for ID

    # Gets ID From Name
    def GetTextChannelName(self) -> discord.TextChannel.name:
        return self.channel.name

    def textChannelID(self, Name: discord.TextChannel) -> discord.TextChannel.id:
        return self.channel.id

    # With this method is possible to change the Text channel name
    def setTextChannelName(self, newName) -> discord.TextChannel.name:
        self.channel.name = newName

    # ------------------------------------------------------------------------------

    def getVoiceChannelID(self) -> discord.VoiceChannel.id:
        return self.channel.id

    def getVoiceChannelName(self) -> discord.VoiceChannel.name:
        return self.channel.name

    def setVoiceChannelName(self, newName) -> discord.VoiceChannel.name:
        self.channel.name = newName

    # --------------------------------------------------------------------------------

    # The number of seconds a member must wait between sending messages
    def getDelay(self) -> discord.TextChannel.id:
        return self.channel.slowmode_delay

    # Can change the n. of seconds of delay between every message
    # secondsDelay is the parameter used to set the value of delay (Int)
    def setDelay(self, secondsDelay: int) -> discord.TextChannel.id:
        self.channel.slowmode_delay = secondsDelay

    # -------------------------------------------------------------------------------------------

    # This method returns a boolean value, to check if a channel is NSFW (Not Safe For Work) or not
    def getNSFW(self):
        return self.channel.nsfw

    # Setter Method, This method can consent the programmer to set the nsfw flag to
    # TRUE if he wants to make NSFW his text channel or FALSE if the channel passed by his ID is not NSFW
    def setNSFW(self, value: bool) -> discord.TextChannel.id:
        self.channel.nsfw = value

    # --------------------------------------------------------------------------------------------

    def getCurrentTextChannel(self, ctx) -> discord.TextChannel.name:
        return ctx.channel.name
