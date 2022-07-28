from io import BytesIO
from string import ascii_letters
from bs4 import BeautifulSoup
from cv2 import DescriptorMatcher_BRUTEFORCE_HAMMING
from nextcord import SlashOption
from dotenv import load_dotenv
from functools import lru_cache
from datetime import datetime
from collections import Counter
from requests.models import PreparedRequest
from requests.exceptions import MissingSchema
from typing import List, Union

import psutil
import os
import time
import nextcord
import random
import imdb
import emoji
import youtube_dl
import urllib.parse
import urllib
import aiohttp
import traceback
import aiofiles
import utils.assets as assets
import json
import importlib
import re as regex
import requests

ydl_op = {
    "format": "bestaudio/best",
    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "384",
        }
    ],
    "noplaylist": "True",
}
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
            type=nextcord.ActivityType.watching,
            name="Nextcord People stab their people",
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


@lru_cache(maxsize=512)
def youtube_info(url):
    with youtube_dl.YoutubeDL(ydl_op) as ydl:
        info = ydl.extract_info(url, download=False)
    return info


def timestamp(i):
    return datetime.fromtimestamp(i)


def convert_to_url(name):
    name = urllib.parse.quote(name)
    return name


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
    author=False,
    fields=None,
    image=None,
):
    embed = nextcord.Embed()
    if color != nextcord.Color.dark_theme():
        if type(color) == int:
            embed = nextcord.Embed(color=nextcord.Color(value=color))
        else:
            embed = nextcord.Embed(color=color)
    if title:
        embed.title = title
    if description:
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
        elif isinstance(author, nextcord.member.Member):
            embed.set_author(name=author.name, icon_url=safe_pfp(author))
        pass

    return embed


def imdb_embed(movie="", re: list = {8: 5160}):
    """
    Returns details about a movie as an embed in discord
    Parameters include movies
    """
    if movie == "":
        return cembed(
            title="Oops",
            description="You must enter a movie name",
            color=nextcord.Color.red(),
        )
    try:
        ia = imdb.IMDb()
        movie = ia.search_movie(movie)
        title = movie[0]["title"]
        mov = ia.get_movie(movie[0].getID())
        di = {
            "Cast": ", ".join([str(i) for i in mov["cast"]][:5]),
            "writer": ", ".join([str(j) for j in mov["writer"]]),
            "Rating": ":star:" * int(mov["rating"]),
            "Genres": ", ".join(mov["genres"]),
            "Year": mov["year"],
            "Director": mov.get("director"),
        }
        plot = mov["plot"][0]
        image = movie[0]["full-size cover url"]
        embed = cembed(title=title, description=plot, color=re[8], image=image)
        n = 0
        for i in di:
            n += 1
            embed.add_field(name=i, value=di[i], inline=(n % 3 == 0))
        return embed
    except Exception as e:
        print(traceback.format_exc())
        return cembed(
            title="Oops",
            description="Something went wrong, check if the name is correct",
            color=re[8],
        )


async def redd(ctx, account: str = "wholesomememes", number: int = 25):
    a = await get_async(
        f"https://meme-api.herokuapp.com/gimme/{account}/{number}", kind="json"
    )
    embeds = []
    bot = getattr(ctx, "bot", getattr(ctx, "client", None))
    if "message" in a.keys():
        return [cembed(title="Oops", description=a["message"], color=bot.re[8])]
    memes = a["memes"]
    for i in memes:
        embed = cembed(
            title=i["title"],
            image=i["url"],
            url=i["postLink"],
            footer=i["author"] + " | " + str(i["ups"]) + " votes",
            color=bot.re[8],
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
            color=bot.re[8],
        )
        embeds.append(embed)
    return embeds


def protect(text):
    return (
        str(text).find("username") == -1
        and str(text).find("os.") == -1
        and str(text).find("ctx.") == -1
        and str(text).find("__import__") == -1
        and str(text).find("sys.") == -1
        and str(text).find("psutil.") == -1
        and str(text).find("clear") == -1
        and str(text).find("dev_users") == -1
        and str(text).find("remove") == -1
        and str(text).find("class.") == -1
        and str(text).find("subclass()") == -1
        and str(text).find("client") == -1
        and str(text).find("quit") == -1
        and str(text).find("exit") == -1
        and str(text).find("while True") == -1
    )


