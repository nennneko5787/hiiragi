from fastapi import APIRouter, Request, Response

from hiiragi.log import logger
from hiiragi.plugin import PluginManager
from hiiragi.protocol.node import Node
from hiiragi.protocol.protocol import EAmuseProtocol
from hiiragi.utils import generateKey, protocol

from . import exceptions

router = APIRouter()


@router.post("//{model}/{module}/{method}")
async def call(request: Request, model: str, module: str, method: str):
    return await handle(request, model=model, module=module, method=method)


@router.post("/")
async def index(request: Request):
    return await handle(request, **dict(request.query_params.items()))


async def handle(request: Request, **kwargs):
    body = await request.body()
    xeamuse = request.headers.get("x-eamuse-info", "")

    compress = "lz77" if request.headers.get("x-compress", "none") != "none" else None
    node = protocol.decode(compress, xeamuse, body)

    game = kwargs["model"].split(":")[0]
    action = kwargs["f"]

    plugin = PluginManager.getPlugin(game)
    if not plugin:
        logger.error(f'Game "{game}" plugin is missing and cannot process your request')
        return
    do = plugin.get(action)
    if not do:
        logger.error(f'Undefined action "{action}"')
        return

    response = await do(request, node)

    if response is None or not isinstance(response, Node):
        raise exceptions.WrongResponse()

    xeamuse, date = generateKey()
    return Response(
        protocol.encode(
            None,
            xeamuse,
            response,
            text_encoding=EAmuseProtocol.SHIFT_JIS,
            packet_encoding=EAmuseProtocol.XML,
        ),
        headers={
            "X-Powered-By": "Hiiragi",
            "X-Compress": "none",
            "X-Eamuse-Info": xeamuse,
            "Date": date,
            "Connection": "keep-alive",
            "Keep-Alive": "timeout=5",
        },
        media_type="application/octet-stream",
    )
