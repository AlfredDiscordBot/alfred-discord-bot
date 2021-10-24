from discord.ext import commands


class Music(commands.cog):
    def __init__(self, bot):
        self.bot = bot


@slash.slash(name="connect", description="Connect to a voice channel")
async def connect_slash(ctx, channel=""):
    req()
    await ctx.defer()
    await connect_music(ctx, channel)


@client.command(aliases=["cm"])
async def connect_music(ctx, channel=""):
    print("Connect music", str(ctx.author))
    try:
        req()
        if not str(ctx.guild.id) in queue_song:
            queue_song[str(ctx.guild.id)] = []
        if not str(ctx.guild.id) in re[3]:
            re[3][str(ctx.guild.id)] = 0
        if channel == "":
            if ctx.author.voice and ctx.author.voice.channel:
                channel = ctx.author.voice.channel.id
                vc_channel[str(ctx.guild.id)] = channel
                voiceChannel = discord.utils.get(ctx.guild.voice_channels, id=channel)
                await voiceChannel.connect()
                voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
                await ctx.send(
                    embed=discord.Embed(
                        title="",
                        description="Connected\nBitrate of the channel: "
                                    + str(ctx.voice_client.channel.bitrate // 1000),
                        color=discord.Color(value=re[8]),
                    )
                )
            else:
                await ctx.send(
                    embed=discord.Embed(
                        title="",
                        description="You are not in a voice channel",
                        color=discord.Color(value=re[8]),
                    )
                )
        else:
            if channel in [i.name for i in ctx.guild.voice_channels]:
                voiceChannel = discord.utils.get(ctx.guild.voice_channels, name=channel)
                vc_channel[str(ctx.guild.id)] = voiceChannel.id
                await voiceChannel.connect()
                voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
                await ctx.send(
                    embed=discord.Embed(
                        title="",
                        description="Connected\nBitrate of the channel: "
                                    + str(ctx.voice_client.channel.bitrate // 1000),
                        color=discord.Color(value=re[8]),
                    )
                )
            else:
                await ctx.send(
                    embed=discord.Embed(
                        title="",
                        description="The voice channel does not exist",
                        color=discord.Color(value=re[8]),
                    )
                )

    except Exception as e:
        await ctx.send(
            embed=discord.Embed(
                title="Hmm", description=str(e), color=discord.Color(value=re[8])
            )
        )
        channel = client.get_channel(dev_channel)
        await channel.send(
            embed=discord.Embed(
                title="Connect music",
                description=str(e)
                            + "\n"
                            + str(ctx.guild.name)
                            + ": "
                            + str(ctx.channel.name),
                color=discord.Color(value=re[8]),
            )
        )


@client.command()
async def addto(ctx, mode, *, text):
    req()
    present = 1
    voiceChannel = discord.utils.get(
        ctx.guild.voice_channels, id=vc_channel[str(ctx.guild.id)]
    )
    member = voiceChannel.members
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


@client.command(aliases=["cq"])
async def clearqueue(ctx):
    req()
    mem = [
        (str(i.name) + "#" + str(i.discriminator))
        for i in discord.utils.get(
            ctx.guild.voice_channels, id=vc_channel[str(ctx.guild.id)]
        ).members
    ]
    if mem.count(str(ctx.author)) > 0:
        if len(queue_song[str(ctx.guild.id)]) > 0:
            queue_song[str(ctx.guild.id)].clear()
        re[3][str(ctx.guild.id)] = 0
        await ctx.send(
            embed=discord.Embed(
                title="Cleared queue",
                description="_Done_",
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


@client.command()
async def remove(ctx, n):
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


@client.command(aliases=["curr"])
async def currentmusic(ctx):
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
        if len(check) < 3000 and len(check) > 0:
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


def repeat(ctx, voice):
    req()
    if not queue_song[str(ctx.guild.id)][re[3][str(ctx.guild.id)]] in da1.keys():
        aa = str(
            urllib.request.urlopen(
                queue_song[str(ctx.guild.id)][re[3][str(ctx.guild.id)]]
            )
                .read()
                .decode()
        )
        starting = aa.find("<title>") + len("<title>")
        ending = aa.find("</title>")
        da1[queue_song[str(ctx.guild.id)][re[3][str(ctx.guild.id)]]] = (
            aa[starting:ending]
                .replace("&#39;", "'")
                .replace(" - YouTube", "")
                .replace("&amp;", "&")
        )
    time.sleep(1)
    if re[7].get(ctx.guild.id, -1) == 1 and not voice.is_playing():
        re[3][str(ctx.guild.id)] += 1
        if re[3][str(ctx.guild.id)] >= len(queue_song[str(ctx.guild.id)]):
            re[3][str(ctx.guild.id)] = 0
    if re[2].get(ctx.guild.id, -1) == 1 or re[7].get(ctx.guild.id, -1) == 1:
        if not voice.is_playing():
            URL = youtube_download(
                ctx, queue_song[str(ctx.guild.id)][re[3][str(ctx.guild.id)]]
            )
            voice.play(
                discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS),
                after=lambda e: repeat(ctx, voice),
            )


@slash.slash(
    name="autoplay",
    description="Plays the next song automatically if its turned on",
)
async def autoplay_slash(ctx):
    req()
    await ctx.defer()
    await autoplay(ctx)


@slash.slash(name="loop", description="Loops the same song")
async def loop_slash(ctx):
    await ctx.defer()
    req()
    await loop(ctx)


@client.command()
async def show_playlist(ctx, *, name):
    num = 0
    embeds = []
    if name in list(da.keys()):
        st = ""
        for i in da[name]:
            num += 1
            if i in da1:
                st += str(num) + ". " + str(da1[i]) + "\n"
            if num % 10 == 0 and num != 0:
                embeds.append(
                    cembed(
                        title="Playlist",
                        description=st,
                        color=re[8],
                        thumbnail=client.user.avatar_url_as(format="png"),
                    )
                )
                st = ""
        if len(da) < 10:
            embeds.append(
                cembed(
                    title="Playlist",
                    description=st,
                    color=re[8],
                    thumbnail=client.user.avatar_url_as(format="png"),
                )
            )
        await pa(embeds, ctx)
    else:
        await ctx.send(
            embed=cembed(
                title="Playlist",
                description="This playlist is not found",
                color=re[8],
                thumbnail=client.user.avatar_url_as(format="png"),
            )
        )


@client.command()
async def autoplay(ctx):
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


@client.command()
async def loop(ctx):
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


@client.command(aliases=["q"])
async def queue(ctx, *, name=""):
    req()
    try:
        mem = [str(names) for names in ctx.voice_client.channel.members]
    except:
        mem = []
    if mem.count(str(ctx.author)) > 0 and name != "":
        if 'spotify' in name:
            if 'playlist' in name:
                await ctx.send('Enqueued the given Spotify playlist.')
                try:
                    for song in fetch_spotify_playlist(name, 500):
                        try:
                            name = convert_to_url(song)
                            sear = "https://www.youtube.com/results?search_query=" + name
                            htm = urllib.request.urlopen(sear)
                            video = regex.findall(r"watch\?v=(\S{11})", htm.read().decode())
                            url = "https://www.youtube.com/watch?v=" + video[0]
                            st = ""
                            num = 0
                            name_of_the_song = await get_name(url)
                            print(name_of_the_song, ":", url)
                            da1[url] = name_of_the_song
                            queue_song[str(ctx.guild.id)].append(url)
                        except:
                            pass
                except:
                    pass
            elif 'track' in name:
                name = spotify.spotify_track(name)
                name = convert_to_url(name)
                sear = "https://www.youtube.com/results?search_query=" + name
                htm = urllib.request.urlopen(sear)
                video = regex.findall(r"watch\?v=(\S{11})", htm.read().decode())
                url = "https://www.youtube.com/watch?v=" + video[0]
                st = ""
                num = 0
                name_of_the_song = await get_name(url)
                print(name_of_the_song, ":", url)
                da1[url] = name_of_the_song
                queue_song[str(ctx.guild.id)].append(url)
        else:
            name = convert_to_url(name)
            sear = "https://www.youtube.com/results?search_query=" + name
            htm = urllib.request.urlopen(sear)
            video = regex.findall(r"watch\?v=(\S{11})", htm.read().decode())
            url = "https://www.youtube.com/watch?v=" + video[0]

            st = ""
            await ctx.send("Added to queue")
            num = 0
            name_of_the_song = await get_name(url)
            print(name_of_the_song, ":", url)
            da1[url] = name_of_the_song
            queue_song[str(ctx.guild.id)].append(url)
        for i in queue_song[str(ctx.guild.id)]:
            if num >= len(queue_song[str(ctx.guild.id)]) - 10:
                if not i in da1.keys():
                    da1[i] = await get_name(i)
                st = st + str(num) + ". " + da1[i].replace("&quot", "'") + "\n"
            num += 1
        # st=st+str(num)+". "+da1[i]+"\n"
        if st == "":
            st = "_Empty_"
        em = discord.Embed(
            title="Queue", description=st, color=discord.Color(value=re[8])
        )
        mess = await ctx.send(embed=em)
        await mess.add_reaction("⏮")
        await mess.add_reaction("⏸")
        await mess.add_reaction("▶")
        await mess.add_reaction("🔁")
        await mess.add_reaction("⏭")
        await mess.add_reaction("⏹")
        await mess.add_reaction(emoji.emojize(":keycap_*:"))
        await mess.add_reaction(emoji.emojize(":upwards_button:"))
        await mess.add_reaction(emoji.emojize(":downwards_button:"))
    elif name == "":
        num = 0
        st = ""
        if len(queue_song[str(ctx.guild.id)]) < 30:
            for i in queue_song[str(ctx.guild.id)]:
                if not i in da1.keys():
                    da1[i] = youtube_info(i)["title"]
                st = st + str(num) + ". " + da1[i] + "\n"
                num += 1
        else:
            adfg = 0
            num = -1
            for i in queue_song[str(ctx.guild.id)]:
                num += 1
                try:
                    if re[3][str(ctx.guild.id)] < 10:
                        if num < 15:
                            if not i in da1.keys():
                                da1[i] = youtube_info(i)["title"]
                            st = st + str(num) + ". " + da1[i] + "\n"
                    elif re[3][str(ctx.guild.id)] > (
                            len(queue_song[str(ctx.guild.id)]) - 10
                    ):
                        if num > (len(queue_song[str(ctx.guild.id)]) - 15):
                            if not i in da1.keys():
                                da1[i] = youtube_info(i)["title"]
                            st = st + str(num) + ". " + da1[i] + "\n"
                    else:
                        if (
                                re[3][str(ctx.guild.id)] - 10 < num < re[3][str(ctx.guild.id)] + 10
                        ):
                            if not i in da1.keys():
                                da1[i] = youtube_info(i)["title"]
                            st = st + str(num) + ". " + da1[i] + "\n"
                except Exception as e:
                    pass

        if st == "":
            st = "_Empty_"
        embed = discord.Embed(
            title="Queue", description=st, color=discord.Color(value=re[8])
        )
        embed.set_thumbnail(url=client.user.avatar_url_as(format="png"))
        mess = await ctx.send(embed=embed)
        await mess.add_reaction("⏮")
        await mess.add_reaction("⏸")
        await mess.add_reaction("▶")
        await mess.add_reaction("🔁")
        await mess.add_reaction("⏭")
        await mess.add_reaction("⏹")
        await mess.add_reaction(emoji.emojize(":keycap_*:"))
        await mess.add_reaction(emoji.emojize(":upwards_button:"))
        await mess.add_reaction(emoji.emojize(":downwards_button:"))
    else:
        await ctx.send(
            embed=discord.Embed(
                title="Permission denied",
                description="Join the voice channel to modify queue",
                color=discord.Color(value=re[8]),
            )
        )


@client.command(aliases=[">"])
async def next(ctx):
    req()
    try:
        try:
            mem = [str(names) for names in ctx.voice_client.channel.members]
        except:
            mem = []
        if mem.count(str(ctx.author)) > 0:
            re[3][str(ctx.guild.id)] += 1
            if re[3][str(ctx.guild.id)] >= len(queue_song[str(ctx.guild.id)]):
                re[3][str(ctx.guild.id)] = len(queue_song[str(ctx.guild.id)]) - 1
                await ctx.send(
                    embed=discord.Embed(
                        title="Last song",
                        description="Only "
                                    + str(len(queue_song[str(ctx.guild.id)]))
                                    + " songs in your queue",
                        color=discord.Color(value=re[8]),
                    )
                )
            voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
            URL = youtube_download(
                ctx, queue_song[str(ctx.guild.id)][re[3][str(ctx.guild.id)]]
            )
            await ctx.send(
                embed=discord.Embed(
                    title="Playing",
                    description=da1[
                        queue_song[str(ctx.guild.id)][re[3][str(ctx.guild.id)]]
                    ],
                    color=discord.Color(value=re[8]),
                )
            )
            voice.stop()
            voice.play(
                discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS),
                after=lambda e: repeat(ctx, voice),
            )
        else:
            await ctx.send(
                embed=discord.Embed(
                    title="Permission denied",
                    description="Join the voice channel to move to the next song",
                    color=discord.Color(value=re[8]),
                )
            )
    except Exception as e:
        channel = client.get_channel(dev_channel)
        await channel.send(
            embed=discord.Embed(
                title="Error in next function",
                description=str(e)
                            + "\n"
                            + str(ctx.guild)
                            + ": "
                            + str(ctx.channel.name),
                color=discord.Color(value=re[8]),
            )
        )


@client.command(aliases=["<"])
async def previous(ctx):
    req()
    try:
        try:
            mem = [str(names) for names in ctx.voice_client.channel.members]
        except:
            mem = []
        if mem.count(str(ctx.author)) > 0:
            re[3][str(ctx.guild.id)] -= 1
            if re[3][str(ctx.guild.id)] == -1:
                re[3][str(ctx.guild.id)] = 0
                await ctx.send(
                    embed=discord.Embed(
                        title="First song",
                        description="This is first in queue",
                        color=discord.Color(value=re[8]),
                    )
                )
            if (
                    not queue_song[str(ctx.guild.id)][re[3][str(ctx.guild.id)]]
                        in da1.keys()
            ):
                da1[
                    queue_song[str(ctx.guild.id)][re[3][str(ctx.guild.id)]]
                ] = youtube_info(
                    queue_song[str(ctx.guild.id)][re[3][str(ctx.guild.id)]]
                )[
                    "title"
                ]
            voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
            URL = youtube_download(
                ctx, queue_song[str(ctx.guild.id)][re[3][str(ctx.guild.id)]]
            )
            await ctx.send(
                embed=discord.Embed(
                    title="Playing",
                    description=da1[
                        queue_song[str(ctx.guild.id)][re[3][str(ctx.guild.id)]]
                    ],
                    color=discord.Color(value=re[8]),
                )
            )
            voice.stop()
            voice.play(
                discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS),
                after=lambda e: repeat(ctx, voice),
            )
        else:
            await ctx.send(
                embed=discord.Embed(
                    title="Permission denied",
                    description="Join the voice channel to move to the previous song",
                    color=discord.Color(value=re[8]),
                )
            )
    except Exception as e:
        channel = client.get_channel(dev_channel)
        await channel.send(
            embed=discord.Embed(
                title="Error in previous function",
                description=str(e)
                            + "\n"
                            + str(ctx.guild)
                            + ": "
                            + str(ctx.channel.name),
                color=discord.Color(value=re[8]),
            )
        )


@client.command(aliases=["s_q"])
async def search_queue(ctx, part):
    st = ""
    index = 0
    found_songs = 0
    for i in queue_song[str(ctx.guild.id)]:
        if i in da1:
            found_songs += 1
            if da1[i].lower().find(part.lower()) != -1:
                st += str(index) + ". " + da1[i] + "\n"
        index += 1
    if st == "":
        st = "Not found"
    if len(queue_song[str(ctx.guild.id)]) - found_songs > 0:
        st += "\n\nWARNING: Some song names may not be loaded properly, this search may not be accurate"
        st += "\nSongs not found: " + str(
            len(queue_song[str(ctx.guild.id)]) - found_songs
        )
    await ctx.send(
        embed=cembed(
            title="Songs in queue",
            description=st,
            color=re[8],
            thumbnail=client.user.avatar_url_as(format="png"),
        )
    )


@client.command(aliases=["p"])
async def play(ctx, *, ind):
    req()
    if (
            discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild) == None
            and ctx.author.voice
            and ctx.author.voice.channel
    ):
        if not str(ctx.guild.id) in queue_song:
            queue_song[str(ctx.guild.id)] = []
        if not str(ctx.guild.id) in re[3]:
            re[3][str(ctx.guild.id)] = 0
        channel = ctx.author.voice.channel.id
        vc_channel[str(ctx.guild.id)] = channel
        voiceChannel = discord.utils.get(ctx.guild.voice_channels, id=channel)
        await voiceChannel.connect()
    try:
        try:
            mem = [str(names) for names in ctx.voice_client.channel.members]
        except:
            mem = []
        if mem.count(str(ctx.author)) > 0:
            if ind.isnumeric():
                if int(ind) < len(queue_song[str(ctx.guild.id)]):
                    re[3][str(ctx.guild.id)] = int(ind)
                    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
                    URL = youtube_download(
                        ctx, queue_song[str(ctx.guild.id)][re[3][str(ctx.guild.id)]]
                    )
                    if (
                            not queue_song[str(ctx.guild.id)][re[3][str(ctx.guild.id)]]
                                in da1.keys()
                    ):
                        da1[
                            queue_song[str(ctx.guild.id)][re[3][str(ctx.guild.id)]]
                        ] = await get_name(
                            queue_song[str(ctx.guild.id)][re[3][str(ctx.guild.id)]]
                        )
                    mess = await ctx.send(
                        embed=discord.Embed(
                            title="Playing",
                            description=da1[
                                queue_song[str(ctx.guild.id)][re[3][str(ctx.guild.id)]]
                            ],
                            color=discord.Color(value=re[8]),
                        )
                    )
                    voice.stop()
                    voice.play(
                        discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS),
                        after=lambda e: repeat(ctx, voice),
                    )
                    await mess.add_reaction("⏮")
                    await mess.add_reaction("⏸")
                    await mess.add_reaction("▶")
                    await mess.add_reaction("🔁")
                    await mess.add_reaction("⏭")
                    await mess.add_reaction("⏹")
                    await mess.add_reaction(emoji.emojize(":keycap_*:"))
                    await mess.add_reaction(emoji.emojize(":upwards_button:"))
                    await mess.add_reaction(emoji.emojize(":downwards_button:"))
                else:
                    embed = discord.Embed(
                        title="Hmm",
                        description=f"There are only {len(queue_song[str(ctx.guild.id)])} songs",
                        color=discord.Color(value=re[8]),
                    )
                    await ctx.send(embed=embed)
            else:
                name = ind
                if name.find("rick") == -1:
                    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
                    name = convert_to_url(name)
                    htm = urllib.request.urlopen(
                        "https://www.youtube.com/results?search_query=" + name
                    )
                    video = regex.findall(r"watch\?v=(\S{11})", htm.read().decode())
                    url = "https://www.youtube.com/watch?v=" + video[0]
                    URL, name_of_the_song = youtube_download1(ctx, url)
                    voice.stop()
                    voice.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
                    await ctx.send(
                        embed=discord.Embed(
                            title="Playing",
                            description=name_of_the_song,
                            color=discord.Color(value=re[8]),
                        )
                    )
                else:
                    mess = await ctx.send(
                        embed=discord.Embed(
                            title="Playing",
                            description="Rick Astley - Never Gonna Give You Up (Official Music Video) - YouTube :wink:",
                            color=discord.Color(value=re[8]),
                        )
                    )

        else:
            await ctx.send(
                embed=discord.Embed(
                    title="Permission denied",
                    description="Join the voice channel to play the song",
                    color=discord.Color(value=re[8]),
                )
            )
    except Exception as e:
        channel = client.get_channel(dev_channel)
        await channel.send(
            embed=discord.Embed(
                title="Error in play function",
                description=f"{e}\n{ctx.guild.name}: {ctx.channel.name}",
                color=discord.Color(value=re[8]),
            )
        )


