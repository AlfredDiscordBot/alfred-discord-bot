import discord
from discord.ext import commands
from discord_slash import SlashCommand, cog_ext

from main_program import req, re


class AutoPlay(commands.cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def autoplay(self, ctx):
        req()
        if ctx.author.id in [i.id for i in ctx.voice_client.channel.members]:
            st = ""
            re[7][ctx.guild.id] = re[7].get(ctx.guild.id, -1) * -1
            if re[7].get(ctx.guild.id, -1) == 1:
                re[2][ctx.guild.id] = -1
            if re[7][ctx.guild.id] < 0:
                st = "Off"
            else:
                st = "_On_"
            await ctx.send(
                embed=discord.Embed(
                    title="Autoplay", description=st, color=discord.Color(value=re[8])
                )
            )
        else:
            await ctx.send(
                embed=discord.Embed(
                    title="Permissions Denied",
                    description="You need to be in the voice channel to toggle autoplay",
                    color=discord.Color(value=re[8]),
                )
            )

    @cog_ext.cog_slash(
        name="autoplay",
        description="Plays the next song automatically if its turned on",
    )
    async def autoplay_slash(self, ctx):
        req()
        await ctx.defer()
        await self.autoplay(ctx)
