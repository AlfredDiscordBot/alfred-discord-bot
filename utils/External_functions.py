from bs4 import BeautifulSoup
from collections import Counter
from datetime import datetime
from dotenv import load_dotenv
from functools import lru_cache
from io import BytesIO
from matplotlib import colors as mcolors, font_manager as fm, pyplot as plt
from nextcord import SlashOption
from nextcord.ext import commands
from requests.models import PreparedRequest
from requests.exceptions import MissingSchema
from string import ascii_letters
from typing import List, Union

import aiofiles
import aiohttp
import emoji
import importlib
import json
import nextcord
import numpy as np
import os
import psutil
import random
import re as regex
import requests
import time
import traceback
import urllib
import urllib.parse
import utils.assets as assets

SVG2PNG_API_URI = os.getenv("svg2pnguri")
SVG2PNG_API_TOKEN = os.getenv("svg2pngtoken")

m_options = [
    "title",
    "description",
    "color",
    "footer",
    "thumbnail",
    "image",
    "author",
    "url",
    "fields",
    "button",
]

Emoji_alphabets = [chr(i) for i in range(127462, 127488)]

load_dotenv()


def activities(client, FORCED_ACTIVITY=None):
    if FORCED_ACTIVITY:
        return nextcord.Activity(
            type=nextcord.ActivityType.watching, name=FORCED_ACTIVITY
        )
    all_activities = [
        nextcord.Activity(
            type=nextcord.ActivityType.watching, name="Dark Knight Rises"
        ),
        nextcord.Activity(
            type=nextcord.ActivityType.listening, name="Something in the way"
        ),
        nextcord.Activity(
            type=nextcord.ActivityType.listening, name=f"{len(client.guilds)} servers"
        ),
        nextcord.Activity(
            type=nextcord.ActivityType.listening,
            name=f"{len(client.users)} people enjoy Alfred",
        ),
        nextcord.Activity(
            type=nextcord.ActivityType.listening, name="Wayne Enterprise"
        ),
        nextcord.Activity(
            type=nextcord.ActivityType.watching, name="Raimi Trilogy with Thwipper"
        ),
        nextcord.Activity(type=nextcord.ActivityType.watching, name="New Updates"),
    ]
    return random.choice(all_activities)


def timestamp(i):
    return datetime.fromtimestamp(i)


def convert_to_url(name: str):
    name = urllib.parse.quote(name)
    return name


def iso2dtime(iso: str):
    return f"<t:{int(datetime.fromisoformat(iso[:-1]).timestamp())}>"


async def wolf_spoken(wolfram, question):
    question = convert_to_url(question)
    url = f"http://api.wolframalpha.com/v1/spoken?appid={wolfram}&i={question}"
    return await get_async(url)


@lru_cache(maxsize=512)
async def get_youtube_url(url):
    """
    gets the list of url from a channel url
    """
    st = await get_async(url)
    li = regex.findall(r"watch\?v=(\S{11})", st)
    return [f"https://youtube.com/watch?v={w}" for w in li]


def get_if_process_exists(name):
    return (
        len(
            [
                i
                for i in [p.info["name"] for p in psutil.process_iter(["name"])]
                if i.find(name) != -1
            ]
        )
        > 0
    )


def cembed(
    title=None,
    description=None,
    thumbnail=None,
    picture=None,
    url=None,
    color=nextcord.Color.dark_theme(),
    footer=None,
    author: Union[nextcord.Member, bool, dict] = False,
    fields=None,
    image=None,
    button: Union[dict, nextcord.ui.Button] = None,
    **kwargs,
) -> nextcord.Embed:
    """
    All in One Embed, which can accept different datatypes to give different results
    Also returns a view if you pass in [dict | nextcord.ui.Button] through `button`
    title: str
    description: str
    thumbnail: str
    url: str
    color: int | nextcord.Color
    footer: dict | str
    """
    embed = nextcord.Embed()
    if color != nextcord.Color.dark_theme():
        if isinstance(color, str):
            color = int(color.replace("#", "0x"), base=16)
        embed = nextcord.Embed(color=color)
    if title:
        embed.title = title
    if description:
        if isinstance(description, dict):
            description = dict2str(description)
        if isinstance(description, list):
            description = list2str(description)
        embed.description = description
    if thumbnail:
        embed.set_thumbnail(url=thumbnail)
    if picture:
        embed.set_image(url=picture)
    if image:
        embed.set_image(url=image)
    if url:
        embed.url = url
    if fields:
        if isinstance(fields, dict):
            fields = dict2fields(fields, inline=False)
        for i in fields:
            if isinstance(i.get("value"), dict):
                i["value"] = dict2str(i["value"])
            if isinstance(i.get("value"), list):
                i["value"] = list2str(i["value"])
            embed.add_field(**i)
    if footer:
        if isinstance(footer, str):
            embed.set_footer(text=footer)
        else:
            embed.set_footer(
                text=footer.get("text", "Footer Error"),
                icon_url=footer.get(
                    "icon_url",
                    "https://colourlex.com/wp-content/uploads/2021/02/vine-black-painted-swatch.jpg",
                ),
            )
    if author:
        if isinstance(author, str):
            embed.set_author(name=author)
        elif isinstance(author, dict):
            embed.set_author(**author)
        elif isinstance(
            author,
            (nextcord.member.Member, nextcord.user.ClientUser, nextcord.guild.Guild),
        ):
            embed.set_author(name=author.name, icon_url=safe_pfp(author))

    if button:
        view = nextcord.ui.View(timeout=None)
        if isinstance(button, (nextcord.ui.Button, dict)):
            button = [button]
        for i in button[:5]:
            b = i
            if isinstance(b, dict):
                b = nextcord.ui.Button(
                    label=b.get("label", "Link"),
                    emoji=b.get("emoji", "🔗"),
                    url=b.get("url"),
                )
            view.add_item(b)
        return embed, view

    return embed


