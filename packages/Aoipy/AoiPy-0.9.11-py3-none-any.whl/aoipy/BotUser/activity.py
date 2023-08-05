import discord


def activity(text: str, type: str = "Watching"):
    if type.lower() == "watching":
        activities = discord.Activity(type=discord.ActivityType.watching, name=text)
    elif type.lower() == "playing":
        activities = discord.Activity(type=discord.ActivityType.playing, name=text)
    elif type.lower() == "listening":
        activities = discord.Activity(type=discord.ActivityType.listening, name=text)
    else:
        raise SyntaxError("No TYPE selected for bot activity")
    return activities


async def updateActivity(text: str, type: str = "watching"):
    """
    Example:
    @bot.command()
    async def update():
        client.updateActivity("my games!", "playing")
        await send(ctx, "Updated status!")


    """
    from aoipy.BotUser.client.core import bots
    if type.lower() == "watching":
        newAct = await bots.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=text))
    elif type.lower() == "playing":
        newAct = await bots.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=text))
    elif type.lower() == "listening":
        newAct = await bots.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=text))
    else:
        raise SyntaxError("No TYPE Selected")
    return newAct
