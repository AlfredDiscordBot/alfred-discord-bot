"""
Set your env like the example below:
token=
sjdoskenv=
sjdoskenv1=
mysql=
default=
dev=
"""

import helping_hand
from random import choice
from discord.ext import commands, tasks
from discord_slash import SlashCommand, SlashContext
from GoogleNews import GoogleNews
from io import StringIO
from contextlib import redirect_stdout
from External_functions import *
from discord_components import *
import youtube_dl
import os
import re as regex
import urllib.request
import time
import sys
import emoji
import psutil
import asyncio
import cloudscraper
import requests
import aiohttp
from io import BytesIO
import speedtest

# from spotify_client import SpotifyAPI


location_of_file = os.getcwd()
try:
    import mysql.connector as m

    load_dotenv()
except:
    pass

try:
    st_speed = speedtest.Speedtest()
except:
    print("failed")
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
global board, Emoji_list
Emoji_list = [emoji.emojize(":keycap_" + str(i) + ":") for i in range(1, 10)]
Raw_Emoji_list = [emoji.emojize(":keycap_" + str(i) + ":") for i in range(1, 10)]


def reset_board():
    global board
    board = ""
    for i in range(1, 10):
        board = board + emoji.emojize(":keycap_" + str(i) + ":") + " | "
        if i % 3 == 0:
            board = board + "\n----    ----    ----\n"
    return board


board = reset_board()
global sent
sent = None
instagram_posts = []
dictionary = dict(zip(Raw_Emoji_list, Emoji_list))
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
re = [0, "OK", 1, {}, -1, "", "205", 1, 5360, "48515587275%3A0AvceDiA27u1vT%3A26"]
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


# spotify = SpotifyAPI(client_id, client_secret)


# def fetch_spotify_playlist(link, num):
#     if num > 100:
#         songs = []
#         images = []
#         album_names = []
#         artist_names = []
#         track_names = []
#         loops_req = int(num // 100 + 1)
#         offset = 0
#         for loop in range(loops_req):
#             data = spotify.playlist(link=link, num=100, offset=offset)
#             for item in range(100):
#                 try:
#                     none_object = data['items'][item]['track']
#                 except IndexError:
#                     pass
#                 if none_object == None:
#                     pass
#                 else:
#                     try:
#                         track_name = data['items'][item]['track']['name']
#                         artist_name = data['items'][item]['track']['artists'][0]['name']
#                         image = data['items'][item]['track']['album']['images'][1]['url']
#                         album_name = data['items'][item]['track']['album']['name']
#                         songs.append(f'{track_name} - {artist_name}')
#                         images.append(image)
#                         album_names.append(album_name)
#                         artist_names.append(artist_name)
#                         track_names.append(track_name)
#                         success = True
#                     except IndexError:
#                         pass
#             offset += 100
#     else:
#         songs = []
#         images = []
#         album_names = []
#         artist_names = []
#         track_names = []
#         data = spotify.playlist(link=link, num=num, offset=0)
#         for item in range(num):
#             try:
#                 track_name = data['items'][item]['track']['name']
#                 artist_name = data['items'][item]['track']['artists'][0]['name']
#                 image = data['items'][item]['track']['album']['images'][1]['url']
#                 album_name = data['items'][item]['track']['album']['name']
#                 songs.append(f'{track_name} - {artist_name}')
#                 images.append(image)
#                 album_names.append(album_name)
#                 artist_names.append(artist_name)
#                 track_names.append(track_name)
#                 success = True
#             except IndexError:
#                 pass
#     # urls = []
#     # base = 'https://www.youtube.com'
#     # for song in songs:
#     #     result = YoutubeSearch(song, max_results=1).to_dict()
#     #     suffix = result[0]['url_suffix']
#     #     link = base + suffix
#     #     urls.append(link)
#     return songs

def youtube_download(ctx, url):
    with youtube_dl.YoutubeDL(ydl_op) as ydl:
        info = ydl.extract_info(url, download=False)
        URL = info["formats"][0]["url"]
    return URL


def youtube_download1(ctx, url):
    with youtube_dl.YoutubeDL(ydl_op) as ydl:
        info = ydl.extract_info(url, download=False)
        name = info['title']
        URL = info["formats"][0]["url"]
    return (URL, name)


async def search_vid(name):
    pass


def prefix_check(client, message):
    return prefix_dict.get(message.guild.id, ["'"])


client = commands.Bot(
    command_prefix=prefix_check,
    intents=intents,
    case_insensitive=True,
)
slash = SlashCommand(client, sync_commands=True)
client.load_extension('cog')


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


@client.event
async def on_ready():
    print(client.user)
    channel = client.get_channel(dev_channel)
    DiscordComponents(client)
    try:
        print("Starting Load from file")
        try:
            load_from_file()
        except:
            try:
                load_from_file("recover")
            except:
                pass
        print("Finished loading\n")
        print(re)
        print(dev_users)
        print(prefix_dict)
        print("\nStarting devop display")
        await devop_mtext(client, channel, re[8])

        print("Finished devop display")
        print("Starting imports")
        imports = ""
        sys.path.insert(1, location_of_file + "/src")
        for i in os.listdir(location_of_file + "/src"):
            if i.endswith(".py"):
                try:
                    requi = __import__(i[0: len(i) - 3]).requirements()
                    # if requi != "":
                    #     requi = "," + requi
                    if type(requi) is str:
                        eval(f"__import__('{i[0:len(i) - 3]}').main(client,{requi})")
                    if type(requi) is list:
                        eval(
                            f"__import__('{i[0:len(i) - 3]}').main(client,{','.join(requi)})"
                        )
                    imports = imports + i[0: len(i) - 3] + "\n"
                except Exception as e:
                    await channel.send(
                        embed=discord.Embed(
                            title="Error in plugin " + i[0: len(i) - 3],
                            description=str(e),
                            color=discord.Color(value=re[8]),
                        )
                    )
        await channel.send(
            embed=discord.Embed(
                title="Successfully imported",
                description=imports,
                color=discord.Color(value=re[8]),
            )
        )
    except Exception as e:
        mess = await channel.send(
            embed=discord.Embed(
                title="Error in the function on_ready",
                description=str(e),
                color=discord.Color(value=re[8]),
            )
        )
        await mess.add_reaction("❌")
    dev_loop.start()
    print("Prepared")
    youtube_loop.start()


@tasks.loop(minutes=7)
async def youtube_loop():
    list_of_programs = ["blender"]
    for i in list_of_programs:
        if get_if_process_exists(i):
            await client.change_presence(
                activity=discord.Activity(type=discord.ActivityType.playing, name=i)
            )
            break
    else:
        await client.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name=str(len(client.guilds)) + " servers",
            )
        )


