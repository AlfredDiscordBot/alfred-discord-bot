import requests
import hashlib
import psutil
import os
import time
import nextcord as discord
from discord import SlashOption
import random
import imdb
import emoji
import youtube_dl
from dotenv import load_dotenv
import instagramy
from instagramy import *
from instascrape import *
import urllib.parse
import urllib
import aiohttp
import traceback
import aiofiles

from functools import lru_cache
from datetime import datetime
from collections import Counter

ydl_op = {
    "format": "bestaudio/best",
    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "384",
        }
    ],
}
SVG2PNG_API_URI = os.getenv("svg2pnguri")
SVG2PNG_API_TOKEN = os.getenv("svg2pngtoken")

Emoji_alphabets = [emoji.emojize(f":regional_indicator_{chr(i+97)}:") for i in range(26)]

@lru_cache(maxsize = 512)
def youtube_info(url):
    with youtube_dl.YoutubeDL(ydl_op) as ydl:
        info = ydl.extract_info(url, download=False)
    return info

def timestamp(i):
    return datetime.fromtimestamp(i)

def convert_to_url(name):
    name = urllib.parse.quote(name)
    return name


def quad(eq):
    if "x^2" not in eq:
        return "x^2 not found, try again"
    print(eq)
    eq = eq.replace("2+", "2 + ")
    eq = eq.replace("2-", "2 - ")
    eq = eq.replace("x+", "x + ")
    eq = eq.replace("x-", "x - ")

    # try to get correct equation
    parts = [x.strip() for x in eq.split(" ")]
    a, b, c = 0, 0, 0
    for i in parts:
        if i == " ":
            parts.remove(" ")

    for index, part in enumerate(parts):
        if part in ["+", "-"]:
            continue

        symbol = -1 if index - 1 >= 0 and parts[index - 1] == "-" else 1

        if part.endswith("x^2"):
            coeff = part[:-3]
            a = float(coeff) if coeff != "" else 1
            a *= symbol
        elif part.endswith("x"):
            coeff = part[:-1]
            b = float(coeff) if coeff != "" else 1
            b *= symbol
        elif part.isdigit():
            c = symbol * float(part)

    determinant = b ** 2 - (4 * a * c)

    if determinant < 0:
        return "Not Real"
    if determinant == 0:
        root = -b / (2 * a)
        return "Equation has one root:" + str(root)

    if determinant > 0:
        determinant = determinant ** 0.5
        root1 = (-b + determinant) / (2 * a)
        root2 = (-b - determinant) / (2 * a)
        return "This equation has two roots: " + str(root1) + "," + str(root2)


async def memes2():
    st = await get_async("https://cheezburger.com/14858757/40-dumb-memes-for-distractible-scrollers")
    stop = 0
    link = []
    for i in range(0, 40):
        a = st.find("<img class='resp-media' src='", stop) + len(
            "<img class='resp-media' src='"
        )
        b = st.find("' id", a)
        stop = b
        link = link + [st[a:b]]
    return link


async def memes1():
    st = await get_async("http://www.quickmeme.com/")
    stop = 0
    link = []
    for i in range(10):
        a = st.find('"post-image" src="', stop) + len('post-image" src="') + 1
        b = st.find('" alt', a)
        stop = b
        link = link + [st[a:b]]
    return link


async def memes3():
    st = await get_async(
        "https://www.paulbarrs.com/business/funny-memes-website-design"
    )
    stop = 0
    link = []
    for i in range(20):
        a = st.find('srcset="', stop) + len('srcset="')
        b = st.find(".jpg", a) + len(".jpg")
        stop = b
        link += [st[a:b]]
    return link


load_dotenv()


username = str(os.getenv("username"))
password = str(os.getenv("password"))


def get_sessionid(username, password):
    url = "https://i.instagram.com/api/v1/accounts/login/"

    def generate_device_id(username, password):
        m = hashlib.md5()
        m.update(username.encode() + password.encode())

        seed = m.hexdigest()
        volatile_seed = "12345"

        m = hashlib.md5()
        m.update(seed.encode("utf-8") + volatile_seed.encode("utf-8"))
        return "android-" + m.hexdigest()[:16]

    device_id = generate_device_id(username, password)

    payload = {
        "username": username,
        "device_id": device_id,
        "password": password,
    }

    headers = {
        "Accept": "*/*",
        "Content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Accept-Language": "en-US",
        "referer": "https://www.instagram.com/accounts/login/",
        "User-Agent": "Instagram 10.26.0 Android",
    }

    response = requests.post(url, headers=headers, data=payload)
    if response.status_code == 200:
        return response.cookies.get_dict()["sessionid"]

    return response.text


def get_it():
    return get_sessionid(username, password)


