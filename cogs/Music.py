import nextcord
import youtube_dl
import re as regex
import utils.External_functions as ef

from utils.Storage_facility import Variables
from nextcord.abc import GuildChannel
from datetime import datetime
from nextcord.ext import commands
from asyncio import create_task, sleep
from typing import Union

# Use nextcord.slash_command()


def requirements():
    return ["DEV_CHANNEL", "FFMPEG_OPTIONS", "ydl_op"]


class MusicCache:
    def __init__(self):
        self.var = Variables("cogs/__pycache__/YtCache")
        self.data = self.var.show_data()

    def update(self, key: str, data: dict):
        self.data["songs"][key] = data
        self.var.pass_all(**self.data)
        self.var.save()

    def get_value(self, key: str):
        return self.data["songs"].get(key)


class Player:
    def __init__(self, CLIENT: commands.Bot, FFMPEG_OPTIONS, YDL_OP):
        self.CLIENT = CLIENT
        self.FFMPEG_OPTIONS = FFMPEG_OPTIONS
        self.YDL_OP = YDL_OP
        self.cache = MusicCache()

    def info(self, url: str):
        with youtube_dl.YoutubeDL(self.YDL_OP) as ydl:
            info = ydl.extract_info(url, download=False)
        return info

    def download(self, data: dict):
        self.cache.update(self.url_gen(data), self.cache_data(data))
        return self.source(data["formats"][0]["url"])

    def cache_data(self, data: dict):
        return {
            "name": data.get("title", "Unavailable"),
            "duration": data.get("duration", 300),
        }

    async def search_song(self, name: str):
        html = await ef.get_async(
            "https://www.youtube.com/results?search_query={}".format(
                ef.convert_to_url(name)
            )
        )
        if urls := regex.findall(r"watch\?v=(\S{11})", html):
            return urls[0]

    async def get_song(self, url: str):
        value = self.cache.get_value(url)
        if value is None:
            info = self.info(url=url)
            self.download(info)
            return self.cache_data(info)
        else:
            return value

    def source(self, url: str):
        return nextcord.FFmpegPCMAudio(url, **self.FFMPEG_OPTIONS)

    def uploader_date(self, st):
        return int(datetime.strptime(st, "%Y%m%d").timestamp())

    def duration(self, time: int):
        mins, secs = divmod(time, 60)
        hours, mins = divmod(mins, 60)
        if hours == 0:
            return "%02d mins %02d secs" % (mins, secs)
        else:
            return "%d hrs %02d mins %02d secs" % (hours, mins, secs)

    def url_gen(self, data: dict):
        return "https://www.youtube.com/watch?v={}".format(data.get("id"))


class Music(commands.Cog):
    def __init__(self, CLIENT, DEV_CHANNEL, FFMPEG_OPTIONS, ydl_op):
        self.CLIENT = CLIENT
        self.YDL_OP = ydl_op
        self.DEV_CHANNEL = DEV_CHANNEL
        self.FFMPEG_OPTIONS = FFMPEG_OPTIONS
        self.player = Player(self.CLIENT, FFMPEG_OPTIONS, ydl_op)

    def after(self, ctx: Union[commands.context.Context, nextcord.Interaction]):
        create_task(coro=self.repeat(ctx=ctx))

    async def repeat(self, ctx: Union[commands.context.Context, nextcord.Interaction]):
        await sleep(1)
        if not ctx.guild.voice_client:
            return
        index = self.CLIENT.re[3].get(ctx.guild)
        queue = self.CLIENT.queue_song.get(ctx.guild, [])
        if not queue:
            if index is not None:
                del self.CLIENT.re[3]
            await ctx.send(
                embed=ef.cembed(
                    title="Empty queue",
                    description="You have an empty queue, and I can't play any song",
                    color=self.CLIENT.color(ctx.guild),
                    author=ctx.guild,
                    fields={"Maybe...": "Use `'q` or `'p` to add songs to the queue"},
                    thumbnail=ctx.guild.icon,
                )
            )
            return
        if index >= len(queue):
            index = len(queue) - 1
        info = self.player.info(queue[index])
        ctx.guild.voice_client.play(
            self.player.download(info), after=lambda e: self.after(ctx=ctx)
        )

    @nextcord.slash_command(name="music", description="It's music time")
    async def music(self, inter):
        print(inter.user)

    @music.subcommand(name="disconnect", description="Bye")
    async def disconnect(self, inter: nextcord.Interaction):
        if not ef.check_voice(inter):
            await inter.response.send_message(
                embed=ef.cembed(
                    title="Permission Denied",
                    description="You must be in the VC to execute this command",
                    color=self.CLIENT.color(inter.guild),
                    author=inter.guild,
                    thumbnail=self.CLIENT.user.avatar,
                )
            )
            return

        await inter.response.defer()
        voice = inter.guild.voice_client
        voice.stop()
        await voice.disconnect()
        await inter.send(
            embed=ef.cembed(
                title="Bye",
                description="Hope I get to listen to you next time",
                color=self.CLIENT.color(inter.guild),
                author=inter.user,
                thumbnail=self.CLIENT.user.avatar,
            )
        )

    @music.subcommand(name="connect", description="Connect to a voice channel")
    async def connect(
        self,
        inter: nextcord.Interaction,
        channel: GuildChannel = ef.defa(nextcord.ChannelType.voice),
    ):
        if (not channel) and inter.user.voice and (vc := inter.user.voice.channel):
            channel = vc
        await channel.connect()
        await inter.send(
            embed=ef.cembed(
                description={
                    "Connected to": channel.name,
                    "Bitrate": "{}kbps".format(channel.bitrate // 1000),
                    "People": "{} people in the channel".format(len(channel.members)),
                },
                color=self.CLIENT.color(inter.guild),
                author=inter.user,
                footer={
                    "text": "Have fun listening to music",
                    "icon_url": self.CLIENT.user.avatar,
                },
                thumbnail=inter.guild.icon,
            )
        )

    @music.subcommand(name="play", description="play a song")
    async def play(self, inter):
        print(inter.user)

    @play.subcommand(name="song", description="play a song from search")
    async def song(self, inter: nextcord.Interaction, song: str):
        if not ef.check_voice(inter):
            await inter.response.send_message(
                embed=ef.cembed(
                    title="Permission Denied",
                    description="Sorry you cannot play music as you're not in the vc",
                    author=inter.user,
                    color=self.CLIENT.color(inter.guild),
                    thumbnail=self.CLIENT.user.avatar,
                ),
                ephemeral=True,
            )
            return
        await inter.response.defer()
        url = await self.player.search_song(name=song)
        if not url:
            await inter.send(
                embed=ef.cembed(
                    title="Unavailable",
                    description="Couldn't find the song, please try again with a different name",
                    color=self.CLIENT.color(inter.guild),
                    author=inter.guild,
                    thumbnail=self.CLIENT.user.avatar,
                )
            )
            return
        info = self.player.info(url)
        await inter.send(
            embed=ef.cembed(
                title="Playing {}".format(info.get("title")),
                color=self.CLIENT.color(inter.guild),
                thumbnail=info.get("thumbnail"),
                description={
                    "duration": self.player.duration(info.get("duration", 0)),
                    "uploader": info.get("uploader"),
                    "view count": f"{info.get('view_count'):,}",
                    "Uploaded": "<t:{}:R>".format(
                        self.player.uploader_date(info.get("upload_date"))
                    ),
                },
                author=inter.user,
            )
        )
        inter.guild.voice_client.play(
            self.player.download(info), after=lambda e: self.after(ctx=inter)
        )


def setup(client, **i):
    client.add_cog(Music(client, **i))