@tasks.loop(seconds=10)
async def dev_loop():
    global temp_dev
    for i in list(temp_dev.keys()):
        person = client.get_user(i)
        if temp_dev[i][0] > 0:
            temp_dev[i][0] -= 10
            await temp_dev[i][1].edit(
                embed=discord.Embed(
                    title="Done",
                    description=str(person.mention)
                                + "\nTime remaining: "
                                + str(temp_dev[i][0])
                                + "s",
                    color=discord.Color(value=re[8]),
                )
            )
        else:
            await temp_dev[i][1].edit(
                embed=discord.Embed(
                    title="Time up",
                    description="Your time is up, please ask a bot dev to give you access to the script function",
                    color=discord.Color.from_rgb(250, 50, 0),
                )
            )
            temp_dev.pop(i)
    save_to_file()


@dev_loop.before_loop
async def wait_for_ready():
    await client.wait_until_ready()


@youtube_loop.before_loop
async def wait_for_ready():
    await client.wait_until_ready()


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


@client.event
async def on_message_delete(message):
    if not message.channel.id in list(deleted_message.keys()):
        deleted_message[message.channel.id] = []
    if len(message.embeds) <= 0:
        if not message.author.bot:
            deleted_message[message.channel.id].append(
                (str(message.author), message.content)
            )
    else:
        if not message.author.bot:
            deleted_message[message.channel.id].append(
                (str(message.author), message.embeds[0], True)
            )


@client.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.channels, name="announcement")
    print(member.guild)
    if member.guild.id == 841026124174983188:
        channel = client.get_channel(841026124174983193)
    await channel.send(member.mention + " is here")
    embed = discord.Embed(
        title="Welcome!!!",
        description="Welcome to the server, " + member.name,
        color=discord.Color(value=re[8]),
    )
    embed.set_thumbnail(
        url="https://image.shutterstock.com/image-vector/welcome-poster-spectrum-brush-strokes-260nw-1146069941.jpg"
    )
    await channel.send(embed=embed)


@client.event
async def on_member_remove(member):
    if member.guild.id == 743323684705402951:
        channel = client.get_channel(885770265026498601)
    elif member.guild.id == 841026124174983188:
        channel = client.get_channel(841026124174983193)
    else:
        channel = discord.utils.get(member.guild.channels, name="announcement")

    await channel.send(member.mention + " is no longer here")
    embed = discord.Embed(
        title="Bye!!!",
        description="Hope you enjoyed your stay " + member.name,
        color=discord.Color(value=re[8]),
    )
    embed.set_thumbnail(
        url="https://thumbs.dreamstime.com/b/bye-bye-man-says-45256525.jpg"
    )
    await channel.send(embed=embed)



@client.command(aliases=["hi"])
async def check(ctx):
    req()
    print("check")
    em = discord.Embed(
        title="Online",
        description=f"Hi, {ctx.author.name}\nLatency: {int(client.latency * 1000)}",
        color=discord.Color(value=re[8]),
    )
    await ctx.send(embed=em)


@slash.slash(name="check", description="Check if the bot is online")
async def check_slash(ctx):
    req()
    await ctx.defer()
    await check(ctx)


@client.command()
async def clear(ctx, text, num=10):
    req()
    await ctx.channel.purge(limit=1)
    if str(text) == re[1]:
        if (
                ctx.author.guild_permissions.manage_messages
                or ctx.author.id == 432801163126243328
        ):
            confirmation = True
            if int(num) > 10:
                confirmation = await wait_for_confirm(
                    ctx, client, f"Do you want to delete {num} messages", color=re[8]
                )
            if confirmation:
                await ctx.channel.delete_messages(
                    [i async for i in ctx.channel.history(limit=num) if not i.pinned][:100]
                )
        else:
            await ctx.send(
                embed=discord.Embed(
                    title="Permission Denied",
                    description="You cant delete messages",
                    color=discord.Color(value=re[8]),
                )
            )
    else:
        await ctx.send("Wrong password")