def instagram_get1(account, color, SESSIONID):
    try:
        user = InstagramUser(account, sessionid=SESSIONID)
        all_posts = user.posts
        list_of_posts = []
        number = 0
        for i in all_posts[0:7]:
            url = i.post_url
            pos = Post(url)
            headers = {
                "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36 Edg/87.0.664.57",
                "cookie": "sessionid=" + SESSIONID + ";",
            }            
            pos.scrape(headers=headers)
            print(user.posts[number].comments)
            thumb = user.profile_picture_url
            embed = cembed(
                title="Instagram", color=color,
                description=pos.caption,
                footer=str(user.posts[number].comments) + " comments"
            )
            embed.set_image(url=user.posts[number].post_source)
            embed.set_thumbnail(url=thumb)
            list_of_posts.append((embed, url))
            number += 1
        return list_of_posts
    except instagramy.core.exceptions.UsernameNotFound:
        return "User Not Found, please check the spelling"
    except Exception as e:
        print(traceback.print_exc())
        #SESSIONID = get_it()
        return SESSIONID

@lru_cache(maxsize=512)
def get_youtube_url(url):
    """
    gets the list of url from a channel url
    """
    st = requests.get(url).content.decode()
    stop = 0
    li = []
    for i in range(10):
        a = st.find("/watch?v", stop)
        b = st.find('"', a)
        li = li + ["https://www.youtube.com" + st[a:b]]
        stop = b+1
    return li


def get_if_process_exists(name):
    return (
        len(
            [
                i
                for i in [p.info["name"] for p in psutil.process_iter(["name"])]
                if i.find(name) != -1
            ]
        )>0
    )


def cembed(
    title="", description="", thumbnail="", picture="", url="", color=discord.Color.dark_theme(), footer="", author = False, fields = {}, image = ""
):
    embed = discord.Embed()
    if color != discord.Color.dark_theme():
        if type(color) == int:
            embed = discord.Embed(color=discord.Color(value=color))
        else:
            embed = discord.Embed(color=color)
    if title != "":
        embed.title = title
    if description != "":
        embed.description = description
    if thumbnail != "":
        embed.set_thumbnail(url=thumbnail)
    if picture != "":
        embed.set_image(url=picture)
    if image != "":
        embed.set_image(url=image)
    if url != "":
        embed.url = url
    if footer != "":
        embed.set_footer(text=footer)
    if author == True:
        #embed.set_author(name=, icon_url=ctx_author.avatar.url) 
        pass
        
    return embed


def imdb_embed(movie,re):
    """
    Returns details about a movie as an embed in discord
    Parameters include movies
    """
    if movie == "":
        return cembed(
            title="Oops",
            description="You must enter a movie name",
            color=discord.Color.from_rgb(255, 255, 255).value,
        )
    try:
        ia = imdb.IMDb()
        movie = ia.search_movie(movie)
        title = movie[0]["title"]
        summary = ia.get_movie(movie[0].getID()).summary()
        image = movie[0]["full-size cover url"]
        return cembed(
            title=title,
            description=summary[summary.find("=") + 5 :],
            color=re[8],
            picture=image,
        )
    except:
        return cembed(
            title="Oops",
            description="Something went wrong, check if the name is correct",
            color=re[8],
        )

async def redd(account="wholesomememes", number = 25, single=True):
    a = await get_async(f"https://meme-api.herokuapp.com/gimme/{account}/{number}",kind=json)
    l = []
    if not "message" in a.keys():
        for i in a["memes"]:
            l.append((i["title"], i["url"]))
        if single:
            l = [random.choice(l)]
        return l
    else:
        return [(a["code"], a["message"], False)]

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
        "" + (emoji.emojize(":safety_vest:")) + " for recovery \n"
        "⭕ for list of all servers \n"
        "❌ for exiting \n"
        "🔥 for restart\n"
        "📊 for current load\n"
        "❕ for current issues\n"
        "" + emoji.emojize(":satellite:") + " for speedtest\n"
        "" + emoji.emojize(":black_circle:") + " for clear screen\n"
    )
    embed = discord.Embed(
        title="DEVOP", description=text_dev, color=discord.Color(value=color)
    )
    embed.set_thumbnail(url=client.user.avatar.url)
    mess = await channel.send(embed=embed)
    await mess.add_reaction(emoji.emojize(":safety_vest:"))
    await mess.add_reaction("⭕")
    await mess.add_reaction("❌")
    await mess.add_reaction(emoji.emojize(":fire:"))
    await mess.add_reaction(emoji.emojize(":bar_chart:"))
    await mess.add_reaction("❕")
    await mess.add_reaction(emoji.emojize(":satellite:"))
    await mess.add_reaction(emoji.emojize(":black_circle:"))
    await mess.add_reaction(emoji.emojize(":laptop:"))


async def wait_for_confirm(ctx, client, message, color=61620,usr=None):
    mess = await ctx.channel.send(
        embed=discord.Embed(
            title="Confirmation", description=message, color=discord.Color(color)
        )
    )
    await mess.add_reaction(emoji.emojize(":check_mark_button:"))
    await mess.add_reaction(emoji.emojize(":cross_mark_button:"))

    person=usr

    def check(reaction, user):
        a = user == ctx.author if person is None else person == user
        return (
            reaction.message.id == mess.id
            and reaction.emoji
            in [emoji.emojize(":check_mark_button:"), emoji.emojize(":cross_mark_button:")]
            and a
        )

    reaction, user = await client.wait_for("reaction_add", check=check)
    if reaction.emoji == emoji.emojize(":check_mark_button:"):
        await mess.delete()
        return True
    if reaction.emoji == emoji.emojize(":cross_mark_button:"):
        await mess.delete()
        await ctx.channel.send(
            embed=discord.Embed(
                title="Ok cool", description="Aborted", color=discord.Color(color)
            )
        )
        return False