async def devop_mtext(client, channel, color):
    await channel.delete_messages(
        [i async for i in channel.history(limit=100) if not i.pinned][:100]
    )
    text_dev = (
        "You get to activate and reset certain functions in this channel \n"
        "💾 for saving to file \n"
        "⭕ for list of all servers \n"
        "❌ for exiting \n"
        "🔥 for restart\n"
        "📊 for current load\n"
        "❕ for current issues\n"
        "" + emoji.emojize(":satellite:") + " for speedtest\n"
        "" + emoji.emojize(":black_circle:") + " for clear screen\n"
    )
    embed = cembed(
        title="DEVOP", description=text_dev, color=color, footer="Good day Master Wayne"
    )
    embed.set_thumbnail(url=client.user.avatar.url)
    mess = await channel.send(embed=embed)
    await mess.add_reaction("💾")
    await mess.add_reaction("⭕")
    await mess.add_reaction("❌")
    await mess.add_reaction(emoji.emojize(":fire:"))
    await mess.add_reaction(emoji.emojize(":bar_chart:"))
    await mess.add_reaction("❕")
    await mess.add_reaction(emoji.emojize(":satellite:"))
    await mess.add_reaction(emoji.emojize(":black_circle:"))
    await mess.add_reaction(emoji.emojize(":laptop:"))


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


def youtube_download(url: str):
    with youtube_dl.YoutubeDL(ydl_op) as ydl:
        info = ydl.extract_info(url, download=False)
        URL = info["formats"][0]["url"]
    return URL


def youtube_download1(url: str):
    with youtube_dl.YoutubeDL(ydl_op) as ydl:
        info = ydl.extract_info(url, download=False)
        name = info["title"]
        URL = info["formats"][0]["url"]
    return (URL, name)


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
                return await resp.read()
            return await resp.json()


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
        mem = [ID for ID in ctx.guild.voice_client.channel.members]
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
        return user.icon
    return user.avatar.url if user.avatar else user.default_avatar.url


def defa(*types, default=None, choices=[], required=False):
    if types == []:
        return SlashOption(default=default, required=False)
    if choices != []:
        return SlashOption(choices=choices, default=default, required=required)
    return SlashOption(channel_types=types, required=required)