@client.event
async def on_reaction_add(reaction, user):
    req()
    try:
        if not user.bot:
            global color_temp
            save_to_file()
            global Emoji_list
            if (
                    reaction.emoji == emoji.emojize(":upwards_button:")
                    and len(queue_song[str(reaction.message.guild.id)]) > 0
                    and reaction.message.author == client.user
            ):
                await reaction.remove(user)
                if not reaction.message in list(pages.keys()):
                    pages[reaction.message] = 0
                else:
                    if pages[reaction.message] > 0:
                        pages[reaction.message] -= 1
                st = ""
                for i in range(
                        pages[reaction.message] * 10,
                        (pages[reaction.message] * 10) + 10,
                ):
                    try:
                        if (
                                not queue_song[str(reaction.message.guild.id)][i]
                                    in da1.keys()
                        ):
                            da1[
                                queue_song[str(reaction.message.guild.id)][i]
                            ] = youtube_info(
                                queue_song[str(reaction.message.guild.id)][i]
                            )[
                                "title"
                            ]
                        st = (
                                st
                                + str(i)
                                + ". "
                                + da1[queue_song[str(reaction.message.guild.id)][i]]
                                + "\n"
                        )
                    except Exception as e:
                        print(e)
                await reaction.message.edit(
                    embed=discord.Embed(
                        title="Queue",
                        description=st,
                        color=discord.Color(value=re[8]),
                    )
                )
            if (
                    reaction.emoji == emoji.emojize(":downwards_button:")
                    and len(queue_song[str(reaction.message.guild.id)]) > 0
                    and reaction.message.author == client.user
            ):
                await reaction.remove(user)
                if not reaction.message in list(pages.keys()):
                    pages[reaction.message] = 0
                else:
                    if pages[reaction.message] * 10 < len(
                            queue_song[str(reaction.message.guild.id)]
                    ):
                        pages[reaction.message] += 1
                    else:
                        pages[reaction.message] = (
                                len(queue_song[str(reaction.message.guild.id)]) // 10
                        )
                st = ""
                for i in range(
                        pages[reaction.message] * 10,
                        (pages[reaction.message] * 10) + 10,
                ):
                    try:
                        if not queue_song[str(reaction.message.guild.id)][i] in list(
                                da1.keys()
                        ):
                            da1[
                                queue_song[str(reaction.message.guild.id)][i]
                            ] = youtube_info(
                                queue_song[str(reaction.message.guild.id)][i]
                            )[
                                "title"
                            ]
                        st = (
                                st
                                + str(i)
                                + ". "
                                + da1[queue_song[str(reaction.message.guild.id)][i]]
                                + "\n"
                        )
                    except Exception as e:
                        print(e)
                if st == "":
                    st = "End of queue"
                await reaction.message.edit(
                    embed=discord.Embed(
                        title="Queue",
                        description=st,
                        color=discord.Color(value=re[8]),
                    )
                )

            if (
                    reaction.emoji
                    in [emoji.emojize(":keycap_" + str(i) + ":") for i in range(1, 10)]
                    and reaction.message.author.id == client.user.id
            ):
                global board, available, sent, dictionary
                if user != client.user:
                    if sent.id == reaction.message.id:
                        if reaction.emoji in Emoji_list:
                            temp_number = 0
                            for i in range(0, 9):
                                if reaction.emoji == Emoji_list[i]:
                                    temp_number = i
                                    break
                            global board
                            board = board.replace(
                                Raw_Emoji_list[temp_number],
                                emoji.emojize(":cross_mark:"),
                            )
                            await sent.edit(
                                embed=discord.Embed(
                                    title="Tic Tac Toe by Rahul",
                                    description=board,
                                    color=discord.Color(value=re[8]),
                                )
                            )
                            await reaction.remove(user)
                            await reaction.remove(client.user)
                            available.remove(
                                emoji.emojize(":keycap_" + str(temp_number + 1) + ":")
                            )
                            if len(available) == 0:
                                result = " "
                                result = check_win(board)
                                if result != " ":
                                    await sent.edit(
                                        embed=discord.Embed(
                                            title="Tic Tac Toe by Rahul",
                                            description=result,
                                            color=discord.Color(value=re[8]),
                                        )
                                    )
                                else:
                                    await sent.edit(
                                        embed=discord.Embed(
                                            title="Tic Tac Toe by Rahul",
                                            description="Draw",
                                            color=discord.Color(value=re[8]),
                                        )
                                    )
                            else:
                                comp_move = choice(available)
                                board = board.replace(comp_move, O)
                                await sent.edit(
                                    embed=discord.Embed(
                                        title="Tic Tac Toe by Rahul",
                                        description=board,
                                        color=discord.Color(value=re[8]),
                                    )
                                )
                                await sent.remove_reaction(
                                    dictionary[comp_move], client.user
                                )
                                available.remove(comp_move)
                                result = " "
                                result = check_win(board)
                                if result != " ":
                                    await sent.edit(
                                        embed=discord.Embed(
                                            title="Tic Tac Toe by Rahul",
                                            description=result,
                                            color=discord.Color(value=re[8]),
                                        )
                                    )
            if reaction.emoji == emoji.emojize(":musical_note:"):
                await reaction.remove(user)
                if len(queue_song[str(reaction.message.guild.id)]) > 0:
                    description = (
                            "[Current index: "
                            + str(re[3][str(reaction.message.guild.id)])
                            + "]("
                            + queue_song[str(reaction.message.guild.id)][
                                re[3][str(reaction.message.guild.id)]
                            ]
                            + ")\n"
                    )
                    info = youtube_info(
                        queue_song[str(reaction.message.guild.id)][
                            re[3][str(reaction.message.guild.id)]
                        ]
                    )
                    check = "\n\nDescription: \n" + info["description"] + "\n"
                    if len(check) < 3000 and len(check) > 0:
                        description += check
                    description += (
                            "\nDuration: "
                            + str(info["duration"] // 60)
                            + "min "
                            + str(info["duration"] % 60)
                            + "sec"
                            + f"\n\n{info['view_count']} views\n{info['like_count']} :thumbsup:\n{info['dislike_count']} :thumbdown:"
                    )
                    await reaction.message.edit(
                        embed=cembed(
                            title=str(
                                da1[
                                    queue_song[str(reaction.message.guild.id)][
                                        re[3][str(reaction.message.guild.id)]
                                    ]
                                ]
                            ),
                            description=description,
                            color=re[8],
                            thumbnail=info["thumbnail"],
                        )
                    )
                else:
                    await reaction.message.edit(
                        embed=discord.Embed(
                            title="Empty queue",
                            description="Your queue is currently empty",
                            color=discord.Color(value=re[8]),
                        )
                    )
            if reaction.emoji == discord.utils.get(client.emojis, name="blue_down"):
                if (
                        str(user) != str(client.user)
                        and reaction.message.author == client.user
                ):
                    await reaction.remove(user)
                    temp_tup = color_temp
                    if temp_tup[2] - 25 >= 0:
                        re[8] = discord.Color.from_rgb(
                            int(temp_tup[0]),
                            int(temp_tup[1]),
                            int(temp_tup[2]) - 25,
                        ).value
                        color_temp = (
                            int(temp_tup[0]),
                            int(temp_tup[1]),
                            int(temp_tup[2]) - 25,
                        )
                    else:
                        re[8] = discord.Color.from_rgb(
                            int(temp_tup[0]), int(temp_tup[1]), 0
                        ).value
                        color_temp = (int(temp_tup[0]), int(temp_tup[1]), 0)
                    embed = discord.Embed(
                        title="New Color",
                        description=str(color_temp),
                        color=discord.Color(value=re[8]),
                    )
                    await color_message.edit(embed=embed)
            if reaction.emoji == discord.utils.get(client.emojis, name="green_down"):
                if (
                        str(user) != str(client.user)
                        and reaction.message.author == client.user
                ):
                    await reaction.remove(user)
                    temp_tup = color_temp
                    if temp_tup[1] - 25 >= 0:
                        re[8] = discord.Color.from_rgb(
                            int(temp_tup[0]),
                            int(temp_tup[1] - 25),
                            int(temp_tup[2]),
                        ).value
                        color_temp = (
                            int(temp_tup[0]),
                            int(temp_tup[1] - 25),
                            int(temp_tup[2]),
                        )
                    else:
                        re[8] = discord.Color.from_rgb(
                            int(temp_tup[0]), 0, int(temp_tup[2])
                        ).value
                        color_temp = (int(temp_tup[0]), 0, int(temp_tup[2]))
                    embed = discord.Embed(
                        title="New Color",
                        description=str(color_temp),
                        color=discord.Color(value=re[8]),
                    )
                    await color_message.edit(embed=embed)
            if reaction.emoji == emoji.emojize(":red_triangle_pointed_down:"):
                if (
                        str(user) != str(client.user)
                        and reaction.message.author == client.user
                ):
                    await reaction.remove(user)
                    temp_tup = color_temp
                    if temp_tup[0] - 25 >= 0:
                        re[8] = discord.Color.from_rgb(
                            int(temp_tup[0] - 25),
                            int(temp_tup[1]),
                            int(temp_tup[2]),
                        ).value
                        color_temp = (
                            int(temp_tup[0] - 25),
                            int(temp_tup[1]),
                            int(temp_tup[2]),
                        )
                    else:
                        re[8] = discord.Color.from_rgb(
                            0, int(temp_tup[1]), int(temp_tup[2])
                        ).value
                        color_temp = (0, int(temp_tup[1]), int(temp_tup[2]))
                    embed = discord.Embed(
                        title="New Color",
                        description=str(color_temp),
                        color=discord.Color(value=re[8]),
                    )
                    await color_message.edit(embed=embed)
            if reaction.emoji == discord.utils.get(client.emojis, name="blue_up"):
                if (
                        str(user) != str(client.user)
                        and reaction.message.author == client.user
                ):
                    await reaction.remove(user)
                    temp_tup = color_temp
                    if temp_tup[2] + 25 <= 255:
                        re[8] = discord.Color.from_rgb(
                            int(temp_tup[0]),
                            int(temp_tup[1]),
                            int(temp_tup[2]) + 25,
                        ).value
                        color_temp = (
                            int(temp_tup[0]),
                            int(temp_tup[1]),
                            int(temp_tup[2]) + 25,
                        )
                    else:
                        re[8] = discord.Color.from_rgb(
                            int(temp_tup[0]), int(temp_tup[1]), 255
                        ).value
                        color_temp = (int(temp_tup[0]), int(temp_tup[1]), 255)
                    embed = discord.Embed(
                        title="New Color",
                        description=str(color_temp),
                        color=discord.Color(value=re[8]),
                    )
                    await color_message.edit(embed=embed)
            if reaction.emoji == discord.utils.get(client.emojis, name="green_up"):
                if (
                        str(user) != str(client.user)
                        and reaction.message.author == client.user
                ):
                    await reaction.remove(user)
                    temp_tup = color_temp
                    if temp_tup[1] + 25 <= 255:
                        re[8] = discord.Color.from_rgb(
                            int(temp_tup[0]),
                            int(temp_tup[1] + 25),
                            int(temp_tup[2]),
                        ).value
                        color_temp = (
                            int(temp_tup[0]),
                            int(temp_tup[1] + 25),
                            int(temp_tup[2]),
                        )
                    else:
                        re[8] = discord.Color.from_rgb(
                            int(temp_tup[0]), 255, int(temp_tup[2])
                        ).value
                        color_temp = (int(temp_tup[0]), 255, int(temp_tup[2]))
                    embed = discord.Embed(
                        title="New Color",
                        description=str(color_temp),
                        color=discord.Color(value=re[8]),
                    )
                    await color_message.edit(embed=embed)
            if reaction.emoji == emoji.emojize(":red_triangle_pointed_up:"):
                if (
                        str(user) != str(client.user)
                        and reaction.message.author == client.user
                ):
                    await reaction.remove(user)
                    temp_tup = color_temp
                    if temp_tup[0] + 25 <= 255:
                        re[8] = discord.Color.from_rgb(
                            int(temp_tup[0] + 25),
                            int(temp_tup[1]),
                            int(temp_tup[2]),
                        ).value
                        color_temp = (
                            int(temp_tup[0] + 25),
                            int(temp_tup[1]),
                            int(temp_tup[2]),
                        )
                    else:
                        re[8] = discord.Color.from_rgb(
                            255, int(temp_tup[1]), int(temp_tup[2])
                        ).value
                        color_temp = (255, int(temp_tup[1]), int(temp_tup[2]))
                    embed = discord.Embed(
                        title="New Color",
                        description=str(color_temp),
                        color=discord.Color(value=re[8]),
                    )
                    await color_message.edit(embed=embed)
            if reaction.emoji == "⏮":
                if (
                        str(user) != str(client.user)
                        and reaction.message.author == client.user
                ):
                    await reaction.remove(user)
                    req()
                    try:
                        mem = [
                            str(names)
                            for names in reaction.message.guild.voice_client.channel.members
                        ]
                    except:
                        mem = []
                    if mem.count(str(user)) > 0:
                        if (
                                not queue_song[str(reaction.message.guild.id)][
                                        re[3][str(reaction.message.guild.id)]
                                    ]
                                    in da1.keys()
                        ):
                            da1[
                                queue_song[str(reaction.message.guild.id)][
                                    re[3][str(reaction.message.guild.id)]
                                ]
                            ] = youtube_info(
                                queue_song[str(reaction.message.guild.id)][
                                    re[3][str(reaction.message.guild.id)]
                                ]
                            )[
                                "title"
                            ]
                        re[3][str(reaction.message.guild.id)] -= 1
                        if re[3][str(reaction.message.guild.id)] == -1:
                            re[3][str(reaction.message.guild.id)] = 0
                        await reaction.message.edit(
                            embed=discord.Embed(
                                title="Downloading...",
                                description="Downloading the song, please wait for a moment",
                                color=discord.Color(value=re[8]),
                            )
                        )
                        voice = discord.utils.get(
                            client.voice_clients, guild=reaction.message.guild
                        )
                        URL = youtube_download(
                            reaction.message,
                            queue_song[str(reaction.message.guild.id)][
                                re[3][str(reaction.message.guild.id)]
                            ],
                        )
                        voice.stop()
                        voice.play(
                            discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS),
                            after=lambda e: repeat(reaction.message, voice),
                        )
                        url = queue_song[str(reaction.message.guild.id)][
                            re[3][str(reaction.message.guild.id)]
                        ]
                        song_name = da1[url]
                        await reaction.message.edit(
                            embed=discord.Embed(
                                title="Playing",
                                description=f"[{song_name}]({url})",
                                color=discord.Color(value=re[8]),
                            )
                        )
                    else:
                        await reaction.message.edit(
                            embed=discord.Embed(
                                title="Permission denied",
                                description=(
                                        "You need to join the voice channel "
                                        + str(user.name)
                                ),
                                color=discord.Color(value=re[8]),
                            )
                        )
            if reaction.emoji == "⏸":
                if (
                        str(user) != str(client.user)
                        and reaction.message.author == client.user
                ):
                    await reaction.remove(user)
                    req()
                    try:
                        mem = [
                            str(names)
                            for names in reaction.message.guild.voice_client.channel.members
                        ]
                    except:
                        mem = []
                    if mem.count(str(user)) > 0:
                        voice = discord.utils.get(
                            client.voice_clients, guild=reaction.message.guild
                        )
                        url = queue_song[str(reaction.message.guild.id)][
                            re[3][str(reaction.message.guild.id)]
                        ]
                        song_name = da1[url]
                        await reaction.message.edit(
                            embed=discord.Embed(
                                title="Paused",
                                description=f"[{song_name}]({url})",
                                color=discord.Color(value=re[8]),
                            )
                        )
                        voice.pause()
            if reaction.emoji == "▶":
                if (
                        str(user) != str(client.user)
                        and reaction.message.author == client.user
                ):
                    await reaction.remove(user)
                    req()
                    try:
                        mem = [
                            str(names)
                            for names in reaction.message.guild.voice_client.channel.members
                        ]
                    except:
                        mem = []
                    if mem.count(str(user)) > 0:
                        voice = discord.utils.get(
                            client.voice_clients, guild=reaction.message.guild
                        )
                        if (
                                not queue_song[str(reaction.message.guild.id)][
                                        re[3][str(reaction.message.guild.id)]
                                    ]
                                    in da1.keys()
                        ):
                            da1[
                                queue_song[str(reaction.message.guild.id)][
                                    re[3][str(reaction.message.guild.id)]
                                ]
                            ] = youtube_info(
                                queue_song[str(reaction.message.guild.id)][
                                    re[3][str(reaction.message.guild.id)]
                                ]
                            )[
                                "title"
                            ]
                        url = queue_song[str(reaction.message.guild.id)][
                            re[3][str(reaction.message.guild.id)]
                        ]
                        song_name = da1[url]
                        await reaction.message.edit(
                            embed=discord.Embed(
                                title="Playing",
                                description=f"[{song_name}]({url})",
                                color=discord.Color(value=re[8]),
                            )
                        )
                        voice.resume()
                    else:
                        await reaction.message.edit(
                            embed=discord.Embed(
                                title="Permission denied",
                                description=(
                                        "You need to join the voice channel "
                                        + str(user.name)
                                ),
                                color=discord.Color(value=re[8]),
                            )
                        )
            if reaction.emoji == "🔁":
                if (
                        str(user) != str(client.user)
                        and reaction.message.author == client.user
                ):
                    await reaction.remove(user)
                    try:
                        mem = [
                            str(names)
                            for names in reaction.message.guild.voice_client.channel.members
                        ]
                    except Exception as e:
                        mem = []
                    if mem.count(str(user)) > 0:
                        voice = discord.utils.get(
                            client.voice_clients, guild=reaction.message.guild
                        )
                        URL = youtube_download(
                            reaction.message,
                            queue_song[str(reaction.message.guild.id)][
                                re[3][str(reaction.message.guild.id)]
                            ],
                        )
                        voice.stop()
                        voice.play(
                            discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS),
                            after=lambda e: repeat(reaction.message, voice),
                        )
                        if (
                                not queue_song[str(reaction.message.guild.id)][
                                        re[3][str(reaction.message.guild.id)]
                                    ]
                                    in da1.keys()
                        ):
                            da1[
                                queue_song[str(reaction.message.guild.id)][
                                    re[3][str(reaction.message.guild.id)]
                                ]
                            ] = youtube_info(
                                queue_song[str(reaction.message.guild.id)][
                                    re[3][str(reaction.message.guild.id)]
                                ]
                            )[
                                "title"
                            ]
                        url = queue_song[str(reaction.message.guild.id)][
                            re[3][str(reaction.message.guild.id)]
                        ]
                        song_name = da1[url]
                        await reaction.message.edit(
                            embed=discord.Embed(
                                title="Playing",
                                description=f"[{song_name}]({url})",
                                color=discord.Color(value=re[8]),
                            )
                        )
                    else:
                        await reaction.message.edit(
                            embed=discord.Embed(
                                title="Permission denied",
                                description=(
                                        "You need to join the voice channel "
                                        + str(user.name)
                                ),
                                color=discord.Color(value=re[8]),
                            )
                        )
            if reaction.emoji == "⏭":
                if (
                        str(user) != str(client.user)
                        and reaction.message.author == client.user
                ):
                    await reaction.remove(user)
                    req()
                    try:
                        mem = [
                            names.id
                            for names in reaction.message.guild.voice_client.channel.members
                        ]
                    except:
                        mem = []
                    if user.id in mem:
                        if (
                                not queue_song[str(reaction.message.guild.id)][
                                        re[3][str(reaction.message.guild.id)]
                                    ]
                                    in da1.keys()
                        ):
                            da1[
                                queue_song[str(reaction.message.guild.id)][
                                    re[3][str(reaction.message.guild.id)]
                                ]
                            ] = await get_name(
                                queue_song[str(reaction.message.guild.id)]
                            )
                        re[3][str(reaction.message.guild.id)] += 1
                        if re[3][str(reaction.message.guild.id)] >= len(
                                queue_song[str(reaction.message.guild.id)]
                        ):
                            re[3][str(reaction.message.guild.id)] -= 1
                        await reaction.message.edit(
                            embed=discord.Embed(
                                title="Downloading...",
                                description="Downloading the song, please wait for a moment",
                                color=discord.Color(value=re[8]),
                            )
                        )
                        voice = discord.utils.get(
                            client.voice_clients, guild=reaction.message.guild
                        )
                        URL = youtube_download(
                            reaction.message,
                            queue_song[str(reaction.message.guild.id)][
                                re[3][str(reaction.message.guild.id)]
                            ],
                        )
                        voice.stop()
                        voice.play(
                            discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS),
                            after=lambda e: repeat(reaction.message, voice),
                        )
                        url = queue_song[str(reaction.message.guild.id)][
                            re[3][str(reaction.message.guild.id)]
                        ]
                        song_name = da1[url]
                        await reaction.message.edit(
                            embed=discord.Embed(
                                title="Playing",
                                description=f"[{song_name}]({url})",
                                color=discord.Color(value=re[8]),
                            )
                        )
                    else:
                        await reaction.message.edit(
                            embed=discord.Embed(
                                title="Permission denied",
                                description=(
                                        "You need to join the voice channel "
                                        + str(user.name)
                                ),
                                color=discord.Color(value=re[8]),
                            )
                        )
            if reaction.emoji == "⏹":
                req()
                if (
                        str(user) != str(client.user)
                        and reaction.message.author == client.user
                ):
                    await reaction.remove(user)
                    try:
                        mem = [
                            names.id
                            for names in reaction.message.guild.voice_client.channel.members
                        ]
                    except:
                        mem = []
                    if mem.count(user.id) > 0:
                        voice = reaction.message.guild.voice_client
                        voice.stop()
                        await voice.disconnect()
                        if user.id == 734275789302005791:
                            try:
                                await clearqueue(reaction.message)
                            except:
                                pass
                        await reaction.message.edit(
                            embed=discord.Embed(
                                title="Disconnected",
                                description="Bye, Thank you for using Alfred",
                                color=discord.Color(value=re[8]),
                            )
                        )
                    else:
                        await reaction.message.edit(
                            embed=discord.Embed(
                                title="Permission denied",
                                description=(
                                        "You need to join the voice channel "
                                        + str(user.name)
                                ),
                                color=discord.Color(value=re[8]),
                            )
                        )
            if (
                    reaction.emoji == emoji.emojize(":keycap_*:")
                    and reaction.message.author == client.user
            ):
                num = 0
                bitrate = ""
                length = "\nLength of queue: " + str(
                    len(queue_song[str(reaction.message.guild.id)])
                )
                if reaction.message.guild.voice_client != None:
                    bitrate = "\nBitrate of the channel: " + str(
                        reaction.message.guild.voice_client.channel.bitrate // 1000
                    )
                if (
                        str(user) != str(client.user)
                        and reaction.message.author == client.user
                ):
                    st = ""
                    await reaction.remove(user)
                    if len(queue_song[str(reaction.message.guild.id)]) < 27:
                        for i in queue_song[str(reaction.message.guild.id)]:
                            if not i in da1.keys():
                                da1[i] = await get_name(i)
                            st = st + str(num) + ". " + da1[i] + "\n"
                            num += 1
                    else:
                        adfg = 0
                        num = -1
                        for i in queue_song[str(reaction.message.guild.id)]:
                            num += 1
                            try:
                                if re[3][str(reaction.message.guild.id)] < 10:
                                    if num < 15:
                                        if not i in da1.keys():
                                            da1[i] = await get_name(i)
                                        st = st + str(num) + ". " + da1[i] + "\n"
                                elif re[3][str(reaction.message.guild.id)] > (
                                        len(queue_song[str(reaction.message.guild.id)]) - 10
                                ):
                                    if num > (
                                            len(queue_song[str(reaction.message.guild.id)])
                                            - 15
                                    ):
                                        if not i in da1.keys():
                                            da1[i] = await get_name(i)
                                        st = st + str(num) + ". " + da1[i] + "\n"
                                else:
                                    if (
                                            re[3][str(reaction.message.guild.id)] - 10 < num <
                                            re[3][str(reaction.message.guild.id)] + 10
                                    ):
                                        if not i in da1.keys():
                                            da1[i] = await get_name(i)
                                        st = st + str(num) + ". " + da1[i] + "\n"
                            except Exception as e:
                                pass
                    await reaction.message.edit(
                        embed=discord.Embed(
                            title="Queue",
                            description=st + bitrate + length,
                            color=discord.Color(value=re[8]),
                        )
                    )
            if str(user.id) in dev_users:
                global dev_channel
                channel = client.get_channel(dev_channel)
                if (
                        reaction.emoji == emoji.emojize(":laptop:")
                        and str(reaction.message.channel.id) == str(channel.id)
                        and reaction.message.author == client.user
                ):
                    string = ""
                    await reaction.remove(user)
                    for i in dev_users:
                        string = string + str(client.get_user(int(i)).name) + "\n"
                    await channel.send(
                        embed=discord.Embed(
                            title="Developers",
                            description=string + "\n\nThank you for supporting",
                            color=discord.Color(value=re[8]),
                        )
                    )
                if reaction.emoji == emoji.emojize(":bar_chart:") and str(
                        reaction.message.channel.id
                ) == str(channel.id):
                    await reaction.remove(user)
                    cpu_per = str(int(psutil.cpu_percent()))
                    cpu_freq = f"{str(int(psutil.cpu_freq().current))}/{str(int(psutil.cpu_freq().max))}"
                    ram = str(psutil.virtual_memory().percent)
                    swap = str(psutil.swap_memory().percent)
                    usage = f"""
                    CPU Percentage: {cpu_per}
                    CPU Frequency : {cpu_freq}
                    RAM usage: {ram}
                    Swap usage: {swap}
                    """
                    await channel.send(
                        embed=discord.Embed(
                            title="Load",
                            description=usage,
                            color=discord.Color(value=re[8]),
                        )
                    )
                if reaction.emoji == emoji.emojize(":safety_vest:"):
                    await reaction.remove(user)
                    print("recover")
                    load_from_file(".recover.txt")
                    await channel.send(
                        embed=discord.Embed(
                            title="Recover",
                            description="Recovery done",
                            color=discord.Color(value=re[8]),
                        )
                    )
                if reaction.emoji == "⭕" and str(reaction.message.channel.id) == str(
                        channel.id
                ):
                    await reaction.remove(user)
                    text_servers = ""
                    for i in client.guilds:
                        text_servers = text_servers + str(i.name) + "\n"
                    await channel.send(
                        embed=discord.Embed(
                            title="Servers",
                            description=text_servers,
                            color=discord.Color(value=re[8]),
                        )
                    )
                if reaction.emoji == emoji.emojize(":fire:") and str(
                        reaction.message.channel.id
                ) == str(channel.id):
                    try:
                        voice = discord.utils.get(
                            client.voice_clients, guild=reaction.message.guild
                        )
                        voice.stop()
                        await voice.disconnect()
                    except:
                        pass
                    save_to_file()
                    print("Restart " + str(user))
                    await channel.purge(limit=100000000)
                    os.chdir(location_of_file)
                    os.system("nohup python " + location_of_file + "/main.py &")
                    await channel.send(
                        embed=discord.Embed(
                            title="Restart",
                            description=("Requested by " + str(user)),
                            color=discord.Color(value=re[8]),
                        )
                    )
                    sys.exit()
                if reaction.emoji == emoji.emojize(":cross_mark:") and str(
                        reaction.message.channel.id
                ) == str(channel.id):
                    await reaction.remove(user)
                    if len(client.voice_clients) > 0:
                        confirmation = await wait_for_confirm(
                            reaction.message, client,
                            f"There are {len(client.voice_clients)} servers listening to music through Alfred, Do you wanna exit?",
                            color=re[8], usr=user
                        )
                        if not confirmation:
                            return
                    try:
                        for voice in client.voice_clients:
                            voice.stop()
                            await voice.disconnect()
                    except:
                        pass
                    await channel.purge(limit=10000000000)
                    await channel.send(
                        embed=discord.Embed(
                            title="Exit",
                            description=("Requested by " + str(user)),
                            color=discord.Color(value=re[8]),
                        )
                    )
                    sys.exit()
                if reaction.emoji == emoji.emojize(":satellite:") and str(
                        reaction.message.channel.id
                ) == str(channel.id):
                    string = ""
                    await reaction.remove(user)
                    await channel.send("Starting speedtest")
                    download_speed = int(st_speed.download()) // 1024 // 1024
                    upload_speed = int(st_speed.upload()) // 1024 // 1024
                    servers = st_speed.get_servers([])
                    ping = st_speed.results.ping
                    await channel.send(
                        embed=discord.Embed(
                            title="Speedtest Results:",
                            description=str(download_speed)
                                        + "Mbps\n"
                                        + str(upload_speed)
                                        + "Mbps\n"
                                        + str(ping)
                                        + "ms",
                            color=discord.Color(value=re[8]),
                        )
                    )
                if reaction.emoji == "❕" and str(reaction.message.channel.id) == str(
                        channel.id
                ):
                    await reaction.remove(user)
                    issues = ""
                    if psutil.cpu_percent() > 85:
                        issues = issues + "High CPU usage\n"
                    if psutil.virtual_memory().percent > 80:
                        issues = issues + "High RAM usage\n"
                    if psutil.virtual_memory().cached < 719908352:
                        issues = issues + "Low Memory cache\n"
                    if len(entr) == 0:
                        issues = issues + "Variable entr is empty\n"
                    if len(queue_song[str(reaction.message.guild.id)]) == 0:
                        issues = issues + "Variable queue_song is empty\n"
                    if not ".recover.txt" in os.listdir():
                        issues = issues + "Recovery file not found"
                    else:
                        if re[0] < 10000 and len(re) < 4:
                            issues = issues + "Recovery required, attempting recovery\n"
                            load_from_file(".recover.txt")
                            if re[0] < 10000 and len(re) < 4:
                                issues = issues + "Recovery failed\n"
                    await channel.send(
                        embed=discord.Embed(
                            title="Issues with the program",
                            description=issues,
                            color=discord.Color(value=re[8]),
                        )
                    )
                if reaction.emoji == emoji.emojize(":black_circle:") and str(
                        reaction.message.channel.id
                ) == str(channel.id):
                    await devop_mtext(client, channel, re[8])
    except PermissionError:
        await ctx.send(embed=cembed(
            title="Missing Permissions",
            description="Alfred is missing permissions, please try to fix this, best recommended is to add Admin to the bot",
            color=re[8],
            thumbnail=client.user.avatar_url_as(format="png"))
        )
    except Exception as e:
        channel = client.get_channel(dev_channel)
        await channel.send(
            embed=discord.Embed(
                title="Error in on_reaction_add",
                description=str(e)
                            + "\n"
                            + str(reaction.message.guild)
                            + ": "
                            + str(reaction.message.channel.name),
                color=discord.Color(value=re[8]),
            )
        )


