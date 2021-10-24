import urllib
import time
import discord
from discord.ext import commands

from main_program import req, queue_song, re, da1, youtube_download, FFMPEG_OPTIONS


class Repeat(commands.cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    def repeat(self, ctx, voice):
        req()
        if not queue_song[str(ctx.guild.id)][re[3][str(ctx.guild.id)]] in da1.keys():
            aa = str(urllib.request.urlopen(queue_song[str(ctx.guild.id)][re[3][str(ctx.guild.id)]]).read().decode())
            starting = aa.find("<title>") + len("<title>")
            ending = aa.find("</title>")
            da1[queue_song[str(ctx.guild.id)][re[3][str(ctx.guild.id)]]] = (
                aa[starting:ending].replace("&#39;", "'").replace(" - YouTube", "").replace("&amp;", "&")
            )
        time.sleep(1)
        if re[7].get(ctx.guild.id, -1) == 1 and not voice.is_playing():
            re[3][str(ctx.guild.id)] += 1
            if re[3][str(ctx.guild.id)] >= len(queue_song[str(ctx.guild.id)]):
                re[3][str(ctx.guild.id)] = 0
        if re[2].get(ctx.guild.id, -1) == 1 or re[7].get(ctx.guild.id, -1) == 1:
            if not voice.is_playing():
                url = youtube_download(
                    ctx, queue_song[str(ctx.guild.id)][re[3][str(ctx.guild.id)]]
                )
                voice.play(
                    discord.FFmpegPCMAudio(url, **FFMPEG_OPTIONS),
                    after=lambda e: self.repeat(ctx, voice),
                )
