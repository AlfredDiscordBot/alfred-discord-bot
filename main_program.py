"""
Set your env like the example below:
token=
sjdoskenv=
sjdoskenv1=
mysql=
default=
dev=
"""

def temporary_fix():
    from shutil import copyfile
    copyfile("./utils/post.py","/opt/virtualenvs/python3/lib/python3.8/site-packages/instascrape/scrapers/post.py")
    
import os
import sys
sys.path.insert(1,f"{os.getcwd()}/utils/")
temporary_fix()
from keep_alive import keep_alive
import string
import nextcord
from utils import helping_hand
from random import choice
from nextcord import Interaction, SlashOption, ChannelType
from nextcord.ext import commands, tasks
from nextcord.abc import GuildChannel
from GoogleNews import GoogleNews
from dotenv import load_dotenv
from math import *
from statistics import *
from wikipedia import search, summary
from utils.Storage_facility import Variables
from io import StringIO
from contextlib import redirect_stdout
from utils.External_functions import *
import traceback
import googlesearch
import youtube_dl
import re as regex
import urllib.request
import ffmpeg
import time
import emoji
import psutil
import asyncio
import cloudscraper
import requests
import aiohttp
from io import BytesIO
import src.error as ror
from utils.spotify_client import *
import assets

location_of_file = os.getcwd()
start_time = time.time()
try:
    load_dotenv()
except:
    pass
import speedtest

try:
    st_speed = speedtest.Speedtest()
except:
    print("failed")
googlenews = GoogleNews()

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
global sent
global past_respose, generated
observer=[]
mspace={}
past_respose = []
generated = []
deathrate = {}
sent = None
instagram_posts = []
intents = nextcord.Intents().default()
intents.members = True
censor = []
old_youtube_vid = {}
youtube_cache = {}
run_suicide = False
deleted_message = {}
config = {
    'snipe': [841026124174983188, 822445271019421746,830050310181486672, 912569937116147772],
    'respond': [],
    'youtube': {},
    'welcome': {},
    'ticket' : {},
    'security':{}
    }
da = {}
errors = ["```arm"]
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
autor = {}
SESSIONID = None
color_message = None
color_temp = ()
link_for_cats = []
vc_channel = {}
wolfram = os.getenv("wolfram")
prefix_dict = {}
#minor change for github to accept this new branch



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

print("Starting")

def reset_emo():
    emo = assets.Emotes(client)
    return emo
    
def youtube_download(ctx, url):
    with youtube_dl.YoutubeDL(ydl_op) as ydl:
        info=ydl.extract_info(url, download=False) 
        URL = info["formats"][0]["url"]
    return URL

def youtube_download1(ctx, url):
    with youtube_dl.YoutubeDL(ydl_op) as ydl:
        info=ydl.extract_info(url, download=False)
        name=info['title']
        URL = info["formats"][0]["url"]
    return (URL, name)

async def search_vid(name):
    pass

def prefix_check(client, message):
    save_to_file()
    return prefix_dict.get(message.guild.id if message.guild is not None else None, "'"),f"<@{client.user.id}> "


client = nextcord.ext.commands.Bot(
    command_prefix=prefix_check,
    intents=intents,
    case_insensitive=True,
)

def save_to_file():
    global dev_users
    #print("save")
    v = Variables("backup")
    v.pass_all(
        censor = censor,
        da = da,
        da1 = da1,
        entr = entr,
        queue_song = queue_song,
        a_channels = a_channels,
        re = re,
        dev_users = dev_users,
        prefix_dict = prefix_dict,
        observer = observer,
        old_youtube_vid = old_youtube_vid,
        config = config,
        mspace = mspace,
        autor = autor
    )
    v.save()


def load_from_file():
    global censor
    global da
    global da1
    global queue_song
    global entr
    global re
    global dev_users
    global prefix_dict
    global observer
    global old_youtube_vid
    global config
    global mspace
    global autor


    v = Variables("backup").show_data()
    censor = v.get("censor",[])
    da = v.get("da",{})
    da1 = v.get("da1", {})
    queue_song = v.get("queue_song",{})
    entr = v.get("entr",{})
    a_channels = v.get("a_channels",[])
    re = v.get("re",re)
    dev_users = v.get("dev_users",dev_users)
    prefix_dict = v.get("prefix_dict",{})
    observer = v.get("observer",[])
    old_youtube_vid = v.get("old_youtube_vid",{})
    config = v.get("config",config)
    mspace = v.get("mspace",{})
    autor = v.get("autor",{})
    


load_from_file()

report = f"""Started at: {timestamp(int(start_time))}
Current location: {location_of_file}
Requests: {re[0]:,}
Color: {nextcord.Color(re[8]).to_rgb()}
```yml
[ OK ] Loaded all modules
[ OK ] Setup SpeedTest and GoogleNews
[ OK ] Variables initialised 
[ OK ] Load From File Completed
[ OK ] Switching Root ...
[ OK ] Starting On Ready
"""



@client.event
async def on_ready():
    print(client.user)    
    global report
    report+=f"[ OK ] Bot named as {client.user.name}\n"
    channel = client.get_channel(dev_channel)
    if channel:
        report+="[ OK ] Devop found, let's go\n"
    try:
        print("Starting Load from file")
        load_from_file()
        print("Finished loading\n")
        print("\nStarting devop display")
        await devop_mtext(client, channel, re[8])
        report+="[ OK ] Sending Devop Message\n"
        print("Finished devop display")
        print("Starting imports")
        imports = ""
        sys.path.insert(1, location_of_file + "/src")
        for i in os.listdir(location_of_file + "/src"):
            if i.endswith(".py"):
                a = ""
                try:
                    print(i, end="")
                    requi = __import__(i[0 : len(i) - 3]).requirements()
                    # if requi != "":
                    #     requi = "," + requi
                    if type(requi) is str:
                        a = f"__import__('{i[0:len(i)-3]}').main(client,{requi})"
                        eval(a)
                    if type(requi) is list:
                        a = f"__import__('{i[0:len(i)-3]}').main(client,{','.join(requi)})"
                        eval(a)
                    imports = imports + i[0 : len(i) - 3] + "\n"
                    print(": Done")
                    report+=f"[ OK ] Imported {i} successfully\n"
                except Exception as e:
                    await channel.send(
                        embed=cembed(
                            title="Error in plugin " + i[0 : len(i) - 3],
                            description=str(e),
                            color=nextcord.Color(value=re[8]),
                            footer=a
                        )
                    )
                    report+=f"[ {int(time.time()-start_time)} ] Error in {i}: {e}\n"
                    errors.append(f"[ {int(time.time()-start_time)} ] Error in {i}: {str(e)[:10]}...\n")
        await channel.send(
            embed=nextcord.Embed(
                title="Successfully imported",
                description=imports,
                color=nextcord.Color(value=re[8]),
            )
        )
        global run_suicide
        run_suicide = True
        await client.rollout_application_commands()
        
    except Exception as e:
        mess = await channel.send(
            embed=nextcord.Embed(
                title="Error in the function on_ready",
                description=str(e),
                color=nextcord.Color(value=re[8]),
            )
        )
        await mess.add_reaction("❌")
    dev_loop.start()
    print("Prepared")
    youtube_loop.start()
    send_file_loop.start()
    report+="```"
    await channel.send(
        embed=cembed(
            title="Report",
            description=report,
            color=re[8],
            thumbnail=client.user.avatar.url
        )
    )

@tasks.loop(hours=4)
async def send_file_loop():
    await client.get_channel(941601738815860756).send(file=nextcord.File("backup.dat",filename="backup.dat"))
    
@tasks.loop(minutes=30)
async def youtube_loop():
    await client.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.listening, name=str(len(client.guilds))+" servers"))
    print("Youtube_loop")    
    for i,l in config['youtube'].items():
        await asyncio.sleep(2)
        for j in l:
            a = get_youtube_url(j[0])
            if a[0]=="https://www.youtube.com/" or a[0]=="https://www.youtube.com":
                return
            if not old_youtube_vid.get(i, None):
                old_youtube_vid[i] = {}
            if not old_youtube_vid[i].get(j[0], None):
                old_youtube_vid[i][j[0]] = ""
            if old_youtube_vid[i][j[0]] == a[0]:
                continue
            old_youtube_vid[i][j[0]] = a[0]
            try:
                message=j[1]
                await client.get_channel(i).send(embed=cembed(title="New Video out", description=f"New Video from {j[0]}",url=a[0],color=re[8],thumbnail=client.get_channel(i).guild.icon.url))
                await client.get_channel(i).send(a[0]+"\n"+message)
            except Exception as e:
                await client.get_channel(dev_channel).send(embed=cembed(title="Error in youtube_loop",description=f"{str(e)}\nSomething is wrong with channel no. {i}",color=re[8]))            
    save_to_file()


@tasks.loop(minutes = 1)
async def dev_loop():
    try:
        await get_async("https://suicide-detector-api-1.yashvardhan13.repl.co/")
        await get_async("https://Ellisa-Bot.arghyathegod.repl.co")
    except:
        pass
    save_to_file()

@client.slash_command(name = "embed", description = "Create a quick embed using slash commands")
async def quickembed(ctx, text):
    await ctx.send(
        embed=cembed(
            description = text,
            color=re[8]
        )
    )

@client.slash_command(name="neofetch", description="Get Status of the bot")
async def neo(ctx):
    await ctx.response.defer()    
    await neofetch(ctx)
    
@client.command()
async def neofetch(ctx):
    text = helping_hand.neofetch
    text += f"Name   : {client.user.name}\n"
    text += f"ID     : {client.user.id}\n"
    text += f"Users  : {len(client.users)}\n"
    text += f"Servers: {len(client.guilds)}\n"
    text += f"Uptime : {int(time.time()-start_time)}"
    await ctx.send("```yml\n"+text+"\n```")

@client.command()
async def svg(ctx, *, url):
    img = svg2png(url)
    await ctx.send(file=nextcord.File(BytesIO(img), "svg.png"))


@dev_loop.before_loop
async def wait_for_ready():
    await client.wait_until_ready()

@send_file_loop.before_loop
async def wait_for_ready():
    await client.wait_until_ready()


@youtube_loop.before_loop
async def wait_for_ready():
    await client.wait_until_ready()


@client.command()
async def imdb(ctx, *, movie):
    await ctx.send(embed=imdb_embed(movie,re))

@client.command()
async def sniper(ctx):
    if getattr(ctx, 'author', getattr(ctx, 'user', None)).guild_permissions.administrator:
        output=""
        if ctx.guild.id in config['snipe']:
            config['snipe'].remove(ctx.guild.id)
            output="All people can use the snipe command"
            
        else:
            config['snipe'].append(ctx.guild.id)
            output="Only admins can use snipe command"

        await ctx.send(embed=cembed(
            title="Done",
            description=output,
            color=re[8],
            thumbnail=client.user.avatar.url)
        )
    else:
        await ctx.send(
            embed=cembed(
                title="Permission Denied",
                description="Only an admin can toggle this setting",
                color=re[8]
            )
        )
@client.command(aliases=["vote","top.gg",'v'])
async def vote_alfred(ctx):
    await ctx.send(
        embed=cembed(
            title="Hi there",
            description="Alfred is now available in top.gg, so pls vote for it using [the link](https://top.gg/bot/811591623242154046/vote)",
            color=re[8],
            thumbnail=client.user.avatar.url,
            image="https://blog.top.gg/content/images/2021/12/logo-white-5.png",
            footer="Stay Safe and be happy | Gotham Knights"
        )
    )

@client.slash_command("vote",description="Vote for Alfred in top.gg")
async def vo(ctx):
    await vote_alfred(ctx)
    
@client.command(aliases=['response'])
async def toggle_response(ctx):
    if getattr(ctx, 'author', getattr(ctx, 'user', None)).guild_permissions.administrator:
        output=""
        if ctx.guild.id in config['respond']:
            config['respond'].remove(ctx.guild.id)
            output="Auto respond turned on"
            
        else:
            config['respond'].append(ctx.guild.id)
            output="Auto respond turned off"

        await ctx.send(embed=cembed(
            title="Enabled",
            description=output,
            color=re[8],
            thumbnail=client.user.avatar.url)
        )
    else:
        await ctx.reply(
            embed=cembed(
                title="Permissions Denied",
                description="You need admin permissions to toggle this",
                color=nextcord.Color.red(),
                thumbnail=client.user.avatar.url
            )
        )

@client.slash_command(name = "giveaway", description = "You can use this for giveaway")
async def giveaway(ctx, role_to_ping:nextcord.Role = None, donor:nextcord.User = None, heading = "Giveaway", description = "Giveaway", emoj = emoji.emojize(":party_popper:")):
    await ctx.response.defer()
    if not ctx.user.guild_permissions.administrator:
        await ctx.send(
            embed=cembed(
                title="Permissions Denied",
                description="You need admin permission to access this function",
                color=re[8]
            )
        )
        return
    if heading is None: heading = "Giveaway"    
    if donor is None:donor = ctx.user
    embed=cembed(
        title=heading,
        description=description,
        color=re[8]
    )    
    text = "Giveaway" + str(role_to_ping.mention) if role_to_ping is not None else ""
    embed.set_author(name=donor.name,icon_url=safe_pfp(donor))
    m = await ctx.send("Giveaway",embed=embed)
    await ctx.send(text)
    await m.add_reaction(emoj)

