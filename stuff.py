from dotenv import load_dotenv
import speedtest
import time
import emoji
import discord
from GoogleNews import GoogleNews
import traceback
import youtube_dl
from External_functions import *
from discord_components import *
import asyncio
from discord.ext import commands
from discord_slash import SlashCommand

global sent
sent = None
instagram_posts = []
intents = discord.Intents.default()
intents.members = True
temp_dev = {}
censor = []
old_youtube_vid = []
deleted_message = {}
da = {}
entr = {}
da1 = {}
queue_song = {}
temporary_list = []
dev_channel = int(os.getenv("dev"))
re = [0, "OK", {}, {}, -1, "", "205", {}, 5360, "48515587275%3A0AvceDiA27u1vT%3A26",1]
a_channels = [822500785765875749, 822446957288357888]
cat = {}
youtube = []
pages = {}
SESSIONID = None
color_message = None
color_temp = ()
vc_channel = {}
wolfram = os.getenv("wolfram")
prefix_dict = {}
mute_role = {743323684705402951: 876708632325148672, 851315724119310367: 0}

# replace your id with this
dev_users = ["432801163126243328"]
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
FFMPEG_OPTIONS = {
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    "options": "-vn",
}   

def reset_board():
    global board
    board = ""
    for i in range(1, 10):
        board = board + emoji.emojize(":keycap_" + str(i) + ":") + " | "
        if i % 3 == 0:
            board = board + "\n----    ----    ----\n"
    return board
    
#global board, Emoji_list
board = reset_board()
Emoji_list = [emoji.emojize(":keycap_" + str(i) + ":") for i in range(1, 10)]
Raw_Emoji_list = [emoji.emojize(":keycap_" + str(i) + ":") for i in range(1, 10)]
dictionary = dict(zip(Raw_Emoji_list, Emoji_list))


async def transformer(api, header, json):
    async with aiohttp.ClientSession() as session:
        async with session.post(api, headers=header, json=json) as resp:
            return await resp.json()

def addt(p1, p2):
    da[p1] = p2
    return "Done"


def get_elem(k):
    return da.get(k, "Not assigned yet")


def de(k):
    del da[k]
    return "Done"


def req():
    re[0] = re[0] + 1


def g_req():
    return re[0]


async def pa(embeds, ctx):
    message = await ctx.send(
        embed=embeds[0],
        components=[
            [
                Button(style=ButtonStyle.green, label="<"),
                Button(style=ButtonStyle.green, label=">"),
            ]
        ],
    )
    pag = 0

    def check(res):
        return message.id == res.message.id

    while True:
        try:
            res = await client.wait_for("button_click", check=check)
            if res.component.label == ">" and pag + 1 != len(embeds):
                pag += 1
                await res.edit_origin(embed=embeds[pag])
            elif res.component.label == "<" and pag != 0:
                pag -= 1
                await res.edit_origin(embed=embeds[pag])

        except asyncio.TimeoutError:
            break


def set_coin_toss_message(message):
    global coin_toss_message
    coin_toss_message = message


def get_dev_users():
    return dev_users


def set_dev_users(update_dev):
    global dev_users
    dev_users = update_dev


async def pa1(embeds, ctx):
    message = await ctx.send(embed=embeds[0])
    pag = 0
    await message.add_reaction("◀️")
    await message.add_reaction("▶️")

    def check(reaction, user):
        return (
                user != client.user
                and str(reaction.emoji) in ["◀️", "▶️"]
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
        except asyncio.TimeoutError:
            break


def youtube_download(ctx, url):
    with youtube_dl.YoutubeDL(ydl_op) as ydl:
        info = ydl.extract_info(url, download=False)
        URL = info["formats"][0]["url"]
    return URL


def youtube_download1(ctx, url):
    with youtube_dl.YoutubeDL(ydl_op) as ydl:
        info = ydl.extract_info(url, download=False)
        name = info['title']
        url = info["formats"][0]["url"]
    return url, name


async def search_vid(name):
    pass


def prefix_check(client, message):
    return prefix_dict.get(message.guild.id, ["'"])


def save_to_file(a=""):
    global dev_users
    if ".backup.txt" in os.listdir("./"):
        os.remove("./.backup.txt")
    if ".recover.txt" in os.listdir("./") and a == "recover":
        os.remove("./.recover.txt")

    def start_writing(file):
        file.write(f"mute_role={str(mute_role)}\n")
        file.write("censor=" + str(censor) + "\n")
        file.write("da=" + str(da) + "\n")
        file.write("da1=" + str(da1) + "\n")
        file.write("queue_song=" + str(queue_song) + "\n")
        file.write("a_channels=" + str(a_channels) + "\n")
        file.write("re=" + str(re) + "\n")
        file.write("dev_users=" + str(dev_users) + "\n")
        file.write(f"prefix_dict={str(prefix_dict)}\n")
        # file.write("entr=" + str(entr) + "\n")
        file.close()

    if True:
        file = open(".backup.txt", "w")
        start_writing(file)
    if a == "recover":
        file = open(".recover.txt", "w")
        start_writing(file)
    if a == "save":
        file = open(".safe.txt", "w")
        start_writing(file)


def load_from_file(file_name=".backup.txt", ss=0):
    if file_name in os.listdir("./"):
        file = open(file_name, "r")
        global mute_role
        global censor
        global da
        global da1
        global queue_song
        global entr
        global re
        global dev_users
        global prefix_dict

        def start_from(text, i):
            return eval(i[len(text):])

        txt_from_file = [i for i in file.readlines() if i != ""]
        try:
            print(type(txt_from_file))
            print(len(txt_from_file))
            for i in txt_from_file:
                if i.startswith("prefix_dict="):
                    print(start_from("prefix_dict=", i))
                    prefix_dict = start_from("prefix_dict=", i)
                if i.startswith("censor="):
                    censor = start_from("censor=", i)
                if i.startswith("da="):
                    da = start_from("da=", i)
                if i.startswith("da1="):
                    da1 = start_from("da1=", i)
                if i.startswith("queue_song="):
                    queue_song = start_from("queue_song=", i)
                if i.startswith("mute_role="):
                    mute_role = start_from("mute_role=", i)
                # if i.startswith("entr="):
                #    entr=start_from("entr=",i)
                if i.startswith("re="):
                    re = start_from("re=", i)
                if i.startswith("dev_users="):
                    dev_users = start_from("dev_users=", i)

        except Exception as e:
            print(traceback.print_exc())
    save_to_file()



load_from_file()


location_of_file = os.getcwd()
try:
    import mysql.connector as m

    load_dotenv()
except:
    pass

try:
    st_speed = speedtest.Speedtest()
except:
    print("Speedtest failed")
googlenews = GoogleNews()
start_time = time.time()
X = "❌"
O = "⭕"
global coin_toss_message, coin_message
coin_toss_message = None
coin_message = (
        "Pick "
        + emoji.emojize(":face_with_head-bandage:")
        + " for heads \nPick "
        + emoji.emojize(":hibiscus:")
        + " for tails"


)

client = commands.Bot(
    command_prefix=prefix_check,
    intents=intents,
    case_insensitive=True,
)
slash = SlashCommand(client, sync_commands=True)








