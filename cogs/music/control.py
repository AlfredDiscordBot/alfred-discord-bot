import urllib

import discord
import emoji
from discord.ext import commands
from regex import regex

from External_functions import get_name, convert_to_url, youtube_info
from cogs.music.repeat import Repeat
from main_program import req, re, queue_song, vc_channel, youtube_download, da1, FFMPEG_OPTIONS, youtube_download1, \
    dev_channel


class Controls(commands.cog):
    def __init__(self, bot):
        self.bot = bot
        self.repeat = Repeat(bot)

    @commands.command()
    async def pause(self, ctx):
        req()
        try:
            mem = [str(names) for names in ctx.voice_client.channel.members]
        except:
            mem = []
        if mem.count(str(ctx.author)) > 0:
            voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
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

    @commands.command()
    async def resume(self, ctx):
        req()
        try:
            mem = [str(names) for names in ctx.voice_client.channel.members]
        except:
            mem = []
        if mem.count(str(ctx.author)) > 0:
            voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
            voice.resume()
            await ctx.send(
                embed=discord.Embed(title="Resume", color=discord.Color(value=re[8]))
            )

    @commands.command(aliases=["p"])
    async def play(self, ctx, *, ind):
        req()
        if (
                discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild) is None
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
                        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
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
                            after=lambda e: self.repeat.repeat(ctx, voice),
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
                        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
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
                                description="Rick Astley - Never Gonna Give You Up (Official Music Video) - YouTube "
                                            ":wink:",
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
            channel = self.bot.get_channel(dev_channel)
            await channel.send(
                embed=discord.Embed(
                    title="Error in play function",
                    description=f"{e}\n{ctx.guild.name}: {ctx.channel.name}",
                    color=discord.Color(value=re[8]),
                )
            )

    @commands.command(aliases=[">"])
    async def next(self, ctx):
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
                voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
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
                    after=lambda e: self.repeat.repeat(ctx, voice),
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
            channel = self.bot.get_channel(dev_channel)
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

    @commands.command(aliases=["<"])
    async def previous(self, ctx):
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
                voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
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
                    after=lambda e: self.repeat.repeat(ctx, voice),
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
            channel = self.bot.get_channel(dev_channel)
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
