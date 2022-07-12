from __future__ import annotations
from typing import TYPE_CHECKING
import typing_extensions  # type: ignore    
from os import environ

from .utils import GuildContext

from nextcord.ext import commands
from nextcord import Intents


if TYPE_CHECKING:
    from typing_extensions import Self
    from typing import Dict, Union, TypeAlias, TypeVar, Type

    from nextcord import Message

    C: TypeAlias = TypeVar("C", bound="commands.Context")
    E: TypeAlias = TypeVar("E", bound="Exception")
    CT: TypeAlias = Type[C]
    ET: TypeAlias = Type[E]
    


class Alfred(commands.Bot):
    def __init__(self: Self):
        kwargs: Dict[
            str, Union[
                str,
                Intents
            ]
        ] = {
            "shard_id": environ.get("SHARD", 1),
            "shard_count": environ.get("SHARD_COUNT", 1),
            "intents": Intents.all()
        }
        super().__init__(
            **kwargs
        )
    
    def _load_envs(self: Self) -> None:
        self._token: str = os.getenv("TOKEN")
        self._dev_channel: int = os.getenv("DEV_CHANNEL")
    
    async def get_context(
        self: Self,
        message: Message,
        *,
        cls: CT = GuildContext,
    ) -> C:
        return super().get_context(message=message, cls=cls)
    
    async def on_command_error(self: Self, ctx: CT, exc: ET) -> None:  # type: ignore
        if isinstance(exc, commands.MissingPermissions):
            await ctx.send("You lack permissions to execute this action.")
        if isinstance(exc, commands.BotMissingPermissions):
            await ctx.send("I lack permissions to execute this action.")
        if isinstance(exc, commands.CommandNotFound):
            pass
        await self.get_channel(self._dev_channel).send(f"Error: {exc}")
    
    


bot = Alfred()
bot.run(environ['token'])