@client.command()
@commands.cooldown(1,10,commands.BucketType.guild)
async def roll(ctx):
    if not ctx.author.guild_permissions.administrator:
        await ctx.send(
            embed=cembed(
                title="Permissions Denied",
                description="You need admin permission to access this function"
            )
        )
        return
    if not ctx.message.reference:
        await ctx.send("You need to reply to a giveaway message by Alfred")
        return
    message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
    if not message.author == client.user:
        await ctx.reply("Heyyyyy, wait a minute, that's not my giveaway mesage")
        return
    if not message.clean_content.startswith("Giveaway"): 
        await ctx.reply("Ok that's my messsage, but is that a giveaway message?????")
        return
    reaction = message.reactions[0]
    users = await reaction.users().flatten()
    users.remove(client.user)
    await message.edit(
        embed=cembed(
            title="Time up",
            description="The giveaway has ended, hope you get it the next time",
            color=re[8],
            thumbnail=client.user.avatar.url
        )
    )
    lu = random.choice(users)
    await reaction.remove(lu)
    lu = lu.mention
    await ctx.send(f"Congragulations, {lu} has won the giveaway")
    

@client.slash_command(name = "pfp",description="Get a person's avatar")
async def pfp_pic(ctx, member: nextcord.User = "-"):
    if member == "-": member = ctx.user
    await get_pfp(ctx, member)

@client.command(aliases=["pfp"])
async def get_pfp(ctx, member:nextcord.Member=None):    
    req()   
    user = getattr(ctx,'author',getattr(ctx,'user',None))
    if not member: member = user
    embed=cembed(
        title=f"Profile Picture -> {member.name}",
        footer=f"Amazing picture | Requested by {user.name}",
        picture=safe_pfp(member),
        color=member.color
    )
    await ctx.send(embed=embed)
    
@client.slash_command(name="effects",description="cool effects with your profile picture")
async def eff(ctx, effect = helping_hand.effects_helper(), member:nextcord.Member="-"):
    await ctx.response.defer()
    if member == "-": member = ctx.user
    await effects(ctx, effect = effect, member = member)

@client.slash_command(name="removeduplicates", description = "removes all the duplicate songs in your queue")
async def remove_duplicates(ctx):    
    await ctx.response.defer()
    re[3][str(ctx.guild.id)] = 0
    songs = queue_song[str(ctx.guild.id)]
    for i in songs:
        if queue_song[str(ctx.guild.id)].count(i)>1:
            queue_song[str(ctx.guild.id)].remove(i)
    await ctx.send(
        embed=cembed(
            title="Done",
            description=f"Removed songs",
            color = re[8]
        )
    )
    
@client.command(aliases=['ef','effect'])
async def effects(ctx, effect:str = None, member:nextcord.Member=None):
    req()
    if member == None:
        url = getattr(ctx, 'author', getattr(ctx, 'user', None)).avatar.url
    else:
        print(member)
        url = member.avatar.url
    url = str(url)

    if effect == None:
        await ctx.send(
                    embed=cembed(
                        title="OOPS",
                        description="""Hmm You seem to be forgetting an argument \n `effects <effect> <member>` if member is none the users pfp will be modified \n The list of effects is \n- cartoonify \n- watercolor \n- canny \n- pencil \n- econify \n- negative \n- pen \n- candy \n- composition \n- feathers \n- muse \n- mosaic \n- night \n- scream \n- wave \n- udnie """,
                        color=re[8],
                    )
                )
        return

    styles = ['candy', 'composition', 'feathers', 'muse', 'mosaic', 'night', 'scream', 'wave', 'udnie']

    effects = ['cartoonify', 'watercolor', 'canny', 'pencil', 'econify', 'negative', 'pen']

    if effect not in styles and effect not in effects and effect is not None:
        await ctx.send(
                    embed=cembed(
                        title="OOPS",
                        description="""hmm no such effect. The effects are given below. \n `effects <effect> <member> if member is none the users pfp will be modified \n The list of effects is \n- cartoonify \n- watercolor \n- canny \n- pencil \n- econify \n- negative \n- pen \n- candy \n- composition \n- feathers \n- muse \n- mosaic \n- night \n- scream \n- wave \n- udnie """,
                        color=re[8],
                    )
                )
        return
    elif effect in styles:
        json = {"url":url, "effect":effect}

        byte = await post_async("https://suicide-detector-api-1.yashvardhan13.repl.co/style", json=json, output="content")

    elif effect in effects:
        json = {"url":url, "effect":effect}

        byte = await post_async("https://suicide-detector-api-1.yashvardhan13.repl.co/cv", json=json)    
        
    await ctx.send(file=nextcord.File(BytesIO(byte), 'effect.png'))

@client.command(aliases=['transform'])
async def blend(ctx, urlef:str = None, member:nextcord.Member=None, ratio=0.5):
    req()
    if member == None:
        url = getattr(ctx, 'author', getattr(ctx, 'user', None)).avatar.url
    else:
        url = member.avatar.url

    url = str(url)

    if urlef == None:
        await ctx.send(
                    embed=cembed(
                        title="OOPS",
                        description="""Hmm You seem to be forgetting an argument \n 'effects <style url> <member[optional]> <ratio[optional]> if member is none the users pfp will be modified. The default ratio is 0.5""",
                        color=re[8],
                    )
                )
        return

    json = {"url":url, "url2":urlef, "ratio":ratio}

    byte = await post_async("https://suicide-detector-api-1.yashvardhan13.repl.co/style_predict", json=json)
    await ctx.send(file=nextcord.File(BytesIO(byte), 'effect.png'))


@client.command(aliases=['autoreaction'])
async def autoreact(ctx, channel: nextcord.TextChannel = None,*, Emojis: str = ""):
    if not getattr(ctx, 'author', getattr(ctx, 'user', None)).guild_permissions.administrator:
        await ctx.send(
            embed=cembed(
                title="Permissions Denied",
                description="You cannot set autoreact, you do not have admin privilege",
                color=re[8]
            )
        )
        return
    if not channel:
        await ctx.send(
            embed=cembed(
                title="Hmm",
                description=emoji.emojize("You need to mention a channel\n'autoreact #channel :one:|:two:|:three:"),
                color=re[8]
            )
        )
        return
    if Emojis == "":
        await ctx.send(
            embed = cembed(
                title="Hmm",
                description="You need one or more emojis separated by |",
                color=re[8]
            )
        )
        return
    if channel.id not in autor:
        autor[channel.id]=[i.strip() for i in emoji.demojize(Emojis).split("|")]
    else:
        autor[channel.id]+=[i.strip() for i in emoji.demojize(Emojis).split("|")]
    await ctx.send(
        embed=cembed(
            title="Done",
            description=f"For every message in {channel.mention} Alfred will add {Emojis} reaction",
            color=re[8]
        )
    )




@client.command()
async def remove_autoreact(ctx, channel: nextcord.TextChannel = None):
    if not getattr(ctx, 'author', getattr(ctx, 'user', None)).guild_permissions.administrator:
        await ctx.send(
            embed=cembed(
                title="Permissions Denied",
                description="You cannot remove autoreact, you do not have admin privilege",
                color=re[8]
            )
        )
        return
    if not channel.id in autor:
        await ctx.send(
            embed=cembed(
                title="Hmm",
                description="This channel does not have any reactions",
                color=re[8]
            )
        )
        return
    confirmation = await wait_for_confirm(ctx,client,"Do you want to remove every automatic reaction in this channel?",color=re[8],usr=getattr(ctx, 'author', getattr(ctx, 'user', None)))
    if not confirmation:
        return
    autor.pop(channel.id)
    await ctx.send(
        embed=cembed(
            title="Done",
            description="Removed every reaction in ",
            color=re[8]
        )
    )

@client.command(aliases=['suicide'])
async def toggle_suicide(ctx):
    if getattr(ctx, 'author', getattr(ctx, 'user', None)).guild_permissions.administrator:
        output=""
        if ctx.guild.id in observer:
            observer.remove(ctx.guild.id)
            output="enabled"
        else:
            observer.append(ctx.guild.id)
            output="disabled"
        await ctx.reply(embed=cembed(title="Done",description=f"I've {output} the suicide observer",color=re[8]))
    else:
        await ctx.send(
            embed=cembed(
                title="Permission Denied",
                description="Only an admin can toggle this setting",
                color=re[8]
            )
        )

@client.slash_command(name = "subscribe", description = "Subscribe to a youtube channel")
async def sub_slash(ctx, channel: GuildChannel = None, url = None, message = ""):
    await ctx.response.defer()
    await subscribe(ctx, channel = channel, url = url, message = message)

@client.slash_command(name = "unsubscribe", description = "remove a youtube channel from a textchannel")
async def unsub_slash(ctx, channel: GuildChannel = None, url = None):
    await ctx.response.defer()
    await unsubscribe(ctx, channel = channel, url = url)

@client.command()
async def subscribe(ctx, channel: nextcord.TextChannel=None, url=None, *, message=""):
    if getattr(ctx, 'author', getattr(ctx, 'user', None)).guild_permissions.administrator:
        if 'youtube' not in config: config['youtube']={}
        if channel.id not in config['youtube']: config['youtube'][channel.id]=set()
        if url is not None:
            url = check_end(url)
            config['youtube'][channel.id].add((url,message))
            await ctx.send(embed=cembed(title="Done",description=f"Added {url} to the list and it'll be displayed in {channel.mention}",color=re[8],thumbnail=client.user.avatar.url))
        else:
            all_links = "\n".join([i[0] for i in config['youtube'][channel.id]])
            await ctx.send(embed=cembed(
                title="All youtube subscriptions in this channel",
                description=all_links,
                color=re[8],
                thumbnail = client.user.avatar.url
            ))
    else:
        await ctx.send(
            embed=cembed(
                title="Permission Denied",
                description="Only an admin can set it",
                color=re[8],
                thumbnail=client.user.avatar.url
            )
        )

@client.command()
async def unsubscribe(ctx, channel: nextcord.TextChannel=None, url=None):
    if getattr(ctx, 'author', getattr(ctx, 'user', None)).guild_permissions.administrator:
        if 'youtube' not in config: config['youtube']={}
        if channel.id not in config['youtube']: config['youtube'][channel.id]=set()
        if url is None:   
            all_links = "\n".join([i[0] for i in config['youtube'][channel.id]])
            await ctx.send(embed=cembed(
                title="All youtube subscriptions in this channel",
                description=all_links,
                color=re[8],
                thumbnail = client.user.avatar.url
            ))
            return
        try:
            url = check_end(url)
            for u,m in config['youtube'][channel.id]:
                if u == url:
                    config['youtube'][channel.id].remove((u,m))
                    break

            
            await ctx.send(embed=cembed(title="Done",description=f"Removed {url} from the list",color=re[8],thumbnail=client.user.avatar.url))
        except KeyError:
            await ctx.reply(embed=cembed(title="Hmm",description=f"The URL provided is not in {channel.name}'s subscriptions",color=re[8]))
    else:
        await ctx.send(
            embed=cembed(
                title="Permission Denied",
                description="Only an admin can remove subscriptions",
                color=re[8],
                thumbnail=client.user.avatar.url
            )
        )



@client.command()
@commands.cooldown(1,1000,commands.BucketType.guild)
async def entrar(ctx, *, num=re[6]):
    print("Entrar", str(getattr(ctx, 'author', getattr(ctx, 'user', None))))
    global re
    re[0] = re[0] + 1
    lol = ""
    header = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36",
        "referer": "https://entrar.in",
    }
    suvzsjv = {
        "username": os.getenv("sjdoskenv"),
        "password": os.getenv("sjdoskenv1"),
        "captcha": "0",
    }
    announcement_data = {"announcementlist": "true", "session": "205"}
    re[6] = num
    announcement_data["session"] = str(num)
    # class="label-input100"
    try:
        with requests.Session() as s:
            scraper = cloudscraper.create_scraper(sess=s)
            r = scraper.get("https://entrar.in/login/login", headers=header)
            st = r.content.decode()
            start_captcha = st.find(
                '<span class="label-input100" style="font-size: 18px;">'
            ) + len('<span class="label-input100" style="font-size: 20px;">')
            end_captcha = st.find("=", start_captcha)
            suvzsjv["captcha"] = str(eval(st[start_captcha:end_captcha]))
            url = "https://entrar.in/login/auth/"
            r = scraper.post(url, data=suvzsjv, headers=header)
            r = scraper.get("https://entrar.in/", headers=header)
            r = scraper.post(
                "https://entrar.in/parent_portal/announcement", headers=header
            )
            r = scraper.get(
                "https://entrar.in/parent_portal/announcement", headers=header
            )
            await asyncio.sleep(2)
            r = scraper.post(
                "https://entrar.in/parent_portal/announcement",
                data=announcement_data,
                headers=header,
            )
            channel = nextcord.utils.get(ctx.guild.channels, name="announcement")
            if ctx.guild.id == 727061931373887531:
                channel = nextcord.utils.get(ctx.guild.channels, name="bot")
            elif ctx.guild.id == 743323684705402951:
                channel = client.get_channel(868085346867490866)
            st = r.content.decode()
            for i in range(1, 5):
                await asyncio.sleep(1)
                a = st.find('<td class="text-wrap">' + str(i) + "</td>")
                b = st.find('<td class="text-wrap">' + str(i + 1) + "</td>")
                print(a, b)
                le = len('<td class="text-wrap">' + str(i + 1) + "</td>") - 1
                if b == -1:
                    await ctx.send(
                        embed=nextcord.Embed(
                            title="End Of List",
                            description="",
                            color=nextcord.Color(value=re[8]),
                        )
                    )
                    break
                c = st.find("&nbsp;&nbsp; ", a, b) + len("&nbsp;&nbsp; ")
                d = st.find("<", c, b)
                out = st[c:d].strip()
                e = a + le
                f = st.find("<td>", e, e + 15) + len("<td>")
                g = st.find("</td>", e, e + 45)
                date = st[f:g]
                h = st.find('<a target="_blank" href="', a, b) + len(
                    '<a target="_blank" href="'
                )
                j = st.find('"', h, b)
                try:
                    link = str(st[h:j])
                    print(link)
                    if (
                        link
                        == 'id="simpletable" class="table table-striped table-bordered nowrap'
                    ):
                        continue
                    req = scraper.get(link)
                    k = out + date
                    if not str(ctx.guild.id) in entr:
                        entr[str(ctx.guild.id)] = []
                    if k in entr[str(ctx.guild.id)]:
                        continue
                    entr[str(ctx.guild.id)].append(str(k))
                    lol = lol + out + " Date:" + date + "\n"
                    with open((out + ".pdf"), "wb") as pdf:
                        pdf.write(req.content)
                        await channel.send(file=nextcord.File(out + ".pdf"))
                        pdf.close()
                    os.remove(out + ".pdf")
                except Exception as e:
                    print(traceback.print_exc())
            if lol != "":
                embed = nextcord.Embed(
                    title="New announcements",
                    description=lol,
                    color=nextcord.Color(value=re[8]),
                )
                embed.set_thumbnail(url="https://entrar.in/logo_dir/entrar_white.png")
                await channel.send(embed=embed)
                await ctx.send("Done")
            else:
                await channel.send(
                    embed=nextcord.Embed(
                        title="Empty",
                        description="No new announcement",
                        color=nextcord.Color(value=re[8]),
                    )
                )
                await ctx.send("Done")
    except Exception as e:
        await ctx.send(
            embed=cembed(
                title="Oops",
                description="Something went wrong\n" + str(e),
                color=re[8],
                thumbnail="https://entrar.in/logo_dir/entrar_white.png",
            )
        )