class IMDB:
    def __init__(self, RAW_DATA: dict):
        self.RAW = RAW_DATA
        self.ratings = self.create_rating()
        self.description, self.title = (
            self.RAW.get("plot", ""),
            "🎥{} [ {} ]".format(
                self.RAW.get("title", "Unavailable"), self.RAW.get("rated", "-")
            ),
        )
        self.genres = list(self.RAW.get("genres", "").split(", "))
        self.misc_data = self.generate_misc_data()
        self.image = self.RAW.get("poster")
        if not validate_url(self.image):
            self.image = None

    def create_rating(self):
        temp: list = self.RAW.get("ratings", [])
        return {i["source"]: i["value"] for i in temp}

    def generate_misc_data(self):
        misc_data = {}
        for _ in (
            "director",
            "writer",
            "runtime",
            "actors",
            "votes",
            "boxoffice",
            "rating",
            "type",
            "awards",
        ):
            misc_data[_] = self.RAW.get(_)
        return misc_data

    def generate_embed(self, color: int):
        return cembed(
            title=self.title,
            description=self.description,
            color=color,
            author={
                "name": "IMDB",
                "icon_url": "https://ia.media-imdb.com/images/M/MV5BODc4MTA3NjkzNl5BMl5BcG5nXkFtZTgwMDg0MzQ2OTE@._V1_.png",
            },
            fields={"`Information`": self.generate_misc_data()},
            url=self.RAW.get("imdburl"),
            footer={
                "text": "This command is powered by PopCat API",
                "icon_url": "https://play-lh.googleusercontent.com/ID5wHCs0FsgS018pX0e0My5z3u4cBG7dAYAr2owB9gwylWaNZTJ0pWAKl9It7ys5iEM",
            },
            image=self.image,
        )


async def imdb_embed(movie: str, color: int):
    """
    Returns details about a movie as an embed in discord
    Parameters include movies
    """
    RAW = await get_async(
        "https://api.popcat.xyz/imdb?q={query}".format(query=convert_to_url(movie)),
        kind="json",
    )
    if "error" in RAW:
        return cembed(
            title="Error",
            description="Sorry, something went wrong",
            color=color,
            author={
                "name": "IMDB",
                "icon_url": "https://ia.media-imdb.com/images/M/MV5BODc4MTA3NjkzNl5BMl5BcG5nXkFtZTgwMDg0MzQ2OTE@._V1_.png",
            },
            footer={
                "text": "Sorry for the inconvenience",
                "icon_url": "https://ia.media-imdb.com/images/M/MV5BODc4MTA3NjkzNl5BMl5BcG5nXkFtZTgwMDg0MzQ2OTE@._V1_.png",
            },
        )
    imdb = IMDB(RAW)
    return imdb.generate_embed(color=color)


async def redd(ctx, account: str = "wholesomememes", number: int = 25):
    a = await get_async(
        f"https://redditAPI.alvinbengeorge.repl.co/meme/{account}", kind="json"
    )
    embeds = []
    bot = getattr(ctx, "bot", getattr(ctx, "client", None))
    if "message" in a.keys():
        return [cembed(title="Oops", description=a["message"], color=bot.re[8])]
    memes = a
    for i in memes:
        embed = cembed(
            title=i["title"],
            image=i["url"],
            url=i["postLink"],
            footer=i["author"] + " | " + str(i["ups"]) + " votes",
            color=bot.color(ctx.guild),
            thumbnail=bot.user.avatar.url,
        )
        if not ctx.channel.nsfw:
            if i["nsfw"]:
                continue
        embeds.append(embed)
    if not embeds:
        embed = cembed(
            title="Something seems wrong",
            description="There are no posts in this accounts, or it may be `NSFW`",
            color=bot.color(ctx.guild),
        )
        embeds.append(embed)
    return embeds


