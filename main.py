def temporary_fix():
    from shutil import copyfile
    copyfile("./utils/post.py","/opt/virtualenvs/python3/lib/python3.8/site-packages/instascrape/scrapers/post.py")
    
import os
import sys
import subprocess
sys.path.insert(1,f"{os.getcwd()}/utils/")
sys.path.insert(1,f"{os.getcwd()}/src")
sys.path.insert(1,f"{os.getcwd()}/cogs")
print("Booting up")
temporary_fix()
from keep_alive import keep_alive
import string
import nextcord

from utils import helping_hand
from random import choice
from nextcord import Interaction, SlashOption, ChannelType
from nextcord.ext import commands, tasks
from nextcord.abc import GuildChannel
from dotenv import load_dotenv
from math import *
from statistics import *
from utils.Storage_facility import Variables
from io import StringIO
from contextlib import redirect_stdout
from utils.External_functions import *
import traceback
import youtube_dl
import re as regex
import urllib.request
import ffmpeg
import time
import emoji
import psutil
import asyncio 
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
global sent
observer=[]
mspace={}
deathrate = {}
sent = None
intents = nextcord.Intents().default()
intents.members = True
intents.message_content = True
old_youtube_vid = {}
youtube_cache = {}
deleted_message = {}
config = {
    'snipe': [841026124174983188, 822445271019421746,830050310181486672, 912569937116147772],
    'respond': [],
    'youtube': {},
    'welcome': {},
    'ticket' : {},
    'security':{},
    'commands':{},
    'reactions':{}
    }
da = {}
errors = ["```arm"]
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
vc_channel = {}
wolfram = os.getenv("wolfram")
prefix_dict = {}



# replace your id with this
dev_users = {"432801163126243328"}
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

async def search_vid(name):
    pass

def prefix_check(client, message):
    return prefix_dict.get(message.guild.id if message.guild is not None else None, "'"),f"<@{client.user.id}> "


client = nextcord.ext.commands.Bot(
    command_prefix=prefix_check,
    intents=intents,
    case_insensitive=True,
)

try:
    store = Variables("storage")
except:
    os.remove("storage.dat")
    store = Variables("storage")

def save_to_file():
    global dev_users
    print("save")
    store = Variables("storage")
    store.pass_all(
        da = client.da,
        mspace = client.mspace,
        da1 = client.da1,
        queue_song = client.queue_song,
        a_channels = a_channels,
        re = re,
        dev_users = dev_users,
        prefix_dict = prefix_dict,
        observer = observer,
        old_youtube_vid = old_youtube_vid,
        config = config,        
        autor = autor,
        time = str(datetime.datetime.now().time())
    )
    store.save()


def load_from_file():
    global da
    global da1
    global queue_song
    global re
    global dev_users
    global prefix_dict
    global observer
    global old_youtube_vid
    global config
    global mspace
    global autor

    v = store.show_data()    
    da = v.get("da",{})
    da1 = v.get("da1", {})
    queue_song = v.get("queue_song",{})
    a_channels = v.get("a_channels",[])
    re = v.get("re",re)
    dev_users = v.get("dev_users",dev_users)
    prefix_dict = v.get("prefix_dict",{})
    observer = v.get("observer",[])
    old_youtube_vid = v.get("old_youtube_vid",{})
    config = v.get("config",config)
    mspace = v.get("mspace",{})
    autor = v.get("autor",{})    

    #using these to pass to other files like cogs
    client.re = re
    client.dev_users = dev_users
    client.config = config
    client.prefix_dict = prefix_dict
    client.da = da
    client.da1 = da1
    client.queue_song = queue_song
    client.mspace = mspace
    client.observer = observer
    
    


try:
    load_from_file()
except:
    print("Failed to load\n\n\n")
    
report = f"""Started at: {timestamp(int(start_time))}
Current location: {location_of_file}
Requests: {re[0]:,}
Color: {nextcord.Color(re[8]).to_rgb()}
```yml
[ OK ] Loaded all modules
[ OK ] Setup SpeedTest
[ OK ] Variables initialised 
[ OK ] Load From File Completed
[ OK ] Switching Root ...
"""

