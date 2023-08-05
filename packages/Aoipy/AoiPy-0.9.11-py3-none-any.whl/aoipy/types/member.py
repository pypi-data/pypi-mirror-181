import discord
from discord.ext import commands

class Member:
    def __init__(self, member: discord.Member):
        self.member = commands.MemberConverter().convert(member)

    async def banMember(self, reason: str = None) -> discord.Member.ban:
        if reason is None:
            return await self.member.ban()
        else:
            return await self.member.ban(reason=reason)

    async def kickMember(self, reason: str = None):
        if reason is None:
            return await self.member.kick()
        else:
            return await self.member.kick(reason=reason)

    def getNick(self):
        return self.member.display_name

    def getRoles(self):
        return self.member.roles

    def getJoinDate(self):
        return self.member.joined_at

    def sendMessage(self, message, embed: bool = False):
        if embed:
            return self.member.send(embed=message)
        else:
            return self.member.send(message)
