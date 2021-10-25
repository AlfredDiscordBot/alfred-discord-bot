import discord
from discord.ext import commands
from discord_slash import cog_ext

from stuff import req, re


class Loop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def loop(self, ctx):
        req()
        if ctx.author.id in [i.id for i in ctx.voice_client.channel.members]:
            st = ""
            re[2][ctx.guild.id] = re[2].get(ctx.guild.id, -1) * -1
            if re[2].get(ctx.guild.id, 1) == 1:
                re[7][ctx.guild.id] = -1
            if re[2].get(ctx.guild.id, 1) < 0:
                st = "Off"
            else:
                st = "_On_"
            await ctx.send(
                embed=discord.Embed(
                    title="Loop", description=st, color=discord.Color(value=re[8])
                )
            )
        else:
            await ctx.send(
                embed=discord.Embed(
                    title="Permissions Denied",
                    description="You need to be in the voice channel to toggle loop",
                    color=discord.Color(value=re[8]),
                )
            )

    @cog_ext.cog_slash(name="loop", description="Loops the same song")
    async def loop_slash(self, ctx):
        await ctx.defer()
        req()
        await self.loop(ctx)


def setup(bot):
    bot.add_cog(Loop(bot))