import discord
import emoji
from discord.ext import commands
from discord_slash import cog_ext

from External_functions import youtube_info, cembed
from cogs.music.repeat import Repeat
from stuff import req, queue_song, re, vc_channel, da1, youtube_download, FFMPEG_OPTIONS, dev_channel


class Again(commands.cog):
    def __init__(self, bot):
        self.bot = bot
        self.repeat = Repeat(bot)


    @commands.command()
    async def again(self, ctx):
        req()
        if ctx.author.voice and ctx.author.voice.channel:
            if not str(ctx.guild.id) in queue_song:
                queue_song[str(ctx.guild.id)] = []
            if not str(ctx.guild.id) in re[3]:
                re[3][str(ctx.guild.id)] = 0
            if discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild) is None:
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
                    voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
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
                            thumbnail=self.bot.user.avatar_url_as(format="png"),
                        )
                    )
                    URL = youtube_download(
                        ctx, queue_song[str(ctx.guild.id)][re[3][str(ctx.guild.id)]]
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
                    await ctx.send(
                        embed=cembed(
                            title="Permission denied",
                            description="Join the voice channel to play the song",
                            color=re[8],
                            thumbnail=self.bot.user.avatar_url_as(format="png"),
                        )
                    )
            except Exception as e:
                channel = self.bot.get_channel(dev_channel)
                await ctx.send(
                    embed=cembed(
                        title="Error",
                        description=str(e),
                        color=re[8],
                        thumbnail=self.bot.user.avatar_url_as(format="png"),
                    )
                )
                await channel.send(
                    embed=discord.Embed(
                        title="Error in play function",
                        description=f"{e}\n{ctx.guild.name}: {ctx.channel.name}",
                        color=discord.Color(value=re[8]),
                    )
                )


    @cog_ext.cog_slash(name="again", description="Repeat the song")
    async def again_slash(self, ctx):
        req()
        await ctx.defer()
        await self.again(ctx)
