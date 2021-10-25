import urllib

import discord
import emoji
from discord.ext import commands
from regex import regex

from External_functions import youtube_info, get_name, convert_to_url, cembed
from stuff import re, da1, queue_song, req, pa, da
from spotify_client import spotify, fetch_spotify_playlist


class Queue(commands.cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def show_playlist(self, ctx, *, name):
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
                            thumbnail=self.bot.user.avatar_url_as(format="png"),
                        )
                    )
                    st = ""
            if len(da) < 10:
                embeds.append(
                    cembed(
                        title="Playlist",
                        description=st,
                        color=re[8],
                        thumbnail=self.bot.user.avatar_url_as(format="png"),
                    )
                )
            await pa(embeds, ctx)
        else:
            await ctx.send(
                embed=cembed(
                    title="Playlist",
                    description="This playlist is not found",
                    color=re[8],
                    thumbnail=self.bot.user.avatar_url_as(format="png"),
                )
            )

    @commands.command(aliases=["q"])
    async def queue(self, ctx, *, name=""):
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
            embed.set_thumbnail(url=self.bot.user.avatar_url_as(format="png"))
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

    @commands.command(aliases=["s_q"])
    async def search_queue(self, ctx, part):
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
                thumbnail=self.bot.user.avatar_url_as(format="png"),
            )
        )
