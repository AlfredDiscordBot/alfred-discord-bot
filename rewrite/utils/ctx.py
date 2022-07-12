from __future__ import annotations
import typing_extensions  # type: ignore
from typing import TYPE_CHECKING


from nextcord.ext import commands

if TYPE_CHECKING:
    from typing_extensions import Self, TypeVar, TypeAlias, Optional



class GuildContext(commands.Context):
    def tick(self: Self, mode: bool) -> str:
        if mode is True:
            return "✅"
        return "❌"
        