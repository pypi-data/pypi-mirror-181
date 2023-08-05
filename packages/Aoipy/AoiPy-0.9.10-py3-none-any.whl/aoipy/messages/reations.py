import discord


def addReaction(message: discord.Message, emoji: discord.Emoji):
    return message.add_reaction(emoji)


def removeReaction(message: discord.Message, emoji: discord.Emoji, member: discord.Member):
    return message.remove_reaction(emoji, member)
