import discord


# Gets TextChannel ID From Name
def getTextChannelID(name: discord.TextChannel) -> discord.TextChannel.name:
    return name.id


# No Setter Method for ID

# Gets ID From Name
def GetTextChannelName(ID: discord.TextChannel) -> discord.TextChannel.name:
    return ID.name


def textChannelID(Name: discord.TextChannel) -> discord.TextChannel.id:
    return Name.id


# With this method is possible to change the Text channel name
def setTextChannelName(ID: discord.TextChannel, newName) -> discord.TextChannel.name:
    ID.name = newName


# ------------------------------------------------------------------------------

def getVoiceChannelID(name: discord.VoiceChannel) -> discord.VoiceChannel.id:
    return name.id


def getVoiceChannelName(id: discord.VoiceChannel) -> discord.VoiceChannel.name:
    return id.name


def setVoiceChannelName(ID: discord.VoiceChannel, newName) -> discord.VoiceChannel.name:
    ID.name = newName


# --------------------------------------------------------------------------------

# The number of seconds a member must wait between sending messages
def getDelay(ID: discord.TextChannel) -> discord.TextChannel.id:
    return ID.slowmode_delay


# Can change the n. of seconds of delay between every message
# secondsDelay is the parameter used to set the value of delay (Int)
def setDelay(ID: discord.TextChannel, secondsDelay: int) -> discord.TextChannel.id:
    ID.slowmode_delay = secondsDelay


# -------------------------------------------------------------------------------------------

# This method returns a boolean value, to check if a channel is NSFW (Not Safe For Work) or not
def getNSFW(ID: discord.TextChannel):
    return ID.nsfw


# Setter Method, This method can consent the programmer to set the nsfw flag to
# TRUE if he wants to make NSFW his text channel or FALSE if the channel passed by his ID is not NSFW
def setNSFW(ID: discord.TextChannel, value: bool) -> discord.TextChannel.id:
    ID.nsfw = value


# --------------------------------------------------------------------------------------------

def getCurrentTextChannel(ctx) -> discord.TextChannel.name:
    return ctx.channel.name
