from functools import lru_cache
import discord
from discord import Color
from discord.ext import commands
import aiohttp
import asyncio
from bs4 import BeautifulSoup
import datetime
import requests


def requirements():
    return ["re"]


@lru_cache(maxsize=128)
def get_repo_image_url(url):
    text = requests.get(url)
    soup = BeautifulSoup(text.content, "lxml")
    image_url = soup.find("meta", property="og:image")['content']
    return image_url


def trend_embed(
    title="",
    description="",
    thumbnail="",
    url="",
    color=Color.blurple(),
    author_url="",
    icon_url="",
    name="",
    forks=0,
    stars=0,
    language="",
    text=""
):
    image_url = get_repo_image_url(url)
    embed = discord.Embed()
    embed.color = color
    embed.set_author(name=name, url=author_url, icon_url=icon_url)
    embed.description = description
    embed.title = title
    embed.url = url
    embed.timestamp = datetime.datetime.now()
    embed.set_image(url=image_url)
    embed.set_thumbnail(url=thumbnail)
    embed.add_field(
        name="Language", value=f"{'-' if language == '' else language}", inline=True)
    embed.add_field(
        name="Stars ⭐", value=f"[{stars}]({url}/stargazers)", inline=True)
    embed.add_field(
        name="Forks 🍴", value=f"[{forks}]({url}/network/members)", inline=True)
    embed.set_footer(text=text)
    return embed


def main(client: commands, re):
    async def pa1(embeds, ctx):
        message = await ctx.send(embed=embeds[0])
        pag = 0

        await message.add_reaction("⏮️")
        await message.add_reaction("◀️")
        await message.add_reaction("▶️")

        await message.add_reaction("⏭️")

        def check(reaction, user):
            return (
                user != client.user
                and str(reaction.emoji) in ["◀️", "▶️", "⏮️", "⏭️"]
                and reaction.message.id == message.id
            )

        while True:
            try:
                reaction, user = await client.wait_for(
                    "reaction_add", timeout=360, check=check
                )
                await message.remove_reaction(reaction, user)
                if str(reaction.emoji) == "▶️" and pag + 1 != len(embeds):
                    pag += 1
                    await message.edit(embed=embeds[pag])
                elif str(reaction.emoji) == "◀️" and pag != 0:
                    pag -= 1
                    await message.edit(embed=embeds[pag])
                elif str(reaction.emoji) == "⏭️":
                    pag = 24
                    await message.edit(embed=embeds[pag])
                elif str(reaction.emoji) == "⏮️":
                    pag = 0
                    await message.edit(embed=embeds[pag])
            except asyncio.TimeoutError:
                break

    @client.command(aliases=["trend", "ght"])
    async def trending_github(ctx):
        rec = {}
        async with aiohttp.ClientSession() as session:
            async with session.get("https://ghapi.huchen.dev/repositories?language=javascript&since=weekly") as resp:
                rec = await resp.json()
            await session.close()
        embeds = []
        for index, i in enumerate(rec[0:25]):
            name = i["name"]
            author = i["author"]
            thumbnail = i["avatar"] if "avatar" in i.keys() else None
            description = i["description"]
            color = i["langColor"]
            forks = i["forks"]
            stars = i["stars"]
            language = i["language"]
            output = f"description: {description}\nforks: {forks}\nstars: {stars}\nlanguage: {language}\n\nAuthor: {author}"
            embeds += [
                trend_embed(title=f"{author}/{name}",
                            description=description,
                            thumbnail=thumbnail,
                            url=f"https://github.com/{author}/{name}",
                            color=int(
                                "eb4034" if color is None else color.lstrip("#"), 16),
                            author_url=f"https://github.com/{author}",
                            icon_url=thumbnail,
                            name=author,
                            stars=stars,
                            forks=forks,
                            language=language,
                            text=f"{index + 1} of 25")
            ]
        await pa1(embeds, ctx)
