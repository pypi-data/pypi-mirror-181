import discord


async def banMember(member: discord.Member, reason: str = None):
    if reason is None:
        return await member.ban()
    else:
        return await member.ban(reason=reason)


async def kickMember(member: discord.Member, reason: str = None):
    if reason is None:
        return await member.kick()
    else:
        return await member.kick(reason=reason)


def getNick(member: discord.Member):
    return member.display_name


def getRoles(member: discord.Member):
    return member.roles


def getJoinDate(member: discord.Member):
    return member.joined_at


def sendMessage(user: discord.User, message, embed: bool = False):
    if embed:
        user.send(embed=message)
    else:
        user.send(message)