async def wait_for_confirm(ctx, client, message: str, color=61620, usr=None):
    mess = await ctx.channel.send(
        embed=cembed(
            title="Confirmation",
            description=message,
            color=color,
            author=usr or getattr(ctx, "author", getattr(ctx, "user", False)),
        )
    )
    await mess.add_reaction(emoji.emojize(":check_mark_button:"))
    await mess.add_reaction(emoji.emojize(":cross_mark_button:"))

    person = usr

    def check(reaction, user):
        return (
            reaction.message.id == mess.id
            and reaction.emoji
            in [
                emoji.emojize(":check_mark_button:"),
                emoji.emojize(":cross_mark_button:"),
            ]
            and user == getattr(ctx, "author", getattr(ctx, "user", None))
            if person is None
            else person == user
        )

    reaction, user = await client.wait_for("reaction_add", check=check)
    if reaction.emoji == emoji.emojize(":check_mark_button:"):
        await mess.delete()
        return True
    if reaction.emoji == emoji.emojize(":cross_mark_button:"):
        await mess.edit(
            embed=cembed(
                title="Ok cool",
                description="Aborted",
                color=nextcord.Color(color),
                author=user,
            )
        )
        try:
            await mess.clear_reactions()
        except Exception:
            print("Failed to clear reactions", ctx.guild.id)
        return False


def equalise(all_strings: List[str]):
    """
    Makes all string same size
    """
    maximum = max(list(map(len, all_strings)))
    return {i: i + " " * (maximum - len(i)) for i in all_strings}


def reset_emo(client):
    emo = assets.Emotes(client)
    return emo


def subtract_list(l1: List, l2: List):
    a = []
    for i in l1:
        if i not in l2:
            a.append(i)
    return a


def extract_color(color: str):
    """
    Extracts RGB from Hex
    """
    color = color.replace("#", "0x")
    try:
        return nextcord.Color(int(color, base=16)).to_rgb()
    except Exception:
        print(traceback.format_exc())


def svg2png(url: str):
    """Convert SVG image (url) to PNG format."""
    res = requests.get(
        SVG2PNG_API_URI, params=[("url", url), ("token", SVG2PNG_API_TOKEN)]
    )
    return res.content


async def get_name(url: str):
    """
    get Youtube Video Name through Async
    """
    a = await get_async(url)
    return (
        a[a.find("<title>") + len("<title>") : a.find("</title>")]
        .replace("&amp;", "&")
        .replace(" - YouTube", "")
        .replace("&#39;", "'")
    )


async def get_async(url: str, headers: dict = {}, kind: str = "content"):
    """
    Simple Async get request
    """
    output = ""
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as resp:
            if kind == "json":
                try:
                    output = await resp.json()
                except Exception as e:
                    print(e)
                    output = await resp.text()
            elif kind.startswith("file>"):
                f = await aiofiles.open(kind[5:], mode="wb")
                await f.write(await resp.read())
                await f.close()
                return
            elif kind == "fp":
                output = BytesIO(await resp.read())
            else:
                output = await resp.text()

        await session.close()
    return output


async def post_async(api: str, header: dict = {}, json: dict = {}):
    async with aiohttp.ClientSession() as session:
        async with session.post(api, headers=header, json=json) as resp:
            if resp.headers["Content-Type"] != "application/json":
                return await resp.read(), resp.headers["Content-Type"]
            return await resp.json(), resp.headers["Content-Type"]


def suicide_m(client, color):
    """
    Returns Suicide Embed
    """
    return cembed(
        title="Suicide and Self harm prevention",
        description="\n".join(
            [
                i.strip()
                for i in """ 
    You are not alone ...
    And your Life is worth a lot ..
    SPEAK OUT !!


    If you're having any suicidal thoughts, please seek help immediately. Talk about what bothers you and what can be done to solve the problem


    international suicide helplines>>> https://www.opencounseling.com/suicide-hotlines
        """.split(
                    "\n"
                )
            ]
        ),
        color=color,
        thumbnail=client.user.avatar.url,
        picture="https://www.humanium.org/en/wp-content/uploads/2019/09/shutterstock_1140282473-scaled.jpg",
    )


def check_end(s: str):
    if not s.endswith("/videos"):
        return s + "/videos"
    return s


def check_voice(ctx):
    """
    Checks if the user is in the Voice Channel
    """
    try:
        mem = [member.id for member in ctx.guild.voice_client.channel.members]
    except:
        mem = []
    return getattr(ctx, "author", getattr(ctx, "user", None)).id in mem


async def player_reaction(mess):
    await mess.add_reaction("⏮")
    await mess.add_reaction("⏸")
    await mess.add_reaction("▶")
    await mess.add_reaction("🔁")
    await mess.add_reaction("⏭")
    await mess.add_reaction("⏹")
    await mess.add_reaction(emoji.emojize(":keycap_*:"))
    await mess.add_reaction(emoji.emojize(":upwards_button:"))
    await mess.add_reaction(emoji.emojize(":downwards_button:"))
    await mess.add_reaction(emoji.emojize(":musical_note:"))


def remove_all(original, s):
    """
    Removes specified `s` from the string
    """
    for i in s:
        original = original.replace(i, "")
    return original


def safe_pfp(user: Union[nextcord.Member, nextcord.guild.Guild]):
    if user is None:
        return
    if isinstance(user, nextcord.guild.Guild):
        return (
            str(user.icon)
            if user.icon
            else "https://cdn.logojoy.com/wp-content/uploads/20210422095037/discord-mascot.png"
        )
    return user.avatar.url if user.avatar else user.default_avatar.url


