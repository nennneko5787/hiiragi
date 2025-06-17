from contextlib import asynccontextmanager

from fastapi import FastAPI

from hiiragi.backend import route
from hiiragi.log import logger
from hiiragi.plugin import PluginManager


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Hiiragi is loading...")
    PluginManager.loadPlugins()
    logger.info("Hiiragi is loaded!")
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(route.router)
