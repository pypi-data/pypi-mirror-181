from typing import TypeVar, Callable, Any, Coroutine
import asyncio
import discord
from discord.ext import commands
import asyncio
global bots


def Bot(prefix: str, case_insensitive: bool = False, intents: tuple = ("default",), activity=None, help_command=None):
    global bots
    if "all" in intents:
        intent = discord.Intents.all()
    elif "default" in intents:
        intent = discord.Intents.default()
    else:
        intent = discord.Intents.default()
        if "message" in intents:
            intent.message_content = True
        if "members" in intents:
            intent.members = True
        if "presences" in intents:
            intent.presences = True

    if activity is None:
        clients = commands.Bot(command_prefix=prefix, case_insensitive=case_insensitive, intents=intent, help_command=help_command)
        bots = clients
    else:
        clients = commands.Bot(command_prefix=prefix, case_insensitive=case_insensitive, intents=intent, activity=activity, help_command=help_command)
        bots = clients
    return clients


def run(token: str):
    global bots
    bots.run(token)


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


########################################
#              EVENTS                  #
########################################
# Wrapping the original Coroutine into our own functions that'll make them into decorators
# The functions then aren't limited to the name of the event


# Application Commands

def onApplicationCommand(Func):

    @bots.event
    async def on_application_command(*args, **kwargs):
        Func(*args, **kwargs)
    return Func


def onApplicationCommandComplete(Func):

    @bots.event
    async def on_application_command_completion(*args, **kwargs):
        Func(*args, **kwargs)
    return Func


def onApplicationCommandError(Func):

    @bots.event
    async def on_application_command_error(*args, **kwargs):
        Func(*args, **kwargs)
    return Func

# AutoMod


def onAutoModRuleCreate(Func):

    @bots.event
    async def on_auto_moderation_rule_create(*args, **kwargs):
        Func(*args, **kwargs)
    return Func


def onReady(Func, *args, **kwargs):
    global bots

    @bots.event
    async def on_ready():
        Func(*args, **kwargs)
    return Func


def onMessage(Func):
    global bots

    @bots.event
    async def on_message(*args, **kwargs):
        Func(*args, **kwargs)
    return Func

