from discord.ext import commands
from main_program import re
import discord


class Utils(commands.cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def set_sessionid(ctx, sessionid):
        re[9] = sessionid
        await ctx.send(
            embed=discord.Embed(description="SessionID set", color=discord.Color(re[8]))
        )
