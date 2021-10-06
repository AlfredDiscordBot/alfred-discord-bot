import discord 
import traceback
from discord.channel import TextChannel
from discord.ext.commands.context import Context
from functools import wraps
from typing import Callable, Union, Awaitable


class ErrorLogger:
    """
    ErrorLogger: error logging utility class
    provides with few methods and decorators to track the error 

    :param dev_channel: TextChannel to send the error emebd
    """
    def __init__(self, dev_channel: Union[TextChannel, None]) -> None:
        self.set_channel(dev_channel)
    
    def set_channel(self, dev_channel: Union[TextChannel, None]) -> None:
        """
        Set the Log channel to the Dev Channel
        
        :param dev_channel: TextChannel to send the error embed
        """
        self.channel = dev_channel
    
    @staticmethod
    def get_embed(error_traceback: str, guild_name: str) -> discord.Embed:
        """
        Create Embed using the error_traceback and guild_name.

        :param str error_traceback: the tracback for the error.
        :param guild_name: the name of the server in which the error was recorded.
        """
        embed = discord.Embed(
            color = discord.Color.from_rgb(240, 196, 25),
            description = f"```py\n{str(error_traceback)}\n```",
            title = "Error",
        )

        embed.set_thumbnail(url="https://github.com/alvinbengeorge/alfred-discord-bot/blob/replit/error.png?raw=true")
        embed.set_footer(text=f"in {guild_name}")

        return embed
    
    async def log(self, error_traceback: str, guild_name: str) -> None:
        """
        Log the error_traceback in the dev_channel

        :param str error_traceback: the tracback for the error.
        :param guild_name: the name of the server in which the error was recorded.
        """
        embed = self.get_embed(error_traceback, guild_name)
        await self.channel.send(embed=embed)

    def track_command(self, function: Callable) -> Awaitable:
        """
        track the errors of the command function wrapped by track_command decorator
        
        :param function: command function to track.
        """
        
        @wraps(function)
        async def wrapper(ctx: Context, *args, **kwargs):
            try:
                await function(ctx, *args, **kwargs)
            except:
                await self.log(traceback.format_exc(), ctx.guild.name)
        
        return wrapper
