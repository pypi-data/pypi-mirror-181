import discord


def getUserName(user: discord.User):
    return user.name


def getUserDescriminator(user: discord.User):
    return user.discriminator


def getUserCreationDate(user: discord.User):
    return user.created_at


def getUserID(user: discord.User):
    return user.id


def getUserMention(user: discord.User):
    return user.mention
