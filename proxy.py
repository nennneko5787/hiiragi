import httpx
from fastapi import FastAPI, Request, Response

from hiiragi.protocol.node import Node
from hiiragi.protocol.protocol import EAmuseProtocol

app = FastAPI()

TARGET_BASE_URL = "http://localhost:8082"

protocol = EAmuseProtocol()


def modify(node: Node) -> Node:
    if node.name != "response":
        # Not what we expected, bail
        return None
    body = node.children[0]
    if body.name == "services":
        for child in body.children:
            if child.name == "item":
                if child.attribute("name") == "ntp":
                    # Don't override this
                    continue
                elif child.attribute("name") == "keepalive":
                    # Don't override this
                    continue
                else:
                    # Get netloc to replace
                    child.set_attribute(
                        "url",
                        child.attribute("url").replace(
                            "localhost:8082", "localhost:8083"
                        ),
                    )
        return node
    return None


@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy(request: Request, path: str, f: str):
    target_url = f"{TARGET_BASE_URL}/{path}"
    body = await request.body()

    compress = "lz77" if request.headers.get("x-compress", "none") != "none" else None
    req = protocol.decode(compress, request.headers.get("x-eamuse-info"), body)

    # Get query parameter
    query_string = request.url.query
    if query_string:
        target_url += f"?{query_string}"

    # Proxing
    async with httpx.AsyncClient() as client:
        response = await client.request(
            method=request.method,
            url=target_url,
            headers={
                key: value
                for key, value in request.headers.items()
                if key.lower() != "host"
            },
            content=body,
        )

    headers = dict(response.headers)

    compress = "lz77" if response.headers.get("x-compress", "none") != "none" else None
    res = protocol.decode(
        compress, response.headers.get("x-eamuse-info"), response.content
    )

    with open(f"./responses/{f}.txt", "w") as fp:
        fp.write(str(req) + "\n\n" + str(res))

    res = modify(res) or res
    data = protocol.encode(
        compress,
        response.headers.get("x-eamuse-info"),
        res,
        text_encoding=EAmuseProtocol.SHIFT_JIS,
        packet_encoding=EAmuseProtocol.XML,
    )

    # return
    del headers["content-length"]
    return Response(data, headers=headers)


# port: 8083