def defa(*types, default=None, choices=[], required=False):
    if types == []:
        return SlashOption(default=default, required=False)
    if choices != []:
        return SlashOption(choices=choices, default=default, required=required)
    return SlashOption(channel_types=types, required=required)


async def ly(song, color: int):
    """
    Returns lyrics Embed of a song
    """
    j = await get_async(
        f"https://api.popcat.xyz/lyrics?song={convert_to_url(song)}", kind="json"
    )
    return cembed(
        title=j.get("title", "Couldnt get title"),
        description=j.get("lyrics", "Unavailable"),
        color=color,
        thumbnail=j.get("image"),
        author={
            "name": j.get("artist", "Unavailable"),
            "icon_url": "https://cdn.iconscout.com/icon/free/png-256/youtube-music-4054283-3352965.png",
        },
    )


async def isReaction(ctx, embed, clear=False):
    """
    Adaptive solution for Interaction, Reaction and Prefix commands
    """
    if isinstance(ctx, nextcord.message.Message):
        message = await ctx.edit(embed=embed)
    else:
        message = await ctx.send(embed=embed)
    if clear:
        try:
            await message.clear_reactions()
        except:
            pass


def uniq(li):
    return list(Counter(li).keys())


def timestamp(i):
    return time.ctime(i)


class SpaceX:
    """
    SpaceX Simple API -> Coded By alvinbengeorge
    """

    def __init__(self):
        self.name = None
        self.time = None
        self.fno = None
        self.thumbnail = None
        self.youtube = None
        self.wikipedia = None
        self.crew = []
        self.id = None

    async def setup(self):
        js = await get_async(
            "https://api.spacexdata.com/v4/launches/latest", kind="json"
        )
        self.name = js["name"]
        self.time = timestamp(int(js["date_unix"]))
        self.thumbnail = js["links"]["patch"]["large"]
        self.youtube = js["links"]["webcast"]
        self.wikipedia = js["links"]["wikipedia"]
        self.crew = js["crew"]
        self.id = js["id"]
        self.fno = js["flight_number"]

    async def history(self, color: Union[nextcord.Color, int]):
        jso = await get_async("https://api.spacexdata.com/v4/history", kind="json")
        embeds = []
        for i in jso[::-1]:
            embed = cembed(
                title=i["title"],
                description=i["details"],
                color=color,
                thumbnail="https://www.spacex.com/static/images/share.jpg",
                footer=i["id"] + " | " + str(timestamp(i["event_date_unix"])),
            )
            embeds.append(embed)
        print("Done")
        return embeds


class Meaning:
    """
    Meaning Simple API -> Coded by alvinbengeorge
    """

    def __init__(self, word: str, color: Union[int, nextcord.Color]):
        self.word = (word,)
        self.url = "https://api.dictionaryapi.dev/api/v2/entries/en/" + convert_to_url(
            word
        )
        self.result = None
        self.embeds = []
        self.color = color
        self.thumbnail = "https://i.pinimg.com/originals/75/7c/da/757cda6d9ac2a7f0db09c41b83931b53.png"

    async def setup(self):
        self.result = await get_async(self.url, kind="json")
        return self.result

    def create_texts(self):
        if self.result == None:
            raise IndexError("Run setup first |coro|")
        elif type(self.result) == dict:
            a = cembed(
                title=self.result["title"],
                description=self.result["message"],
                color=self.color,
                thumbnail="https://c.tenor.com/IHdlTRsmcS4AAAAC/404.gif",
            )
            self.embeds.append(a)
        else:
            r = self.result
            description = f"**Phonetics**: {r[0].get('phonetic')}\n"
            description += (
                f"**Part of speech**: {r[0]['meanings'][0].get('partOfSpeech')}"
            )
            embed = cembed(
                title=r[0]["word"],
                description=description,
                color=self.color,
                thumbnail=self.thumbnail,
            )
            self.embeds.append(embed)
            definitions = r[0]["meanings"][0]["definitions"]
            page = 0
            for i in definitions:
                page += 1
                des = i["definition"]
                example = i.get("example")
                synonyms = i.get("synonyms")
                antonyms = i.get("antonyms")
                if example is None:
                    example = f"{page} of {len(definitions)}"
                embed = cembed(
                    title=r[0]["word"],
                    description=des,
                    color=self.color,
                    footer=example,
                    thumbnail=self.thumbnail,
                )
                if synonyms and synonyms != []:
                    embed.add_field(
                        name="Synonyms", value=", ".join(synonyms), inline=True
                    )
                if antonyms and antonyms != []:
                    embed.add_field(
                        name="Antonyms", value=",".join(antonyms), inline=True
                    )
                self.embeds.append(embed)
        return self.embeds