@client.command()
async def again(ctx):
    req()
    if ctx.author.voice and ctx.author.voice.channel:
        if not str(ctx.guild.id) in queue_song:
            queue_song[str(ctx.guild.id)] = []
        if not str(ctx.guild.id) in re[3]:
            re[3][str(ctx.guild.id)] = 0
        if discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild) == None:
            channel = ctx.author.voice.channel.id
            vc_channel[str(ctx.guild.id)] = channel
            voiceChannel = discord.utils.get(ctx.guild.voice_channels, id=channel)
            await voiceChannel.connect()
        mem = []
        try:
            try:
                mem = [str(names) for names in ctx.voice_client.channel.members]
            except:
                mem = []
            if mem.count(str(ctx.author)) > 0:
                voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
                bitrate = "\nBitrate of the channel: " + str(
                    ctx.voice_client.channel.bitrate // 1000
                )
                if (
                        not queue_song[str(ctx.guild.id)][re[3][str(ctx.guild.id)]]
                            in da1.keys()
                ):
                    da1[
                        queue_song[str(ctx.guild.id)][re[3][str(ctx.guild.id)]]
                    ] = youtube_info(
                        queue_song[str(ctx.guild.id)][re[3][str(ctx.guild.id)]]
                    )[
                        "title"
                    ]
                mess = await ctx.send(
                    embed=cembed(
                        title="Playing",
                        description=da1[
                                        queue_song[str(ctx.guild.id)][re[3][str(ctx.guild.id)]]
                                    ]
                                    + bitrate,
                        color=re[8],
                        thumbnail=client.user.avatar_url_as(format="png"),
                    )
                )
                URL = youtube_download(
                    ctx, queue_song[str(ctx.guild.id)][re[3][str(ctx.guild.id)]]
                )
                voice.stop()
                voice.play(
                    discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS),
                    after=lambda e: repeat(ctx, voice),
                )
                await mess.add_reaction("⏮")
                await mess.add_reaction("⏸")
                await mess.add_reaction("▶")
                await mess.add_reaction("🔁")
                await mess.add_reaction("⏭")
                await mess.add_reaction("⏹")
                await mess.add_reaction(emoji.emojize(":keycap_*:"))
                await mess.add_reaction(emoji.emojize(":upwards_button:"))
                await mess.add_reaction(emoji.emojize(":downwards_button:"))
            else:
                await ctx.send(
                    embed=cembed(
                        title="Permission denied",
                        description="Join the voice channel to play the song",
                        color=re[8],
                        thumbnail=client.user.avatar_url_as(format="png"),
                    )
                )
        except Exception as e:
            channel = client.get_channel(dev_channel)
            await ctx.send(
                embed=cembed(
                    title="Error",
                    description=str(e),
                    color=re[8],
                    thumbnail=client.user.avatar_url_as(format="png"),
                )
            )
            await channel.send(
                embed=discord.Embed(
                    title="Error in play function",
                    description=f"{e}\n{ctx.guild.name}: {ctx.channel.name}",
                    color=discord.Color(value=re[8]),
                )
            )


