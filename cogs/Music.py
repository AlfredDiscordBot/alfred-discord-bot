import nextcord
import youtube_dl
import re as regex
import utils.External_functions as ef

from utils.Storage_facility import Variables
from utils.assets import Button, color
from nextcord.abc import GuildChannel
from datetime import datetime
from nextcord.ext import commands
from asyncio import run_coroutine_threadsafe, sleep
from typing import Union

# Use nextcord.slash_command()


def requirements():
    return ["DEV_CHANNEL", "FFMPEG_OPTIONS", "ydl_op"]


class MusicCache:
    def __init__(self):
        self.var = Variables("cogs/__pycache__/YtCache")
        self.data = self.var.show_data()
        if not self.data:
            self.data = {"songs": {}}
            self.var.pass_all(**self.data)
            self.var.save()

    def update(self, key: str, data: dict):
        self.data["songs"][key] = data
        self.var.pass_all(**self.data)
        self.var.save()

    def get_value(self, key: str):
        return self.var.show_data()["songs"].get(key)


class Player:
    def __init__(self, CLIENT: commands.Bot, FFMPEG_OPTIONS, YDL_OP):
        self.CLIENT = CLIENT
        self.FFMPEG_OPTIONS = FFMPEG_OPTIONS
        self.YDL_OP = YDL_OP
        self.cache = MusicCache()
        self.temp_cache = {}

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
            return "https://youtube.com/watch?v=" + urls[0]

    def get_song(self, url: str):
        value = self.cache.data["songs"].get(url)
        if value == None:
            info = self.info(url=url)
            self.cache.update(url, self.cache_data(info))
            return self.cache_data(info)
        else:
            return value

    def get_info(self, url: str):
        if not (info := self.temp_cache.get(url)):
            info = self.info(url)
        data = {
            "title": info.get("title"),
            "description": info.get("description", "")[:4000],
            "thumbnail": info.get("thumbnail"),
            "fields": {
                "Info": ef.dict2str(
                    {
                        "Duration": self.duration(info.get("duration", 300)),
                        "Views": f'{info.get("view_count"):,}',
                        "Likes": f'{info.get("like_count"):,}',
                    }
                )
            },
            "url": url,
            "author": {
                "name": info.get("uploader"),
                "icon_url": "https://w7.pngwing.com/pngs/354/296/png-transparent-youtube-logo-computer-icons-youtube-angle-rectangle-logo.png",
            },
        }
        self.temp_cache[url] = info
        return data

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
    def __init__(self, CLIENT: commands.Bot, DEV_CHANNEL, FFMPEG_OPTIONS, ydl_op):
        self.CLIENT = CLIENT
        self.YDL_OP = ydl_op
        self.DEV_CHANNEL = DEV_CHANNEL
        self.FFMPEG_OPTIONS = FFMPEG_OPTIONS
        self.player = Player(self.CLIENT, FFMPEG_OPTIONS, ydl_op)

    def datasetup(self, guild: nextcord.guild.Guild):
        if guild.id not in self.CLIENT.re[3]:
            self.CLIENT.re[3][guild.id] = 0
        if guild.id not in self.CLIENT.queue_song:
            self.CLIENT.queue_song[guild.id] = []

    def add(self, guild: nextcord.guild.Guild, url: str):
        if guild.id not in self.CLIENT.queue_song:
            self.CLIENT.queue_song[guild.id] = []
        if (
            self.CLIENT.queue_song[guild.id] != []
            and self.CLIENT.queue_song[guild.id][-1] == url
        ):
            return
        self.CLIENT.queue_song[guild.id].append(url)

    def MusicButtonView(self, inter: nextcord.Interaction):
        pause, resume, after, before, show, stop, loop, autoplay = (
            Button(style=color, label="Pause", emoji="⏸️", row=0),
            Button(style=color, label="Resume", emoji="▶️", row=0),
            Button(style=color, label="Next", emoji="⏭️", row=0),
            Button(style=color, label="Previous", emoji="⏮️", row=0),
            Button(style=color, label="Queue", emoji="*️⃣", row=1),
            Button(style=color, label="Stop", emoji="⏹️", row=1),
            Button(style=color, label="Loop", emoji="🔂", row=1),
            Button(style=color, label="Autoplay", emoji="➡️", row=1),
        )
        pause.callback = self.pause(inter)
        resume.callback = self.resume(inter)
        view = nextcord.ui.View(timeout=None)
        for i in (pause, resume, after, before, show, stop, loop, autoplay):
            view.add_item(i)
        return view

    def get_current(self, guild: nextcord.guild.Guild):
        try:
            if (queue := self.CLIENT.queue_song.get(guild.id)) and (
                (index := self.CLIENT.re[3].get(guild.id)) >= 0
            ):
                return ef.cembed(
                    **self.player.get_info(queue[index]),
                    color=self.CLIENT.color(guild),
                    footer={
                        "text": "Current Index: {}".format(index),
                        "icon_url": self.CLIENT.user.avatar,
                    },
                )
        except IndexError:
            if not queue:
                del self.CLIENT.re[3][guild.id]
            elif index >= len(queue):
                self.CLIENT.re[3][guild.id] = 0
            return self.get_current(guild=guild)

        return ef.cembed(
            title="Oops",
            description="It seems like you've not played anything yet",
            color=self.CLIENT.color(guild),
            author=guild,
            thumbnail=self.CLIENT.user.avatar,
        )

    def after(self, ctx: Union[commands.context.Context, nextcord.Interaction]):
        coro = self.repeat(ctx=ctx)
        fut = run_coroutine_threadsafe(coro=coro, loop=self.CLIENT.loop)
        try:
            fut.result()
        except Exception as e:
            raise e

    async def repeat(self, ctx: Union[commands.context.Context, nextcord.Interaction]):
        await sleep(1)
        if (not ctx.guild.voice_client) or (ctx.guild.voice_client.is_playing()):
            return
        index = self.CLIENT.re[3].get(ctx.guild.id)
        queue = self.CLIENT.queue_song.get(ctx.guild.id, [])
        if not queue:
            if index is not None:
                del self.CLIENT.re[3]
            await ctx.send(
                embed=ef.cembed(
                    title="Empty queue",
                    description="You have an empty queue, and I can't play any song",
                    color=self.CLIENT.color(ctx.guild),
                    author=ctx.guild,
                    fields={
                        "Maybe...": "Use `/music play song` to add songs to the queue"
                    },
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

    @music.subcommand(name="current", description="Show current song")
    async def curr(self, inter: nextcord.Interaction):
        await inter.response.defer()
        embed = self.get_current(inter.guild)
        await inter.send(embed=embed)

    @music.subcommand(name="queue", description="Queue")
    async def queue(self, inter):
        print(inter.user)

    @music.subcommand(name="add", description="Add a song to the queue")
    async def addtoqueue(self, inter: nextcord.Interaction, song: str):
        url = await self.player.search_song(song)
        self.datasetup(inter.guild)
        mini_info = self.player.get_song(url)
        self.CLIENT.queue_song[inter.guild.id].append(url)
        await inter.send(
            embed=ef.cembed(
                title="Added",
                description=mini_info["name"],
                color=self.CLIENT.color(inter.guild),
                author=inter.user,
                thumbnail=self.CLIENT.user.avatar,
            ),
            view=self.MusicButtonView(inter),
        )

    @queue.subcommand(name="show", description="Shows the song in the server queue")
    async def show_queue(self, inter: nextcord.Interaction):
        if not self.CLIENT.queue_song.get(inter.guild.id):
            await inter.send(
                embed=ef.cembed(
                    title="Looks like...",
                    description="Your queue is empty",
                    color=self.CLIENT.color(inter.guild),
                    author=inter.guild,
                )
            )
            return
        await inter.response.defer()
        l = len(self.CLIENT.queue_song.get(inter.guild.id, []))
        index = self.CLIENT.re[3].get(inter.guild.id, 0)
        start = 0 if l < 20 else index - 10
        end = index + 10
        songs = self.CLIENT.queue_song.get(inter.guild.id, [])[start:end]
        await inter.send(
            embed=ef.cembed(
                title="Queue",
                description=[
                    f"`{ind}.` {content}"
                    for ind, content in enumerate(
                        [self.player.get_song(i).get("name") for i in songs]
                    )
                ],
                color=self.CLIENT.color(inter.guild),
                author=inter.guild,
            ),
            view=self.MusicButtonView(inter),
        )

    @music.subcommand(name="disconnect", description="Bye")
    async def leave(self, inter: nextcord.Interaction):
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
        await voice.disconnect(force=True)
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
        if not channel:
            await inter.send(
                embed=ef.cembed(
                    description="You need to provide a channel, or you need to be in a channel",
                    color=self.CLIENT.color(inter.guild),
                    author=inter.user,
                )
            )
            return
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
            ),
            view=self.MusicButtonView(inter),
        )

    @music.subcommand(name="stop", description="Stop the music")
    async def disconnect(self, inter: nextcord.Interaction):
        if not ef.check_voice(inter):
            await inter.response.send_message(
                embed=ef.cembed(
                    title="Permission Denied",
                    description="You are not in the vc",
                    color=self.CLIENT.color(inter.guild),
                    thumbnail=self.CLIENT.user.avatar,
                    author=inter.user,
                ),
                ephemeral=True,
            )
            return
        voice = inter.guild.voice_client
        voice.stop()
        await voice.disconnect()

    @music.subcommand(name="pause", description="Pause the music")
    async def pause(self, inter: nextcord.Interaction):
        if ef.check_voice(inter):
            voice = inter.guild.voice_client
            voice.pause()
            await inter.send(
                embed=ef.cembed(
                    title="Paused",
                    description="Use the command `/music resume` to resume the song",
                    color=self.CLIENT.color(inter.guild),
                    thumbnail=self.CLIENT.user.avatar,
                    author=inter.user,
                )
            )
        else:
            await inter.response.send_message(
                embed=ef.cembed(
                    title="Permission Denied",
                    description="Sorry you can't pause the song, you need to be in the vc to execute this command",
                    color=self.CLIENT.color(inter.guild),
                    author=inter.user,
                    thumbnail=self.CLIENT.user.avatar,
                )
            )

    @music.subcommand(name="resume", description="Resume the song")
    async def resume(self, inter: nextcord.Interaction):
        if ef.check_voice(inter):
            inter.guild.voice_client.resume()
            await inter.send(
                embed=ef.cembed(
                    description="Resuming the song", color=self.CLIENT.color
                )
            )
        else:
            await inter.send(
                embed=ef.cembed(
                    title="Permission Denied",
                    description="You need to be in the VC to resume the song",
                    color=self.CLIENT.color(inter.guild),
                )
            )

    @music.subcommand(name="play", description="play a song")
    async def play(self, inter):
        print(inter.user)

    @play.subcommand(name="song", description="play a song from search")
    async def song(self, inter: nextcord.Interaction, song: str):
        if (not inter.guild.voice_client) and (uservoice := inter.user.voice):
            await uservoice.channel.connect()
        elif not ef.check_voice(inter):
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
        self.datasetup(inter.guild)
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
        self.add(inter.guild, url=url)
        info = self.player.info(url)
        if (voice := inter.guild.voice_client).is_playing():
            voice.stop()
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
        self.player.cache.update(url, self.player.cache_data(info))
        self.CLIENT.re[3][inter.guild.id] = (
            len(self.CLIENT.queue_song[inter.guild.id]) - 1
        )
        voice.play(self.player.download(info), after=lambda e: self.after(ctx=inter))

    @play.subcommand(name="queue", description="Play song from queue, pass index value")
    async def play_queue(self, inter: nextcord.Interaction, index: int):
        if (not inter.guild.voice_client) and (uservoice := inter.user.voice):
            await uservoice.channel.connect()
        elif not ef.check_voice(inter):
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
        if (
            (queue := self.CLIENT.queue_song.get(inter.guild.id, []))
            and len(queue) > index
            and index >= 0
        ):
            if (voice := inter.guild.voice_client).is_playing():
                voice.stop()
            info = self.player.info(queue[index])
            embed = ef.cembed(
                title="Playing {} [ {} ]".format(info.get("title"), index),
                url=queue[index],
                description={
                    "duration": self.player.duration(info.get("duration", 0)),
                    "uploader": info.get("uploader"),
                    "view count": f"{info.get('view_count'):,}",
                    "Uploaded": "<t:{}:R>".format(
                        self.player.uploader_date(info.get("upload_date"))
                    ),
                },
                color=self.CLIENT.color(inter.guild),
                thumbnail=self.CLIENT.user.avatar,
                author=inter.guild,
                footer={
                    "text": "Thank you for choosing Alfred",
                    "icon_url": self.CLIENT.user.avatar,
                },
            )
            self.player.cache.update(queue[index], self.player.cache_data(info))
            voice.play(self.player.download(info), after=lambda e: self.after(inter))
            await inter.send(embed=embed)
        elif len(queue) <= index:
            await inter.send(
                embed=ef.cembed(
                    title="I'm sorry but",
                    description="Looks like there's not that many songs in your queue",
                    color=self.CLIENT.color(inter.guild),
                    thumbnail=self.CLIENT.user.avatar,
                    author=inter.guild,
                    footer={
                        "text": "If you see any bugs, DO NOT call ghostbusters\nGet to my support server or use feedback",
                        "icon_url": self.CLIENT.user.avatar,
                    },
                ),
                ephemeral=True,
            )
        else:
            await inter.send(
                embed=ef.cembed(
                    title="Hmmmm",
                    description="You must've entered a number less than `0`, which is `sus` indeed",
                    fields={
                        "Anyway the point is...": "Index value can only be from 0 to {}".format(
                            len(queue) - 1
                        )
                    },
                )
            )

    @play.subcommand(name="next", description="Play the next song")
    async def next(self, inter: nextcord.Interaction):
        await inter.response.defer()
        if (not inter.guild.voice_client) and (vc := inter.user.voice):
            await vc.connect()
        elif not ef.check_voice(inter):
            await inter.send(
                embed=ef.cembed(
                    title="Permission Denied",
                    description="You cannot change the song, you need to be in the VC",
                    color=self.CLIENT.color(inter.guild),
                    author=inter.user,
                    thumbnail=self.CLIENT.user.avatar,
                )
            )
            return
        self.datasetup(inter.guild)
        if len(queue := self.CLIENT.queue_song[inter.guild.id]) > (
            self.CLIENT.re[3][inter.guild.id] + 1
        ):
            self.CLIENT.re[3][inter.guild.id] += 1
        info = self.player.info(url=queue[self.CLIENT.re[3][inter.guild.id]])
        embed = ef.cembed(
            title="Playing {}".format(info.get("title")),
            description={
                "Current Index": "{}".format(self.CLIENT.re[3][inter.guild.id]),
                "Duration": self.player.duration(info.get("duration")),
                "Uploader": info.get("uploader"),
                "Likes": f"{info.get('like_count', 0):,}👍",
            },
            color=self.CLIENT.color(inter.guild),
            thumbnail=self.CLIENT.user.avatar,
            author=inter.guild,
        )

        voice = inter.guild.voice_client
        if voice.is_playing():
            voice.stop()
        voice.play(self.player.download(info), after=lambda e: self.after(inter))
        await inter.send(embed=embed)

    @play.subcommand(name="previous", description="Play the previous song")
    async def previous(self, inter: nextcord.Interaction):
        await inter.response.defer()
        if (not inter.guild.voice_client) and (vc := inter.user.voice):
            await vc.connect()
        elif not ef.check_voice(inter):
            await inter.send(
                embed=ef.cembed(
                    title="Permission Denied",
                    description="You cannot change the song, you need to be in the VC",
                    color=self.CLIENT.color(inter.guild),
                    author=inter.user,
                    thumbnail=self.CLIENT.user.avatar,
                )
            )
            return
        self.datasetup(inter.guild)
        if (index := self.CLIENT.re[3][inter.guild.id] - 1) > 0:
            self.CLIENT.re[3][inter.guild.id] -= 1
        info = self.player.info(url=self.CLIENT.queue_song[inter.guild.id][index])
        embed = ef.cembed(
            title="Playing {}".format(info.get("title")),
            description={
                "Current Index": "{}".format(index),
                "Duration": self.player.duration(info.get("duration")),
                "Uploader": info.get("uploader"),
                "Likes": f"{info.get('like_count', 0):,}👍",
            },
            color=self.CLIENT.color(inter.guild),
            thumbnail=self.CLIENT.user.avatar,
            author=inter.guild,
        )

        voice = inter.guild.voice_client
        if voice.is_playing():
            voice.stop()
        voice.play(self.player.download(info), after=lambda e: self.after(inter))
        await inter.send(embed=embed)


def setup(client, **i):
    client.add_cog(Music(client, **i))