async def animals(client, ctx, color: Union[int, nextcord.Color], number: int = 10):
    d2 = await get_async(
        f"https://zoo-animal-api.herokuapp.com/animals/rand/{number}", kind="json"
    )
    user = getattr(ctx, "author", getattr(ctx, "user", None))
    embeds = []
    for d in d2:
        embed = cembed(
            title=d["name"],
            description=d["diet"],
            color=color,
            thumbnail=client.user.avatar.url,
            image=d["image_link"],
            footer=d["active_time"],
            author=user,
            fields={
                "Latin name": d["latin_name"],
                "Animal Type": d["animal_type"],
                "Length": f"{d['length_min']} to {d['length_max']} feet",
                "Weight": f"{int(float(d['weight_min'])*0.453592)} to {int(float(d['weight_max'])*0.453592)} kg",
                "Life Span": f"{d['lifespan']} years",
                "Habitat": f"{d['habitat']}, {d['geo_range']}",
            },
        )

        embeds.append(embed)
    return embeds


def audit_check(log):
    latest = log[0]
    che = log[:10]
    initiators = Counter([i.user for i in che])
    for i in initiators:
        tim = time.time() - 120
        offensive = [
            nextcord.AuditLogAction.kick,
            nextcord.AuditLogAction.ban,
            nextcord.AuditLogAction.channel_delete,
        ]
        actions = [
            j.action
            for j in che
            if j.user == i and j.action in offensive and j.created_at.timestamp() > tim
        ]
        if len(actions) > 5:
            return i


def check_command(ctx):
    ctx.bot.re[0] += 1
    a = ctx.bot.config["commands"]
    if a.get(str(ctx.command.name)):
        if ctx.guild.id in a[ctx.command.name]:
            return False
    return True


async def quo(color):
    a = await get_async("https://api.quotable.io/random", kind="json")
    footer = ", ".join(a["tags"])
    description = a["content"]
    title = a["author"]
    return cembed(title=title, description=description, footer=footer, color=color)


co = """
import nextcord
import utils.assets
import time
import traceback
import utils.External_functions as ef
from nextcord.ext import commands

# Use nextcord.slash_command()

def requirements():
    return []

class {name}(commands.Cog):
    def __init__(self, CLIENT):
        self.CLIENT = CLIENT


def setup(client,**i):
    client.add_cog({name}(client,**i))
""".strip()


def cog_creator(name: str):
    if f"{name}.py" in os.listdir("cogs/"):
        return "Already exists"

    with open(f"cogs/{name}.py", "w") as f:
        f.write(co.format(name=name))

    return "Done"


class Attributor:
    def __init__(self, data: dict):
        for i in data:
            setattr(self, i, data[i])


class Pokemon:
    def __init__(self):
        self.pokemons = {}
        for i in requests.get(
            "https://pokeapi.co/api/v2/pokemon/?limit=1000000"
        ).json()["results"]:
            self.pokemons.update({i["name"]: i["url"]})

    def search(self, name: str):
        return [
            i
            for i in self.pokemons
            if regex.findall(name.lower().replace("_", r"\S{1}"), i.lower())
        ][:25]

    async def get_stats(self, pokemon: str, embed: bool = False, color=28656):
        try:
            d = await get_async(self.pokemons[pokemon], kind="json")
        except:
            if embed:
                return cembed(description="Not found", color=color)
            return {"message": "Not Found"}

        if not embed:
            return d
        embed = cembed(
            title=pokemon,
            color=color,
            thumbnail=d["sprites"]["front_default"],
            fields={i["stat"]["name"]: i["base_stat"] for i in d["stats"]},
        )
        embed.add_field(name="Weight", value=d["weight"])
        embed.add_field(
            name="Abilities",
            value="\n".join([i["ability"]["name"] for i in d["abilities"]]),
        )
        return embed


def validate_url(url: str) -> bool:
    """
    Checks if the url is valid or not
    """
    prepared_request = PreparedRequest()
    try:
        prepared_request.prepare_url(url, None)
        return True
    except MissingSchema as e:
        return False


class TechTerms:
    def __init__(self):
        pass

    async def search(self, query):
        """
        async search a query from techterms.com
        """
        if not query:
            l = await get_async("https://techterms.com/ac?query=a")
        else:
            l = await get_async(f"https://techterms.com/ac?query={query}")
        return [i["value"] for i in json.loads(l)]

    async def get_page_as_embeds(self, query):
        url = f"https://techterms.com/definition/{query.lower().replace(' ', '_')}"
        content = await get_async(url)
        if "Term not found" in content:
            return [
                {
                    "title": "Not found",
                    "description": "The definition that you're looking for is not available in TechTerms",
                }
            ]
        soup = BeautifulSoup(content, "html.parser")
        l = soup.find_all("div", class_="card hasheader")[0]
        line = chr(9600) * 30
        title = l.h1.get_text()
        embeds = []
        ps = l.find_all("p")
        n = 0
        for i in ps:
            n += 1
            description = f"```\n{line}\n{i.get_text()}\n{line}\n```"
            embed = {
                "title": title,
                "description": description,
                "url": url,
                "footer": {
                    "text": f"Source: TechTerms.com | {n} of {len(ps)}",
                    "icon_url": "https://play-lh.googleusercontent.com/heAUDFlRj040etj32Pve296Az4r_sgsUECjZNqSJOQAWA96qeqWdfE0pxtx-JNbIbG4",
                },
                "image": "https://play-lh.googleusercontent.com/MDWegEXmQwrcDJBbgjO_83EHp4-PIBdb_IXfYcUQLO5JmQ9w7Td-ZOZ7mKx12Rvctpz4=w600-h300-pc0xffffff-pd",
            }
            embeds.append(embed)
        return embeds


