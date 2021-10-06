import discord 
import traceback
from functools import wraps
from typing import Callable


class ErrorLogger:
    def __init__(self, dev_channel: discord.channel.TextChannel):
        self.set_channel(dev_channel)
    
    def set_channel(self, dev_channel: discord.channel.TextChannel):
        self.channel = dev_channel
    
    @staticmethod
    def get_embed(error_traceback: str, guild_name: str):
        embed = discord.Embed(
            color = discord.Color.from_rgb(240, 196, 25),
            description = f"```py\n{str(error_traceback)}\n```",
            title = "Error",
        )

        embed.set_thumbnail(url="https://github.com/alvinbengeorge/alfred-discord-bot/blob/replit/error.png?raw=true")
        embed.set_footer(text=f"in {guild_name}")

        return embed
    
    async def log(self, error_traceback: str, guild_name: str):
        embed = self.get_embed(error_traceback, guild_name)
        await self.channel.send(embed=embed)

    def track_command(self, function: Callable):
        @wraps(function)
        async def wrapper(ctx, *args, **kwargs):
            try:
                await function(ctx, *args, **kwargs)
            except:
                await self.log(traceback.format_exc(), ctx.guild.name)
        
        return wrapper