@client.slash_command(name="imdb", description="Give a movie name")
async def imdb_slash(ctx, movie):
    await ctx.response.defer()
    req()
    try:
        await ctx.send(embed=imdb_embed(movie,re))
    except Exception as e:
        await ctx.send(
            embed=cembed(
                title="Oops",
                description=str(e),
                color=re[8],
                thumbnail=client.user.avatar.url,
            )
        )


@client.slash_command(name="emoji", description="Get Emojis from other servers")
async def emoji_slash(ctx, emoji_name, number=None):
    req()
    if not number: number = 0
    number=int(number)
    if nextcord.utils.get(client.emojis, name=emoji_name) != None:
        emoji_list = [names.name for names in client.emojis if names.name == emoji_name]
        le = len(emoji_list)
        if le >= 2:
            if number > le - 1:
                number = le - 1
        emoji = [names for names in client.emojis if names.name == emoji_name][
            number
        ].id
        await ctx.send(str(nextcord.utils.get(client.emojis, id=emoji)))
    else:
        await ctx.send(
            embed=nextcord.Embed(
                description="The emoji is not available",
                color=nextcord.Color(value=re[8]),
            )
        )


@client.command(aliases=["e", "emoji"])
@commands.cooldown(1,5,commands.BucketType.guild)
async def uemoji(ctx, emoji_name, number=1):
    req()
    number-=1
    try:
        await ctx.message.delete()
    except:
        pass
    if emoji_name.startswith(":"):
        emoji_name = emoji_name[1:]
    if emoji_name.endswith(":"):
        emoji_name = emoji_name[:-1]
    if nextcord.utils.get(client.emojis, name=emoji_name) != None:
        emoji_list = [names.name for names in client.emojis if names.name == emoji_name]
        le = len(emoji_list)
        if le >= 2:
            if number > le - 1:
                number = le - 1
        emoji = [names for names in client.emojis if names.name == emoji_name][number]
        webhook = await ctx.channel.create_webhook(name=getattr(ctx, 'author', getattr(ctx, 'user', None)).name)
        await webhook.send(
            emoji, username=getattr(ctx, 'author', getattr(ctx, 'user', None)).name, avatar_url=getattr(ctx, 'author', getattr(ctx, 'user', None)).avatar.url
        )
        await webhook.delete()

    else:
        await ctx.send(
            embed=nextcord.Embed(
                description="The emoji is not available",
                color=nextcord.Color(value=re[8]),
            )
        )


@client.slash_command(name="svg2png", description="Convert SVG image to png format")
async def svg2png_slash(ctx, url):
    req()
    await ctx.response.defer()
    img = svg2png(url)
    await ctx.send(file=nextcord.File(BytesIO(img), "svg.png"))


@client.command()
async def set_sessionid(ctx, sessionid):
    if str(ctx.author.id) not in dev_users: return
    re[9] = sessionid
    await ctx.send(
        embed=nextcord.Embed(description="SessionID set", color=nextcord.Color(re[8]))
    )

@client.slash_command(name="instagram",description="get recnt instagram posts of the account")
async def insta_slash(ctx, account):
    await ctx.response.defer()
    await instagram(ctx, account = account)

@client.command(alias=['insta'])
async def instagram(ctx, account):    
    try:
        links = instagram_get1(account, re[8], re[9])
        if links == "User Not Found, please check the spelling":
            await ctx.send(
                embed=cembed(
                    title="Hmm",
                    description=links,
                    color=re[8],
                    thumbnail=client.user.avatar.url
                )
            )
            return
        if type(links) == str:
            re[9]=links
            links=instagram_get1(account, re[8], re[9])
        embeds = []
        for a in links:
            if a is not None and type(a) != type("aa"):
                embeds.append(a[0])
            elif type(a) != type("aa"):
                re[9] = links
            else:                
                await ctx.send(
                    embed=nextcord.Embed(
                        description="Oops!, something is wrong.",
                        color=nextcord.Color(value=re[8]),
                    )
                )
                break
        await pa1(embeds, ctx)
    except IndexError:
        embed = cembed(
            title="Error in instagram",
            description=f"Sorry, we couldnt find posts in {account}, please check again if it's private or if {account} has posted anything",
            color=re[8],
            thumbnail=client.user.avatar.url,
        )
        await ctx.send(embed=embed)
        await client.get_channel(dev_channel).send(embed=embed)


@client.command(aliases=["cw"])
async def clear_webhooks(ctx):
    webhooks = await ctx.channel.webhooks()
    print(webhooks)
    for webhook in webhooks:
        try:
            if webhook.user is client.user:
                await webhook.delete()            
        except Exception as e:
            print(e)
    await ctx.send(
        embed=cembed(
            title="Done",
            description="Deleted all the webhooks by alfred",
            color=re[8],
            thumbnail=client.user.avatar.url
        )
    )


@client.command()
async def show_webhooks(ctx):
    webhooks = await ctx.channel.webhooks()
    await ctx.send(str(webhooks))

@client.slash_command(name="color",description="Change color theme", guild_ids= [822445271019421746])
async def color_slash(ctx, rgb_color=defa(default="")):    
    rgb_color = rgb_color.replace("(","").replace(")","").split(",")
    if str(ctx.user.id) not in dev_users:
        await ctx.send(
            embed=cembed(
                title="Woopsies",
                description="This is a `developer-only` function",
                color=re[8],
                thumbnail=client.user.avatar.url
            )
        )
        return
    if len(rgb_color)!=3:
        await ctx.send(
            embed=cembed(
                title="Error",
                description="You need RGB values, 3 values seperated with commas\nExample: `(128,128,128)`",
                color=re[8],
                footer="Give it another try",
                thumbnail=client.user.avatar.url
            )
        )
        return

    re[8] = discord.Color.from_rgb(*[int(i) for i in rgb_color]).value
    if re[8]>16777215: re[8] = 16777215
    embed=cembed(
        title="Done",
        description=f"Color set as {nextcord.Color(re[8]).to_rgb()}\n`{re[8]}`",
        color=re[8],
        thumbnail = client.user.avatar.url,
        footer=f"Executed by {ctx.user.name} in {ctx.channel.name}"
    )
    await ctx.send(embed=embed)
    await client.get_channel(dev_channel).send(embed=embed)

    
@client.command()
async def load(ctx):
    print("Load", str(getattr(ctx, 'author', getattr(ctx, 'user', None))))
    req()
    try:
        cpu_per = str(int(psutil.cpu_percent()))
        cpu_freq = (
            str(int(psutil.cpu_freq().current)) + "/" + str(int(psutil.cpu_freq().max))
        )
        ram = str(psutil.virtual_memory().percent)
        swap = str(psutil.swap_memory().percent)
        usage = f"""
        CPU Percentage: {cpu_per}%
        CPU Frequency : {cpu_freq}%
        RAM usage: {ram}
        Swap usage: {swap}
        """
        embed = nextcord.Embed(
            title="Current load",
            description='\n'.join([i.strip() for i in usage.split('\n')]),
            color=nextcord.Color(value=re[8]),
        )
        embed.set_thumbnail(url=client.user.avatar.url)        
    except Exception as e:
        channel = client.get_channel(dev_channel)
        embed = nextcord.Embed(
            title="Load failed",
            description=str(e),
            color=nextcord.Color(value=re[8]),
        )
        embed.set_thumbnail(url=client.user.avatar.url)
    await ctx.channel.send(embed=embed)



@client.slash_command(name="pr", description="Prints what you ask it to print")
async def pr_slash(ctx, text):
    req()
    await ctx.send(text)

@client.slash_command(
    name="reddit",
    description="Gives you a random reddit post from the account you specify",
)
async def reddit_slash(ctx, account="wholesomememes"):
    req()
    await reddit_search(ctx, account)


@client.command(aliases=["reddit"])
async def reddit_search(ctx, account="wholesomememes", number=1):
    req()
    if number == 1:
        embeds = []
        a = await redd(account, number = 40, single=False)
        if a[2]:
            for i in a:
                embeds += [
                    cembed(
                        description="**" + i[0] + "**",
                        picture=i[1],
                        color=re[8],
                        thumbnail=client.user.avatar.url,
                    )
                ]
            await pa1(embeds, ctx)
        else:
            await ctx.send(embed=cembed(title=a[0], color=re[8], description=a[1]))
            

async def pa1(embeds, ctx, start_from=0, restricted = False):    
    message = await ctx.send(embed=embeds[start_from])
    if len(embeds) == 1: return
    if type(ctx) == nextcord.Interaction:
        message = await ctx.original_message()
    pag = start_from
    await message.add_reaction("◀️")
    await message.add_reaction("▶️")
    
    

    def check(reaction, user):
        if not restricted:            
            return (
                user.id != client.user.id
                and str(reaction.emoji) in ["◀️", "▶️"]
                and reaction.message.id == message.id
            )
        else:
            a = (
                user.id != client.user.id
                and str(reaction.emoji) in ["◀️", "▶️"]
                and reaction.message.id == message.id
                and user.id == getattr(ctx, 'author', getattr(ctx,'user',None)).id
            )
            return a

    while True:
        try:
            reaction, user = await client.wait_for(
                "reaction_add", timeout=720, check=check
            )            
            if str(reaction.emoji) == "▶️" and pag + 1 != len(embeds):
                pag += 1
                await message.edit(embed=embeds[pag])
            elif str(reaction.emoji) == "◀️" and pag != 0:
                pag -= 1
                await message.edit(embed=embeds[pag])
            try:
                await message.remove_reaction(reaction, user)
            except:
                pass
        except asyncio.TimeoutError:
            await message.remove_reaction("◀️", client.user)
            await message.remove_reaction("▶️", client.user)
            break


@client.command(aliases=["c"])
async def cover_up(ctx):
    await ctx.message.delete()
    await asyncio.sleep(0.5)
    mess = await ctx.send(nextcord.utils.get(client.emojis, name="enrique"))
    await mess.delete()


@client.command()
async def remove_dev(ctx, member: nextcord.Member):
    print(member)
    global dev_users
    if str(getattr(ctx, 'author', getattr(ctx, 'user', None)).id) in ["432801163126243328","803855283821871154","723539849969270894"]:
        dev_users.remove(str(member.id))
        await ctx.send(member.mention + " is no longer a dev")
    else:
        await ctx.send(
            embed=nextcord.Embed(
                title="Permission Denied",
                description="Dude! You are not Alvin",
                color=nextcord.Color(value=re[8]),
            )
        )


@client.command()
async def add_dev(ctx, member: nextcord.Member):
    print(member)
    print("Add dev", str(getattr(ctx, 'author', getattr(ctx, 'user', None))))
    global dev_users
    if str(getattr(ctx, 'author', getattr(ctx, 'user', None)).id) in dev_users:
        dev_users.add(str(member.id))
        await ctx.send(member.mention + " is a dev now")
    else:
        await ctx.send(
            embed=nextcord.Embed(
                title="Permission Denied",
                description="Dude! you are not a dev",
                color=nextcord.Color(value=re[8]),
            )
        )

@client.command()
async def dev_op(ctx):
    if str(getattr(ctx, 'author', getattr(ctx, 'user', None)).id) in list(dev_users):
        print("devop", str(getattr(ctx, 'author', getattr(ctx, 'user', None))))
        channel = client.get_channel(dev_channel)
        await devop_mtext(client, channel, re[8])
    else:
        await ctx.send(embed=cembed(title="Permission Denied",description="You cannot use the devop function, only a developer can",color=re[8]))

