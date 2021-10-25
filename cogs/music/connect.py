import discord
from discord.ext import commands
from discord_slash import cog_ext

from stuff import req, queue_song, re, vc_channel, dev_channel


class Connect(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="connect", description="Connect to a voice channel")
    async def connect_slash(self, ctx, channel=""):
        req()
        await ctx.defer()
        await self.connect_music(ctx, channel)

    @commands.command(aliases=["cm"])
    async def connect_music(self, ctx, channel=""):
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
                    voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
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
                    voicechannel = discord.utils.get(ctx.guild.voice_channels, name=channel)
                    vc_channel[str(ctx.guild.id)] = voicechannel.id
                    await voicechannel.connect()
                    voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
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
            channel = self.bot.get_channel(dev_channel)
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



def setup(bot):
    bot.add_cog(Connect(bot))