class Proton:
    def __init__(self):
        self.games = []

    async def setup(self):
        m = await get_async("https://protondb.max-p.me/games", kind="json")
        for i in m:
            t = list(i.items())
            self.games.append((t[0][1], t[1][1]))

    def search_game(self, name):
        search_results = []
        name = name.lower()
        for i in self.games:
            if name in i[1].lower():
                search_results.append(i)
        return search_results

    async def report(self, name):
        if self.search_game(name) == []:
            return []
        id = self.search_game(name)[0][0]

        report = await get_async(
            f"https://protondb.max-p.me/games/{id}/reports", kind="json"
        )
        reports = []
        for i in report:
            details = f"```\n{i['notes'] if i['notes'] else '-'}\n```\n\n```yml\nCompatibility: {i['rating']}\nOperating System: {i['os']}\nGPU Driver: {i['gpuDriver']}\nProton: {i['protonVersion']}\nSpecs: {i['specs']}\n```"

            reports.append(
                {
                    "title": str([j[1] for j in self.games if j[0] == id][0]),
                    "description": details,
                    "footer": timestamp(int(i["timestamp"])),
                    "thumbnail": "https://live.mrf.io/statics/i/ps/www.muylinux.com/wp-content/uploads/2019/01/ProtonDB.png?width=1200&enable=upscale",
                    "image": "https://pcgw-community.sfo2.digitaloceanspaces.com/monthly_2020_04/chrome_a3Txoxr2j5.jpg.4679e68e37701c9fbd6a0ecaa116b8e5.jpg",
                }
            )
        return reports


class PublicAPI:
    def __init__(self, client):
        self.BASE_URL = "https://api.publicapis.org/entries"
        self.data = {}
        self.all_names = []
        self.client = client
        self.author = None

    async def update(self, author):
        if self.data == {}:
            self.data = await get_async(self.BASE_URL, kind="json")
            self.all_names = [i["API"] for i in self.data["entries"]]
        self.author = author

    def search_result(self, name):
        if not self.data:
            return []

        return [i for i in self.all_names if name.lower() in i.lower()]

    def find(self, name):
        return self.all_names.index(name)

    def flush(self):
        self.data.clear()
        self.all_names.clear()

    def return_embed(self, index, color):
        if index == -1:
            return cembed(
                title="Not Found",
                description="The API you're looking for is not found",
                color=color,
            )
        info = self.data["entries"][index]
        return cembed(
            title=info["API"],
            description=info["Description"],
            color=color,
            url=info.get("Link"),
            fields=[
                {"name": k, "value": v if v else "-", "inline": False}
                for k, v in info.items()
            ],
            footer=f"{self.data['count']} Entries",
            author=self.author,
            thumbnail="https://www.elemental.co.za/cms/resources/uploads/blog/86/926f6aaba773.png",
        )


def delete_all(s: str, ch: Union[List, str]):
    for i in ch:
        s = s.replace(i, "")
    return s


class MineCraft:
    def __init__(self, client):
        self.client = client
        self.BASE_URL = "https://www.digminecraft.com/"
        self.HTML = requests.get(
            "https://www.digminecraft.com/effects/index.php"
        ).content.decode()
        self.soup = BeautifulSoup(self.HTML, "html.parser")
        self.CATEGORIES = {}

    def all_categories(self) -> dict:
        for category in self.soup.find_all("div", class_="menu")[1:]:
            for tables in category.find_all("ul"):
                for rows in tables.find_all("li"):
                    if a := rows.a:
                        self.CATEGORIES[a.get_text()] = self.BASE_URL + a["href"]

        return self.CATEGORIES

    async def get_options(self, URL: str) -> str:
        strings = [""]
        self.HTML = await get_async(URL)
        self.soup = BeautifulSoup(self.HTML, "html.parser")

        for i in self.soup.find_all("a", class_="list-group-item"):
            strings[
                -1
            ] += f"[{i.get_text().strip()}](https://www.digminecraft.com{i['href']})\n"
            if len(strings[-1]) % 10 == 0:
                strings.append("")

        return strings

    def create_sections(self, soup: BeautifulSoup) -> dict:
        article = soup.find("div", class_="article").div
        sections = [
            {
                "title": article.find("h1").get_text().upper(),
                "description": "This is created from DigMineCraft.com",
            },
            {"title": article.find("h1").get_text().upper(), "description": ""},
        ]
        for i in article.find_all("p"):
            if i.h2:
                sections[1]["description"] += f"**{i.get_text().strip()}**\n"
            else:
                sections[1]["description"] += i.get_text().strip() + "\n"

        return sections

    async def get_article(self, URL: str) -> nextcord.Embed:
        a = await get_async(URL)
        soup = BeautifulSoup(a, "html.parser")
        all_sections = self.create_sections(soup)
        embeds = []
        for i in all_sections:
            embeds.append(
                cembed(
                    **i,
                    author=self.client.user,
                    color=self.client.re[8],
                    thumbnail="https://www.digminecraft.com/mechanism_recipes/images/completed_beacon.png",
                )
            )
        return embeds