@client.slash_command(name="addto",description="put queue or playlist and it will add the songs to your playlist to queue or queue to playlist")
async def addto(ctx, mode = defa(choices=['queue','playlist','show','clear'])):
    await ctx.response.defer()
    if not (ctx.user.voice and ctx.guild.voice_client): 
        await ctx.send("You need to connect to a voice channel")
        return
    if mode == "queue":        
        if ctx.user.id in list(da.keys()):
            queue_song[str(ctx.guild.id)]+=da[ctx.user.id]
            await ctx.send("Added your playlist to queue")
        else:
            await ctx.send("You do not have a Playlist")
            return
    if mode == "playlist":
        if ctx.user.id not in list(da.keys()):
            da[ctx.user.id] = []
        for i in queue_song[str(ctx.guild.id)]:
            if i not in da[ctx.user.id]:
                da[ctx.user.id].append(i)
        await ctx.send("Added songs in queue to playlist\n*Note: The songs are added uniquely, which means that if a song in queue is repeated in your playlist, then that song wont be added*")
    if mode == "clear":
        if da.get(ctx.user.id): 
            del da[ctx.user.id]
            await ctx.send("Cleared your playlist")
        else:
            await ctx.send("You had no playlist registered")
    if mode == "show":
        l = []
        thumbnail = ctx.user.default_avatar.url
        if ctx.user.avatar:
            thumbnail = ctx.user.avatar.url
        songs = da.get(ctx.user.id)
        for i in songs:
            if not da1.get(i):
                da1[i] = await get_name(i)
            l.append(f"{da1.get(i)}\n")            
            
        st = []
        for i in range(len(songs)//10):
            s = i*10
            e = i*10+10
            if e > len(l): e = len(l)
            st.append(''.join(l[s:e]))
            
        embeds=[]
        for i in st:
            embed=cembed(
                title=f"Playlist of {ctx.user.name}",
                description=i,
                color=re[8],
                thumbnail=thumbnail
            )
            embeds.append(embed)
        await pa1(embeds,ctx)
        
            

@client.command()
async def reset_from_backup(ctx):
    print("reset_from_backup", str(getattr(ctx, 'author', getattr(ctx, 'user', None))))
    channel = client.get_channel(dev_channel)
    if str(getattr(ctx, 'author', getattr(ctx, 'user', None)).id) in list(dev_users):
        try:
            load_from_file()
            await ctx.send(
                embed=nextcord.Embed(
                    title="Done",
                    description="Reset from backup: done",
                    color=nextcord.Color(value=re[8]),
                )
            )
            await channel.send(
                embed=nextcord.Embed(
                    title="Done",
                    description="Reset from backup: done\nBy: " + str(getattr(ctx, 'author', getattr(ctx, 'user', None))),
                    color=nextcord.Color(value=re[8]),
                )
            )
        except Exception as e:
            await channel.send(
                embed=nextcord.Embed(
                    title="Reset_from_backup failed",
                    description=str(e),
                    color=nextcord.Color(value=re[8]),
                )
            )
    else:
        await ctx.send(embed=cembed(title="Permission Denied",description="Only developers can access this function",color=re[8],thumbnail=client.user.avatar.url))

        await channel.send(embed=cembed(description=f"{getattr(ctx, 'author', getattr(ctx, 'user', None)).name} from {ctx.guild.name} tried to use reset_from_backup command",color=re[8]))


@client.command()
async def docs(ctx, name):
    try:
        if name.find("(") == -1:
            await ctx.send(
                embed=nextcord.Embed(
                    title="Docs",
                    description=str(eval(name + ".__doc__")),
                    color=nextcord.Color(value=re[8]),
                )
            )
        else:
            await ctx.send(
                embed=nextcord.Embed(
                    title="Permissions Denied",
                    description="Functions are not allowed. Try without the brackets to get the information",
                    color=nextcord.Color(value=re[8]),
                )
            )
    except Exception as e:
        await ctx.send(
            embed=nextcord.Embed(
                title="Error", description=str(e), color=nextcord.Color(value=re[8])
            )
        )


@client.slash_command(name="snipe", description="Get the last few deleted messages")
async def snipe_slash(ctx, number):
    req()
    await snipe(ctx, number)


@client.command()
async def snipe(ctx, number=None):
    if not number:
        number = 50
    number = int(number)
    if (
        getattr(ctx, 'author', getattr(ctx, 'user', None)).guild_permissions.manage_messages
        or ctx.guild.id not in config['snipe']
    ):
        message = deleted_message.get(ctx.channel.id,[("Empty","Nothing to snipe here")])[::-1]
        count=0
        embeds = []
        s = ""
        for i in message[:number]:
            count+=1            
            if len(i) < 3:
                s+="**" + i[0] + ":**\n" + i[1]+"\n\n"     
                if count%5==0 or count == len(message) or count == number:
                    embed=cembed(
                        title="Snipe",
                        description=s,
                        color=re[8],
                        thumbnail=ctx.guild.icon.url
                    )
                    embeds.append(embed)
                    s=""        
                
            else:
                await ctx.send("**" + i[0] + ":**")
                await ctx.send(embed=i[1])
        if len(embeds)>0: 
            await pa1(embeds, ctx, start_from = 0, restricted = True)
    else:
        await ctx.send(
            embed=cembed(
                title="Permissions Denied",
                description="Sorry guys, only admins can snipe now",
                color=re[8],
                thumbnail=getattr(client.user.avatar,'url'),
            )
        )

@client.event
async def on_bulk_message_delete(messages):
    for i in messages:
        await on_message_delete(i)

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

@client.slash_command(name = "welcome", description = "set welcome channel")
async def wel(ctx, channel: GuildChannel = defa(ChannelType.text)):
    await ctx.response.defer()
    if ctx.user.guild_permissions.administrator:
        config['welcome'][ctx.guild.id] = channel.id
        await ctx.send(
            embed=cembed(
                title="Done",
                description=f"Set {channel.mention} for welcome and exit messages.",
                color=re[8],
                thumbnail=client.user.avatar.url
            )
        )
    else:
        await ctx.send(
            embed=cembed(
                title="Permissions Denied",
                description="You need to be an admin to do this",
                thumbnail = client.user.avatar.url,
                color=re[8]
            )
        )

@client.event
async def on_member_join(member):
    print(member.guild)
    if member.guild.id in config['welcome']:
        channel = client.get_channel(config['welcome'][member.guild.id])
    else: return
    await channel.send(member.mention + " is here")
    embed = nextcord.Embed(
        title="Welcome!!!",
        description="Welcome to the server, " + member.name,
        color=nextcord.Color(value=re[8]),
    )
    embed.set_thumbnail(
        url="https://image.shutterstock.com/image-vector/welcome-poster-spectrum-brush-strokes-260nw-1146069941.jpg"
    )
    await channel.send(embed=embed)
    if member.guild.id in config['security']:
        audit_log = await member.guild.audit_logs(limit=10).flatten()
        latest=audit_log[0]
        if member.bot:
            channel = client.get_channel(config['security'][member.guild.id])
            if channel:
                await channel.send(
                    embed=cembed(
                        title="Bot added",
                        description=f"{latest.target.mention} was added by {latest.user.mention}, please be careful while handling bots and try not to provide it with all the permissions as it can be dangerous",
                        color=re[8],
                        footer="Security alert by Alfred"
                    )
                )

@client.event
async def on_member_remove(member):
    print(member.guild)
    if member.guild.id in config.get('welcome',[]):
        channel = client.get_channel(config['welcome'][member.guild.id])
    else: return

    await channel.send(member.mention + " is no longer here")
    embed = nextcord.Embed(
        title="Bye!!!",
        description="Hope you enjoyed your stay " + member.name,
        color=nextcord.Color(value=re[8]),
    )
    embed.set_thumbnail(
        url="https://thumbs.dreamstime.com/b/bye-bye-man-says-45256525.jpg"
    )
    await channel.send(embed=embed)    
    if member.guild.id in config['security']:
        a = client.get_guild(member.guild.id)
        audit_log = await a.audit_logs(limit=10).flatten()
        latest = audit_log[0]
        if latest.target == member:
            channel = client.get_channel(config['security'][member.guild.id])
            if latest.action == nextcord.AuditLogAction.ban:
                await channel.send(
                    embed=cembed(
                        title=f"Banned",
                        description=f"{latest.user.mention} banned {latest.target.name}",
                        color=re[8],
                        footer="Security alert by Alfred",
                        thumbnail=member.guild.icon.url
                    )
                )
            elif latest.action == nextcord.AuditLogAction.kick:
                await channel.send(
                    embed=cembed(
                        title=f"Kicked",
                        description=f"{latest.user.mention} kicked {latest.target.name}",
                        color=re[8],
                        footer="Security alert by Alfred",
                        thumbnail=member.guild.icon.url
                    )
                )

@client.slash_command(name="connect", description="Connect to a voice channel")
async def connect_slash(ctx, channel: GuildChannel = defa(ChannelType.voice)):
    req()
    await connect_music(ctx, channel)


@client.command(aliases=["cm",'join','cn','connect'])
async def connect_music(ctx, channel=None):
    if type(channel) == nextcord.channel.VoiceChannel: 
        channel = channel.name
    print("Connect music", str(getattr(ctx, 'author', getattr(ctx, 'user', None))))
    try:
        req()
        user = getattr(ctx, 'author', getattr(ctx, 'user', None))
        if not str(ctx.guild.id) in queue_song:
            queue_song[str(ctx.guild.id)] = []
        if not str(ctx.guild.id) in re[3]:
            re[3][str(ctx.guild.id)] = 0
        if channel == None:
            if user.voice and user.voice.channel:
                channel = user.voice.channel.id
                vc_channel[str(ctx.guild.id)] = channel
                voiceChannel = nextcord.utils.get(ctx.guild.voice_channels, id=channel)
                await voiceChannel.connect()
                voice = nextcord.utils.get(client.voice_clients, guild=ctx.guild)
                await ctx.send(
                    embed=nextcord.Embed(
                        title="",
                        description="Connected\nBitrate of the channel: "
                        + str(ctx.guild.voice_client.channel.bitrate // 1000),
                        color=nextcord.Color(value=re[8]),
                    )
                )
            else:
                emo = assets.Emotes(client)
                await ctx.send(
                    embed=nextcord.Embed(
                        title="",
                        description=f"You are not in a voice channel {emo.join_vc}",
                        color=nextcord.Color(value=re[8]),
                    )
                )
        else:
            if channel in [i.name for i in ctx.guild.voice_channels]:
                voiceChannel = nextcord.utils.get(ctx.guild.voice_channels, name=channel)
                vc_channel[str(ctx.guild.id)] = voiceChannel.id
                await voiceChannel.connect()
                voice = nextcord.utils.get(client.voice_clients, guild=ctx.guild)
                await ctx.send(
                    embed=nextcord.Embed(
                        title="",
                        description="Connected\nBitrate of the channel: "
                        + str(getattr(ctx, 'voice_client', getattr(ctx.guild, 'voice_client', None)).channel.bitrate // 1000),
                        color=nextcord.Color(value=re[8]),
                    )
                )
            else:
                await ctx.send(
                    embed=nextcord.Embed(
                        title="",
                        description="The voice channel does not exist",
                        color=nextcord.Color(value=re[8]),
                    )
                )

    except Exception as e:
        await ctx.send(
            embed=nextcord.Embed(
                title="Hmm", description=str(e), color=nextcord.Color(value=re[8])
            )
        )
        channel = client.get_channel(dev_channel)
        await channel.send(
            embed=cembed(
                title="Connect music",
                description=traceback.format_exc(),
                footer = f"{getattr(ctx, 'author', getattr(ctx, 'user', None)).name}: {ctx.guild}",
                color=re[8],
            )
        )


@client.command(aliases=["cq"])
async def clearqueue(ctx):
    req()
    mem = [
        (str(i.name) + "#" + str(i.discriminator))
        for i in nextcord.utils.get(
            ctx.guild.voice_channels, id=vc_channel[str(ctx.guild.id)]
        ).members
    ]
    if mem.count(str(getattr(ctx, 'author', getattr(ctx, 'user', None)))) > 0:
        if len(queue_song[str(ctx.guild.id)]) > 0:
            queue_song[str(ctx.guild.id)].clear()
        re[3][str(ctx.guild.id)] = 0
        await ctx.send(
            embed=cembed(
                title="Cleared queue",
                description="_Done_",
                color=re[8],
            )
        )
    else:
        await ctx.send(
            embed=nextcord.Embed(
                title="Permission denied",
                description="Join the voice channel to modify queue",
                color=nextcord.Color(value=re[8]),
            )
        )


@client.command()
async def remove(ctx, n):
    req()
    try:
        mem = [str(names) for names in getattr(ctx, 'voice_client', getattr(ctx.guild, 'voice_client', None)).channel.members]
    except:
        mem = []
    if mem.count(str(getattr(ctx, 'author', getattr(ctx, 'user', None)))) > 0:
        if int(n) < len(queue_song[str(ctx.guild.id)]):
            await ctx.send(
                embed=nextcord.Embed(
                    title="Removed",
                    description=da1[queue_song[str(ctx.guild.id)][int(n)]],
                    color=nextcord.Color(value=re[8]),
                )
            )
            if re[3][str(ctx.guild.id)]>int(n):re[3][str(ctx.guild.id)]-=1
            del da1[queue_song[str(ctx.guild.id)][int(n)]]
            queue_song[str(ctx.guild.id)].pop(int(n))
        else:
            await ctx.send(
                embed=nextcord.Embed(
                    title="Not removed",
                    description="Only "
                    + len(queue_song[str(ctx.guild.id)])
                    + " song(s) in your queue",
                    color=nextcord.Color(value=re[8]),
                )
            )
    else:
        await ctx.send(
            embed=nextcord.Embed(
                title="Permission denied",
                description="Join the voice channel to modify queue",
                color=nextcord.Color(value=re[8]),
            )
        )


@client.command(aliases=["curr"])
async def currentmusic(ctx):
    req()
    if len(queue_song[str(ctx.guild.id)]) > 0:
        description = f"[Current index: {str(re[3][str(ctx.guild.id)])}]({queue_song[str(ctx.guild.id)][re[3][str(ctx.guild.id)]]})\n"
        info = youtube_info(queue_song[str(ctx.guild.id)][re[3][str(ctx.guild.id)]])
        check = "\n\nDescription: \n" + info["description"] + "\n"
        if len(check) < 3000 and len(check) > 0:
            description += check
        description += (
            f"\nDuration: {str(info['duration'] // 60)}min {str(info['duration'] % 60)}sec"
            + f"\n\n{info['view_count']} views\n{info['like_count']} :thumbsup:\n"
        )
        embed=cembed(
            title=str(da1[queue_song[str(ctx.guild.id)][re[3][str(ctx.guild.id)]]]),
            description=description,
            color=re[8],
            thumbnail=info["thumbnail"],
        )
        await isReaction(ctx,embed)
    else:
        embed=cembed(
            title="Empty queue",
            description="Your queue is currently empty",
            color=re[8],
            footer="check 'q if you have any song"
        )
        await isReaction(embed)

def repeat(ctx, voice):
    req()
    songs = queue_song.get(str(ctx.guild.id),[])
    if len(songs) == 0: return
    index = re[3].get(str(ctx.guild.id),0)
    if len(songs)<index:
        index = 0
        re[3][str(ctx.guild.id)]=index
    song = songs[index]
    if not song in da1.keys():
        aa = str(urllib.request.urlopen(song).read().decode())
        starting = aa.find("<title>") + len("<title>")
        ending = aa.find("</title>")
        da1[song] = (
            aa[starting:ending]
            .replace("&#39;", "'")
            .replace(" - YouTube", "")
            .replace("&amp;", "&")
        )
    time.sleep(1)
    if re[7].get(ctx.guild.id,-1) == 1 and not voice.is_playing():
        re[3][str(ctx.guild.id)] += 1
        if re[3][str(ctx.guild.id)] >= len(queue_song[str(ctx.guild.id)]):
            re[3][str(ctx.guild.id)] = 0
    if re[2].get(ctx.guild.id,-1) == 1 or re[7].get(ctx.guild.id,-1) == 1:
        if not voice.is_playing():
            URL = youtube_download(ctx, song)
            voice.play(
                nextcord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS),
                after=lambda e: repeat(ctx, voice),
            )


@client.slash_command(
    name="autoplay",
    description="Plays the next song automatically if its turned on",
)
async def autoplay_slash(ctx):
    req()
    
    await autoplay(ctx)


@client.slash_command(name="loop", description="Loops the same song")
async def loop_slash(ctx):
    req()
    await loop(ctx)


@client.command()
async def autoplay(ctx):
    req()
    if getattr(ctx, 'author', getattr(ctx, 'user', None)).id in [i.id for i in getattr(ctx, 'voice_client', getattr(ctx.guild, 'voice_client', None)).channel.members]:
        st = ""
        re[7][ctx.guild.id] = re[7].get(ctx.guild.id,-1) * -1
        if re[7].get(ctx.guild.id,-1) == 1:
            re[2][ctx.guild.id] = -1
        if re[7][ctx.guild.id] < 0:
            st = "Off"
        else:
            st = "_On_"
        await ctx.send(
            embed=nextcord.Embed(
                title="Autoplay", description=st, color=nextcord.Color(value=re[8])
            )
        )
    else:
        await ctx.send(
            embed=nextcord.Embed(
                title="Permissions Denied",
                description="You need to be in the voice channel to toggle autoplay",
                color=nextcord.Color(value=re[8]),
            )
        )


@client.command()
async def loop(ctx):
    req()
    if getattr(ctx, 'author', getattr(ctx, 'user', None)).id in [i.id for i in getattr(ctx, 'voice_client', getattr(ctx.guild, 'voice_client', None)).channel.members]:
        st = ""
        re[2][ctx.guild.id] = re[2].get(ctx.guild.id,-1) * -1
        if re[2].get(ctx.guild.id,1) == 1:
            re[7][ctx.guild.id] = -1
        if re[2].get(ctx.guild.id,1) < 0:
            st = "Off"
        else:
            st = "_On_"
        await ctx.send(
            embed=nextcord.Embed(
                title="Loop", description=st, color=nextcord.Color(value=re[8])
            )
        )
    else:
        await ctx.send(
            embed=nextcord.Embed(
                title="Permissions Denied",
                description="You need to be in the voice channel to toggle loop",
                color=nextcord.Color(value=re[8]),
            )
        )


@client.command(aliases=["q"])
@commands.cooldown(1,5,commands.BucketType.guild)
async def queue(ctx, *, name=""):
    req()
    st = ""
    num = 0
    try:
        mem = [str(names) for names in getattr(ctx, 'voice_client', getattr(ctx.guild, 'voice_client', None)).channel.members]
    except:
        mem = []
    if mem.count(str(getattr(ctx, 'author', getattr(ctx, 'user', None)))) > 0 and name != "":
        if 'spotify' in name:
            if 'playlist' in name:
                await ctx.send('Enqueued the given Spotify playlist.')
                try:
                    songs = await fetch_spotify_playlist(name, 500)
                    for song in songs:
                        try:
                            name = convert_to_url(song)
                            sear = "https://www.youtube.com/results?search_query=" + name
                            htm = await get_async(sear)
                            video = regex.findall(r"watch\?v=(\S{11})", htm)
                            url = "https://www.youtube.com/watch?v=" + video[0]
                            st = ""
                            num = 0
                            name_of_the_song = await get_name(url)
                            da1[url] = name_of_the_song
                            queue_song[str(ctx.guild.id)].append(url)
                        except Exception as e:
                            print(e)
                            break
                except Exception as e:
                    print(e)
            elif 'track' in name:
                name = convert_to_url(name)
                sear = "https://www.youtube.com/results?search_query=" + name
                htm = await get_async(sear)
                video = regex.findall(r"watch\?v=(\S{11})", htm)
                url = "https://www.youtube.com/watch?v=" + video[0]
                st = ""
                num = 0
                name_of_the_song = await get_name(url)
                print(name_of_the_song, ":", url)
                da1[url] = name_of_the_song
                queue_song[str(ctx.guild.id)].append(url)
        else:       
            name = convert_to_url(name)
            sear = "https://www.youtube.com/results?search_query=" + name
            htm = await get_async(sear)
            video = regex.findall(r"watch\?v=(\S{11})", htm)
            url = "https://www.youtube.com/watch?v=" + video[0]

            st = ""
            await ctx.send("Added to queue")
            num = 0
            name_of_the_song = await get_name(url)
            print(name_of_the_song, ":", url)
            da1[url] = name_of_the_song
            queue_song[str(ctx.guild.id)].append(url)
            
        for i in queue_song[str(ctx.guild.id)]:
            if num >= len(queue_song[str(ctx.guild.id)]) - 10:
                if not i in da1.keys():
                    da1[i] = await get_name(i)
                st = st + str(num) + ". " + da1[i].replace("&quot", "'") + "\n"
            num += 1
        # st=st+str(num)+". "+da1[i]+"\n"
        if st == "":
            st = "_Empty_"
        em = nextcord.Embed(
            title="Queue", description=st, color=nextcord.Color(value=re[8])
        )
        mess = await ctx.send(embed=em)
        if type(ctx) == nextcord.Interaction:
            mess = await ctx.original_message()
        await player_pages(mess)
    elif name == "":
        num = 0
        st = ""
        if len(queue_song[str(ctx.guild.id)]) < 30:
            for i in queue_song[str(ctx.guild.id)]:
                if not i in da1.keys():
                    da1[i] = youtube_info(i)["title"]
                st = st + str(num) + ". " + da1[i] + "\n"
                num += 1
        else:
            adfg = 0
            num = -1
            for i in queue_song[str(ctx.guild.id)]:
                num += 1
                try:
                    if re[3][str(ctx.guild.id)] < 10:
                        if num < 15:
                            if not i in da1.keys():
                                da1[i] = youtube_info(i)["title"]
                            st = st + str(num) + ". " + da1[i] + "\n"
                    elif re[3][str(ctx.guild.id)] > (
                        len(queue_song[str(ctx.guild.id)]) - 10
                    ):
                        if num > (len(queue_song[str(ctx.guild.id)]) - 15):
                            if not i in da1.keys():
                                da1[i] = youtube_info(i)["title"]
                            st = st + str(num) + ". " + da1[i] + "\n"
                    else:
                        if (
                            num > re[3][str(ctx.guild.id)] - 10
                            and num < re[3][str(ctx.guild.id)] + 10
                        ):
                            if not i in da1.keys():
                                da1[i] = youtube_info(i)["title"]
                            st = st + str(num) + ". " + da1[i] + "\n"
                except Exception as e:
                    pass

        if st == "":
            st = "_Empty_"
        embed = nextcord.Embed(
            title="Queue", description=st, color=nextcord.Color(value=re[8])
        )
        embed.set_thumbnail(url=client.user.avatar.url)
        mess = await ctx.send(embed=embed)
        if type(ctx) == nextcord.Interaction:
            mess = await ctx.original_message()
        await player_pages(mess)
    else:
        await ctx.send(
            embed=nextcord.Embed(
                title="Permission denied",
                description="Join the voice channel to modify queue",
                color=nextcord.Color(value=re[8]),
            )
        )



async def player_pages(mess):
    await player_reaction(mess)    
    emojis =  emoji.emojize(":upwards_button:"),emoji.emojize(":downwards_button:")
    def check(reaction, user):
        return (
            user.id != client.user.id
            and str(reaction.emoji) in emojis
            and reaction.message.id == mess.id
        )
    page=re[3][str(mess.guild.id)]//10
    while True:
        songs = queue_song[str(mess.guild.id)]
        try:
            reaction, user = await client.wait_for("reaction_add",check=check, timeout=None)
            if reaction.emoji == emojis[0] and page>0:
                page-=1
            elif reaction.emoji == emojis[1] and page<=len(songs):
                page+=1
            cu = page * 10
            st = '\n'.join([f"{i}. {da1[songs[i]]}" for i in range(cu,cu+10) if len(songs)>i])
            await mess.edit(
                embed=cembed(
                    title="Queue",
                    description=st,
                    color=re[8],
                    footer='Amazing songs btw, keep going' if len(songs)!=0 else 'Use queue to add some songs'
                )
            )
            await reaction.remove(user)
        except asyncio.TimeoutError:
            await mess.clear_reactions()
            
                
                

@client.command(aliases=[">", "skip"])
async def next(ctx):
    req()
    try:
        try:
            mem = [str(names) for names in getattr(ctx, 'voice_client', getattr(ctx.guild, 'voice_client', None)).channel.members]
        except:
            mem = []
        if mem.count(str(getattr(ctx, 'author', getattr(ctx, 'user', None)))) > 0:
            re[3][str(ctx.guild.id)] += 1
            if re[3][str(ctx.guild.id)] >= len(queue_song[str(ctx.guild.id)]):
                re[3][str(ctx.guild.id)] = len(queue_song[str(ctx.guild.id)]) - 1
                await ctx.send(
                    embed=nextcord.Embed(
                        title="Last song",
                        description="Only "
                        + str(len(queue_song[str(ctx.guild.id)]))
                        + " songs in your queue",
                        color=nextcord.Color(value=re[8]),
                    )
                )
            song = queue_song[str(ctx.guild.id)][re[3][str(ctx.guild.id)]]
            voice = nextcord.utils.get(client.voice_clients, guild=ctx.guild)
            URL = youtube_download(ctx, song)            
            embed=nextcord.Embed(
                title="Playing",
                description=da1.get(song,"Unavailable"),
                color=nextcord.Color(value=re[8]),
            )
            await isReaction(ctx,embed)
            voice.stop()
            voice.play(
                nextcord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS),
                after=lambda e: repeat(ctx, voice),
            )
        else:
            embed=nextcord.Embed(
                title="Permission denied",
                description="Join the voice channel to move to the next song",
                color=nextcord.Color(value=re[8]),
            )
            await isReaction(ctx,embed)
    except Exception as e:
        channel = client.get_channel(dev_channel)
        await channel.send(
            embed=cembed(
                title="Error in next function",
                description=str(e),
                footer=f"{ctx.channel.name}:{ctx.guild.name}",
                color=nextcord.Color(value=re[8]),
            )
        )


@client.command()
async def set_prefix(ctx, *, pref):
    if getattr(ctx, 'author', getattr(ctx, 'user', None)).guild_permissions.administrator:
        if pref.startswith('"') and pref.endswith('"') and len(pref)>1:
            pref=pref[1:-1]
        prefix_dict[ctx.guild.id] = pref
        await ctx.send(
            embed=cembed(title="Done", description=f"Prefix set as {pref}", color=re[8])
        )
    else:
        await ctx.send(
            embed=cembed(
                title="Permissions Denied",
                description="You cannot change the prefix, you need to be an admin",
                color=re[8],
            )
        )


@client.command()
async def remove_prefix(ctx):
    if getattr(ctx, 'author', getattr(ctx, 'user', None)).guild_permissions.administrator:
        if prefix_dict.get(ctx.guild.id, False):
            prefix_dict.pop(ctx.guild.id)
        await ctx.send(
            embed=cembed(title="Done", description=f"Prefix removed", color=re[8])
        )
    else:
        await ctx.send(
            embed=cembed(
                title="Permissions Denied",
                description="You cannot change the prefix, you need to be an admin",
                color=re[8],
            )
        )


@client.slash_command(name="news", description="Latest news from a given subject")
async def news_slash(ctx, subject="Technology"):
    req()    
    await ctx.response.defer()
    await news(ctx, subject)

@client.command()
async def news(ctx, subject="Technology"):
    googlenews.get_news(subject)
    news_list = googlenews.get_texts()
    googlenews.clear()
    string = ""
    for i in range(0, 10):
        string = string + str(i) + ". " + news_list[i] + "\n"
    await ctx.send(
        embed=cembed(
            title="News",
            description=string,
            color=re[8],
            thumbnail=client.user.avatar.url,
        )
    )


@client.command(aliases=["<"])
async def previous(ctx):
    req()
    try:
        try:
            mem = [str(names) for names in getattr(ctx, 'voice_client', getattr(ctx.guild, 'voice_client', None)).channel.members]
        except:
            mem = []
        if mem.count(str(getattr(ctx, 'author', getattr(ctx, 'user', None)))) > 0:            
            re[3][str(ctx.guild.id)] -= 1
            if re[3][str(ctx.guild.id)] == -1:
                re[3][str(ctx.guild.id)] = len(queue_song.get(str(ctx.guild.id),[]))-1          
            song = queue_song[str(ctx.guild.id)][re[3][str(ctx.guild.id)]]
            if not song in da1.keys():
                da1[song] = youtube_info(song)["title"]
            voice = nextcord.utils.get(client.voice_clients, guild=ctx.guild)
            URL = youtube_download(ctx, song)
            embed=nextcord.Embed(
                title="Playing",
                description=da1[song],
                color=nextcord.Color(value=re[8]),
            )
            voice.stop()
            voice.play(
                nextcord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS),
                after=lambda e: repeat(ctx, voice),
            )
            await isReaction(ctx,embed)
        else:
            embed=nextcord.Embed(
                title="Permission denied",
                description="Join the voice channel to move to the previous song",
                color=nextcord.Color(value=re[8]),
            )
            await isReaction(ctx,embed)
    except Exception as e:
        channel = client.get_channel(dev_channel)
        await channel.send(
            embed=cembed(
                title="Error in previous function",
                description=str(e),
                color=nextcord.Color(value=re[8]),
                footer=f"{ctx.author.name}: {ctx.guild.name}"
            )
        )