for i in os.listdir(location_of_file + "/src"):
    if i.endswith(".py"):
        a = ""
        try:
            print(i, end="")
            requi = __import__(i[0 : len(i) - 3]).requirements()
            if type(requi) is str:
                a = f"__import__('{i[0:len(i)-3]}').main(client,{requi})"
                eval(a)
            if type(requi) is list:
                a = f"__import__('{i[0:len(i)-3]}').main(client,{','.join(requi)})"
                eval(a)
            print(": Done")
            report+=f"[ OK ] Imported {i} successfully\n"
        except Exception as e:
            print(": Error")
            report+=f"[ {int(time.time()-start_time)} ] Error in {i}: {e}\n{a} \n"
            errors.append(f"[ {int(time.time()-start_time)} ] Error in {i}: {str(e)[:10]}...\n")

@client.event
async def on_ready():
    print(client.user)    
    global report
    await client.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.watching, name="Booting in progress"))
    report+=f"[ OK ] Starting On Ready\n[ OK ] Bot named as {client.user.name}\n"
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
        
        with open("commands.txt","w") as f:
          for i in client.commands:
            f.write(i.name+"\n")
        report+="[ OK ] Updated commands txt file"
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
    save_to_file()
    await client.get_channel(941601738815860756).send(file=nextcord.File("storage.dat",filename="storage.dat"))
    
@tasks.loop(minutes=30)
async def youtube_loop():
    #await client.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.listening, name=str(len(client.guilds))+" servers"))
    await client.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.listening, name="Beta AutoMod"))
    print("Youtube_loop")    
    for i,l in config['youtube'].items():
        await asyncio.sleep(2)
        for j in l:
            try:
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
            except: pass
    print("Done")

@tasks.loop(seconds = 30)
async def dev_loop():
    save_to_file()
    try:
        a = await get_async("https://suicide-detector-api-1.yashvardhan13.repl.co/")
        if a != '{"message":"API is running"}':
            ch = client.get_channel(976470062691135529)
            await ch.send(
                embed=cembed(
                    title="Fix her",
                    description="Your server is offline Master Bruce, Go check it out ||plssssss||",
                    color=re[8],
                    footer="Why does this server fall sir?",
                    thumbnail=client.user.avatar.url
                )
            )
        await get_async("https://Ellisa-Bot.arghyathegod.repl.co")
    except:
        await client.get_channel(dev_channel).send(
            embed=ef.cembed(
                description=str(traceback.format_exc()),
                color=re[8],
                footer="Error in keep alive dev_loop",
                thumbnail=client.user.avatar.url
            )
        )

@client.command()
@commands.check(check_command)
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

@client.command(aliases=['autoreaction'])
@commands.check(check_command)
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
@commands.check(check_command)
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


@client.slash_command(name="emoji", description="Get Emojis from other servers")
async def emoji_slash(ctx, emoji_name, number=1):
    req()
    number=int(number) - 1
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
@commands.check(check_command)
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
        user = getattr(ctx, 'author', getattr(ctx, 'user', None))
        emoji = [names for names in client.emojis if names.name == emoji_name][number]
        webhook = await ctx.channel.create_webhook(name=user.name)
        await webhook.send(emoji, username=user.name, avatar_url=safe_pfp(user))
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
    
@client.command(aliases=["cw"])
@commands.check(check_command)
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