@client.command()
async def yey(ctx):
    req()
    print("yey")
    em = discord.Embed(title="*yey*", color=discord.Color(value=re[8]))
    await ctx.send(embed=em)


@client.command()
async def lol(ctx):
    req()
    em = discord.Embed(title="***L😂L***", color=discord.Color(value=re[8]))
    await ctx.send(embed=em)


@client.command(aliases=["cen"])
async def add_censor(ctx, *, text):
    req()
    string = ""
    censor.append(text.lower())
    for i in range(0, len(text)):
        string = string + "-"
    em = discord.Embed(
        title="Added " + string + " to the list",
        decription="Done",
        color=discord.Color(value=re[8]),
    )
    await ctx.send(embed=em)


@client.command()
async def changeM(ctx, *, num):
    if str(ctx.author.id) in dev_users:
        num = int(num)

        if num == 1:
            re[10] = 1
            await ctx.send(
                embed=discord.Embed(
                    title="Model change",
                    description="Changed to blenderbot",
                    color=discord.Color(value=re[8]),
                )
            )
        elif num == 2:
            re[10] = 2
            await ctx.send(
                embed=discord.Embed(
                    title="Model change",
                    description="Changed to dialo-gpt",
                    color=discord.Color(value=re[8]),
                )
            )
        else:

            await ctx.send(
                embed=discord.Embed(
                    title="Model change",
                    description="Bruh thats not a valid option",
                    color=discord.Color(value=re[8]),
                )
            )

    else:
        await ctx.send(
            embed=discord.Embed(
                title="Model change",
                description="F off thout isn't un dev user",
                color=discord.Color(value=re[8]),
            )
        )