@client.slash_command(name="dictionary", description="Use the dictionary for meaning")
async def dic(ctx, word):
    await ctx.response.defer()
    try:
        mean = ef.Meaning(word = text, color = re[8])
        await mean.setup()
        await pa1(mean.create_texts(),ctx)
    except Exception as e:
        await ctx.send(
            embed=ef.cembed(
                title="Something is wrong",
                description="Oops something went wrong, I gotta check this out real quick, sorry for the inconvenience",
                color=discord.Color.red(),
                thumbnail=client.user.avatar.url
            )
        )


@client.command(aliases=["s_q"])
async def search_queue(ctx, part):
    st = ""
    index = 0
    found_songs = 0
    for i in queue_song[str(ctx.guild.id)]:
        if i in da1:
            found_songs += 1
            if da1[i].lower().find(part.lower()) != -1:
                st += str(index) + ". " + da1[i] + "\n"
        index += 1
    if st == "":
        st = "Not found"
    if len(queue_song[str(ctx.guild.id)]) - found_songs > 0:
        st += "\n\nWARNING: Some song names may not be loaded properly, this search may not be accurate"
        st += "\nSongs not found: " + str(
            len(queue_song[str(ctx.guild.id)]) - found_songs
        )
    await ctx.send(
        embed=cembed(
            title="Songs in queue",
            description=st,
            color=re[8],
            thumbnail=client.user.avatar.url,
        )
    )

