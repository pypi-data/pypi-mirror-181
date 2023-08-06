from graphql import OperationType
from pydantic import Field
from rath import rath
import contextvars
import logging

from rath.links.base import TerminatingLink
from rath.contrib.fakts.links.aiohttp import FaktsAIOHttpLink
from rath.contrib.fakts.links.websocket import FaktsWebsocketLink
from rath.contrib.herre.links.auth import HerreAuthLink
from rath.links.aiohttp import AIOHttpLink
from rath.links.auth import AuthTokenLink

from rath.links.base import TerminatingLink
from rath.links.compose import compose
from rath.links.dictinglink import DictingLink
from rath.links.shrink import ShrinkingLink
from rath.links.split import SplitLink
from rath.links.websockets import WebSocketLink
from rath.links.compose import TypedComposedLink, compose


current_unlok_rath = contextvars.ContextVar("current_unlok_rath")


class UnlokLinkComposition(TypedComposedLink):
    dicting: DictingLink = Field(default_factory=DictingLink)
    auth: AuthTokenLink
    split: SplitLink


class UnlokRath(rath.Rath):
    link: UnlokLinkComposition

    async def __aenter__(self):
        await super().__aenter__()
        current_unlok_rath.set(self)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await super().__aexit__(exc_type, exc_val, exc_tb)
        current_unlok_rath.set(None)