async def transformer(api, header, json):
    async with aiohttp.ClientSession() as session:
        async with session.post(api, headers=header, json=json) as resp:
            return await resp.json()


global past_respose, generated

past_respose = []
generated = []


@client.event
async def on_message(msg):
    auth = os.getenv("transformers_auth")
    headeras = {"Authorization": f"Bearer {auth}"}
    if re[10] == 1:
        API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
    else:
        API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-large"

    try:
        for word in censor:
            if word in msg.content.lower() and msg.guild.id in [
                822445271019421746,
                841026124174983188,
                853670839891394591,
            ]:
                await msg.delete()
        if msg.guild.id in [822445271019421746]:
            if "?" in msg.content.lower() and re[4] == 1:
                await msg.channel.send("thog dont caare")
            elif "why do chips".strip() in msg.content.lower():
                await msg.channel.send(
                    "https://pics.me.me/thumb_why-do-chips-get-stale-gross-i-just-eat-a-49666262.png"
                )
            else:
                if re[4] == 1:
                    for i in ["what", "how", "when", "why", "who", "where"]:
                        if i in msg.content.lower():
                            await msg.channel.send("thog dont caare")
                            break

        if msg.content.lower().startswith("alfred"):

            input_text = msg.content.lower().replace("alfred", "")
            payload = {
                "inputs": {
                    "past_user_inputs": past_respose,
                    "generated_responses": generated,
                    "text": input_text,
                },
                "parameters": {"repetition_penalty": 1.33},
            }

            output = await transformer(API_URL, header=headeras, json=payload)

            if len(past_respose) < 50:
                past_respose.append(input_text)
                generated.append(output["generated_text"])
            else:
                past_respose.pop(0)
                generated.pop(0)
                past_respose.append(input_text)
                generated.append(output["generated_text"])

            print(output)
            await msg.reply(output["generated_text"])

        if f"<@!{client.user.id}>" in msg.content:
            prefi = prefix_dict.get(msg.guild.id, "'")
            embed = discord.Embed(
                title="Hi!! I am Alfred.",
                description=f"""Prefix is {prefi}\nFor more help, type {prefi}help""",
                color=discord.Color(value=re[8]),
            )
            embed.set_image(
                url=random.choice(
                    [
                        "https://giffiles.alphacoders.com/205/205331.gif",
                        "https://c.tenor.com/PQu-tE-5HxwAAAAd/michael-caine-the-dark-knight.gif",
                    ]
                )
            )

            await msg.channel.send(embed=embed)
        if msg.content.startswith(prefix_dict.get(msg.guild.id, "'")) == 0:
            save_to_file("recover")
        await client.process_commands(msg)
    except Exception as e:
        channel = client.get_channel(dev_channel)
        await channel.send(
            embed=discord.Embed(
                title="Error", description=str(e), color=discord.Color(value=re[8])
            )
        )


