import asyncio
import discord
global bots

# Random Functions here for testing

async def wait(ctx, types: str, check=None, timer=60, everyone: bool = False):
    global bots
    timeout = "ASYNCIO TIMEOUT ERROR"
    if check is None:
        try:
            if everyone is False:
                def check(msg):
                    if msg.author == ctx.author:
                        return True
                return await bots.wait_for(types.lower(), check=check, timeout=timer)
            else:
                return await bots.wait_for(types.lower(), timeout=timer)
        except asyncio.TimeoutError:
            raise TimeoutError(timeout)
    else:
        try:
            return await bots.wait_for(types.lower(), check=check, timeout=timer)
        except asyncio.TimeoutError:
            return TimeoutError(timeout)


async def send(ctx, message, delete_after: int or float = None, embed: bool = False):
    if delete_after is None and embed is False:
        return await ctx.send(message)
    elif embed is False and delete_after is not None:
        return await ctx.send(message, delete_after=delete_after)
    elif embed is True:
        return await ctx.send(embed=message)


def run(bot, token: str, startMessage: str = None, intents: str = "all"):
    global bots
    bots = bot
    @bot.event
    async def on_ready():
        if startMessage is None:
            return
        else:
            if "None" in startMessage:
                startMessage1 = startMessage.replace("None", str(bot.user.name))
                print(startMessage1)
                return
            else:
                print(startMessage)
                return
    bot.run(token)


def embed(title, description, color=None):
    return discord.Embed(title=title, description=description, color=color)

