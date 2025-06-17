import time

from fastapi import Request

from hiiragi.plugin import Plugin
from hiiragi.protocol.node import Node

name = "Hiiragi BeatStream Plugin"
game = "NBT"
version = "2025.06.17"


async def getServices(request: Request, node: Node):
    response = Node.void("response")

    # <services>
    services = Node.void("services")
    services.set_attribute("method", "get")
    services.set_attribute("expire", "10800")
    services.set_attribute("mode", "operation")
    services.set_attribute("status", "0")

    # <item>
    ntp = Node.void("item")
    ntp.set_attribute("name", "ntp")
    ntp.set_attribute("url", "ntp://pool.ntp.org/")
    services.add_child(ntp)

    keepalive = Node.void("item")
    keepalive.set_attribute("name", "keepalive")
    keepalive.set_attribute(
        "url",
        "http://127.0.0.1/core/keepalive?pa=127.0.0.1&amp;ia=127.0.0.1&amp;ga=127.0.0.1&amp;ma=127.0.0.1&amp;t1=2&amp;t2=10",
    )
    services.add_child(keepalive)

    itemUrls = {
        "cardmng": "http://localhost:8083",
        "facility": "http://localhost:8083",
        "message": "http://localhost:8083",
        "numbering": "http://localhost:8083",
        "package": "http://localhost:8083",
        "pcbevent": "http://localhost:8083",
        "pcbtracker": "http://localhost:8083",
        "pkglist": "http://localhost:8083",
        "posevent": "http://localhost:8083",
        "userdata": "http://localhost:8083",
        "userid": "http://localhost:8083",
        "eacoin": "http://localhost:8083",
        "local": "http://localhost:8083",
        "local2": "http://localhost:8083",
        "lobby": "http://localhost:8083",
        "lobby2": "http://localhost:8083",
        "dlstatus": "http://localhost:8083",
        "netlog": "http://localhost:8083",
        "sidmgr": "http://localhost:8083",
        "globby": "http://localhost:8083",
    }

    for name, url in itemUrls.items():
        item = Node.void("item")
        item.set_attribute("name", name)
        item.set_attribute("url", url)
        services.add_child(item)

    response.add_child(services)

    return response


async def alivePCBTracker(request: Request, node: Node):
    response = Node.void("response")
    pcbtracker = Node.void("pcbtracker")
    pcbtracker.set_attribute("status", "0")
    pcbtracker.set_attribute("expire", "1200")
    pcbtracker.set_attribute("ecenable", node.attribute("ecflag", "1"))
    pcbtracker.set_attribute("eclimit", "0")
    pcbtracker.set_attribute("limit", "0")
    pcbtracker.set_attribute("time", str(round(time.time())))

    response.add_child(pcbtracker)

    return response


async def getMessage(request: Request, node: Node):
    response = Node.void("response")

    message = Node.void("message")
    message.set_attribute("expire", "300")
    message.set_attribute("status", "0")

    response.add_child(message)

    return response


async def getFacility(request: Request, node: Node):
    response = Node.void("response")

    facility = Node.void("facility")
    facility.set_attribute("status", "0")

    location = Node.void("location")
    location.add_child(Node.string("id", "ea"))
    location.add_child(Node.string("country", "AX"))
    location.add_child(Node.string("region", "1"))
    location.add_child(Node.string("name", "CORE"))
    location.add_child(Node.u8("type", 0))
    location.add_child(Node.string("countryname", "UNKNOWN"))
    location.add_child(Node.string("countryjname", "不明"))
    location.add_child(Node.string("regionname", "CORE"))
    location.add_child(Node.string("regionjname", "CORE"))
    location.add_child(Node.string("customercode", "AXUSR"))
    location.add_child(Node.string("companycode", "AXCPY"))
    location.add_child(Node.s32("latitude", 6666))
    location.add_child(Node.s32("longitude", 6666))
    location.add_child(Node.u8("accuracy", 0))
    facility.add_child(location)

    line = Node.void("line")
    line.add_child(Node.string("id", "."))
    line.add_child(Node.u8("class", 0))
    facility.add_child(line)

    portfw = Node.void("portfw")
    portfw.add_child(Node.ipv4("globalip", "127.0.0.1"))  # request.client.host
    portfw.add_child(Node.s16("globalport", 5700))  # request.client.port
    portfw.add_child(Node.s16("privateport", 5700))  # request.client.port
    facility.add_child(portfw)

    public = Node.void("public")
    public.add_child(Node.u8("flag", 1))
    public.add_child(Node.string("name", "UNKNOWN"))
    public.add_child(Node.s32("latitude", 0))
    public.add_child(Node.s32("longitude", 0))
    facility.add_child(public)

    share = Node.void("share")
    eacoin = Node.void("eacoin")
    eacoin.add_child(Node.s32("notchamount", 0))
    eacoin.add_child(Node.s32("notchcount", 0))
    eacoin.add_child(Node.s32("supplylimit", 100000))
    share.add_child(eacoin)

    url = Node.void("url")
    url.add_child(Node.string("eapass", "CORE v1.50c"))
    url.add_child(Node.string("arcadefan", "CORE v1.50c"))
    url.add_child(Node.string("konaminetdx", "CORE v1.50c"))
    url.add_child(Node.string("konamiid", "CORE v1.50c"))
    url.add_child(Node.string("eagate", "CORE v1.50c"))
    share.add_child(url)

    facility.add_child(share)

    response.add_child(facility)

    return response


async def putPCBevent(request: Request, node: Node):
    response = Node.void("response")

    pcbevent = Node.void("pcbevent")
    pcbevent.set_attribute("status", "0")

    response.add_child(pcbevent)

    return response


async def packageList(request: Request, node: Node):
    response = Node.void("response")

    package = Node.void("package")
    package.set_attribute("expire", "1200")
    package.set_attribute("status", "0")

    response.add_child(package)

    return response


def load(plugin: Plugin):
    plugin.dispatch("services.get", getServices)
    plugin.dispatch("pcbtracker.alive", alivePCBTracker)
    plugin.dispatch("message.get", getMessage)
    plugin.dispatch("facility.get", getFacility)
    plugin.dispatch("pcbevent.put", putPCBevent)
    plugin.dispatch("package.list", packageList)
