import discord
from discord.ext import commands

from External_functions import youtube_info, cembed
from stuff import req, queue_song, re, da1


class CurrentMusic(commands.cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["curr"])
    async def currentmusic(self, ctx):
        req()
        if len(queue_song[str(ctx.guild.id)]) > 0:
            description = (
                    "[Current index: "
                    + str(re[3][str(ctx.guild.id)])
                    + "]("
                    + queue_song[str(ctx.guild.id)][re[3][str(ctx.guild.id)]]
                    + ")\n"
            )
            info = youtube_info(queue_song[str(ctx.guild.id)][re[3][str(ctx.guild.id)]])
            check = "\n\nDescription: \n" + info["description"] + "\n"
            if 3000 > len(check) > 0:
                description += check
            description += (
                    f"\nDuration: {str(info['duration'] // 60)}min {str(info['duration'] % 60)}sec"
                    + f"\n\n{info['view_count']} views\n{info['like_count']} :thumbsup:\n{info['dislike_count']} :thumbdown:"
            )
            await ctx.send(
                embed=cembed(
                    title=str(da1[queue_song[str(ctx.guild.id)][re[3][str(ctx.guild.id)]]]),
                    description=description,
                    color=re[8],
                    thumbnail=info["thumbnail"],
                )
            )
        else:
            await ctx.send(
                embed=discord.Embed(
                    title="Empty queue",
                    description="Your queue is currently empty",
                    color=discord.Color(value=re[8]),
                )
            )