@client.command()
async def thog(ctx, *, text):
    if ctx.author.guild_permissions.administrator:
        if re[1] == text:
            re[4] = re[4] * -1
            if re[4] == 1:
                await ctx.send(
                    embed=discord.Embed(
                        title="Thog",
                        description="Activated",
                        color=discord.Color(value=re[8]),
                    )
                )
            else:
                await ctx.send(
                    embed=discord.Embed(
                        title="Thog",
                        description="Deactivated",
                        color=discord.Color(value=re[8]),
                    )
                )
        else:
            await ctx.message.delete()
            await ctx.send("Wrong password")
    else:
        await ctx.send(
            embed=cembed(
                title="Permissions Denied",
                description="You cannot toggle thog",
                color=re[8],
            )
        )


@client.command(aliases=["m"])
async def python_shell(ctx, *, text):
    req()
    print("Python Shell", text, str(ctx.author))
    global dev_users
    if str(ctx.author.id) in dev_users:
        if str(ctx.author.guild.id) != "727061931373887531":
            try:
                text = text.replace("```py", "")
                text = text.replace("```", "")
                a = eval(text)
                print(text)
                em = discord.Embed(
                    title=text,
                    description=text + "=" + str(a),
                    color=discord.Color(value=re[8]),
                )
                em.set_thumbnail(
                    url="https://engineering.fb.com/wp-content/uploads/2016/05/2000px-Python-logo-notext.svg_.png"
                )
                await ctx.send(embed=em)
            except Exception as e:
                await ctx.send(
                    embed=discord.Embed(
                        title="Error_message",
                        description=str(e),
                        color=discord.Color(value=re[8]),
                    )
                )
        else:
            await ctx.send(
                embed=discord.Embed(
                    title="Banned",
                    description="You've been banned from using python shell",
                    color=discord.Color(value=re[8]),
                )
            )
    else:
        await ctx.message.delete()
        await ctx.send(
            embed=discord.Embed(
                title="Permission denied",
                description="",
                color=discord.Color(value=re[8]),
            )
        )


