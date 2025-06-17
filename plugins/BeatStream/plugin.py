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
    facility = Node.void("item")
    facility.set_attribute("name", "facility")
    facility.set_attribute("url", "http://localhost:8083/")

    message = Node.void("item")
    message.set_attribute("name", "message")
    message.set_attribute("url", "http://localhost:8083/")

    pcbtracker = Node.void("item")
    pcbtracker.set_attribute("name", "pcbtracker")
    pcbtracker.set_attribute("url", "http://localhost:8083/")

    # add child node
    services.add_child(facility)
    services.add_child(message)
    services.add_child(pcbtracker)
    response.add_child(services)

    return response


async def alivePCBTracker(request: Request, node: Node):
    response = Node.void("response")

    pcbtracker = Node.void("pcbtracker")
    pcbtracker.set_attribute("status", "0")
    pcbtracker.set_attribute("expire", "1200")
    pcbtracker.set_attribute("ecenable", node.attribute("ecflag"))
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
    location.add_child(Node.string("id", ""))
    location.add_child(Node.string("country", "UK"))
    location.add_child(Node.string("region", ""))
    location.add_child(Node.string("name", "Hello Flask"))
    location.add_child(Node.u8("type", 0))
    location.add_child(Node.string("countryname", "UK-c"))
    location.add_child(Node.string("countryjname", ""))
    location.add_child(Node.string("regionname", "UK-r"))
    location.add_child(Node.string("regionjname", ""))
    location.add_child(Node.string("customercode", ""))
    location.add_child(Node.string("companycode", ""))
    location.add_child(Node.s32("latitude", 0))
    location.add_child(Node.s32("longitude", 0))
    location.add_child(Node.u8("accuracy", 0))
    facility.add_child(location)

    line = Node.void("line")
    line.add_child(Node.string("id", ""))
    line.add_child(Node.u8("class", 0))
    facility.add_child(line)

    portfw = Node.void("portfw")
    portfw.add_child(Node.ipv4("globalip", request.client.host))
    portfw.add_child(Node.s16("globalport", 5000))
    portfw.add_child(Node.s16("privateport", 5000))
    facility.add_child(portfw)

    public = Node.void("public")
    public.add_child(Node.u8("flag", 1))
    public.add_child(Node.string("name", ""))
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
    url.add_child(Node.string("eapass", "www.ea-pass.konami.net"))
    url.add_child(Node.string("arcadefan", "www.konami.jp/am"))
    url.add_child(Node.string("konaminetdx", "http://am.573.jp"))
    url.add_child(Node.string("konamiid", "http://id.konami.jp"))
    url.add_child(Node.string("eagate", "http://eagate.573.jp"))
    share.add_child(url)

    facility.add_child(share)

    response.add_child(facility)
    return response


async def pcbevent(request: Request, node: Node):
    response = Node.void("response")

    pcbevent = Node.void("pcbevent")
    pcbevent.set_attribute("status", "0")

    pcbevent.add_child(response)

    return response


async def packageList(request: Request, node: Node):
    response = Node.void("response")

    package = Node.void("package")
    package.set_attribute("expire", "600")
    package.set_attribute("status", "0")

    response.add_child(package)

    return response


def load(plugin: Plugin):
    plugin.dispatch("services.get", getServices)
    plugin.dispatch("pcbtracker.alive", alivePCBTracker)
    plugin.dispatch("message.get", getMessage)
    plugin.dispatch("facility.get", getFacility)
    plugin.dispatch("pcbevent.put", pcbevent)
    plugin.dispatch("package.list", packageList)
