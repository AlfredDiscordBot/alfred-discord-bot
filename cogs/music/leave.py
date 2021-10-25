import discord
from discord.ext import commands
from discord_slash import cog_ext

from stuff import req, vc_channel, queue_song, re, dev_channel, save_to_file


class Leave(commands.cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["cq"])
    async def clearqueue(self, ctx):
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

    @cog_ext.cog_slash(name="dc", description="Disconnect the bot from your voice channel")
    async def leave_slash(self, ctx):
        req()
        await ctx.defer()
        await self.leave(ctx)

    @commands.command(aliases=["dc"])
    async def leave(self, ctx):
        req()
        try:
            try:
                mem = [names.id for names in ctx.voice_client.channel.members]
            except:
                mem = []
            if mem.count(ctx.author.id) > 0:
                if ctx.author.id == 734275789302005791:
                    await self.clearqueue(ctx)
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
            channel = self.bot.get_channel(dev_channel)
            await channel.send(
                embed=discord.Embed(
                    title="Error in leave",
                    description=f"{e}\n{ctx.guild.name}: {ctx.channel.name}",
                    color=discord.Color(value=re[8]),
                )
            )
        save_to_file()