async def ly(song, re: List):
    """
    Returns lyrics Embed of a song
    """
    j = await get_async(
        f"https://api.popcat.xyz/lyrics?song={convert_to_url(song)}", kind="json"
    )
    return cembed(
        title=j.get("title", "Couldnt get title"),
        description=j.get("lyrics", "Unavailable"),
        color=re[8],
        thumbnail=j.get("image"),
        footer=j.get("artist", "Unavailable"),
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

    def __init__(self, color: Union[int, nextcord.Color]):
        self.name = None
        self.time = None
        self.fno = None
        self.thumbnail = None
        self.youtube = None
        self.wikipedia = None
        self.crew = []
        self.id = None
        self.color = color

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

    async def history(self):
        jso = await get_async("https://api.spacexdata.com/v4/history", kind="json")
        embeds = []
        for i in jso[::-1]:
            embed = cembed(
                title=i["title"],
                description=i["details"],
                color=self.color,
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
            }
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

class <name>(commands.Cog):
    def __init__(self, CLIENT):
        self.CLIENT = CLIENT


def setup(client,**i):
    client.add_cog(<name>(client,**i))
""".strip()


def cog_creator(name: str):
    if f"{name}.py" in os.listdir("cogs/"):
        return "Already exists"

    with open(f"cogs/{name}.py", "w") as f:
        f.write(co.replace("<name>", name))

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
            title=pokemon, color=color, thumbnail=d["sprites"]["front_default"]
        )
        for i in d["stats"]:
            embed.add_field(name=i["stat"]["name"], value=i["base_stat"])
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
    return '\n'.join(f"`{i.upper()}: ` {j}" for i, j in d.items())


def line_strip(text: str):
    return "\n".join([i.strip() for i in text.split("\n")])

def nunchaku(var, t):
    if not var:
        return t()
    return var


class Detector:
    def __init__(self, CLIENT):
        self.deathrate = {}
        self.CLIENT = CLIENT

    async def process_message(self, message: nextcord.message.Message):
        content = "".join([i for i in message.clean_content if i in ascii_letters])
        if content:
            if message.author.id not in self.deathrate:
                self.deathrate[message.author.id] = 0

            try:
                preds = await post_async(
                    "https://suicide-detector-api-1.yashvardhan13.repl.co/classify",
                    json={"text": content},
                )
            except AttributeError:
                preds = {"result": None}

            if preds.get("result") == "Sucide":
                self.deathrate[message.author.id] += 1
            else:
                return None

            if self.deathrate.get(message.author.id) >= 10:
                self.deathrate[message.author.id] = 0
                return suicide_m(self.CLIENT, self.CLIENT.re[8])
        else:
            return None

async def pypi_call(package: str, ctx):
    j = await get_async(f"https://pypi.org/pypi/{package}/json", kind="json")
    return PyPi(j, ctx).render_embeds()

class PyPi:
    def __init__(self, DICTIONARY, ctx):
        self.COLOR: int = 5160
        self.AUTHOR: nextcord.Member = None
        if isinstance(ctx, nextcord.Interaction):
            self.COLOR = ctx.client.re[8]
            self.AUTHOR = ctx.user
        else:
            self.COLOR = ctx.bot.re[8],
            self.AUTHOR = ctx.author
        self.DICTIONARY: dict = DICTIONARY
        self.DEFAULT_IMAGE = "https://miro.medium.com/max/1200/1*8Zh-mzLnVMDsbvXdKsU4lw.png"
        self.DEFAULT_THUMBNAIL = "https://i2.wp.com/sefiks.com/wp-content/uploads/2020/03/pip_big.jpg?resize=496%2C496&ssl=1"

    def render_embeds(self):
        if 'message' in self.DICTIONARY:
            return [
                cembed(
                    title="Error",
                    color=nextcord.Color.red(),
                    description=self.DICTIONARY.get('message', "Could not get the error message"),
                    thumbnail=self.DEFAULT_THUMBNAIL,
                    image=self.DEFAULT_IMAGE,
                    author=self.AUTHOR,
                    fields=dict2fields({'Solutions': 'Find if the package exists, this can also happen when the API is down'})
                )
            ]
        embeds = [
            self.first_page()
        ]
        return embeds

    def requirements(self, info: dict):
        if dist:=info.get('requires_dist', ""):
            dist = '```yml\n- '+'\n- '.join([_ for _ in dist[:5]])+"\n```"
        return f"`Requires dist: ` {dist}\n`Requires Python: ` {info.get('requires_python')}"

    def first_page(self):
        info: dict = self.DICTIONARY['info']
        description=info.get('summary')
        self.footer={
            'text': f'Latest Version: {info["version"]}',
            'icon_url': self.DEFAULT_THUMBNAIL
        }
        project_urls = "\n".join([f"`{i.upper()}: ` [🔗]({j})" for i, j in nunchaku(info["project_urls"], dict).items()])
        title, url=info.get('name'), info.get('package_url')
        fields={
            'Requirements': self.requirements(info),
            'Classifiers': '```yml\n- '+'\n- '.join(info['classifiers'][:5])+'\n```',
            'Stats': f'`LICENSE: ` {info.get("license")} \n{project_urls}',
            'Releases': '\n'.join([f"[{i}](https://pypi.org/project/{title}/{i})" for i in self.DICTIONARY['releases']][1:5])
        }

        image = self.DEFAULT_IMAGE
        for i in nunchaku(info['project_urls'], dict).values():
            if i.startswith("https://github.com/"):
                image = f"https://opengraph.githubassets.com/1/{'/'.join(i.split('/')[3:5])}"
                break
        
        return cembed(
            title=title,
            url=url,
            description=description,
            color=self.COLOR,
            author=self.AUTHOR,
            footer=self.footer,
            fields=fields,
            thumbnail=self.DEFAULT_THUMBNAIL,
            image=image
        )