@client.slash_command(name = "play", description = "play a song, you can also put a song name in that")
async def play_slash(ctx, index):
    await play(ctx, index = index)

@client.slash_command(name = "queue", description = "play a song")
async def queue_slash(ctx, song = "-"):
    if song is None: await ctx.send("Sending queue")
    if song == "-": song = ""
    await queue(ctx, name = song)

@client.slash_command(name="guess",description="guess the song game")
async def guess(ctx):
    await ctx.response.defer()
    if not ctx.user.voice:
        await ctx.send("Join a vc and then try again")
        return
    songs = da[432801163126243328]    
    voice = ctx.user.voice
    if not ctx.guild.voice_client:
        await voice.channel.connect()    
    voice = ctx.guild.voice_client
    voice.stop()
    song = random.choice(songs)
    URL = youtube_download(ctx, song)
    voice.play(nextcord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
    await ctx.send("Guess this Song, you have 30 seconds to tell")
    try:
        message = await client.wait_for("message",timeout=30,check=lambda m: m.author == ctx.user and ctx.channel == m.channel)
        voice.stop()
        if len(message.content)<3: 
            await ctx.send("Type more than 5 letters of the song")
            return
        if message.content.lower() in ["lyrics", "official", 'video']:
            await ctx.send(f"That's cheating, anyway that was {da1[song]}")
            return
        if message.content.lower() in da1[song].lower(): 
            await ctx.send(f"Correct that was {da1[song]}")
        else:
            await ctx.send(f"Incorrect, that was {da1[song]}")
    except asyncio.TimeoutError:
        await ctx.send(f"Time up, that was {da1[song]}")
    
@client.command(aliases=["p"])
@commands.cooldown(1,10,commands.BucketType.guild)
async def play(ctx, *, index):
    ind = index
    req()    
    if (
        ctx.guild.voice_client == None
        and getattr(ctx, 'author', getattr(ctx, 'user', None)).voice
        and getattr(ctx, 'author', getattr(ctx, 'user', None)).voice.channel
    ):
        if not str(ctx.guild.id) in queue_song:
            queue_song[str(ctx.guild.id)] = []
        if not str(ctx.guild.id) in re[3]:
            re[3][str(ctx.guild.id)] = 0
        channel = getattr(ctx, 'author', getattr(ctx, 'user', None)).voice.channel.id
        vc_channel[str(ctx.guild.id)] = channel
        voiceChannel = nextcord.utils.get(ctx.guild.voice_channels, id=channel)
        await voiceChannel.connect()
    try:
        try:
            mem = [str(names) for names in getattr(ctx, 'voice_client', getattr(ctx.guild, 'voice_client', None)).channel.members]
        except:
            mem = []
        if mem.count(str(getattr(ctx, 'author', getattr(ctx, 'user', None)))) > 0:
            if ind.isnumeric():
                if int(ind) <= len(queue_song[str(ctx.guild.id)]):
                    re[3][str(ctx.guild.id)] = int(ind)
                    voice = nextcord.utils.get(client.voice_clients, guild=ctx.guild)
                    song = queue_song[str(ctx.guild.id)][re[3][str(ctx.guild.id)]]
                    URL = youtube_download(ctx, song)
                    if song not in da1:
                        da1[song] = await get_name(song)
                    mess = await ctx.send(
                        embed=nextcord.Embed(
                            title="Playing",
                            description=da1[song],
                            color=nextcord.Color(value=re[8]),
                        )
                    )
                    voice.stop()
                    voice.play(
                        nextcord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS),
                        after=lambda e: repeat(ctx, voice),
                    )
                    await player_pages(mess)
                else:
                    embed = nextcord.Embed(
                        title="Hmm",
                        description=f"There are only {len(queue_song[str(ctx.guild.id)])} songs",
                        color=nextcord.Color(value=re[8]),
                    )
                    await ctx.send(embed=embed)
            else:
                name = ind
                voice = nextcord.utils.get(client.voice_clients, guild=ctx.guild)
                name = convert_to_url(name)
                htm = await get_async("https://www.youtube.com/results?search_query=" + name)
                video = regex.findall(r"watch\?v=(\S{11})", htm)
                if len(video) == 0: 
                    await ctx.send(
                        embed=cembed(
                            description="We couldnt find the song, please try it with a different name, shorter name is prefered",
                            color=re[8]
                        )
                    )
                    return
                url = "https://www.youtube.com/watch?v=" + video[0]
                URL, name_of_the_song = youtube_download1(ctx, url)
                re[3][str(ctx.guild.id)] = len(queue_song[str(ctx.guild.id)])
                if queue_song[str(ctx.guild.id)]==[]: queue_song[str(ctx.guild.id)].append(url)
                if queue_song[str(ctx.guild.id)][-1] != url:
                    queue_song[str(ctx.guild.id)].append(url)
                da1[URL] = name_of_the_song
                voice.stop()
                voice.play(
                    nextcord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS),
                    after=lambda e: repeat(ctx, voice),
                )
                await ctx.send(
                    embed=nextcord.Embed(
                        title="Playing",
                        description=name_of_the_song,
                        color=nextcord.Color(value=re[8]),
                    )
                )

        else:
            await ctx.send(
                embed=nextcord.Embed(
                    title="Permission denied",
                    description="Join the voice channel to play the song",
                    color=nextcord.Color(value=re[8]),
                )
            )
    except Exception as e:
        channel = client.get_channel(dev_channel)
        await ctx.send(
            embed=nextcord.Embed(
                title="Error in play function",
                description=f"{e}",
                color=nextcord.Color(value=re[8]),
            )
        )
        await channel.send(
            embed=nextcord.Embed(
                title="Error in play function",
                description=f"{e}\n{ctx.guild.name}: {ctx.channel.name}",
                color=nextcord.Color(value=re[8]),
            )
        )


@client.command()
async def again(ctx):
    req()
    if getattr(ctx, 'author', getattr(ctx, 'user', None)).voice and getattr(ctx, 'author', getattr(ctx, 'user', None)).voice.channel:
        if not str(ctx.guild.id) in queue_song:
            queue_song[str(ctx.guild.id)] = []
        if not str(ctx.guild.id) in re[3]:
            re[3][str(ctx.guild.id)] = 0
            
        if ctx.guild.voice_client == None:
            channel = getattr(ctx, 'author', getattr(ctx, 'user', None)).voice.channel.id
            vc_channel[str(ctx.guild.id)] = channel
            voiceChannel = nextcord.utils.get(ctx.guild.voice_channels, id=channel)
            await voiceChannel.connect()
        mem = []
        try:
            try:
                mem = [str(names) for names in getattr(ctx, 'voice_client', getattr(ctx.guild, 'voice_client', None)).channel.members]
            except:
                mem = []
            if mem.count(str(getattr(ctx, 'author', getattr(ctx, 'user', None)))) > 0:
                voice = nextcord.utils.get(client.voice_clients, guild=ctx.guild)
                bitrate = "\nBitrate of the channel: " + str(
                    getattr(ctx, 'voice_client', getattr(ctx.guild, 'voice_client', None)).channel.bitrate // 1000
                )
                song = queue_song[str(ctx.guild.id)][re[3][str(ctx.guild.id)]]
                if song not in da1:
                    da1[song] = youtube_info(song)["title"]                
                URL = youtube_download(ctx, song)
                voice.stop()
                voice.play(
                    nextcord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS),
                    after=lambda e: repeat(ctx, voice),
                )
                embed=cembed(
                        title="Playing",
                        description=da1[song] + bitrate,
                        color=re[8],
                        thumbnail=client.user.avatar.url,
                    )
                if type(ctx) != nextcord.message: 
                    mess = await ctx.send(embed=embed)
                    await player_pages(mess)
                else:
                    await isReaction(ctx,embed)
            else:
                emo = assets.Emotes(client)
                embed=cembed(
                    title="Permission denied",
                    description=f"{emo.animated_wrong} Join the voice channel to play the song",
                    color=re[8],
                    thumbnail=client.user.avatar.url,
                )
        except Exception as e:
            channel = client.get_channel(dev_channel)
            await ctx.channel.send(
                embed=cembed(
                    title="Error",
                    description=str(e),
                    color=re[8],
                    thumbnail=client.user.avatar.url,
                )
            )
            await channel.send(
                embed=nextcord.Embed(
                    title="Error in play function",
                    description=f"{e}\n{ctx.guild.name}: {ctx.channel.name}",
                    color=nextcord.Color(value=re[8]),
                )
            )


@client.slash_command(name="again", description="Repeat the song")
async def again_slash(ctx):
    req()
    await ctx.response.defer()
    await again(ctx)


@client.slash_command(name="memes", description="Memes from Alfred yey")
async def memes(ctx):
    await ctx.response.defer()
    req()
    await memes(ctx)

@client.command()
async def feedback(ctx, *, text):
    embed=cembed(
        title=f"Message from {getattr(ctx, 'author', getattr(ctx, 'user', None)).name}: {ctx.guild.name}",
        description=text,
        color=re[8],
        thumbnail=client.user.avatar.url
    )
    await ctx.send(embed=embed)
    confirmation = await wait_for_confirm(ctx,client,"Do you want to send this to the developers?",color=re[8])
    if not confirmation:
        return
    await client.get_channel(932890298013614110).send(
        content=str(ctx.channel.id)+" "+str(ctx.author.id),
        embed=embed
        
    )
    await ctx.send(
        embed=cembed(
            title="Done",
            description="I've given this info to the developers, they will try fixing it asap :smiley:",
            color=re[8]
        )
    )

@client.slash_command(name = "feedback",description="Send a feedback to the developers")
async def f_slash(ctx, text):
    await feedback(ctx, text=text)

@client.command(aliases=["::"])
async def memes(ctx):
    global link_for_cats
    if len(link_for_cats) == 0:
        try:            
            print("Finished meme")
            link_for_cats += await memes1()
            print("Finished meme1")
            link_for_cats += await memes2()
            print("Finished meme2")
            link_for_cats += await memes3()
            print("Finished meme3")
            link_for_cats += await memes4()
            print("Finished meme4")
        except Exception as e:
            await ctx.channel.send(
                embed=cembed(
                    title="Meme issues",
                    description="Something went wrong during importing memes\n"
                    + str(e),
                    color=re[8],
                    thumbnail=client.user.avatar.url,
                )
            )
    await ctx.send(choice(link_for_cats))
    save_to_file()