@slash.slash(name="again", description="Repeat the song")
async def again_slash(ctx):
    req()
    await ctx.defer()
    await again(ctx)


@slash.slash(name="dc", description="Disconnect the bot from your voice channel")
async def leave_slash(ctx):
    req()
    await ctx.defer()
    await leave(ctx)


@client.command(aliases=["dc"])
async def leave(ctx):
    req()
    try:
        try:
            mem = [names.id for names in ctx.voice_client.channel.members]
        except:
            mem = []
        if mem.count(ctx.author.id) > 0:
            if ctx.author.id == 734275789302005791:
                await clearqueue(ctx)
            voice = ctx.guild.voice_client
            voice.stop()
            await voice.disconnect()
            await ctx.send(
                embed=discord.Embed(
                    title="Disconnected",
                    description="Bye",
                    color=discord.Color(value=re[8]),
                )
            )
        else:
            await ctx.send(
                embed=discord.Embed(
                    title="Permission denied",
                    description="Nice try dude! Join the voice channel",
                    color=discord.Color(value=re[8]),
                )
            )
    except Exception as e:
        await ctx.send(
            embed=discord.Embed(
                title="Hmm", description=str(e), color=discord.Color(value=re[8])
            )
        )
        channel = client.get_channel(dev_channel)
        await channel.send(
            embed=discord.Embed(
                title="Error in leave",
                description=f"{e}\n{ctx.guild.name}: {ctx.channel.name}",
                color=discord.Color(value=re[8]),
            )
        )
    save_to_file()


