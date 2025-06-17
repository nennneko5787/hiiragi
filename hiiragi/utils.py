from datetime import datetime

from hiiragi.protocol.protocol import EAmuseProtocol

protocol = EAmuseProtocol()

PRNG_STATE = 0x41C64E6D


def prng():
    global PRNG_STATE
    upper = (PRNG_STATE * 0x838C9CDA + 0x6072) & 0xFFFFFFFF
    PRNG_STATE = (PRNG_STATE * 0x41C64E6D + 0x3039) & 0xFFFFFFFF
    PRNG_STATE = (PRNG_STATE * 0x41C64E6D + 0x3039) & 0xFFFFFFFF
    return (upper & 0x7FFF0000) | ((PRNG_STATE >> 15) & 0xFFFF)


def generateKey():
    date = datetime.now()

    version = 1
    secondsHex = format(int(date.timestamp()), "08x")
    salt = (prng() & 0xFFFF) << 16 | (prng() & 0xFFFF)
    saltHex = format(salt, "04x")[0:4]
    return f"{version}-{secondsHex}-{saltHex}", date.strftime(
        "%a, %d %b %Y %H:%M:%S GMT"
    )