@client.command()
async def exe(ctx, *, text):
    req()
    global temp_dev
    if (ctx.author.id in temp_dev and protect(text)) or (
            str(ctx.author.id) in dev_users
    ):
        mysql_password = "Denied"
        if text.find("passwd=") != -1:
            mysql_password = os.getenv("mysql")
        text = text.replace("```py", "```")
        text = text[3:-3].strip()
        f = StringIO()
        with redirect_stdout(f):
            try:
                exec(text)
            except Exception as e:
                traceback.print_tb(e.__traceback__)
                error_mssg = "Following Error Occured:\n" + "\n".join(
                    [
                        line
                        for line in traceback.format_exception(
                        type(e), e, e.__traceback__
                    )
                        if "in exe" not in line
                    ]
                )
                await ctx.send(
                    embed=discord.Embed(
                        title="Error",
                        description=error_mssg,
                        color=discord.Color.from_rgb(255, 40, 0),
                    )
                )
        output = f.getvalue()
        embeds = []
        if output == "":
            output = "_"
        for i in range(len(output) // 2000):
            em = cembed(title="Python", description=output[i * 2000:i * 2000 + 2000], color=re[8])
            em.set_thumbnail(
                url="https://engineering.fb.com/wp-content/uploads/2016/05/2000px-Python-logo-notext.svg_.png"
            )
            embeds.append(em)
        await pa(embeds, ctx)
    else:
        await ctx.send(
            embed=discord.Embed(
                title="Denied",
                description="Ask Devs to give access for scripts",
                color=discord.Color(value=re[8]),
            )
        )


@client.command()
async def gen(ctx, *, text):
    req()
    API_URL2 = "https://api-inference.huggingface.co/models/EleutherAI/gpt-neo-2.7B"
    header2 = {"Authorization": f"Bearer {os.environ['transformers_auth']}"}
    payload2 = {
        "inputs": text,
        "parameters": {"max_new_tokens": 250, "return_full_text": True},
    }

    output = await genpost(API_URL2, header2, payload2)
    await ctx.reply(
        embed=cembed(
            title="Generated text", description=output[0]["generated_text"], color=re[8]
        )
    )


@client.command()
async def get_req(ctx):
    req()
    number = g_req()
    em = discord.Embed(
        title="Requests", description=str(number), color=discord.Color(value=re[8])
    )
    await ctx.send(embed=em)


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


@client.command(aliases=['muter'])
async def set_mute_role(ctx, role_for_mute: discord.Role):
    if ctx.author.guild_permissions.administrator:
        mute_role[ctx.guild.id] = role_for_mute.id
        await ctx.send(embed=cembed(title="Done", description=f"Mute role set as {role_for_mute.mention}", color=re[8]))
    else:
        await ctx.send(embed=cembed(title="Permissions Denied", description="You need to be an admin to set mute role",
                                    color=re[8]))


@client.command(aliases=["mu"])
@commands.has_permissions(kick_members=True)
async def mute(ctx, member: discord.Member):
    req()
    print("Member id: ", member.id)
    add_role = None
    if ctx.guild.id in mute_role:
        add_role = [i for i in ctx.guild.roles if i.id == mute_role[ctx.guild.id]][0]
        await member.add_roles(add_role)
        await ctx.send("Muted " + member.mention)
    else:
        add_role = discord.utils.get(ctx.guild.roles, name="dunce")
        await member.add_roles(add_role)
        await ctx.send("Muted " + member.mention)


@client.command(aliases=["um"])
@commands.has_permissions(kick_members=True)
async def unmute(ctx, member: discord.Member):
    req()
    add_role = None
    if ctx.guild.id in mute_role:
        add_role = [i for i in ctx.guild.roles if i.id == mute_role[ctx.guild.id]][0]
        await member.remove_roles(add_role)
        await ctx.send("Unmuted " + member.mention)
    else:
        add_role = discord.utils.get(ctx.guild.roles, name="dunce")
        await member.remove_roles(add_role)
        await ctx.send("Unmuted " + member.mention)
        print(member, "unmuted")


@client.command()
async def testing_help(ctx):
    test_help = []
    thumbnail = "https://static.wikia.nocookie.net/newdcmovieuniverse/images/4/47/Pennyalf.PNG/revision/latest?cb=20190207195903"
    test_help.append(
        cembed(
            title="Help",
            description="Hi I am Alfred. I was made by [Alvin](https://github.com/alvinbengeorge/).\nPrefix for this bot is '",
            thumbnail=thumbnail,
            picture=client.user.avatar_url_as(format="png"),
            color=re[8],
        )
    )
    test_help.append(
        cembed(
            title="Source Code for Alfred",
            description="Here you go, click this link and it'll redirect you to the github page\n[Github page](https://github.com/alvinbengeorge/alfred-discord-bot)\n\nClick this link to invite the bot \n[Invite Link](https://discord.com/oauth2/authorize?client_id=811591623242154046&permissions=8&scope=bot%20applications.commands)",
            color=re[8],
            thumbnail="https://github.githubassets.com/images/modules/open_graph/github-octocat.png",
            picture=client.user.avatar_url_as(format="png"),
        )
    )
    test_help += helping_hand.help_him(ctx, client, re)
    await pa(test_help, ctx)


@slash.slash(name="help", description="Help from Alfred")
async def help_slash(ctx):
    req()
    await ctx.defer()
    await h(ctx)


client.remove_command("help")


@client.group(invoke_without_command=True)
async def help(ctx):
    req()
    print("help")
    embeds = []
    for i in help_list:
        em = discord.Embed(
            title="```Help```", description=i, color=discord.Color(value=re[8])
        )
        em.set_thumbnail(
            url="https://static.wikia.nocookie.net/newdcmovieuniverse/images/4/47/Pennyalf.PNG/revision/latest?cb=20190207195903"
        )
        embeds.append(em)
    await pa(embeds, ctx)


@client.group(invoke_without_command=True)
async def h(ctx):
    req()
    print("help")
    embeds = []
    for i in help_list:
        em = discord.Embed(
            title="```Help```", description=i, color=discord.Color(value=re[8])
        )
        em.set_thumbnail(
            url="https://static.wikia.nocookie.net/newdcmovieuniverse/images/4/47/Pennyalf.PNG/revision/latest?cb=20190207195903"
        )
        embeds.append(em)
    await pa1(embeds, ctx)


client.run(os.getenv("token"))
