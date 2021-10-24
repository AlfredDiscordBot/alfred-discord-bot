from io import BytesIO

import discord
from discord.ext import commands

from External_functions import imdb_embed, cembed, svg2png, instagram_get1
from main_program import re, req, dev_channel, pa
from discord_slash import cog_ext, SlashContext


class Scraping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def imdb(self, ctx, *, movie):
        await ctx.send(embed=imdb_embed(movie))

    @commands.command()
    async def svg(self, ctx, *, url):
        img = svg2png(url)
        await ctx.send(file=discord.File(BytesIO(img), "svg.png"))

    @commands.command()
    async def instagram(self, ctx, account):
        try:
            links = instagram_get1(account, re[8], re[9])
            embeds = []
            for a in links:
                if a is not None and type(a) != type("aa"):
                    embeds.append(a[0])
                elif type(a) != type("aa"):
                    re[9] = a
                else:
                    await ctx.send(
                        embed=discord.Embed(
                            description="Oops!, something is wrong.",
                            color=discord.Color(value=re[8]),
                        )
                    )
                    break
            await pa(embeds, ctx)
        except Exception as e:
            embed = cembed(
                title="Error in instagram",
                description=f"{e}\n{ctx.guild.name}: {ctx.channel}",
                color=re[8],
                thumbnail=self.bot.user.avatar_url_as(format="png"),
            )
            await ctx.send(embed=embed)
            await self.bot.get_channel(dev_channel).send(embed=embed)

    @cog_ext.cog_slash(name="imdb", description="Give a movie name")
    async def imdb_slash(self, ctx: SlashContext, movie):
        req()
        await ctx.defer()
        try:
            await ctx.send(embed=imdb_embed(movie))
        except Exception as e:
            await ctx.send(
                embed=cembed(
                    title="Oops",
                    description=str(e),
                    color=re[8],
                    thumbnail=self.bot.user.avatar_url_as(format="png"),
                )
            )

    @cog_ext.cog_slash(name="svg2png", description="Convert SVG image to png format")
    async def svg2png_slash(self, ctx: SlashContext, url):
        req()
        await ctx.defer()
        img = svg2png(url)
        await ctx.send(file=discord.File(BytesIO(img), "svg.png"))
