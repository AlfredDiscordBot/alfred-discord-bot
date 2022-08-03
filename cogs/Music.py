import nextcord
import utils.assets as assets
import time
import utils.External_functions as ef
import emoji
import asyncio
import traceback
import re as regex

from nextcord.abc import GuildChannel
from nextcord import Interaction, ChannelType
from nextcord.ext import commands
from utils.spotify_client import fetch_spotify_playlist
from nextcord import SlashOption

# Use nextcord.slash_command() and commands.command()


def requirements():
    return ["DEV_CHANNEL", "FFMPEG_OPTIONS"]


class Music(commands.Cog):
    def __init__(self, CLIENT, DEV_CHANNEL, FFMPEG_OPTIONS):
        self.CLIENT = CLIENT
        self.FFMPEG_OPTIONS = FFMPEG_OPTIONS
        self.DEV_CHANNEL = DEV_CHANNEL

    @nextcord.slash_command(name="music", description="Loop or autoplay")
    async def control(self, inter):
        print(inter.user)

    @control.subcommand(name="autoplay", description="Toggle Autoplay")
    async def autoplay_slash(self, inter):
        await self.autoplay(inter)

    @control.subcommand(name="loop", description="Toggle Loop")
    async def loop_slash(self, inter):
        await self.loop(inter)

    @control.subcommand(name="again", description="Repeat the song")
    async def again_slash(self, inter):
        await inter.response.defer()
        await self.again(inter)

    @control.subcommand(
        name="disconnect", description="Disconnect the bot from your voice channel"
    )
    async def leave_slash(self, inter):
        await self.leave(inter)

    @control.subcommand(
        name="play", description="play a song, you can also put a song name in that"
    )
    async def play_slash(self, inter, index):
        await inter.response.defer()
        await self.play(inter, index=index)

    @control.subcommand(name="connect", description="Connect to a voice channel")
    async def connect_slash(
        self, inter, channel: GuildChannel = ef.defa(ChannelType.voice)
    ):
        await self.connect_music(inter, channel)

    @control.subcommand(name="queue", description="play a song")
    async def queue_slash(self, inter, song: str = None):
        await self.queue(inter, name=song)

    @control.subcommand(
        name="removeduplicates",
        description="removes all the duplicate songs in your queue",
    )
    async def remove_duplicates(self, inter):
        await inter.response.defer()
        self.CLIENT.re[3][inter.guild.id] = 0
        songs = self.CLIENT.queue_song[inter.guild.id]
        for i in songs:
            if self.CLIENT.queue_song[inter.guild.id].count(i) > 1:
                self.CLIENT.queue_song[inter.guild.id].remove(i)
        await inter.send(
            embed=ef.cembed(
                title="Done", description=f"Removed songs", color=self.CLIENT.re[8]
            )
        )

    @control.subcommand(name="lyrics", description="Gets lyrics of a song")
    async def lyrics_slash(self, inter, song):
        await inter.response.defer()
        await self.lyrics(inter, song=song)

    @commands.command()
    @commands.check(ef.check_command)
    async def autoplay(self, ctx):
        user = getattr(ctx, "author", getattr(ctx, "user", None))
        if ctx.guild.voice_client and user.id in [
            i.id for i in ctx.guild.voice_client.channel.members
        ]:
            st = ""
            self.CLIENT.re[7][ctx.guild.id] = (
                self.CLIENT.re[7].get(ctx.guild.id, -1) * -1
            )
            if self.CLIENT.re[7].get(ctx.guild.id, -1) == 1:
                self.CLIENT.re[2][ctx.guild.id] = -1
            if self.CLIENT.re[7][ctx.guild.id] < 0:
                st = "Off"
            else:
                st = "_On_"
            await ctx.send(
                embed=ef.cembed(
                    title="Autoplay",
                    description=st,
                    color=self.CLIENT.re[8],
                    author=user,
                )
            )
        else:
            await ctx.send(
                embed=ef.cembed(
                    title="Permissions Denied",
                    description="You need to be in the voice channel with Alfred to toggle autoplay",
                    color=self.CLIENT.re[8],
                    author=user,
                )
            )

    @commands.command()
    @commands.check(ef.check_command)
    async def loop(self, ctx):
        user = getattr(ctx, "author", getattr(ctx, "user", None))
        if ctx.guild.voice_client and user.id in [
            i.id for i in ctx.guild.voice_client.channel.members
        ]:
            st = ""
            self.CLIENT.re[2][ctx.guild.id] = (
                self.CLIENT.re[2].get(ctx.guild.id, -1) * -1
            )
            if self.CLIENT.re[2].get(ctx.guild.id, 1) == 1:
                self.CLIENT.re[7][ctx.guild.id] = -1
            if self.CLIENT.re[2].get(ctx.guild.id, 1) < 0:
                st = "Off"
            else:
                st = "_On_"
            await ctx.send(
                embed=nextcord.Embed(
                    title="Loop",
                    description=st,
                    color=nextcord.Color(value=self.CLIENT.re[8]),
                )
            )
        else:
            await ctx.send(
                embed=nextcord.Embed(
                    title="Permissions Denied",
                    description="You need to be in the voice channel to toggle loop",
                    color=nextcord.Color(value=self.CLIENT.re[8]),
                )
            )

    @commands.command(aliases=["cq"])
    @commands.check(ef.check_command)
    async def clearqueue(self, ctx):
        if ef.check_voice(ctx):
            if len(self.CLIENT.queue_song.get(ctx.guild.id, [])) > 0:
                self.CLIENT.queue_song[ctx.guild.id].clear()
            self.CLIENT.re[3][ctx.guild.id] = 0
            await ctx.send(
                embed=ef.cembed(
                    title="Cleared queue",
                    description="_Done_",
                    color=self.CLIENT.re[8],
                    thumbnail=self.CLIENT.user.avatar.url,
                )
            )
        else:
            await ctx.send(
                embed=nextcord.Embed(
                    title="Permission denied",
                    description="Join the voice channel to modify queue",
                    color=nextcord.Color(value=self.CLIENT.re[8]),
                )
            )

    @commands.command()
    @commands.check(ef.check_command)
    async def pause(self, ctx):
        self.CLIENT.re[0] += 1
        user = getattr(ctx, "author", getattr(ctx, "user", None))
        mem = (
            [i.id for i in ctx.guild.voice_client.channel.members]
            if ctx.guild.voice_client
            else []
        )
        embed = None
        if mem.count(user.id) > 0:
            voice = nextcord.utils.get(self.CLIENT.voice_clients, guild=ctx.guild)
            voice.pause()
            url = self.CLIENT.queue_song[ctx.guild.id][self.CLIENT.re[3][ctx.guild.id]]
            song = self.CLIENT.da1.get(url, "Unavailable")
            embed = ef.cembed(
                title="Paused",
                description=f"[{song}]({url})",
                color=self.CLIENT.re[8],
                author=user,
            )
        else:
            embed = ef.cembed(
                title="Permission denied",
                description="Join the channel to pause the song",
                color=self.CLIENT.re[8],
                author=user,
            )
        await ef.isReaction(ctx, embed)

    @commands.command(aliases=["dc", "disconnect"])
    @commands.check(ef.check_command)
    async def leave(self, ctx):
        self.CLIENT.re[0] += 1
        mem = (
            [names.id for names in ctx.guild.voice_client.channel.members]
            if ctx.guild.voice_client
            else []
        )
        user = getattr(ctx, "author", getattr(ctx, "user", None))
        if len(mem) == 1 and mem[0] == self.CLIENT.user.id:
            if user.guild_permissions.administrator:
                user = self.CLIENT.user
        if mem.count(user.id) > 0:
            voice = ctx.guild.voice_client
            voice.stop()
            await voice.disconnect()
            embed = ef.cembed(
                title="Disconnected",
                description="Bye, Thank you for using Alfred",
                color=self.CLIENT.re[8],
                author=user,
            )

        else:
            embed = ef.cembed(
                title="Permission denied",
                description="Nice try dude! Join the voice channel",
                color=self.CLIENT.re[8],
                author=user,
            )
        await ef.isReaction(ctx, embed, clear=True)

    @control.subcommand(
        name="playlist",
        description="put queue or playlist and it will add the songs to your playlist to queue or queue to playlist",
    )
    async def addto(
        self,
        inter: Interaction,
        mode=ef.defa(choices=["add to queue", "add to playlist", "show", "clear"]),
        from_user: nextcord.User = None,
    ):
        await inter.response.defer()
        if not from_user:
            from_user = inter.user
        if not (inter.user.voice and inter.guild.voice_client):
            await inter.send("You need to connect to a voice channel")
            return
        if mode == "add to queue":
            if from_user.id in list(self.CLIENT.da.keys()):
                self.CLIENT.queue_song[inter.guild.id] += self.CLIENT.da[from_user.id]
                await inter.send("Added your playlist to queue")
            else:
                await inter.send("You do not have a Playlist")
                return
        if mode == "add to playlist":
            if inter.user.id not in list(self.CLIENT.da.keys()):
                self.CLIENT.da[inter.user.id] = []
            for i in self.CLIENT.queue_song[inter.guild.id]:
                if i not in self.CLIENT.da[inter.user.id]:
                    self.CLIENT.da[inter.user.id].append(i)
            await inter.send(
                "Added songs in queue to playlist\n*Note: The songs are added uniquely, which means that if a song in queue is repeated in your playlist, then that song wont be added*"
            )
        if mode == "clear":
            if self.CLIENT.da.get(inter.user.id):
                confirmation = await ef.wait_for_confirm(
                    inter, self.CLIENT, "Are you sure?", self.CLIENT.re[8]
                )
                if confirmation:
                    del self.CLIENT.da[inter.user.id]
                    await inter.send("Cleared your playlist")
                else:
                    await inter.send("Cancelled")
            else:
                await inter.send("You had no playlist registered")
        if mode == "show":
            l = []
            thumbnail = ef.safe_pfp(from_user)
            songs = self.CLIENT.da.get(from_user.id, [])
            n = 0
            for i in songs:
                n += 1
                if not self.CLIENT.da1.get(i):
                    self.CLIENT.da1[i] = await ef.get_name(i)
                l.append(f"`{n}.` {self.CLIENT.da1.get(i)}\n")

            st = []
            for i in range(len(songs) // 10):
                s = i * 10
                e = i * 10 + 10
                if e > len(l):
                    e = len(l)
                st.append("".join(l[s:e]))

            if st == []:
                if len(l) > 0:
                    st = "".join(l)
                st = ["This person may not have set a playlist yet"]

            embeds = []
            for i in st:
                embed = ef.cembed(
                    title=f"Playlist of {from_user.name}",
                    description=i,
                    color=self.CLIENT.re[8],
                    thumbnail=thumbnail,
                )
                embeds.append(embed)
            await assets.pa(inter, embeds, start_from=0, restricted=True)

    @commands.command(aliases=["cm", "join", "cn", "connect"])
    @commands.check(ef.check_command)
    async def connect_music(self, ctx, channel=None):
        if type(channel) == nextcord.channel.VoiceChannel:
            channel = channel.name
        print("Connect music", str(getattr(ctx, "author", getattr(ctx, "user", None))))
        try:
            self.CLIENT.re[0] += 1
            user = getattr(ctx, "author", getattr(ctx, "user", None))
            if not ctx.guild.id in self.CLIENT.queue_song:
                self.CLIENT.queue_song[ctx.guild.id] = []
            if not ctx.guild.id in self.CLIENT.re[3]:
                self.CLIENT.re[3][ctx.guild.id] = 0
            if channel == None:
                if user.voice and user.voice.channel:
                    voiceChannel = user.voice.channel
                    await voiceChannel.connect()
                    await ctx.send(
                        embed=ef.cembed(
                            description="Connected\nBitrate of the channel: "
                            + str(ctx.guild.voice_client.channel.bitrate // 1000),
                            color=self.CLIENT.re[8],
                        )
                    )
                else:
                    emo = assets.Emotes(self.CLIENT)
                    await ctx.send(
                        embed=nextcord.Embed(
                            description=f"You are not in a voice channel {emo.join_vc}",
                            color=nextcord.Color(value=self.CLIENT.re[8]),
                        )
                    )
            else:
                if channel in [i.name for i in ctx.guild.voice_channels]:
                    voiceChannel = nextcord.utils.get(
                        ctx.guild.voice_channels, name=channel
                    )
                    await voiceChannel.connect()
                    await ctx.send(
                        embed=ef.cembed(
                            title="Connected",
                            description=f"Connected to {voiceChannel.name} \nBitrate of the channel: "
                            + str(ctx.guild.voice_client.channel.bitrate // 1000),
                            color=nextcord.Color(value=self.CLIENT.re[8]),
                        )
                    )
                else:
                    await ctx.send(
                        embed=ef.cembed(
                            description="The voice channel does not exist",
                            color=nextcord.Color(value=self.CLIENT.re[8]),
                        )
                    )

        except Exception as e:
            await ctx.send(
                embed=nextcord.Embed(
                    title="Hmm",
                    description=str(e),
                    color=nextcord.Color(value=self.CLIENT.re[8]),
                )
            )
            channel = self.CLIENT.get_channel(self.DEV_CHANNEL)
            await channel.send(
                embed=ef.cembed(
                    title="Connect music",
                    description=traceback.format_exc(),
                    footer=f"{getattr(ctx, 'author', getattr(ctx, 'user', None)).name}: {ctx.guild}",
                    color=self.CLIENT.re[8],
                )
            )

    @commands.command(aliases=["s_q"])
    @commands.check(ef.check_command)
    async def search_queue(self, ctx, part):
        st = ""
        index = 0
        found_songs = 0
        for i in self.CLIENT.queue_song[ctx.guild.id]:
            if i in self.CLIENT.da1:
                found_songs += 1
                if self.CLIENT.da1[i].lower().find(part.lower()) != -1:
                    st += str(index) + ". " + self.CLIENT.da1[i] + "\n"
            index += 1
        if st == "":
            st = "Not found"
        if len(self.CLIENT.queue_song[ctx.guild.id]) - found_songs > 0:
            st += "\n\nWARNING: Some song names may not be loaded properly, this search may not be accurate"
            st += "\nSongs not found: " + str(
                len(self.CLIENT.queue_song[ctx.guild.id]) - found_songs
            )
        await ctx.send(
            embed=ef.cembed(
                title="Songs in queue",
                description=st,
                color=self.CLIENT.re[8],
                thumbnail=self.CLIENT.user.avatar.url,
            )
        )

    @commands.command(aliases=["q"])
    @commands.check(ef.check_command)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def queue(self, ctx, *, name=""):
        self.CLIENT.re[0] += 1
        st = ""
        num = 0
        if ef.check_voice(ctx) and name != "":
            if "spotify" in name:
                if "playlist" in name:
                    await ctx.send("Enqueued the given Spotify playlist.")
                    try:
                        songs = await fetch_spotify_playlist(name, 500)
                        for song in songs:
                            try:
                                name = ef.convert_to_url(song)
                                sear = (
                                    "https://www.youtube.com/results?search_query="
                                    + name
                                )
                                htm = await ef.get_async(sear)
                                video = regex.findall(r"watch\?v=(\S{11})", htm)
                                url = "https://www.youtube.com/watch?v=" + video[0]
                                st = ""
                                num = 0
                                if url not in self.CLIENT.da1:
                                    name_of_the_song = await ef.get_name(url)
                                    self.CLIENT.da1[url] = name_of_the_song
                                self.CLIENT.queue_song[ctx.guild.id].append(url)
                            except Exception as e:
                                print(e)
                                break
                    except Exception as e:
                        print(e)
                elif "track" in name:
                    name = ef.convert_to_url(name)
                    sear = "https://www.youtube.com/results?search_query=" + name
                    htm = await ef.get_async(sear)
                    video = regex.findall(r"watch\?v=(\S{11})", htm)
                    url = "https://www.youtube.com/watch?v=" + video[0]
                    st = ""
                    num = 0
                    if url not in self.CLIENT.da1:
                        name_of_the_song = await ef.get_name(url)
                        print(name_of_the_song, ":", url)
                        self.CLIENT.da1[url] = name_of_the_song
                    self.CLIENT.queue_song[ctx.guild.id].append(url)
            else:
                name = ef.convert_to_url(name)
                sear = "https://www.youtube.com/results?search_query=" + name
                htm = await ef.get_async(sear)
                video = regex.findall(r"watch\?v=(\S{11})", htm)
                url = "https://www.youtube.com/watch?v=" + video[0]

                st = ""
                await ctx.send("Added to queue")
                num = 0
                if url not in self.CLIENT.da1:
                    name_of_the_song = await ef.get_name(url)
                    self.CLIENT.da1[url] = name_of_the_song
                self.CLIENT.queue_song[ctx.guild.id].append(url)

            for i in self.CLIENT.queue_song[ctx.guild.id]:
                if num >= len(self.CLIENT.queue_song[ctx.guild.id]) - 10:
                    if not i in self.CLIENT.da1.keys():
                        self.CLIENT.da1[i] = await ef.get_name(i)
                    st = (
                        st
                        + str(num)
                        + ". "
                        + self.CLIENT.da1[i].replace("&quot", "'")
                        + "\n"
                    )
                num += 1
            # st=st+str(num)+". "+da1[i]+"\n"
            if st == "":
                st = "_Empty_"
            em = nextcord.Embed(
                title="Queue",
                description=st,
                color=nextcord.Color(value=self.CLIENT.re[8]),
            )
            mess = await ctx.send(embed=em)
            if type(ctx) == nextcord.Interaction:
                mess = await ctx.original_message()
            await self.player_pages(mess)
        elif not name:
            num = 0
            st = ""
            if ctx.guild.id not in self.CLIENT.queue_song:
                await ctx.send(
                    embed=ef.cembed(
                        title="Empty",
                        description="Empty queue, add a song to the queue using 'q command",
                        color=self.CLIENT.re[8],
                        footer="You can also use play command",
                    )
                )
                return
            if len(self.CLIENT.queue_song[ctx.guild.id]) < 30:
                for i in self.CLIENT.queue_song[ctx.guild.id]:
                    if not i in self.CLIENT.da1:
                        self.CLIENT.da1[i] = ef.youtube_info(i)["title"]
                    st += f"`{num}.` {self.CLIENT.da1[i]}\n"
                    num += 1
            else:
                num = self.CLIENT.re[3].get(ctx.guild.id, 10)
                if num < 10:
                    num = 10
                for i in range(num - 10, num + 10):
                    try:
                        st += f"`{i}.` {self.CLIENT.da1.get(self.CLIENT.queue_song[ctx.guild.id][i],'Unavailable')}\n"
                    except:
                        pass
            embed = ef.cembed(
                title="Queue",
                description=st if st != "" else "Empty",
                color=self.CLIENT.re[8],
                thumbnail=self.CLIENT.user.avatar.url,
            )
            mess = await ctx.send(embed=embed)
            if isinstance(ctx, nextcord.Interaction):
                mess = await ctx.original_message()
            await self.player_pages(mess)
        else:
            await ctx.send(
                embed=ef.cembed(
                    title="Permission denied",
                    description="Join the voice channel to modify queue",
                    color=self.CLIENT.re[8],
                    author=getattr(ctx, "author", getattr(ctx, "user", None)),
                )
            )

    @commands.command()
    @commands.check(ef.check_command)
    async def again(self, ctx):
        self.CLIENT.re[0] += 1
        user = getattr(ctx, "author", getattr(ctx, "user", None))
        if user.voice and user.voice.channel:
            if not ctx.guild.id in self.CLIENT.queue_song:
                self.CLIENT.queue_song[ctx.guild.id] = []
            if not ctx.guild.id in self.CLIENT.re[3]:
                self.CLIENT.re[3][ctx.guild.id] = 0

            if ctx.guild.voice_client == None:
                voiceChannel = user.voice.channel
                await voiceChannel.connect()
            mem = []
            try:
                if ef.check_voice(ctx):
                    voice = ctx.guild.voice_client
                    bitrate = "\nBitrate of the channel: " + str(
                        voice.channel.bitrate // 1000
                    )
                    song = self.CLIENT.queue_song[ctx.guild.id][
                        self.CLIENT.re[3][ctx.guild.id]
                    ]
                    if song not in self.CLIENT.da1:
                        self.CLIENT.da1[song] = ef.youtube_info(song)["title"]
                    URL = ef.youtube_download(song)
                    voice.stop()
                    voice.play(
                        nextcord.FFmpegPCMAudio(URL, **self.FFMPEG_OPTIONS),
                        after=lambda e: self.repeat(ctx, voice),
                    )
                    embed = ef.cembed(
                        title="Playing",
                        description=self.CLIENT.da1[song] + bitrate,
                        color=self.CLIENT.re[8],
                        thumbnail=self.CLIENT.user.avatar.url,
                    )
                    if isinstance(ctx, nextcord.Message):
                        mess = await ctx.channel.send(embed=embed)
                        await self.player_pages(mess)
                    else:
                        await ef.isReaction(ctx, embed)
                else:
                    emo = assets.Emotes(self.CLIENT)
                    embed = ef.cembed(
                        title="Permission denied",
                        description=f"{emo.animated_wrong} Join the voice channel to play the song",
                        color=self.CLIENT.re[8],
                        thumbnail=self.CLIENT.user.avatar.url,
                    )
            except Exception as e:
                channel = self.CLIENT.get_channel(self.DEV_CHANNEL)
                await ctx.channel.send(
                    embed=ef.cembed(
                        title="Error",
                        description=str(e),
                        color=self.CLIENT.re[8],
                        thumbnail=self.CLIENT.user.avatar.url,
                    )
                )
                await channel.send(
                    embed=nextcord.Embed(
                        title="Error in play function",
                        description=f"{e}\n{ctx.guild.name}: {ctx.channel.name}",
                        color=nextcord.Color(value=self.CLIENT.re[8]),
                    )
                )

    @commands.command(aliases=["<"])
    @commands.check(ef.check_command)
    async def previous(self, ctx):
        self.CLIENT.re[0] += 1
        try:
            if ef.check_voice(ctx):
                self.CLIENT.re[3][ctx.guild.id] -= 1
                if self.CLIENT.re[3][ctx.guild.id] == -1:
                    self.CLIENT.re[3][ctx.guild.id] = (
                        len(self.CLIENT.queue_song.get(ctx.guild.id, [])) - 1
                    )
                song = self.CLIENT.queue_song[ctx.guild.id][
                    self.CLIENT.re[3][ctx.guild.id]
                ]
                voice = nextcord.utils.get(self.CLIENT.voice_clients, guild=ctx.guild)
                URL, name = ef.youtube_download1(song)
                self.CLIENT.da1[song] = name
                embed = nextcord.Embed(
                    title="Playing",
                    description=self.CLIENT.da1[song],
                    color=nextcord.Color(value=self.CLIENT.re[8]),
                )
                voice.stop()
                voice.play(
                    nextcord.FFmpegPCMAudio(URL, **self.FFMPEG_OPTIONS),
                    after=lambda e: self.repeat(ctx, voice),
                )
            else:
                embed = nextcord.Embed(
                    title="Permission denied",
                    description="Join the voice channel to move to the previous song",
                    color=nextcord.Color(value=self.CLIENT.re[8]),
                )
            await ef.isReaction(ctx, embed)
        except Exception as e:
            channel = self.CLIENT.get_channel(self.DEV_CHANNEL)
            await channel.send(
                embed=ef.cembed(
                    title="Error in previous function",
                    description=str(e),
                    color=nextcord.Color(value=self.CLIENT.re[8]),
                    footer=f"{ctx.author.name}: {ctx.guild.name}",
                )
            )

    async def player_pages(self, mess):
        await ef.player_reaction(mess)
        emojis = emoji.emojize(":upwards_button:"), emoji.emojize(":downwards_button:")

        def check(reaction, user):
            return (
                user.id != self.CLIENT.user.id
                and str(reaction.emoji) in emojis
                and reaction.message.id == mess.id
            )

        page = self.CLIENT.re[3][mess.guild.id] // 10
        while True:
            songs = self.CLIENT.queue_song[mess.guild.id]
            try:
                reaction, user = await self.CLIENT.wait_for(
                    "reaction_add", check=check, timeout=None
                )
                if reaction.emoji == emojis[0] and page > 0:
                    page -= 1
                elif reaction.emoji == emojis[1] and page <= len(songs) // 10:
                    page += 1
                cu = page * 10
                st = ""
                for i in range(cu, cu + 10):
                    if len(songs) > i:
                        if not self.CLIENT.da1.get(songs[i]):
                            self.CLIENT.da1[songs[i]] = await ef.get_name(songs[i])
                        st += f"`{i}.` {self.CLIENT.da1.get(songs[i],'Unavailable')}\n"
                await mess.edit(
                    embed=ef.cembed(
                        title="Queue",
                        description=st,
                        color=self.CLIENT.re[8],
                        footer="Amazing songs btw, keep going"
                        if len(songs) != 0
                        else "Use queue to add some songs",
                    )
                )
                await reaction.remove(user)
            except asyncio.TimeoutError:
                await mess.clear_reactions()

    @commands.command()
    @commands.check(ef.check_command)
    async def stop(self, ctx):
        self.CLIENT.re[0] += 1
        if ef.check_voice(ctx):
            voice = nextcord.utils.get(self.CLIENT.voice_clients, guild=ctx.guild)
            voice.stop()
            await ctx.send(embed=ef.cembed(title="Stop", color=self.CLIENT.re[8]))
        else:
            await ctx.send(
                embed=ef.cembed(
                    title="Permission denied",
                    description="Join the channel to stop the song",
                    color=self.CLIENT.re[8],
                )
            )

    @commands.command()
    @commands.check(ef.check_command)
    async def resume(self, ctx):
        self.CLIENT.re[0] += 1
        if ef.check_voice(ctx):
            voice = nextcord.utils.get(self.CLIENT.voice_clients, guild=ctx.guild)
            voice.resume()
            url = self.CLIENT.queue_song[ctx.guild.id][self.CLIENT.re[3][ctx.guild.id]]
            song_name = self.CLIENT.da1[url]
            embed = nextcord.Embed(
                title="Playing",
                description=f"[{song_name}]({url})",
                color=nextcord.Color(value=self.CLIENT.re[8]),
            )

        else:
            embed = ef.cembed(
                title="Permissions Denied",
                description="You need to be in the voice channel to resume this",
                color=self.CLIENT.re[8],
            )
        await ef.isReaction(ctx, embed)

    def repeat(self, ctx, voice):
        songs = self.CLIENT.queue_song.get(ctx.guild.id, [])
        if len(songs) == 0:
            return
        index = self.CLIENT.re[3].get(ctx.guild.id, 0)
        if len(songs) < index:
            index = 0
            self.CLIENT.re[3][ctx.guild.id] = index
        time.sleep(1)
        if self.CLIENT.re[7].get(ctx.guild.id, -1) == 1 and not voice.is_playing():
            self.CLIENT.re[3][ctx.guild.id] += 1
            index = self.CLIENT.re[3].get(ctx.guild.id, 0)
            if self.CLIENT.re[3][ctx.guild.id] >= len(
                self.CLIENT.queue_song[ctx.guild.id]
            ):
                self.CLIENT.re[3][ctx.guild.id] = 0
        if (
            self.CLIENT.re[2].get(ctx.guild.id, -1) == 1
            or self.CLIENT.re[7].get(ctx.guild.id, -1) == 1
        ):
            if not voice.is_playing():
                URL, name = ef.youtube_download1(songs[index])
                if not songs[index] in self.CLIENT.da1:
                    self.CLIENT.da1[songs[index]] = name
                voice.play(
                    nextcord.FFmpegPCMAudio(URL, **self.FFMPEG_OPTIONS),
                    after=lambda e: self.repeat(ctx, voice),
                )

    @commands.command()
    @commands.check(ef.check_command)
    async def lyrics(self, ctx, *, song):
        embed = await ef.ly(song, self.CLIENT.re)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.check(ef.check_command)
    async def remove(self, ctx, index):
        if not ef.check_voice(ctx):
            await ctx.send(
                embed=ef.cembed(
                    title="Permissions Denied",
                    description=f"Join the voice channel to modify queue{assets.Emotes(self.CLIENT).animated_wrong}",
                    color=self.CLIENT.re[8],
                    thumbnail=self.CLIENT.user.avatar.url,
                )
            )
            return
        if self.CLIENT.queue_song.get(ctx.guild.id):
            if len(self.CLIENT.queue_song[ctx.guild.id]) < index:
                a = self.CLIENT.queue_song[ctx.guild.id].pop(index)
                await ctx.send(
                    embed=ef.cembed(
                        title="Removed",
                        description=f"Removed {self.CLIENT.da1.get(a, 'Unavailable')}",
                        color=self.CLIENT.re[8],
                        thumbnail=self.CLIENT.user.avatar.url,
                    )
                )
            else:
                await ctx.send(
                    embed=ef.cembed(
                        title="Couldn't remove",
                        description=f"The list has only {len(self.CLIENT.queue_song[ctx.guild.id])-1}",
                        color=self.CLIENT.re[8],
                    )
                )
        else:
            await ctx.send(
                embed=ef.cembed(
                    title="Empty",
                    description="Your Queue is Empty",
                    color=self.CLIENT.re[8],
                )
            )

    @commands.command(aliases=["p"])
    @commands.check(ef.check_command)
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def play(self, ctx, *, index):
        ind = index
        user = getattr(ctx, "author", getattr(ctx, "user", None))
        self.CLIENT.re[0] += 1
        if ctx.guild.voice_client == None and user.voice and user.voice.channel:
            if not ctx.guild.id in self.CLIENT.queue_song:
                self.CLIENT.queue_song[ctx.guild.id] = []
            if not ctx.guild.id in self.CLIENT.re[3]:
                self.CLIENT.re[3][ctx.guild.id] = 0
            channel = user.voice.channel.id
            voiceChannel = nextcord.utils.get(ctx.guild.voice_channels, id=channel)
            await voiceChannel.connect()
        try:
            if ef.check_voice(ctx):
                voice = nextcord.utils.get(self.CLIENT.voice_clients, guild=ctx.guild)
                if ind.isnumeric():
                    if int(ind) <= len(self.CLIENT.queue_song[ctx.guild.id]):
                        self.CLIENT.re[3][ctx.guild.id] = int(ind)
                        index = self.CLIENT.re[3][ctx.guild.id]
                        songs = self.CLIENT.queue_song[ctx.guild.id]
                        song = songs[index]
                        URL, name_of_the_song = ef.youtube_download1(song)
                        self.CLIENT.da1[song] = name_of_the_song
                        mess = await ctx.send(
                            embed=nextcord.Embed(
                                title="Playing",
                                description=self.CLIENT.da1[song],
                                color=nextcord.Color(self.CLIENT.re[8]),
                            )
                        )
                        voice.stop()
                        voice.play(
                            nextcord.FFmpegPCMAudio(URL, **self.FFMPEG_OPTIONS),
                            after=lambda e: self.repeat(ctx, voice),
                        )
                        await self.player_pages(mess)
                    else:
                        songs = self.CLIENT.queue_song[ctx.guild.id]
                        embed = nextcord.Embed(
                            title="Hmm",
                            description=f"There are only {len(songs)} songs",
                            color=nextcord.Color(self.CLIENT.re[8]),
                        )
                        await ctx.send(embed=embed)
                else:
                    name = ind
                    name = ef.convert_to_url(name)
                    htm = await ef.get_async(
                        "https://www.youtube.com/results?search_query=" + name
                    )
                    video = regex.findall(r"watch\?v=(\S{11})", htm)
                    if len(video) == 0:
                        await ctx.send(
                            embed=ef.cembed(
                                description="We couldnt find the song, please try it with a different name, shorter name is prefered",
                                color=self.CLIENT.re[8],
                            )
                        )
                        return
                    url = "https://www.youtube.com/watch?v=" + video[0]
                    URL, name_of_the_song = ef.youtube_download1(url)
                    self.CLIENT.re[3][ctx.guild.id] = len(
                        self.CLIENT.queue_song[ctx.guild.id]
                    )
                    songs = self.CLIENT.queue_song[ctx.guild.id]
                    if len(songs) == 0 or songs[-1] != url:
                        self.CLIENT.queue_song[ctx.guild.id].append(url)
                    self.CLIENT.da1[url] = name_of_the_song
                    voice.stop()
                    voice.play(
                        nextcord.FFmpegPCMAudio(URL, **self.FFMPEG_OPTIONS),
                        after=lambda e: self.repeat(ctx, voice),
                    )
                    await ctx.send(
                        embed=nextcord.Embed(
                            title="Playing",
                            description=name_of_the_song,
                            color=nextcord.Color(value=self.CLIENT.re[8]),
                        )
                    )

            else:
                await ctx.send(
                    embed=nextcord.Embed(
                        title="Permission denied",
                        description="Join the voice channel to play the song",
                        color=nextcord.Color(value=self.CLIENT.re[8]),
                    )
                )
        except Exception as e:
            channel = self.CLIENT.get_channel(self.DEV_CHANNEL)
            await ctx.send(
                embed=nextcord.Embed(
                    title="Error in play function",
                    description=f"{e}",
                    color=nextcord.Color(value=self.CLIENT.re[8]),
                )
            )
            await channel.send(
                embed=nextcord.Embed(
                    title="Error in play function",
                    description=f"{traceback.format_exc()}\n{ctx.guild.name}: {ctx.channel.name}",
                    color=nextcord.Color(value=self.CLIENT.re[8]),
                )
            )

    @commands.command(aliases=["curr"])
    @commands.check(ef.check_command)
    async def currentmusic(self, ctx):
        self.CLIENT.re[0] += 1
        if len(self.CLIENT.queue_song[ctx.guild.id]) > 0:
            songs = self.CLIENT.queue_song[ctx.guild.id]
            index = self.CLIENT.re[3][ctx.guild.id]
            description = f"[Current index: {index}]({songs[index]})\n"
            info = ef.youtube_info(songs[index])
            check = "\n\nDescription: \n" + info["description"] + "\n"
            if len(check) < 3000 and len(check) > 0:
                description += check
            description += (
                f"\nDuration: {str(info['duration'] // 60)}min {info['duration'] % 60}sec"
                + f"\n\n{info['view_count']} views\n{info['like_count']} :thumbsup:\n"
            )
            embed = ef.cembed(
                title=self.CLIENT.da1[songs[index]],
                description=description,
                color=self.CLIENT.re[8],
                thumbnail=info["thumbnail"],
            )
            await ef.isReaction(ctx, embed)
        else:
            embed = ef.cembed(
                title="Empty queue",
                description="Your queue is currently empty",
                color=self.CLIENT.re[8],
                footer="check 'q if you have any song",
            )
            await ef.isReaction(ctx, embed)

    @commands.command(aliases=[">", "skip"])
    @commands.check(ef.check_command)
    async def next(self, ctx):
        self.CLIENT.re[0] += 1
        try:
            if ef.check_voice(ctx):
                self.CLIENT.re[3][ctx.guild.id] += 1
                if self.CLIENT.re[3][ctx.guild.id] >= len(
                    self.CLIENT.queue_song[ctx.guild.id]
                ):
                    self.CLIENT.re[3][ctx.guild.id] = (
                        len(self.CLIENT.queue_song[ctx.guild.id]) - 1
                    )
                    await ctx.send(
                        embed=ef.cembed(
                            title="Last song",
                            description="Only "
                            + str(len(self.CLIENT.queue_song[ctx.guild.id]))
                            + " songs in your queue",
                            color=self.CLIENT.re[8],
                        )
                    )
                song = self.CLIENT.queue_song[ctx.guild.id][
                    self.CLIENT.re[3][ctx.guild.id]
                ]
                voice = nextcord.utils.get(self.CLIENT.voice_clients, guild=ctx.guild)
                URL = ef.youtube_download(song)
                embed = ef.cembed(
                    title="Playing",
                    description=self.CLIENT.da1.get(song, "Unavailable"),
                    color=self.CLIENT.re[8],
                )
                await ef.isReaction(ctx, embed)
                voice.stop()
                voice.play(
                    nextcord.FFmpegPCMAudio(URL, **self.FFMPEG_OPTIONS),
                    after=lambda e: self.repeat(ctx, voice),
                )
            else:
                embed = nextcord.Embed(
                    title="Permission denied",
                    description="Join the voice channel to move to the next song",
                    color=nextcord.Color(value=self.CLIENT.re[8]),
                )
                await ef.isReaction(ctx, embed)
        except Exception as e:
            channel = self.CLIENT.get_channel(self.DEV_CHANNEL)
            await channel.send(
                embed=ef.cembed(
                    title="Error in next function",
                    description=traceback.format_exc(),
                    footer=f"{ctx.channel.name}:{ctx.guild.name}",
                    color=self.CLIENT.re[8],
                )
            )

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user.bot:
            return
        if reaction.emoji == "⏸":
            if (
                str(user) != str(self.CLIENT.user)
                and reaction.message.author == self.CLIENT.user
            ):
                await reaction.remove(user)
                self.CLIENT.re[0] += 1
                reaction.message.author = user
                await self.pause(reaction.message)
        if reaction.emoji == "⏹":
            if (
                str(user) != str(self.CLIENT.user)
                and reaction.message.author == self.CLIENT.user
            ):
                await reaction.remove(user)
                reaction.message.author = user
                await self.leave(reaction.message)
        if reaction.emoji == "🔁":
            if (
                str(user) != str(self.CLIENT.user)
                and reaction.message.author == self.CLIENT.user
            ):
                try:
                    await reaction.remove(user)
                except:
                    pass
                reaction.message.author = user
                await self.again(reaction.message)

        if reaction.emoji == "⏮":
            if (
                str(user) != str(self.CLIENT.user)
                and reaction.message.author == self.CLIENT.user
            ):
                try:
                    await reaction.remove(user)
                except:
                    pass
                reaction.message.author = user
                await self.previous(reaction.message)
        if reaction.emoji == "⏭":
            if (
                str(user) != str(self.CLIENT.user)
                and reaction.message.author == self.CLIENT.user
            ):
                try:
                    await reaction.remove(user)
                except:
                    pass
                reaction.message.author = user
                await self.next(reaction.message)
        if reaction.emoji == "▶":
            if (
                str(user) != str(self.CLIENT.user)
                and reaction.message.author == self.CLIENT.user
            ):
                try:
                    await reaction.remove(user)
                except:
                    pass
                reaction.message.author = user
                await self.resume(reaction.message)
        if reaction.emoji == emoji.emojize(":musical_note:"):
            await self.currentmusic(reaction.message)
            await reaction.remove(user)

        if (
            reaction.emoji == emoji.emojize(":keycap_*:")
            and reaction.message.author == self.CLIENT.user
        ):
            ctx = reaction.message
            try:
                await reaction.remove(user)
            except:
                pass
            st = ""
            index = self.CLIENT.re[3][ctx.guild.id]
            songs = self.CLIENT.queue_song[ctx.guild.id]
            lower = 0 if index - 10 < 0 else index - 10
            higher = len(songs) if index + 10 > len(songs) else index + 10
            length = f"Length of queue: {len(songs)}\n"
            if ctx.guild.voice_client:
                bitrate = f"\n\nBitrate of the channel {reaction.message.guild.voice_client.channel.bitrate//1000}kbps\n"
                latency = f"Latency: {int(reaction.message.guild.voice_client.latency*1000)}ms"
            else:
                bitrate = "Not Connected\n"
                latency = ""

            for i in range(lower, higher):
                song = f"{i}. {self.CLIENT.da1[songs[i]]}"
                if i == index:
                    song = f"*{song}*"
                st = f"{st}{song}\n"
            await reaction.message.edit(
                embed=nextcord.Embed(
                    title="Queue",
                    description=st + bitrate + length + latency,
                    color=nextcord.Color(value=self.CLIENT.re[8]),
                )
            )


def setup(CLIENT, **i):
    CLIENT.add_cog(Music(CLIENT, **i))
