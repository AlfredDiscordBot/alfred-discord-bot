import discord
from discord.ext import commands

from main_program import req, vc_channel, addt, queue_song, get_elem, re


class AddTo(commands.cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def addto(self, ctx, mode, *, text):
        req()
        present = 1
        voicechannel = discord.utils.get(
            ctx.guild.voice_channels, id=vc_channel[str(ctx.guild.id)]
        )
        member = voicechannel.members
        for mem in member:
            if str(ctx.author) == str(mem):
                present = 0
                break
        if mode == "playlist" and present == 0:
            addt(text, queue_song[str(ctx.guild.id)].copy())
            await ctx.send("Done")
        elif mode == "queue" and present == 0:
            print(len(get_elem(str(text))))
            song_list = ""
            for i in range(0, len(get_elem(str(text)))):
                link_add = get_elem(str(text))[i]
                queue_song[str(ctx.guild.id)].append(link_add)
            await ctx.send(
                embed=discord.Embed(
                    title="Songs added",
                    description="Done",
                    color=discord.Color(value=re[8]),
                )
            )
        else:
            if present == 0:
                await ctx.send("Only playlist and queue")
            else:
                await ctx.send(
                    embed=discord.Embed(
                        title="Permission denied",
                        description="Join the voice channel to modify queue",
                        color=discord.Color(value=re[8]),
                    )
                )
