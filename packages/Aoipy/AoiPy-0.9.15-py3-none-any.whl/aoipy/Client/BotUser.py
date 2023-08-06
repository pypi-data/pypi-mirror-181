# Soon..`
global client


def loadBotItems(bot):
    """Not for client-side use"""
    global client
    client = bot


def botUsername():
    global client
    return client.user


def botName():
    global client
    return client.user.name


def botID():
    global client
    return client.user.id


def botDiscriminator():
    global client
    return client.user.discriminator


def botOwnerID():
    global client
    return client.owner_id


def botIsOwner() -> bool:
    global client
    return client.is_owner