def equalise(all_strings):
    maximum = max(list(map(len, all_strings)))
    a = {}
    _ = [a.update({i: i + " " * (maximum - len(i))}) for i in all_strings]
    return a

def subtract_list(l1, l2):
    a = []
    for i in l1:
        if i not in l2:
            a.append(i)
    return a

def extract_color(color):
    try:
        color_temp = (
            int("0x" + str(hex(color))[2:4], 16),
            int("0x" + str(hex(color))[4:6], 16),
            int("0x" + str(hex(color))[6:8], 16),
        )
        return color_temp
    except:
        pass


def svg2png(url: str):
    """Convert SVG image (url) to PNG format."""
    # print(SVG2PNG_API_URI, SVG2PNG_API_TOKEN)
    res = requests.get(
        SVG2PNG_API_URI, params=[("url", url), ("token", SVG2PNG_API_TOKEN)]
    )
    return res.content



async def get_name(url):
    '''
    get Youtube Video Name through Async
    '''
    a = await get_async(url)
    return (
        a[a.find("<title>") + len("<title>") : a.find("</title>")]
        .replace("&amp;", "&")
        .replace(" - YouTube", "")
        .replace("&#39;", "'")
    )

async def get_async(url, headers = {}, kind = "content"):
    '''
    Simple Async get request
    '''
    output = ""
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as resp:
            if kind == "json":                
                output = await resp.json()
            elif kind.startswith("file>"):
                f = await aiofiles.open(kind[5:], mode = "wb")
                await f.write(await resp.read())
                await f.close()
                return
            elif kind == "fp":
                output = await resp.read()
            else:
                output = await resp.text()
                
        await session.close()
    return output
    
async def post_async(api, header = {}, json = {}, output = "content"):
    async with aiohttp.ClientSession() as session:
        async with session.post(api, headers=header, json=json) as resp:
            if resp.headers['Content-Type'] != 'application/json':
                return await resp.read()
            return await resp.json()
            
def suicide_m(client,color):
    return cembed(
        title="Suicide and Self harm prevention",
        description=""" 
    You are not alone ...
    And your Life is worth a lot ..
    SPEAK OUT !!


    If you're having any suicidal thoughts, please seek help immediately. Talk about what bothers you and what can be done to solve the problem


    international suicide helplines>>> https://www.opencounseling.com/suicide-hotlines
        """,
        color=color,
        thumbnail=client.user.avatar.url,
        picture="https://www.humanium.org/en/wp-content/uploads/2019/09/shutterstock_1140282473-scaled.jpg"
    )

def check_end(s : str):
    if not s.endswith("/videos"):
        return s+"/videos"
    return s

def check_voice(ctx):
    try:
        mem = [str(names) for names in getattr(ctx, 'voice_client', getattr(ctx.guild, 'voice_client', None)).channel.members]
    except:
        mem = []
    return mem.count(str(getattr(ctx, 'author', getattr(ctx, 'user', None)))) > 0

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

def remove_all(original,s):
    for i in s:
        original.replace(i,"")
    return original

def defa(*types, default = None, choices=[]):
    if types == []: return SlashOption(default = default, required = False)
    if choices != []:
        return SlashOption(choices=choices, default = None)   
    return SlashOption(channel_types = types)

async def ly(song, re):
    j = await get_async(f"https://api.popcat.xyz/lyrics?song={convert_to_url(song)}",kind="json")
    return cembed(title=j['title'],description=j['lyrics'],color=re[8],thumbnail=j['image'],footer=j['artist'])

async def isReaction(ctx, embed, clear = False):
    if type(ctx) == discord.message.Message:
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
    def __init__(self,color):
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
        js = await get_async("https://api.spacexdata.com/v4/launches/latest", kind="json")
        self.name = js['name']
        self.time = timestamp(int(js['date_unix']))
        self.thumbnail = js['links']['patch']['large']
        self.youtube = js['links']['webcast']
        self.wikipedia = js['links']['wikipedia']
        self.crew = js['crew']
        self.id = js['id']
        self.fno = js['flight_number']

    async def history(self):
        jso = await get_async("https://api.spacexdata.com/v4/history", kind = "json")
        embeds = []
        for i in jso[::-1]:
            embed = cembed(
                title=i['title'],
                description=i['details'],
                color=self.color,
                thumbnail="https://www.spacex.com/static/images/share.jpg",
                footer = i['id'] + " | " + str(timestamp(i['event_date_unix']))
            )
            embeds.append(embed)
        print("Done")
        return embeds

m_options = [
    'title',
    'description',
    'color',
    'footer',
    'thumbnail',
    'image',
    'picture',
    'author'   
]