async def poll(ctx, Options = "", Question = "", image=""):
    channel = ctx.channel
    if Options == "":
        await ctx.send(
            embed=cembed(
                title="Here's how you should do it",
                description="First give the options seperated with `|`(make sure there's no space when writing the options), then mention the channel and write down the question",
                color=re[8],
                footer="There's also a slash command if you feel this is uncomfortable"
            )
        )
        return
    text = Question+"\n\n"
    Options = Options.split("|")
    if len(Options)>=20:
        reply = "Use this if you want to redo\n\n"
        reply+= f"Question: {Questions}"
        reply+= f"Options: {'|'.join(Options)}"
        await ctx.send(
            embed=cembed(
                title="Sorry you can only give 20 options",
                description=reply,
                color=discord.Color.red(),
                thumbnail=client.user.avatar.url
            )
        )
    for i in range(len(Options)):
        text+=f"{emoji.emojize(f':keycap_{i+1}:') if i<10 else Emoji_alphabets[i-10]} | {Options[i].strip()}\n"

    embed=cembed(
        title="Poll",
        description=text,
        color=re[8],
        footer=f"from {getattr(ctx, 'author', getattr(ctx, 'user', None)).name} | {ctx.guild.name}",
        picture = image
    )
    embed.set_author(name = getattr(ctx, 'author', getattr(ctx, 'user', None)).name, icon_url = getattr(ctx, 'author', getattr(ctx, 'user', None)).avatar.url if getattr(ctx, 'author', getattr(ctx, 'user', None)).avatar else client.user.avatar.url)
    message = await ctx.send(
        embed = embed
    )
    
    for i in range(len(Options)): await message.add_reaction(emoji.emojize(f":keycap_{i+1}:") if i<10 else Emoji_alphabets[i-10])

@client.slash_command(name="polling", description="Seperate options with |")
async def polling_slash(ctx, question = None, options="yes|no",image=" "):
    await ctx.response.defer()
    if image == " ": image = None
    await poll(ctx, Options = options, Question = question if question else "", image = image)

@client.slash_command(name="eval",description="This is only for developers",guild_ids= [822445271019421746])
async def eval_slash(ctx,text):
    await python_shell(ctx, text = text)

@client.command(aliases=["!"])
async def restart_program(ctx, text):
    if str(getattr(ctx, 'author', getattr(ctx, 'user', None)).id) in list(dev_users):
        if len(client.voice_clients)>0:
            confirmation = await wait_for_confirm(
                ctx, client, f"There are {len(client.voice_clients)} servers listening to music through Alfred, Do you wanna exit?", color=re[8]                        
            )
            if not confirmation:
                return
        try:
            for voice in client.voice_clients:
                voice.stop()
                await voice.disconnect()
        except:
            pass
        save_to_file()
        print("Restart")
        await ctx.channel.send(
            embed=cembed(
                title="Restarted",
                description="The program is beginning it's restarting process",
                color=re[8],
                thumbnail=client.user.avatar.url
            )
        )
        await client.get_channel(dev_channel).send(
            embed=cembed(
                title="Restart",
                description=f"Requested by {getattr(ctx, 'author', getattr(ctx, 'user', None)).name}",
                thumbnail=client.user.avatar.url,
                color=re[8]
                
            )
        )
        os.system("busybox reboot")
    else:
        await ctx.channel.send(embed=cembed(title="Permission Denied",description="Only developers can access this function",color=re[8],thumbnail=client.user.avatar.url))
        await client.get_channel(dev_channel).send(embed=cembed(description=f"{getattr(ctx, 'author', getattr(ctx, 'user', None)).name} from {ctx.guild.name} tried to use restart_program command",color=re[8]))



@client.slash_command(name="disconnect", description="Disconnect the bot from your voice channel")
async def leave_slash(ctx):
    req()    
    await leave(ctx)


@client.command(aliases=["dc"])
async def leave(ctx):
    req()
    try:
        mem = [names.id for names in ctx.guild.voice_client.channel.members]
    except:
        mem = []    
    user = getattr(ctx, 'author', getattr(ctx, 'user', None))
    if len(mem) == 1 and mem[0] == client.user.id:
        if user.guild_permissions.administrator:
            user = client.user
    if mem.count(user.id) > 0:                
        if user.id == 734275789302005791:
            await clearqueue(ctx)
        voice = ctx.guild.voice_client
        voice.stop()
        await voice.disconnect()
        embed=nextcord.Embed(
            title="Disconnected",
            description="Bye, Thank you for using Alfred",
            color=nextcord.Color(value=re[8]),
        )            
    else:
        embed=nextcord.Embed(
            title="Permission denied",
            description="Nice try dude! Join the voice channel",
            color=nextcord.Color(value=re[8]),
        )
    await isReaction(ctx,embed,clear=True)

    save_to_file()


@client.command()
async def pause(ctx):
    req()
    try:
        mem = [str(names) for names in getattr(ctx, 'voice_client', getattr(ctx.guild, 'voice_client', None)).channel.members]
    except:
        mem = []
    embed = None
    if mem.count(str(getattr(ctx, 'author', getattr(ctx, 'user', None)))) > 0:
        voice = nextcord.utils.get(client.voice_clients, guild=ctx.guild)
        voice.pause()
        url = queue_song[str(ctx.guild.id)][re[3][str(ctx.guild.id)]]
        song = da1.get(url, "Unavailable")
        embed=nextcord.Embed(
            title="Paused",
            description=f"[{song}]({url})",
            color=nextcord.Color(value=re[8]),
        )
    else:
        embed=nextcord.Embed(
            title="Permission denied",
            description="Join the channel to pause the song",
            color=nextcord.Color(value=re[8]),
        )
    await isReaction(ctx,embed)


@client.command(aliases=["*"])
async def change_nickname(ctx, member: nextcord.Member, *, nickname):
    if (
        getattr(ctx, 'author', getattr(ctx, 'user', None)).guild_permissions.change_nickname
        or getattr(ctx, 'author', getattr(ctx, 'user', None)).id == 432801163126243328
    ):
        await member.edit(nick=nickname)
        await ctx.send(
            embed=nextcord.Embed(
                title="Nickname Changed",
                description=(
                    "Nickname changed to "
                    + member.mention
                    + " by "
                    + getattr(ctx, 'author', getattr(ctx, 'user', None)).mention
                ),
                color=nextcord.Color(value=re[8]),
            )
        )
    else:
        await ctx.send(
            embed=nextcord.Embed(
                title="Permissions Denied",
                description="You dont have permission to change others nickname",
                color=nextcord.Color(value=re[8]),
            )
        )
@client.command()
async def dev_test(ctx, id:nextcord.Member=None):
    if id:
        if str(id.id) in dev_users:
            await ctx.send(f"{id} is a dev!")
        else:
            await ctx.send(f"{id} is not a dev!")
    else:
        await ctx.send("You need to mention somebody")


@client.command()
async def resume(ctx):
    req()
    try:
        mem = [str(names) for names in getattr(ctx, 'voice_client', getattr(ctx.guild, 'voice_client', None)).channel.members]
    except:
        mem = []
    if mem.count(str(getattr(ctx, 'author', getattr(ctx, 'user', None)))) > 0:
        voice = nextcord.utils.get(client.voice_clients, guild=ctx.guild)
        voice.resume()
        url = queue_song[str(ctx.guild.id)][re[3][str(ctx.guild.id)]]
        song_name = da1[url]
        embed=nextcord.Embed(
            title="Playing",
            description=f"[{song_name}]({url})",
            color=nextcord.Color(value=re[8]),
        )

    else:
        embed = cembed(
            title="Permissions Denied",
            description="You need to be in the voice channel to resume this",
            color=re[8]
        )
    await isReaction(ctx,embed)


@client.slash_command(name="wikipedia", description="Get a topic from wikipedia")
async def wiki_slash(ctx, text):
    await ctx.response.defer()
    await wikipedia(ctx, text = text)


@client.command(aliases=["w"])
async def wikipedia(ctx, *, text):
    try:
        req()
        embeds = []
        for i in search(text):
            t = str(i.encode("utf-8"))
            em = cembed(
                title=str(t).title(),
                description=str(summary(t, sentences=5)),
                color=nextcord.Color(value=re[8]),
                thumbnail="https://1000logos.net/wp-content/uploads/2017/05/Wikipedia-logos.jpg"
            )
            embeds.append(em)
        await pa1(embeds,ctx)
    except Exception as e:
        await ctx.send(
            embed=cembed(
                title="Hmm",
                description=str(e),
                color=re[8],
                thumbnail=client.user.avatar.url
            )
        )


@client.command(aliases=["hi","ping"])
async def check(ctx):
    req()
    print("check")
    emo = assets.Emotes(client)
    r = g_req()
    em = cembed(
        title=f"Online {emo.check}",
        description=f"Hi, {getattr(ctx, 'author', getattr(ctx, 'user', None)).name}\nLatency: \t{int(client.latency*1000)}ms\nRequests: \t{r:,}\nAwake time: {int(time.time()-start_time)}s",
        color=re[8],
        footer="Have fun, bot has many features, check out /help",
        thumbnail = client.user.avatar.url
    )
    await ctx.send(embed=em)


@client.slash_command(name="check", description="Check if the bot is online")
async def check_slash(ctx):
    req()
    await check(ctx)


@client.event
async def on_message_edit(message_before, message_after):
    await client.process_commands(message_after)

@client.command()
async def clear(ctx, text, num=10):
    req()
    await ctx.message.delete()
    if str(text) == re[1]:
        user = getattr(ctx, 'author', getattr(ctx, 'user', None))
        if user.guild_permissions.manage_messages or user.id == 432801163126243328:
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
                embed=nextcord.Embed(
                    title="Permission Denied",
                    description="You cant delete messages",
                    color=nextcord.Color(value=re[8]),
                )
            )
    else:
        await ctx.send("Wrong password")

@client.slash_command(name="ticket",description="create a ticket message")
async def tick(ctx, description=None):
    await ctx.response.defer()
    if not ctx.user.guild_permissions.administrator:
        emo = assets.Emotes(client)
        await ctx.send(
            embed=cembed(
                title="Permissions Denied",
                description=f"{e.animated_wrong}You're not an admin to create a ticket message",
                color=re[8]
            )
        )
        return
    if not description:
        description = "Open your tickets here"
    message = await ctx.send(
        embed=cembed(
            title="Ticket",
            description=description,
            color=re[8],
            thumbnail=ctx.guild.icon.url
        )
    )
    await message.add_reaction(emoji.emojize(":ticket:"))    
    config['ticket'][ctx.guild.id] = (ctx.channel.id, message.id)

@client.command()
async def close_ticket(ctx):    
    if type(ctx.channel) != nextcord.Thread: return
    if ctx.channel.owner == client.user:
        confirm = await wait_for_confirm(ctx,client,"Do you want to close this ticket?", re[8])
        if not confirm: return
        if not ctx.author.id == int(ctx.channel.name.split()[-1]):
            if not ctx.author.guild_permissions.administrator:
                return
        
        await ctx.send(
            embed=cembed(
                description="Deleting the ticket in 5 seconds",
                color=re[8]
            )
        )
        await asyncio.sleep(5)
        await ctx.channel.delete()
        

@client.event
async def on_raw_reaction_add(payload):
    #0->channel id
    #1->message id
    if payload.member.bot: return    
    if payload.emoji.name == chr(127915):
        if payload.guild_id not in config['ticket']: return
        if not client.get_channel(config['ticket'][payload.guild_id][0]):
            del config['ticket'][payload.guild_id]
            return
        if payload.channel_id != config['ticket'][payload.guild_id][0]: return
        msg = payload.message_id
        channel = client.get_channel(config['ticket'][payload.guild_id][0])
        print(payload.emoji.name)
        ms = await channel.fetch_message(msg)
        if msg != config['ticket'][payload.guild_id][1]: return
        await ms.remove_reaction(payload.emoji, payload.member)
        mess = await channel.send(
            embed=cembed(description=f"Creating Ticket for {payload.member.name}", color=re[8])
        )
        
        th = await channel.create_thread(name = f"Ticket - {payload.member.name} {payload.member.id}", reason = f"Ticket - {payload.member.name}", auto_archive_duration = 60, message = mess)
        await mess.delete()
        await th.send(client.get_user(payload.user_id).mention)
        
    
