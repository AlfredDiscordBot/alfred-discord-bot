from io import BytesIO

import discord
import requests
from discord.ext import commands

from External_functions import imdb_embed, cembed, svg2png, instagram_get1
from main_program import re, req, dev_channel, pa
from discord_slash import cog_ext, SlashContext
from GoogleNews import GoogleNews
from wikipedia import search, summary


class Scraping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.googlenews = GoogleNews()

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

    @cog_ext.cog_slash(name="news", description="Latest news from a given subject")
    async def news_slash(self, ctx, *, subject="Technology"):
        req()
        await ctx.defer()
        await self.news(ctx, subject)

    @commands.command()
    async def news(self, ctx, subject="Technology"):
        self.googlenews.get_news(subject)
        news_list = self.googlenews.get_texts()
        self.googlenews.clear()
        string = ""
        for i in range(0, 10):
            string = string + str(i) + ". " + news_list[i] + "\n"
        await ctx.send(
            embed=cembed(
                title="News",
                description=string,
                color=re[8],
                thumbnail=self.bot.user.avatar_url_as(format="png"),
            )
        )

    @commands.command(aliases=["dict"])
    async def dictionary(self, ctx, *, text):
        try:
            data = eval(
                requests.get(
                    "https://api.dictionaryapi.dev/api/v2/entries/en/"
                    + text.replace(" ", "%20")
                ).content.decode()
            )
            if type(data) == type([]):
                data = data[0]
                word = data["word"]
                description = "**Here's What I found:**\n\n"
                if "phonetics" in data.keys():
                    if "text" in data["phonetics"][0]:
                        phonetics = (
                                "**Phonetics:**\n" + data["phonetics"][0]["text"] + "\n\n"
                        )
                        description += phonetics
                if "origin" in list(data.keys()):
                    origin = "**Origin: **" + data["origin"] + "\n\n"
                    description += origin
                if "meanings" in data.keys() and "definitions" in data["meanings"][0]:
                    meanings = data["meanings"][0]["definitions"][0]
                    if "definition" in list(meanings.keys()):
                        meaning = "**Definition: **" + meanings["definition"] + "\n\n"
                        description += meaning
                    if "example" in list(meanings.keys()):
                        example = "**Example: **" + meanings["example"]
                        description += example
            else:
                word = data["title"]
                description = data["message"]

            await ctx.send(
                embed=cembed(
                    title=word,
                    description=description,
                    color=re[8],
                    thumbnail=self.bot.user.avatar_url_as(format="png"),
                )
            )
        except Exception as e:
            print(e)
            await ctx.send(
                embed=cembed(
                    title="Oops",
                    description="Something is wrong\n" + str(e),
                    color=re[8],
                    thumbnail=self.bot.user.avatar_url_as(format="png"),
                )
            )

    @cog_ext.cog_slash(name="wikipedia", description="Get a topic from wikipedia")
    async def wiki_slash(self, ctx, text):
        try:
            req()
            await ctx.defer()
            t = str(search(text)[0].encode("utf-8"))
            em = discord.Embed(
                title=str(t).title(),
                description=str(summary(t, sentences=5)),
                color=discord.Color(value=re[8]),
            )
            em.set_thumbnail(
                url="https://1000logos.net/wp-content/uploads/2017/05/Wikipedia-logos.jpg"
            )
            await ctx.send(embed=em)
        except Exception as e:
            await ctx.send(
                embed=cembed(
                    title="Oops",
                    description=str(e),
                    color=re[8],
                    thumbnail=self.bot.user.avatar_url_as(format="png"),
                )
            )

    @commands.command(aliases=["w"])
    async def wikipedia(self, ctx, *, text):
        req()
        t = str(search(text)[0].encode("utf-8"))
        em = discord.Embed(
            title=str(t).title(),
            description=str(summary(t, sentences=5)),
            color=discord.Color(value=re[8]),
        )
        em.set_thumbnail(
            url="https://1000logos.net/wp-content/uploads/2017/05/Wikipedia-logos.jpg"
        )
        await ctx.send(embed=em)

def setup(client):
    client.add_cog(Scraping(client))
