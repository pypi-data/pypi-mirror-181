# Soon..`
global clients
import asyncio

def loadBotItems(bot):
    """Not for client-side use"""
    global clients
    clients = bot


def botUsername():
    global clients
    return clients.user


def botName():
    global clients
    return clients.user.name


def botID():
    global clients
    return clients.user.id


def botDiscriminator():
    global clients
    return clients.user.discriminator


def botOwnerID():
    global clients
    return clients.owner_id


def botIsOwner() -> bool:
    global clients
    return clients.is_owner


async def wait(ctx, types: str, check=None, timer=60, everyone: bool = False):
        global clients
        timeout = "ASYNCIO TIMEOUT ERROR"
        if check is None:
            try:
                if everyone is False:
                    def check(msg):
                        if msg.author == ctx.author:
                            return True

                    message = await clients.wait_for(types.lower(), check=check, timeout=timer)
                    return message.content
                else:
                    message = await clients.wait_for(types.lower(), timeout=timer)
                    return message.content
            except asyncio.TimeoutError:
                raise TimeoutError(timeout)
        else:
            try:
                return await clients.wait_for(types.lower(), check=check, timeout=timer)
            except asyncio.TimeoutError:
                return TimeoutError(timeout)