@client.slash_command(name="color",description="Change color theme", guild_ids= [822445271019421746])
async def color_slash(ctx, rgb_color=defa(default="")):    
    rgb_color = rgb_color.replace("(","").replace(")","").split(",")
    if str(ctx.user.id) not in dev_users:
        await ctx.send(
            embed=cembed(
                title="Woopsies",
                description="This is a `developer-only` function",
                color=nextcord.Color.red(),
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

    re[8] = nextcord.Color.from_rgb(*[int(i) for i in rgb_color]).value
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
@commands.check(check_command)
async def load(ctx):
    print("Load", str(getattr(ctx, 'author', getattr(ctx, 'user', None))))
    req()
    try:
        cpu_per = str(int(psutil.cpu_percent()))
        cpu_freq = str(int(psutil.cpu_freq().current))
        ram = str(psutil.virtual_memory().percent)
        swap = str(psutil.swap_memory().percent)
        usage = f"""
        CPU Percentage: {cpu_per}%
        CPU Frequency : {cpu_freq}Mhz
        RAM usage: {ram}%
        Swap usage: {swap}%
        Nextcord: {nextcord.__version__}
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

@client.command(aliases=["c"])
@commands.check(check_command)
async def cover_up(ctx):
    await ctx.message.delete()
    await asyncio.sleep(0.5)
    mess = await ctx.send(nextcord.utils.get(client.emojis, name="enrique"))
    await mess.delete()

@client.command()
@commands.check(check_command)
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
@commands.check(check_command)
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
@commands.check(check_command)
async def dev_op(ctx):
    if str(getattr(ctx, 'author', getattr(ctx, 'user', None)).id) in list(dev_users):
        print("devop", str(getattr(ctx, 'author', getattr(ctx, 'user', None))))
        channel = client.get_channel(dev_channel)
        await devop_mtext(client, channel, re[8])
    else:
        await ctx.send(embed=cembed(title="Permission Denied",description="You cannot use the devop function, only a developer can",color=re[8]))

@client.command()
@commands.check(check_command)
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
async def snipe_slash(inter, number = 50):
    req()
    await snipe(inter, number)


@client.command()
@commands.check(check_command)
async def snipe(ctx, number=50):
    number = int(number)
    if (
        getattr(ctx, 'author', getattr(ctx, 'user', None)).guild_permissions.administrator
        or ctx.guild.id not in config['snipe']
    ):
        message = deleted_message.get(ctx.channel.id,[("Empty","Nothing here lol")])[::-1]
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
                        thumbnail=safe_pfp(ctx.guild)
                    )
                    embeds.append(embed)
                    s=""                        
            else:
                await ctx.send("**" + i[0] + ":**",embed=i[1])
        if len(embeds)>0: 
            await assets.pa(ctx, embeds, start_from=0, restricted=True)
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

@client.event
async def on_member_join(member):
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
    if member.guild.id in config['security']:
        print(member.guild)
        a = member.guild
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

@client.command()
@commands.check(check_command)
async def remove(ctx, n):
    req()
    mem = [names.id for names in ctx.guild.voice_client.channel.members] if ctx.guild.voice_client else []
    if mem.count(getattr(ctx, 'author', getattr(ctx, 'user', None)).id) > 0:
        if int(n) < len(queue_song[str(ctx.guild.id)]):
            if re[3][str(ctx.guild.id)]>int(n):re[3][str(ctx.guild.id)]-=1
            del da1[queue_song[str(ctx.guild.id)][int(n)]]
            queue_song[str(ctx.guild.id)].pop(int(n))
            await ctx.send(
                embed=nextcord.Embed(
                    title="Removed",
                    description=da1[queue_song[str(ctx.guild.id)][int(n)]],
                    color=nextcord.Color(value=re[8]),
                )
            )            
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

@client.slash_command(name="dictionary", description="Use the dictionary for meaning")
async def dic(ctx, word):
    await ctx.response.defer()
    try:
        mean = Meaning(word = word, color = re[8])
        await mean.setup()
        await assets.pa(ctx, mean.create_texts(), start_from=0, restricted=False)
    except Exception as e:
        await ctx.send(
            embed=ef.cembed(
                title="Something is wrong",
                description="Oops something went wrong, I gotta check this out real quick, sorry for the inconvenience",
                color=nextcord.Color.red(),
                thumbnail=client.user.avatar.url
            )
        )
        print(traceback.format_exc())

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
    auth = getattr(ctx,'author',getattr(ctx,'user', None)).id
    await client.get_channel(932890298013614110).send(
        content=str(ctx.channel.id)+" "+str(auth),
        embed=embed
        
    )
    await ctx.send(
        embed=cembed(
            title="Done",
            description="I've given this info to the developers, they will try fixing it asap :smiley:",
            color=re[8]
        )
    )

@client.command()
async def rollback(ctx):
    if str(ctx.author.id) not in dev_users or ctx.channel.id != 941601738815860756:
        return
    if not ctx.message.reference:
        await ctx.send("Not replied to a message")
        return
    m = await ctx.channel.fetch_message(ctx.message.reference.message_id)
    if m.attachments == []:
        await ctx.send("No file found")
        return
    attachment = m.attachments[0].url
    if not attachment.endswith("storage.dat"):
        await ctx.send("Not a storage file")
        return
    os.remove("storage.dat")
    await get_async(attachment, kind="file>storage.dat")
    store=Variables("storage")
    load_from_file()
    save_to_file()
    await m.reply("Reverted to this")
    

@client.slash_command(name = "feedback",description="Send a feedback to the developers")
async def f_slash(inter, text):
    await feedback(inter, text=text)
    
async def poll(ctx, Options = "", Question = "", image="https://i.imgur.com/chLCmUl.jpg"):
    channel = ctx.channel
    text = Question+"\n\n"
    Options = Options.split("|")
    if len(Options)>=20:
        reply = "Use this if you want to redo\n\n"
        reply+= f"Question: `{Question}` \n"
        reply+= f"Options: `{'|'.join(Options)}`"
        await ctx.send(
            embed=cembed(
                title="Sorry you can only give 20 options",
                description=reply,
                color=nextcord.Color.red(),
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
async def polling_slash(inter, question, options="yes|no",image=None):
    await inter.response.defer()
    if not image: image = safe_pfp(inter.guild)
    await poll(inter, Options = options, Question = question if question else "", image = image)

@client.slash_command(name="eval",description="This is only for developers",guild_ids= [822445271019421746])
async def eval_slash(ctx,text):
    await python_shell(ctx, text = text)

@client.command(aliases=["!"])
async def restart_program(ctx, text):
    if str(getattr(ctx, 'author', getattr(ctx, 'user', None)).id) in list(dev_users):
        save_to_file()        
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
        await client.change_presence(activity = nextcord.Activity(type = nextcord.ActivityType.listening, name= "Restart"))        
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


@client.command(aliases=["*"])
@commands.check(check_command)
async def change_nickname(ctx, member: nextcord.Member, *, nickname=None):
    user = getattr(ctx, 'author', getattr(ctx, 'user', None))
    if user.guild_permissions.change_nickname and user.top_role.position > member.top_role.position:
        await member.edit(nick=nickname)
        await ctx.send(
            embed=nextcord.Embed(
                title="Nickname Changed",
                description=f"Nickname changed to {member.nick or member.name} by {user.mention}",
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
@commands.check(check_command)
async def dev_test(ctx, id:nextcord.Member=None):
    if id:
        if str(id.id) in dev_users:
            await ctx.send(f"{id} is a dev!")
        else:
            await ctx.send(f"{id} is not a dev!")
    else:
        await ctx.send("You need to mention somebody")

@client.event
async def on_message_edit(message_before, message_after):
    await client.process_commands(message_after)

@client.command()
@commands.check(check_command)
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
   
    
@client.event
async def on_reaction_add(reaction, user):
    req()
    ctx = reaction.message
    try:
        if not user.bot:
            global Emoji_list 
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
                if reaction.emoji == '💾' and reaction.message.channel.id == channel.id:
                    save_to_file()                    
                    await reaction.remove(user)
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
                    os.system("pkill python3")
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
    print(type(error))
    if type(error) == nextcord.errors.HTTPException:
        os.system("busybox reboot")
    if type(error) == nextcord.ext.commands.errors.CheckFailure:
        await ctx.send(
            embed=cembed(
                title="Disabled command",
                description="This command has been disabled by your admin, please ask them to enable it to use this\n\nIf you're an admin and you want to enable this command, use `/commands <enable> <command_name>`",
                color=client.re[8],
                thumbnail=safe_pfp(ctx.author)
            )
        )       
        return
    channel = client.get_channel(dev_channel)
    if error == nextcord.HTTPException: os.system("busybox reboot")
    if type(error) != nextcord.ext.commands.errors.CommandNotFound:
        await ctx.send(embed=ror.error(str(error)))
    await channel.send(embed=cembed(title="Error",description=f"\n{str(error)}", color=re[8], thumbnail=client.user.avatar.url, footer = f"{getattr(ctx, 'author', getattr(ctx, 'user', None)).name}:{ctx.guild.name}"))

@client.event
async def on_message(msg):
    await client.process_commands(msg)             
    try:
        if msg.channel.id in autor:
            for emo in autor[msg.channel.id]:                
                await msg.add_reaction(emoji.emojize(emo.strip()))  
                await asyncio.sleep(1)       
        
    except Exception as e:
        channel = client.get_channel(dev_channel)
        await channel.send(
            embed=nextcord.Embed(
                title="Error", description=str(traceback.format_exc()), color=nextcord.Color(value=re[8])
            )
        )



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
            em = cembed(
                title=text,
                description=str(a),
                color=nextcord.Color(value=re[8]),
                thumbnail="https://engineering.fb.com/wp-content/uploads/2016/05/2000px-Python-logo-notext.svg_.png"
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
                description="Permissions Denied",
                color=nextcord.Color(value=re[8]),
            )
        )

@client.command()
@commands.check(check_command)
async def exe(ctx, *, text):
    req()
    if (
        str(getattr(ctx, 'author', getattr(ctx, 'user', None)).id) in dev_users
    ):
        if False:
            await ctx.send(
                embed=cembed(
                    title="Permissions Denied",
                    description = "You can only use this command in Wayne Enterprises",
                    color=re[8]                    
                )
            )
            return
        text = text.replace("```py", "```")
        text = text[3:-3].strip()
        f = StringIO()
        with redirect_stdout(f):
            try:
                exec(text)
            except Exception as e:
                traceback.print_tb(e.__traceback__)
                error_mssg = "Following Error Occured:\n\n"+traceback.format_exc()
                await ctx.send(embed = ror.error(error_mssg))
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
        await assets.pa(ctx, embeds, start_from=0, restricted=False)
    else:
        await ctx.send(
            embed=nextcord.Embed(
                title="Denied",
                description="Ask Devs to give access for scripts",
                color=nextcord.Color(value=re[8]),
            )
        )
        
@client.command()
async def cute_cat(ctx, res="1920x1080"):
    query = "kitten"
    await get_async(f"https://source.unsplash.com/{res}?{query}",kind="file>cat.png")
    with open("cat.png","rb") as f:
        file = nextcord.File(f)
        em = nextcord.Embed(title=ctx.author, color=re[8])
        em.set_image(url="attachment://cat.png")
        await ctx.send(file=file, embed=em)
    os.remove("cat.png")

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

def reload_extension(name):
    client.unload_extension(f'cogs.{name}')
    return load_extension(name)

def load_extension(name):
    '''
    This will safely add cog for alfred with all the requirements
    '''
    try:
        l = __import__(name).requirements()
        d = {}
        for i in l:
            d[i] = globals()[i]
        client.load_extension(f'cogs.{name}',extras=d)
        return f"[ OK ] Added {name}\n"
    except:
        return f"Error in cog {name}:\n"+traceback.format_exc()+"\n"

def load_all():
    for i in os.listdir(os.getcwd()+"/cogs"):
        if i.endswith(".py"):
            global report
            report+=load_extension(i[:-3])
            
client.remove_command("help")
load_all()
keep_alive()

try: 
    client.run(os.getenv("token"))
except: 
    print(traceback.format_exc())
    time.sleep(20)
    os.system("busybox reboot")
