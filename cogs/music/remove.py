import discord
from discord.ext import commands

from main_program import req, queue_song, da1, re


class Remove(commands.cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def remove(self, ctx, n):
        req()
        try:
            mem = [str(names) for names in ctx.voice_client.channel.members]
        except:
            mem = []
        if mem.count(str(ctx.author)) > 0:
            if int(n) < len(queue_song[str(ctx.guild.id)]):
                await ctx.send(
                    embed=discord.Embed(
                        title="Removed",
                        description=da1[queue_song[str(ctx.guild.id)][int(n)]],
                        color=discord.Color(value=re[8]),
                    )
                )
                del da1[queue_song[str(ctx.guild.id)][int(n)]]
                queue_song[str(ctx.guild.id)].pop(int(n))
            else:
                await ctx.send(
                    embed=discord.Embed(
                        title="Not removed",
                        description="Only "
                                    + len(queue_song[str(ctx.guild.id)])
                                    + " song(s) in your queue",
                        color=discord.Color(value=re[8]),
                    )
                )
        else:
            await ctx.send(
                embed=discord.Embed(
                    title="Permission denied",
                    description="Join the voice channel to modify queue",
                    color=discord.Color(value=re[8]),
                )
            )
