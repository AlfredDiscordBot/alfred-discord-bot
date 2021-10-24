from discord.ext import commands
from discord_slash import cog_ext, SlashContext
import discord

from main_program import req, re


class Emoji(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    @cog_ext.cog_slash(name="emoji", description="Get Emojis from other servers")
    async def emoji_slash(self, ctx: SlashContext, emoji_name, number=0):
        req()
        await ctx.defer()
        if discord.utils.get(self.client.emojis, name=emoji_name) is not None:
            emoji_list = [names.name for names in self.client.emojis if names.name == emoji_name]
            le = len(emoji_list)
            if le >= 2:
                if number > le - 1:
                    number = le - 1
            emoji = [names for names in self.client.emojis if names.name == emoji_name][
                number
            ].id
            await ctx.send(str(discord.utils.get(self.client.emojis, id=emoji)))
        else:
            await ctx.send(
                embed=discord.Embed(
                    description="The emoji is not available",
                    color=discord.Color(value=re[8]),
                )
            )

    @commands.command(aliases=["e", "emoji"])
    async def uemoji(self, ctx, emoji_name, number=0):
        req()
        try:
            await ctx.message.delete()
        except:
            pass
        if discord.utils.get(self.client.emojis, name=emoji_name) is not None:
            emoji_list = [names.name for names in self.client.emojis if names.name == emoji_name]
            le = len(emoji_list)
            if le >= 2:
                if number > le - 1:
                    number = le - 1
            emoji = [names for names in self.client.emojis if names.name == emoji_name][number]
            webhook = await ctx.channel.create_webhook(name=ctx.author.name)
            await webhook.send(
                emoji, username=ctx.author.name, avatar_url=ctx.author.avatar_url
            )
            webhooks = await ctx.channel.webhooks()
            for webhook in webhooks:
                await webhook.delete()

        else:
            await ctx.send(
                embed=discord.Embed(
                    description="The emoji is not available",
                    color=discord.Color(value=re[8]),
                )
            )

    @cog_ext.cog_slash(name="pr", description="Prints what you ask it to print")
    async def pr_slash(self, ctx, text):
        req()
        await ctx.send(text)

    @commands.command(aliases=["say"])
    async def pr(self, ctx, *, text):
        await ctx.send(text)

def setup(client):
    client.add_cog(Emoji(client))