@client.command()
async def pause(ctx):
    req()
    try:
        mem = [str(names) for names in ctx.voice_client.channel.members]
    except:
        mem = []
    if mem.count(str(ctx.author)) > 0:
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
        voice.pause()
        await ctx.send(
            embed=discord.Embed(title="Pause", color=discord.Color(value=re[8]))
        )
    else:
        await ctx.send(
            embed=discord.Embed(
                title="Permission denied",
                description="Join the channel to pause the song",
                color=discord.Color(value=re[8]),
            )
        )


@client.command()
async def resume(ctx):
    req()
    try:
        mem = [str(names) for names in ctx.voice_client.channel.members]
    except:
        mem = []
    if mem.count(str(ctx.author)) > 0:
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
        voice.resume()
        await ctx.send(
            embed=discord.Embed(title="Resume", color=discord.Color(value=re[8]))
        )


@client.command()
async def clear(ctx, text, num=10):
    req()
    await ctx.channel.purge(limit=1)
    if str(text) == re[1]:
        if (
                ctx.author.guild_permissions.manage_messages
                or ctx.author.id == 432801163126243328
        ):
            confirmation = True
            if int(num) > 10:
                confirmation = await wait_for_confirm(
                    ctx, client, f"Do you want to delete {num} messages", color=re[8]
                )
            if confirmation:
                await ctx.channel.delete_messages(
                    [i async for i in ctx.channel.history(limit=num) if not i.pinned][:100]
                )
        else:
            await ctx.send(
                embed=discord.Embed(
                    title="Permission Denied",
                    description="You cant delete messages",
                    color=discord.Color(value=re[8]),
                )
            )
    else:
        await ctx.send("Wrong password")

