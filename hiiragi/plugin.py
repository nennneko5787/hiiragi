import importlib
import os
import types
from typing import Awaitable, Callable, Dict, Optional

from fastapi import Request

from hiiragi.log import logger
from hiiragi.protocol.node import Node


class Plugin:
    def __init__(self, module: types.ModuleType):
        self.__dispatched: Dict[str, Callable[[Request, Node], Awaitable[Node]]] = {}
        self.name = module.name
        self.version = module.version
        module.load(self)

    def dispatch(self, action: str, func: Callable[[Request, Node], Awaitable[Node]]):
        self.__dispatched[action] = func
        logger.debug(f"Dispatched action: {action}")

    def get(self, action: str) -> Optional[Callable[[Request, Node], Awaitable[Node]]]:
        if action not in self.__dispatched:
            return None
        return self.__dispatched[action]


class PluginManager:
    games: Dict[str, Plugin] = {}

    @classmethod
    def __addPlugin(cls, game: str, plugin: Plugin):
        cls.games[game] = plugin

    @classmethod
    def getPlugin(cls, game: str) -> Optional[Plugin]:
        if game not in cls.games:
            return None
        return cls.games[game]

    @classmethod
    def loadPlugins(cls):
        for folder in os.listdir("./plugins/"):
            path = os.path.join("./plugins", folder)
            if os.path.isdir(path):
                pluginPath = os.path.join(path, "plugin.py")
                if os.path.isfile(pluginPath):
                    logger.info(f'Loading "{folder}"...')
                    module = importlib.import_module(f"plugins.{folder}.plugin")
                    cls.__addPlugin(module.game, Plugin(module))
                    logger.info(
                        f"Loaded {module.name} (target: {module.game}, version: {module.version})!"
                    )
                else:
                    logger.warning(f'Folder "{folder}" is not plugin folder.')
