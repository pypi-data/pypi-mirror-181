import discord


class Message:
    def __init__(self, message):
        self.message = message

    async def deleteMessage(self, delay: int or float = None):
        if delay is None:
            return await self.message.delete()
        else:
            return await self.message.delete(delay=delay)

    async def sendChannelMessage(self, ctx, message, delete_after: int or float = None, embed: bool = False):
        if delete_after is None and embed is False:
            return await ctx.send(message)
        elif embed is False and delete_after is not None:
            return await ctx.send(message, delete_after=delete_after)
        elif embed is True and delete_after is not None:
            return await ctx.send(embed=message, delete_after=delete_after)
        else:
            return await ctx.send(embed=message)

    async def sendAuthorDM(self, ctx, message, delete_after: int or float = None, embed: bool = False):
        if delete_after is None and embed is False:
            return await ctx.author.send(message)
        elif delete_after is not None and embed is False:
            return await ctx.author.send(message, delete_after=delete_after)
        elif embed is True and delete_after is not None:
            return await ctx.author.send(message, delete_after=delete_after)
        else:
            return await ctx.author.send(embed=message)

    def mentionedUsers(self, ctx):
        message = ctx.message
        return message.mentions

    def createEmbed(self, title, description, color=None):
        return discord.Embed(title=title, description=description, color=color)

    def getMessageID(self, message: discord.Message):
        return message.id