@client.event
async def on_reaction_add(reaction, user):
    req()
    ctx = reaction.message
    try:
        if not user.bot:
            save_to_file()
            global Emoji_list           
            if reaction.emoji == emoji.emojize(":musical_note:"):               
                await currentmusic(reaction.message)    
                await reaction.remove(user)
            if reaction.emoji == "⏮":
                if (
                    str(user) != str(client.user)
                    and reaction.message.author == client.user
                ):
                    await reaction.remove(user)
                    req()
                    reaction.message.author = user
                    await previous(reaction.message)
            if reaction.emoji == "⏸":
                if (
                    str(user) != str(client.user)
                    and reaction.message.author == client.user
                ):
                    await reaction.remove(user)
                    req()
                    reaction.message.author = user
                    await pause(reaction.message)
            if reaction.emoji == "▶":
                if (
                    str(user) != str(client.user)
                    and reaction.message.author == client.user
                ):
                    await reaction.remove(user)
                    req()
                    reaction.message.author = user
                    await resume(reaction.message)
            if reaction.emoji == "🔁":
                if (
                    str(user) != str(client.user)
                    and reaction.message.author == client.user
                ):
                    await reaction.remove(user)
                    reaction.message.author = user
                    await again(reaction.message)
            if reaction.emoji == "⏭":
                if (
                    str(user) != str(client.user)
                    and reaction.message.author == client.user
                ):
                    await reaction.remove(user)
                    req()
                    reaction.message.author = user
                    await next(reaction.message)
            if reaction.emoji == "⏹":
                req()
                if (
                    str(user) != str(client.user)
                    and reaction.message.author == client.user
                ):
                    await reaction.remove(user)
                    reaction.message.author = user
                    await leave(reaction.message)
            if (
                reaction.emoji == emoji.emojize(":keycap_*:")
                and reaction.message.author == client.user
            ):
                await reaction.remove(user)
                st= ""
                index = re[3][str(ctx.guild.id)] 
                songs = queue_song[str(ctx.guild.id)]
                lower = 0 if index - 10 < 0 else index - 10
                higher = len(songs) if index+10>len(songs) else index+10
                length = f"Length of queue: {len(songs)}\n"
                if ctx.guild.voice_client.channel:
                    bitrate = f"\n\nBitrate of the channel {ctx.guild.voice_client.channel.bitrate//1000}kbps\n"
                else:
                    bitrate = "Not Connected"
                latency = f"Latency: {int(ctx.guild.voice_client.latency*1000)}ms"
                
                for i in range(lower,higher):
                    song = f"{i}. {da1[songs[i]]}"
                    if i == index: 
                        song = f"*{song}*"
                    st = f"{st}{song}\n"
                await reaction.message.edit(
                    embed=nextcord.Embed(
                        title="Queue",
                        description=st + bitrate + length + latency,
                        color=nextcord.Color(value=re[8]),
                    )
                )
            if str(user.id) in list(dev_users):
                global dev_channel
                channel = client.get_channel(dev_channel)
                if (
                    reaction.emoji == emoji.emojize(":laptop:")
                    and str(reaction.message.channel.id) == str(channel.id)
                    and reaction.message.author == client.user
                ):
                    string = ""
                    await reaction.remove(user)
                    for i in list(dev_users):
                        string = string + str(client.get_user(int(i)).name) + "\n"
                    await channel.send(
                        embed=nextcord.Embed(
                            title="Developers",
                            description=string + "\n\nThank you for supporting",
                            color=nextcord.Color(value=re[8]),
                        )
                    )
                if reaction.emoji == emoji.emojize(":bar_chart:") and str(
                    reaction.message.channel.id
                ) == str(channel.id):
                    await reaction.remove(user)
                    reaction.message.author == user
                    await load(reaction.message)              
                if reaction.emoji == "⭕" and ctx.channel.id == channel.id:
                    await reaction.remove(user)
                    await channel.send(
                        embed=nextcord.Embed(
                            title="Servers",
                            description='\n'.join([i.name+"" for i in client.guilds]),
                            color=nextcord.Color(value=re[8]),
                        )
                    )
                if reaction.emoji == emoji.emojize(":fire:") and str(
                    reaction.message.channel.id
                ) == str(channel.id):
                    reaction.message.author = user
                    await restart_program(reaction.message,re[1])
                if reaction.emoji == emoji.emojize(":cross_mark:") and str(
                    reaction.message.channel.id
                ) == str(channel.id):
                    await reaction.remove(user)
                    if len(client.voice_clients)>0:
                        confirmation = await wait_for_confirm(
                            reaction.message, client, f"There are {len(client.voice_clients)} servers listening to music through Alfred, Do you wanna exit?", color=re[8], usr=user                        
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
                        embed=nextcord.Embed(
                            title="Exit",
                            description=("Requested by " + str(user)),
                            color=nextcord.Color(value=re[8]),
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
                        embed=nextcord.Embed(
                            title="Speedtest Results:",
                            description=str(download_speed)
                            + "Mbps\n"
                            + str(upload_speed)
                            + "Mbps\n"
                            + str(ping)
                            + "ms",
                            color=nextcord.Color(value=re[8]),
                        )
                    )
                
                if reaction.emoji == emoji.emojize(":black_circle:") and str(
                    reaction.message.channel.id
                ) == str(channel.id):
                    await devop_mtext(client, channel, re[8])
    except PermissionError:
        await reaction.message.channel.send(embed=cembed(
            title="Missing Permissions",
            description="Alfred is missing permissions, please try to fix this, best recommended is to add Admin to the bot",
            color=re[8],
            thumbnail=client.user.avatar.url)
        )
    except Exception as e:        
        channel = client.get_channel(dev_channel)
        await channel.send(
            embed=cembed(
                title="Error in on_reaction_add",
                description=f"{traceback.format_exc()}",
                footer=f"{reaction.message.guild.name}:{reaction.message.channel.name}",
                color=nextcord.Color(value=re[8]),
            )
        )

@client.event
async def on_command_error(ctx, error):    
    channel = client.get_channel(dev_channel)
    err = ''.join(traceback.format_tb(error.__traceback__))
    if err == '': erro = str(error)
    print(error.with_traceback(error.__traceback__))
    if type(error) != nextcord.ext.commands.errors.CommandNotFound:
        await ctx.send(embed=ror.error(str(error)))
    await channel.send(embed=cembed(title="Error",description=f"\n{str(error)}", color=re[8], thumbnail=client.user.avatar.url, footer = f"{getattr(ctx, 'author', getattr(ctx, 'user', None)).name}:{ctx.guild.name}"))


@client.command(aliases=["cen"])
async def add_censor(ctx, *, text):
    req()
    string = ""
    censor.append(text.lower())
    for i in range(0, len(text)):
        string = string + "-"
    em = nextcord.Embed(
        title="Added " + string + " to the list",
        decription="Done",
        color=nextcord.Color(value=re[8]),
    )
    await ctx.send(embed=em)


@client.command()
async def changeM(ctx, *, num):
    if str(getattr(ctx, 'author', getattr(ctx, 'user', None)).id) in dev_users:
        num = int(num)
        if num == 1:
            re[10] = 1
            await ctx.send(
                embed=nextcord.Embed(
                    title="Model change",
                    description="Changed to blenderbot",
                    color=nextcord.Color(value=re[8]),
                )
            )
        elif num == 2:
            re[10] = 2
            await ctx.send(
                embed=nextcord.Embed(
                    title="Model change",
                    description="Changed to dialo-gpt",
                    color=nextcord.Color(value=re[8]),
                )
            )
        else:

            await ctx.send(
                embed=nextcord.Embed(
                    title="Model change",
                    description="Bruh thats not a valid option",
                    color=nextcord.Color(value=re[8]),
                )
            )

    else:
        await ctx.send(
            embed=nextcord.Embed(
                title="Model change",
                description="F off thout isn't un dev user",
                color=nextcord.Color(value=re[8]),
            )
        )

@client.event
async def on_message(msg):
    save_to_file()
    await client.process_commands(msg) 
    global run_suicide
    if (not msg.guild.id in observer) and (not msg.author.bot):
        try:
            s = msg.clean_content
            
            whitelist = string.ascii_letters + ' '
            global new_s
            new_s = ''.join(c for c in s if c in whitelist)
            req()
    
            new_s = regex.sub(' +', ' ', new_s)
            
            if new_s != '' or new_s is not None: 
                json = {"text" : new_s}
                if msg.author.id not in deathrate.keys():
                    deathrate[msg.author.id]=0
    
                preds = await post_async("https://suicide-detector-api-1.yashvardhan13.repl.co/classify", json=json) 
                if preds["result"] == "Sucide":
                    deathrate[msg.author.id]+=1
                if deathrate[msg.author.id] >=10:
                    await msg.reply(embed=suicide_m(client,re[8]))
                    deathrate[msg.author.id] = 0
        except Exception as e:
            pass
    

    auth = os.getenv("transformers_auth")
    headeras = {"Authorization": f"Bearer {auth}"}
    if re[10] == 1:
        API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
    else:
        API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-large"

    try:
        if msg.content.lower().startswith("alfred ") and msg.guild.id not in config['respond'] and not msg.author.bot:

            input_text = msg.content.lower().replace("alfred", "")
            payload = {
                "inputs": {
                    "past_user_inputs": past_respose,
                    "generated_responses": generated,
                    "text": input_text,
                },
                "parameters": {"repetition_penalty": 1.33},
            }
            if re[10]!=1:
                payload = {
                    "inputs": input_text
                }

            output = await post_async(API_URL, header=headeras, json=payload)

            if len(past_respose) < 50:
                past_respose.append(input_text)
                generated.append(output["generated_text"])
            else:
                past_respose.pop(0)
                generated.pop(0)
                past_respose.append(input_text)
                generated.append(output["generated_text"])

            await msg.reply(output["generated_text"])

        if f"<@!{client.user.id}>" in msg.content:
            prefi = prefix_dict.get(msg.guild.id if msg.guild is not None else None, "'")
            embed = nextcord.Embed(
                title="Hi!! I am Alfred.",
                description=f"""Prefix is {prefi}\nFor more help, type {prefi}help""",
                color=nextcord.Color(value=re[8]),
            )
            embed.set_image(
                url=random.choice(
                    [                        "https://giffiles.alphacoders.com/205/205331.gif",
                        "https://c.tenor.com/PQu-tE-5HxwAAAAd/michael-caine-the-dark-knight.gif",
                    ]
                )
            )

            await msg.channel.send(embed=embed)
        if msg.content.startswith(prefix_dict.get(msg.guild.id if msg.guild is not None else None, "'")) == 0:
            save_to_file()

        if msg.channel.id in autor:
            for emo in autor[msg.channel.id]:                
                await msg.add_reaction(emoji.emojize(emo.strip()))        
                await asyncio.sleep(1)        
        
    except Exception as e:
        channel = client.get_channel(dev_channel)
        await channel.send(
            embed=nextcord.Embed(
                title="Error", description=str(e), color=nextcord.Color(value=re[8])
            )
        )

@client.slash_command(name = "lyrics", description = "Gets a lyrics of a song")
async def lyrics_slash(ctx, song):
    await ctx.response.defer()
    await ctx.send(embed=await ly(song,re))

@client.slash_command(name="sealfred", description="Checks for behaviours like kicking out or banning regularly")
async def SeCurity(ctx, log_channel: GuildChannel = "delete"):
    await ctx.response.defer()        
    if not ctx.permissions.administrator:
        await ctx.send(
            embed=cembed(
                title="Permission",
                description="You need admin permissions to do the security work, Ask your owner to execute this command for protection",
                color=discord.Color.red(),
                thumbnail=client.user.avatar.url
            )
        )
        return
    if log_channel == 'delete':
        if ctx.guild.id in config['security']:
            del config['security'][ctx.guild.id]
        await ctx.send(
            embed=cembed(
                description="Removed SEAlfred from this server, this server is now left unprotected",
                color=re[8]
            )
        )
        return
    channel_id = log_channel.id    
    config['security'][ctx.guild.id] = channel_id
    await ctx.send(
        embed=cembed(
            title="Done",
            description=f"Set {log_channel.mention} as the log channel, all the updates will be pushed to this",
            color=re[8]
        )
    )

@client.command()
async def stop(ctx):
    req()
    try:
        mem = [str(names) for names in getattr(ctx, 'voice_client', getattr(ctx.guild, 'voice_client', None)).channel.members]
    except:
        mem = []
    if mem.count(str(getattr(ctx, 'author', getattr(ctx, 'user', None))))>0:
        voice=nextcord.utils.get(client.voice_clients,guild=ctx.guild)
        voice.stop()
        await ctx.send(embed=nextcord.Embed(title="Stop",color=nextcord.Color(value=re[8])))
    else:
        await ctx.send(embed=nextcord.Embed(title="Permission denied",description="Join the channel to resume the song",color=nextcord.Color(value=re[8])))

@client.command(aliases=["m"])
async def python_shell(ctx, *, text):
    req()
    print("Python Shell", text, str(getattr(ctx, 'author', getattr(ctx, 'user', None))))
    global dev_users
    if str(getattr(ctx, 'author', getattr(ctx, 'user', None)).id) in dev_users:
        try:
            
            text = text.replace("```py", "").replace("```", "")
            a = eval(text)
            print(text)
            em = nextcord.Embed(
                title=text,
                description=text + "=" + str(a),
                color=nextcord.Color(value=re[8]),
            )
            em.set_thumbnail(
                url="https://engineering.fb.com/wp-content/uploads/2016/05/2000px-Python-logo-notext.svg_.png"
            )
            await ctx.send(embed=em)
        except Exception as e:
            await ctx.send(
                embed=nextcord.Embed(
                    title="Error_message",
                    description=str(e),
                    color=nextcord.Color(value=re[8]),
                )
            )
        
    else:
        try:
            await ctx.message.delete()
        except:
            pass
        await ctx.send(
            embed=nextcord.Embed(
                title="Permission denied",
                description="",
                color=nextcord.Color(value=re[8]),
            )
        )


@client.command()
async def exe(ctx, *, text):
    req()
    if (
        str(getattr(ctx, 'author', getattr(ctx, 'user', None)).id) in dev_users
    ):
        if str(getattr(ctx, 'author', getattr(ctx, 'user', None)).id) in dev_users and ctx.guild.id != 822445271019421746:
            await ctx.send(
                embed=cembed(
                    title="Permissions Denied",
                    description = "You can only use this command in Batcave",
                    color=re[8]                    
                )
            )
            return
        mysql_password = "Denied"
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
                await ctx.send(embed = ror.error(str(e)))
        output = f.getvalue()
        embeds=[]
        if output == "":
            output = "_"
        for i in range(len(output)//2000+1):
            em = cembed(title="Python",description=output[i*2000:i*2000+2000],color=re[8])
            em.set_thumbnail(
                url="https://engineering.fb.com/wp-content/uploads/2016/05/2000px-Python-logo-notext.svg_.png"
            )
            embeds.append(em)
        await pa1(embeds,ctx,restricted=True)
    else:
        await ctx.send(
            embed=nextcord.Embed(
                title="Denied",
                description="Ask Devs to give access for scripts",
                color=nextcord.Color(value=re[8]),
            )
        )


def addt(p1, p2):
    da[p1] = p2
    return "Done"


def get_elem(k):
    return da.get(k, "Not assigned yet")

def on_suicider():
    global run_suicide
    run_suicide = True

def de(k):
    del da[k]
    return "Done"


def req():
    re[0] = re[0] + 1


def g_req():
    return re[0]

client.remove_command("help")

@client.command(aliases=['h'])
async def help(ctx):
    test_help = []    
    test_help += helping_hand.help_him(ctx, client, re)    
    await pa1(test_help, ctx, start_from=0)

@client.slash_command(name="help", description="Help from Alfred")
async def help_slash(ctx):
    req()
    await ctx.response.defer()
    await help(ctx)
    
keep_alive()
if os.getenv("dev-bot"):
    client.run(os.getenv("token_dev"))
else:
    client.run(os.getenv("token"))