def cog_requirements(name: str):
    return importlib.import_module(f"cogs.{name}").requirements()


def error_message(error: str):
    return cembed(
        title="An Error has occured",
        description=error,
        color=nextcord.Color.red(),
        thumbnail="https://raw.githubusercontent.com/alvinbengeorge/alfred-discord-bot/default/error.png",
    )


def dict2fields(d: dict, inline: bool = True):
    return [{"name": i, "value": d[i], "inline": inline} for i in d]


def dict2str(d: dict):
    return "\n".join(f"`{i.upper()}: ` {j}" for i, j in d.items())


def list2str(l: list):
    return "• " + "\n• ".join([str(_) for _ in l])


def line_strip(text: str):
    return "\n".join([i.strip() for i in text.split("\n")])


def nunchaku(var, t):
    if not var:
        return t()
    return var


async def pypi_call(package: str, ctx):
    j = await get_async(f"https://pypi.org/pypi/{package}/json", kind="json")
    return PyPi(j, ctx).render_embeds()


class PyPi:
    def __init__(self, DICTIONARY, ctx: commands.context.Context):
        self.ctx = ctx
        self.AUTHOR: nextcord.Member = None
        if isinstance(ctx, nextcord.Interaction):
            self.BOT = ctx.client
            self.AUTHOR = ctx.user
        else:
            self.BOT = ctx.bot
            self.AUTHOR = ctx.author
        self.DICTIONARY: dict = DICTIONARY
        self.DEFAULT_IMAGE = (
            "https://miro.medium.com/max/1200/1*8Zh-mzLnVMDsbvXdKsU4lw.png"
        )
        self.DEFAULT_THUMBNAIL = "https://i2.wp.com/sefiks.com/wp-content/uploads/2020/03/pip_big.jpg?resize=496%2C496&ssl=1"

    def render_embeds(self):
        if "message" in self.DICTIONARY:
            return [
                cembed(
                    title="Error",
                    color=nextcord.Color.red(),
                    description=self.DICTIONARY.get(
                        "message", "Could not get the error message"
                    ),
                    thumbnail=self.DEFAULT_THUMBNAIL,
                    image=self.DEFAULT_IMAGE,
                    author=self.AUTHOR,
                    fields={
                        "Solutions": "Find if the package exists, this can also happen when the API is down"
                    },
                )
            ]
        embeds = [self.first_page()]
        return embeds

    def requirements(self, info: dict):
        if dist := info.get("requires_dist", ""):
            dist = "```yml\n- " + "\n- ".join([_ for _ in dist[:5]]) + "\n```"
        return f"`Requires dist: ` {dist}\n`Requires Python: ` {info.get('requires_python')}"

    def first_page(self):
        info: dict = self.DICTIONARY["info"]
        description = info.get("summary")
        self.footer = {
            "text": f'Latest Version: {info["version"]}',
            "icon_url": self.DEFAULT_THUMBNAIL,
        }
        project_urls = "\n".join(
            [
                f"`{i.upper()}: ` [🔗]({j})"
                for i, j in nunchaku(info["project_urls"], dict).items()
            ]
        )
        title, url = info.get("name"), info.get("package_url")
        fields = {
            "Requirements": self.requirements(info),
            "Classifiers": "```yml\n- "
            + "\n- ".join(info["classifiers"][:5])
            + "\n```",
            "Stats": f'`LICENSE: ` {info.get("license")} \n{project_urls}',
            "Releases": "\n".join(
                [
                    f"[{i}](https://pypi.org/project/{title}/{i})"
                    for i in self.DICTIONARY["releases"]
                ][1:5]
            ),
            "Command": f'pip3 install {title}=={info["version"]}',
        }

        image = self.DEFAULT_IMAGE
        for i in nunchaku(info["project_urls"], dict).values():
            if i.startswith("https://github.com/"):
                image = f"https://opengraph.githubassets.com/1/{'/'.join(i.split('/')[3:5])}"
                break

        return cembed(
            title=title,
            url=url,
            description=description,
            color=self.BOT.color(self.ctx.guild),
            author=self.AUTHOR,
            footer=self.footer,
            fields=fields,
            thumbnail=self.DEFAULT_THUMBNAIL,
            image=image,
        )


