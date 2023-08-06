import discord


async def deleteMessage(message: discord.Message, delay: int or float = None):
    if delay is None:
        return await message.delete()
    else:
        return await message.delete(delay=delay)


async def sendChannelMessage(ctx, message, delete_after: int or float = None, embed: bool = False):
    if delete_after is None and embed is False:
        return await ctx.send(message)
    elif embed is False and delete_after is not None:
        return await ctx.send(message, delete_after=delete_after)
    elif embed is True and delete_after is not None:
        return await ctx.send(embed=message, delete_after=delete_after)
    else:
        return await ctx.send(embed=message)


async def sendAuthorDM(ctx, message, delete_after: int or float = None, embed: bool = False):
    if delete_after is None and embed is False:
        return await ctx.author.send(message)
    elif delete_after is not None and embed is False:
        return await ctx.author.send(message, delete_after=delete_after)
    elif embed is True and delete_after is not None:
        return await ctx.author.send(message, delete_after=delete_after)
    else:
        return await ctx.author.send(embed=message)


def mentionedUsers(ctx):
    message = ctx.message
    return message.mentions


def createEmbed(title, description, color=None):
    return discord.Embed(title=title, description=description, color=color)


def getMessageID(message: discord.Message):
    return message.id


def getMessageAuthor(message: discord.Message):
    return message.author


def getMessageContent(message: discord.Message):
    return message.content


def getMessageChannelName(message: discord.Message):
    return message.channel.name


def getMessageChannelID(message: discord.Message):
    return message.channel.id