class PollGraph:
    def __init__(self, CLIENT: commands.Bot, INTER: nextcord.Interaction):
        self.INTER, self.CLIENT, self.CREATOR = INTER, CLIENT, None
        self.d: dict = {}
        self.options: dict = {}
        self.reactions: dict = {}
        self.font = fm.FontProperties(fname="utils/fonts/xkcd-script.ttf")
        self.question = ""
        self.emojis: List[str] = [
            emoji.emojize(f":keycap_{i+1}:") if i < 10 else Emoji_alphabets[i - 10]
            for i in range(35)
        ]

    def extract_from_message(self, message):
        description = message.embeds[0].description.split("\n\n")
        self.question = "\n\n".join(description[:-1])
        self.options = dict(
            [(j.strip() for j in i.split("|")) for i in description[-1].split("\n")]
        )
        for i in message.reactions:
            if i.emoji not in self.options:
                continue
            self.reactions.update({self.options[i.emoji]: i.count - 1})
        self.CREATOR = message.embeds[0].author

    def arrange_data(self):
        l, v = [], []
        for i, j in self.reactions.items():
            l.append(i)
            v.append(j / (sum(self.reactions.values()) or 1))
        return l, v

    def generate_image(self):
        labels, values = self.arrange_data()
        values = np.array(values)
        # _, ax = plt.subplots()
        # ax.pie(values, labels=labels)
        with plt.xkcd():
            fig = plt.figure(figsize=(6, 5))
            ax = fig.add_axes((0.1, 0.2, 0.8, 0.7))

            # plot fig
            wedges, *_ = ax.pie(
                values,  # data
                wedgeprops=dict(width=0.65),  # width of the donut
                startangle=-40,  # starting angle
                shadow=True,  # shadow for the donut
                autopct="%.1f%%",  # annotations
                # colors = np.random.permutation(list(XKCD_COLORS.values()))
                colors=[
                    mcolors.hsv_to_rgb((156 / 255, 72 / 100, abs(0.7 - v)))
                    for v in (values / np.sum(values))
                ],
                textprops={"fontproperties": self.font, "fontsize": 15},
            )

            bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
            kw = dict(
                arrowprops=dict(arrowstyle="->"), bbox=bbox_props, zorder=0, va="center"
            )
            ax.xaxis.set_ticks_position("bottom")

            for i, p in enumerate(wedges):
                ang = (p.theta2 - p.theta1) / 2.0 + p.theta1

                y = np.sin(np.deg2rad(ang))
                x = np.cos(np.deg2rad(ang))

                horizontalalignment = (
                    "right" if int(np.sign(x) == -1) else "left"
                )  # {-1: "right", 1: "left"}[int(np.sign(x))]
                connectionstyle = "angle,angleA=0,angleB={}".format(ang)

                kw["arrowprops"].update({"connectionstyle": connectionstyle})

                ax.annotate(
                    labels[i],
                    xy=(x, y),
                    xytext=(1.35 * np.sign(x), 1.4 * y),
                    horizontalalignment=horizontalalignment,
                    fontproperties=self.font,
                    size=20,
                    **kw,
                )

        bt = BytesIO()
        plt.savefig(bt, format="png")
        plt.close()
        bt.seek(0)

        return bt

    def inverted_dict(self, dictionary: dict):
        return {v: k for k, v in dictionary.items()}

    def generate_embed(self):
        description = {
            f"{self.inverted_dict(self.options)[k]} | {k}": v
            for k, v in self.reactions.items()
        }
        return nextcord.File(fp=self.generate_image(), filename="result.png"), cembed(
            title="Poll Results",
            description=dict2str(description),
            color=self.CLIENT.color(self.INTER.guild),
            author=self.INTER.user,
            image="attachment://result.png",
            thumbnail=safe_pfp(self.INTER.guild),
            footer={
                "text": f"This Poll was created by {self.CREATOR.name}",
                "icon_url": getattr(self.CREATOR, "icon_url"),
            },
            fields={"`QUESTION`": self.question},
        )


def get_all_slash_commands(Client: commands.Bot):
    return {i.name: i for i in Client.get_all_application_commands()}


def slash_and_sub(Client: commands.Bot, cog=None):
    st = []
    a = get_all_slash_commands(Client=Client)
    for i, j in a.items():
        _condition = True
        if cog:
            _condition = j.parent_cog == cog
        if not _condition:
            continue
        if not getattr(j, "children", None):
            st.append(f"/{i}")
            continue
        for sub in j.children:
            st.append(f"/{i} {sub}")
    return st


def check_slash(inter: nextcord.Interaction):
    inter.client.re[0] += 1
    command: dict = inter.data
    command_name = command.get("name")
    subcommand_name = ""
    if isinstance(options := command.get("options", []), list) and len(options) > 0:
        if isinstance(inter.application_command, nextcord.SlashApplicationSubcommand):
            subcommand_name = f" {options[0].get('name','')}"

    full_command = f"/{command_name}{subcommand_name}".strip()
    if full_command not in inter.client.config["slash"]:
        return True
    if inter.guild.id in inter.client.config["slash"][full_command]:
        return False
    return True


def color(re: list, guild: nextcord.Guild = None):
    """
    Modifiable color server-wise
    """
    result = re[5].get(getattr(guild, "id", None)) or re[8]
    if result == True:
        return guild.me.color.value
    return result


async def itnaChota(url: str):
    response = {}
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://itnachota.herokuapp.com/api/create/link",
            json={"link": url},
        ) as resp:
            response = await resp.json()
    if "code" in response:
        return "itnachota.shashankkumar.me/" + response["code"]
    else:
        return "Sorry, {}".format(response["message"])
