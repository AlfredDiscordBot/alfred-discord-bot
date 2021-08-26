'''
Set your env like the example below:
token=
sjdoskenv=
sjdoskenv1=
mysql=
default=
'''


import discord
from random import choice
from discord.ext import commands, tasks
from discord_slash import SlashCommand
from googlesearch import search
from GoogleNews import GoogleNews
from dotenv import load_dotenv
from math import *
from statistics import *
from wikipedia import search, summary
from io import StringIO
from contextlib import redirect_stdout
from External_functions import *
#from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType
import traceback
import googlesearch
import youtube_dl
import os
import re as regex
import urllib.request
import requests
import ffmpeg
import time
import sys
import emoji
import psutil
import asyncio
import cloudscraper


location_of_file=os.getcwd()
try:
    import mysql.connector as m
    load_dotenv()
except:
    pass
import speedtest
if True:
    try:
        st_speed=speedtest.Speedtest()
    except:
        print("failed")
    googlenews=GoogleNews()
    if os.getcwd()!=os.getenv('default'):
        os.chdir(os.getenv('default'))
    start_time=time.time()
    try:
        md=m.connect(host="localhost", user="root", passwd=os.getenv('mysql'))
        conn=md
        cursor=md.cursor()
    except:
        pass
    X = '❌'
    O = '⭕'
    global coin_toss_message, coin_message
    coin_toss_message=None
    coin_message="Pick "+emoji.emojize(":face_with_head-bandage:")+" for heads \nPick "+emoji.emojize(":hibiscus:")+" for tails"
    global board, Emoji_list
    Emoji_list = [emoji.emojize(":keycap_"+str(i)+":") for i in range(1,10)]
    Raw_Emoji_list = [emoji.emojize(":keycap_"+str(i)+":") for i in range(1,10)]
    def reset_board():
        global board
        board = ""
        for i in range(1,10):
            board=board+emoji.emojize(":keycap_"+str(i)+":")+" | "
            if i%3==0:
                board=board+"\n----    ----    ----\n"
        return board
    board=reset_board()
    global sent
    sent=None
    instagram_posts=[]
    dictionary=dict(zip(Raw_Emoji_list, Emoji_list))
    intents=discord.Intents.default()
    intents.members=True
    client=commands.Bot(command_prefix=["'","Alfred ","alfred "],intents=intents, case_insensitive=True)
    slash = SlashCommand(client, sync_commands=True)
    temp_dev={}
    censor=[]
    old_youtube_vid=[]
    deleted_message={}
    da={}
    entr={}
    da1={}
    queue_song={}
    temporary_list=[]
    dev_channel=834624717410926602
    re=[0,"OK",1,{},-1,'','205',1,5360, "48515587275%3A0AvceDiA27u1vT%3A26"]
    a_channels=[822500785765875749,822446957288357888]
    cat={}
    youtube=[]
    pages={}
    SESSIONID=None
    color_message=None
    color_temp=()    
    link_for_cats=[]
    vc_channel={}
    wolfram=os.getenv('wolfram')
    def mysql_load():
        try:
            aad=m.connect(host="localhost", user="root", passwd=os.getenv('mysql'),database="Discord")
            curs=aad.cursor()
            if len(youtube)==0:
                curs.execute("select * from youtube")
                datas=curs.fetchall()
                for data in datas:
                    youtube.append(data)        
            curs.execute("select * from old")
            datas=curs.fetchall()
            for data in datas:
                old_youtube_vid.append(data)
            aad.commit()
        except:
            time.sleep(10)
            mysql_load()
    mysql_load()
    #replace your id with this
    dev_users=['432801163126243328']
    ydl_op={'format':'bestaudio/best','postprocessors':[{'key':'FFmpegExtractAudio','preferredcodec':'mp3','preferredquality':'128',}],}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    def save_to_file(a=""):
        global dev_users
        if ".backup.txt" in os.listdir("./"):
            os.remove("./.backup.txt")
        if ".recover.txt" in os.listdir("./") and a=="recover":
            os.remove("./.recover.txt")
        if True:
            file = open(".backup.txt", "w")
            file.write("censor="+str(censor)+"\n")
            file.write("da="+str(da)+"\n")
            file.write("da1="+str(da1)+"\n")
            file.write("queue_song="+str(queue_song)+"\n")
            file.write("a_channels="+str(a_channels)+"\n")
            file.write("re="+str(re)+"\n")
            file.write("dev_users="+str(dev_users)+"\n")
            file.write("entr="+str(entr)+"\n")
            file.close()
        if a=="recover":
            file = open(".recover.txt", "w")
            file.write("censor="+str(censor)+"\n")
            file.write("da="+str(da)+"\n")
            file.write("da1="+str(da1)+"\n")
            file.write("queue_song="+str(queue_song)+"\n")
            file.write("a_channels="+str(a_channels)+"\n")
            file.write("re="+str(re)+"\n")
            file.write("dev_users="+str(dev_users)+"\n")
            file.write("entr="+str(entr)+"\n")
        if a=="save":
            file = open(".safe.txt", "w")
            file.write("censor="+str(censor)+"\n")
            file.write("da="+str(da)+"\n")
            file.write("da1="+str(da1)+"\n")
            file.write("queue_song="+str(queue_song)+"\n")
            file.write("a_channels="+str(a_channels)+"\n")
            file.write("re="+str(re)+"\n")
            file.write("dev_users="+str(dev_users)+"\n")
            file.write("entr="+str(entr)+"\n")        
    def load_from_file(file_name=".backup.txt"):
        if file_name in os.listdir("./"):
            file=open(file_name,"r")
            global censor
            global da
            global da1
            global queue_song
            global entr
            global re
            global dev_users
            txt_from_file=str(file.read())
            #censor list
            try:
                a1=txt_from_file.find("censor=")+len("censor")
                a2=txt_from_file.find("]",(a1+1))+1
                a1=txt_from_file.find("[",a1,a2)
                k_censor=eval(txt_from_file[a1:a2])
                censor=k_censor
            except:
                print("Problem with censor list")
            #da dictionary
            try:
                a1=txt_from_file.find("da=")+len("da")
                a2=txt_from_file.find("}",(a1+1))+1
                a1=txt_from_file.find("{",a1,a2)
                k_da=eval(txt_from_file[a1:a2])
                da=k_da
            except:
                print("Problem with da")
            #da1 dictionary
            try:
                a1=txt_from_file.find("da1=")+len("da1")
                a2=txt_from_file.find("}",(a1+1))+1
                a1=txt_from_file.find("{",a1,a2)
                k_da1=eval(txt_from_file[a1:a2])
                da1=k_da1
            except:
                print("Problem with da1")
            #entr list
            try:
                a1=txt_from_file.find("entr=")+len("entr")
                a2=txt_from_file.find("}",(a1+1))+1
                a1=txt_from_file.find("{",a1,a2)
                k_entr=eval(txt_from_file[a1:a2])
                entr=k_entr
            except:
                print("Problem with entr")
            #a_channels list
            try:
                a1=txt_from_file.find("a_channels=")+len("a_channels")
                a2=txt_from_file.find("]",(a1+1))+1
                a1=txt_from_file.find("[",a1,a2)
                k_a_channels=eval(txt_from_file[a1:a2])            
                a_channels=k_a_channels
            except:
                print("Problem with a_channels")
            #dev_users list
            try:
                a1=txt_from_file.find("dev_users=")+len("dev_users")
                a2=txt_from_file.find("]",(a1+1))+1
                a1=txt_from_file.find("[",a1,a2)
                k_dev_users=eval(txt_from_file[a1:a2])
                dev_users=k_dev_users
            except:
                print("Problem with dev_users")
            #queue_song dictionary
            try:
                a1=txt_from_file.find("queue_song=")+len("queue_song")
                a2=txt_from_file.find("}",(a1))+1
                a1=txt_from_file.find("{",a1,a2)
                k_queue_song=eval(txt_from_file[a1:a2])
                queue_song=k_queue_song
            except:
                print("Problem with queue song")
            #re list
            try:
                a1=txt_from_file.find("re=")+len("re")
                a2=txt_from_file.find("]",(a1+1))+1
                a1=txt_from_file.find("[",a1,a2)
                k_re=eval(txt_from_file[a1:a2])
                re=k_re
            except:
                print("Problem with re")
        save_to_file()
    def youtube_download(ctx,url):        
        if True:
            with youtube_dl.YoutubeDL(ydl_op) as ydl:
                URL = youtube_info(url)['formats'][0]['url']
        return URL
    def youtube_info(url):
        with youtube_dl.YoutubeDL(ydl_op) as ydl:
            info=ydl.extract_info(url, download=False)
        return info

    @client.event
    async def on_ready():
        channel = client.get_channel(dev_channel)
        #DiscordComponents(client, change_discord_methods=True)
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
            print("\nStarting devop display")
            await channel.purge(limit=10000000000000000000)
            text_dev="You get to activate and reset certain functions in this channel \n" \
            ""+(emoji.emojize(":safety_vest:"))+" for recovery \n"  \
            "⭕ for list of all servers \n" \
            "❌ for exiting \n" \
            "🔥 for restart\n" \
            "📊 for current load\n" \
            "❕ for current issues\n" \
            ""+emoji.emojize(":satellite:")+" for speedtest\n" \
            ""+emoji.emojize(":black_circle:")+" for clear screen\n" \
            ""+emoji.emojize(":classical_building: for starting Storage bot\n")+""
            embed=discord.Embed(title="DEVOP",description=text_dev,color=discord.Color(value=re[8]))
            embed.set_thumbnail(url=client.user.avatar_url_as(format="png"))
            mess=await channel.send(embed=embed)
            await mess.add_reaction(emoji.emojize(":safety_vest:"))
            await mess.add_reaction("⭕")
            await mess.add_reaction("❌")
            await mess.add_reaction(emoji.emojize(":fire:"))
            await mess.add_reaction(emoji.emojize(":bar_chart:"))
            await mess.add_reaction("❕")
            await mess.add_reaction(emoji.emojize(":satellite:"))
            await mess.add_reaction(emoji.emojize(":black_circle:"))
            await mess.add_reaction(emoji.emojize(":classical_building:"))
            await mess.add_reaction(emoji.emojize(":laptop:"))
            print("Finished devop display")            
            print("Starting imports")
            if True:
                imports=""
                sys.path.insert(1,location_of_file+"/src")
                for i in os.listdir(location_of_file+"/src"):
                    if i.endswith(".py"):
                        try:
                            requi=__import__(i[0:len(i)-3]).requirements()
                            if requi!="":
                                requi=","+requi
                            eval("__import__(i[0:len(i)-3]).main(client"+requi+")")
                            imports=imports+i[0:len(i)-3]+"\n"
                        except Exception as e:
                            await channel.send(embed=discord.Embed(title="Error in plugin "+i[0:len(i)-3], description=str(e),color=discord.Color(value=re[8])))
                await channel.send(embed=discord.Embed(title="Successfully imported",description=imports,color=discord.Color(value=re[8])))
        except Exception as e:
            mess=await channel.send(embed=discord.Embed(title="Error in the function on_ready", description=str(e),color=discord.Color(value=re[8])))
            await mess.add_reaction("❌")
        dev_loop.start()        
        print("Prepared")
        youtube_loop.start()

        
    @tasks.loop(minutes=7)
    async def youtube_loop():
        list_of_programs=['blender','chrome','inkscape','firefox','idle3','brave','gedit','discord']
        for i in list_of_programs:
            if get_if_process_exists(i):
                await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=i))
                break
        else:
            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=str(len(client.guilds))+" servers"))
        for i in youtube:
            try:
                a=get_youtube_url(i[0])[0]
                channel_youtube=client.get_channel(int(i[1]))
                if not (a,str(channel_youtube.guild.id)) in  old_youtube_vid:
                    old_youtube_vid.append((a,str(channel_youtube.guild.id)))
                    aad=m.connect(host="localhost", user="root", passwd=os.getenv('mysql'),database="Discord")        
                    curs=aad.cursor()
                    curs.execute("insert into old (video,channel) values('"+a+"', '"+str(channel_youtube.guild.id)+"')")
                    await channel_youtube.send(embed=discord.Embed(description="New video out from "+i[0],color=discord.Color(value=re[8])))
                    await channel_youtube.send(a)
                    aad.commit()
            except Exception as e:
                server_youtube=client.get_channel(int(i[1])).guild.name
                await client.get_channel(dev_channel).send(embed=discord.Embed(title="Error in Youtube loop",description=str(e)+"\n"+server_youtube,color=discord.Color(value=re[8])))
        try:
            aad=m.connect(host="localhost", user="root", passwd=os.getenv('mysql'),database="Discord")        
            curs=aad.cursor()
            if len(youtube)==0:
                curs.execute("select * from youtube")
                datas=curs.fetchall()
                for data in datas:
                    youtube.append(data)
            else:
                temp=[]
                curs.execute("select * from youtube")
                datas=curs.fetchall()
                for data in datas:
                    temp.append(data)
                if temp!=youtube:
                    curs.execute("delete from youtube")
                    for i in youtube:
                        curs.execute("Insert into youtube (url, channel) values ('"+str(i[0])+"', '"+str(i[1])+"')")
                
                    
            if len(queue_song)!=0:            
                asdf=str(re)
                curs.execute("Delete from queue")
                for j in list(queue_song.keys()):
                    for i in queue_song[j]:
                        curs.execute("Insert into queue (links,server) values ('"+i+"','"+j+"')")
                curs.execute('update requ set variable="'+asdf+'" where  here=1')
                
            else:
                curs.execute("Select distinct(server) from queue")
                servers=cursor.fetchall()
                for i in servers:
                    curs.execute("Select link from queue where server='"+i[0]+"';")
                    urls=curs.fetchall()
                    for url in urls:
                        queue_song[i[0]].append(url[0])
            aad.commit()
        except Exception as e:
            print(e)
    
                
    @tasks.loop(seconds=10)
    async def dev_loop():
        global temp_dev        
        for i in list(temp_dev.keys()):
            person=client.get_user(i)
            if temp_dev[i][0]>0:
                temp_dev[i][0]-=10
                await temp_dev[i][1].edit(embed=discord.Embed(title="Done",description=str(person.mention)+"\nTime remaining: "+str(temp_dev[i][0])+"s",color=discord.Color(value=re[8])))
            else:
                await temp_dev[i][1].edit(embed=discord.Embed(title="Time up", description="Your time is up, please ask a bot dev to give you access to the script function",color=discord.Color.from_rgb(250,50,0)))
                temp_dev.pop(i)
        
        
    @dev_loop.before_loop
    async def wait_for_ready():
        await client.wait_until_ready()

    @youtube_loop.before_loop
    async def wait_for_ready():
        await client.wait_until_ready()

    @client.command()
    async def imdb(ctx,*,movie):
        await ctx.send(embed=imdb_embed(movie))

    @slash.slash(name="imdb",description="Give a movie name")
    async def imdb_slash(ctx,movie):
        req()
        await ctx.defer()
        try:
            await ctx.send(embed=imdb_embed(movie))
        except Exception as e:
            await ctx.send(embed=cembed(title="Oops", description=str(e),color=re[8],thumbnail=client.user.avatar_url_as(format="png")))

        
    @client.command(aliases=['youtube'])
    async def subscribe(ctx, url, channel:discord.TextChannel):
        if url.startswith("http"):
            youtube.append((str(url),str(channel.id)))
            await ctx.send(embed=discord.Embed(description="Added "+url+" to the list\nUpdates will be in "+channel.name+" channel",color=discord.Color(value=re[8])))
        else:
            await ctx.send(embed=discord.Embed(description="Add the full link, including https",color=discord.Color(value=re[8])))

    @slash.slash(name="emoji",description="Get Emojis from other servers")
    async def emoji_slash(ctx,emoji_name,number=0):
        req()
        await ctx.defer()
        if discord.utils.get(client.emojis,name=emoji_name)!=None:
            emoji_list=[names.name for names in client.emojis if names.name==emoji_name]
            le=len(emoji_list)
            if le>=2:
                if number>le-1:
                    number=le-1
            emoji=[names for names in client.emojis if names.name==emoji_name][number].id
            await ctx.send(str(discord.utils.get(client.emojis,id=emoji)))
        else:
            await ctx.send(embed=discord.Embed(description="The emoji is not available",color=discord.Color(value=re[8])))
    
    @client.command(aliases=['e','emoji'])
    async def uemoji(ctx,emoji_name, number=0):
        req()
        try:
            await ctx.message.delete()
        except:
            pass
        if discord.utils.get(client.emojis,name=emoji_name)!=None:
            emoji_list=[names.name for names in client.emojis if names.name==emoji_name]
            le=len(emoji_list)
            if le>=2:
                if number>le-1:
                    number=le-1
            emoji=[names for names in client.emojis if names.name==emoji_name][number]
            webhook=await ctx.channel.create_webhook(name=ctx.author.name)
            await webhook.send(emoji, username=ctx.author.name, avatar_url=ctx.author.avatar_url)
            webhooks = await ctx.channel.webhooks()
            for webhook in webhooks:
                await webhook.delete()
            
        else:
            await ctx.send(embed=discord.Embed(description="The emoji is not available",color=discord.Color(value=re[8])))

    @client.command()
    async def set_sessionid(ctx, sessionid):
        re[9]=sessionid
        await ctx.send(embed=discord.Embed(description="SessionID set",color=discord.Color(re[8])))

    @client.command()
    async def instagram(ctx, account):
        if True:
            a=instagram_get(account,re[8],re[9])
            if a is not None and type(a)!=type("aa"):                
                await ctx.send(embed=a[0])
            elif type(a)!=type("aa"):
                re[9]=a
            else:
                await ctx.send(embed=discord.Embed(description="Oops!, something is wrong.",color=discord.Color(value=re[8])))
    
    @client.command()
    async def set_quality(ctx,number):
        if str(ctx.author.id) in dev_users:
            ydl_op['preferredquality']=str(number)
            await ctx.send(embed=discord.Embed(title="Done", description="Bitrate set to "+number,color=discord.Color(value=re[8])))
        else:
            await ctx.send(embed=discord.Embed(title="Permission Denied", description="You cant set the bitrate of the voice, only devs are allowed to do that",color=discord.Color(value=re[8])))
    @client.command(aliases=['cw'])
    async def clear_webhooks(ctx):
        webhooks = await ctx.channel.webhooks()
        print(webhooks)
        for webhook in webhooks:
            try:
                await webhook.delete()
            except Exception as e:
                print(e)
    @client.command()
    async def show_webhooks(ctx):
        webhooks = await ctx.channel.webhooks()
        await ctx.send(str(webhooks))
        
    @client.command(aliases=['color','||'])    
    async def theme_color(ctx,*,tup1):
        try:
            global color_temp
            req()
            try:
                color_temp=(int("0x"+str(hex(re[8]))[2:4],16),int("0x"+ str(hex(re[8]))[4:6],16),int("0x"+str(hex(re[8]))[6:8],16))
            except:
                pass
            print("Theme color",str(ctx.author))
            if re[8]<1000:
                re[8]=1670655
            global color_message
            tup=eval(tup1)
            if len(tup)<3:
                color_message=await ctx.send(embed=discord.Embed(title="Color Init",description="You must have three values in the form of tuple",color=discord.Color(value=re[8])))
                await color_message.add_reaction(emoji.emojize(":red_triangle_pointed_up:"))
                await color_message.add_reaction(emoji.emojize(":red_triangle_pointed_down:"))
                await color_message.add_reaction(discord.utils.get(client.emojis,name="green_up"))
                await color_message.add_reaction(discord.utils.get(client.emojis,name="green_down"))
                await color_message.add_reaction(discord.utils.get(client.emojis,name="blue_up"))
                await color_message.add_reaction(discord.utils.get(client.emojis,name="blue_down"))
            else:
                color_temp=tup
                re[8]=discord.Color.from_rgb(int(tup[0]),int(tup[1]),int(tup[2])).value
                embed=discord.Embed(title="New Color",description=str(tup),color=discord.Color(value=re[8]))
                await color_message.edit(embed=embed)
        except Exception as e:
            await client.get_channel(dev_channel).send(embed=discord.Embed(title="Error in Theme_Color",description=str(e),color=discord.Color(value=re[8])))
            
            
    @client.command(aliases=['$$'])
    async def recover(ctx):
        print("Recover",str(ctx.author))
        try:
            load_from_file(".recover.txt")
        except Exception as e:
            channel = client.get_channel(dev_channel)
            await channel.send(embed=discord.Embed(title="Recovery failed", description=str(e), color=discord.Color(value=re[8])))

    

    @client.command()
    async def load(ctx):
        print("Load",str(ctx.author))
        req()
        try:
            cpu_per=str(int(psutil.cpu_percent()))
            cpu_freq=str(int(psutil.cpu_freq().current))+"/"+str(int(psutil.cpu_freq().max))
            ram=str(psutil.virtual_memory().percent)
            swap=str(psutil.swap_memory().percent)
            usage="CPU Percentage: "+cpu_per+"%\nCPU Frequency: "+cpu_freq+"\nRAM Usage: "+ram+"%\nSwap Usage: "+swap+"%"
            embed=discord.Embed(title="Current load",description=usage,color=discord.Color(value=re[8]))
            embed.set_thumbnail(url=client.user.avatar_url_as(format="png"))
            await ctx.send(embed=embed)
        except Exception as e:
            channel = client.get_channel(dev_channel)
            embed=discord.Embed(title="Load failed", description=str(e), color=discord.Color(value=re[8]))
            embed.set_thumbnail(url=client.user.avatar_url_as(format="png"))
            await channel.send(embed=embed)
            
    @slash.slash(name="pr",description="Prints what you ask it to print")
    async def pr_slash(ctx,text):
        req()
        await ctx.send(text)
        
    @client.command(aliases=['say'])
    async def pr(ctx,*,text):
        req()
        await ctx.send(text)

    @slash.slash(name="reddit",description="Gives you a random reddit post from the account you specify")
    async def reddit_slash(ctx,account="wholesomememes"):
        req()
        try:
            await ctx.defer()
            await reddit_search(ctx,account)
        except:
            await ctx.send(embed=cembed(title="Oops", description="Something went wrong",color=re[8]))
    @client.command(aliases=['reddit'])
    async def reddit_search(ctx,account="wholesomememes", show_as_list="",number=1):
        req()
        description=""
        if number==1:
            a=reddit(account)[0]
            if len(a)<3:
                await ctx.send(embed=cembed(title=a[0],color=re[8],picture=a[1]))
            else:
                await ctx.send(embed=cembed(title=a[0],color=re[8],description=a[1]))
        
                
        
        
    @client.command(aliases=['l'])
    async def lyrics(ctx,*,string=""):
        print("Lyrics",str(ctx.author))
        try:
            req()
            print(string)
            search_url=""
            url=""
            if True:
                if len(string)==0:
                    search_url=("https://search.azlyrics.com/search.php?q="+(str(da1[queue_song[str(ctx.guild.id)][re[3][str(ctx.guild.id)]]]).replace(" ","+")))
                    print(search_url)
                else:
                    search_url=("https://search.azlyrics.com/search.php?q="+string.replace(" ","+"))
                    print(search_url)
                html_code=urllib.request.urlopen(search_url).read().decode()
                pos_1=html_code.find('text-left visitedlyr')
                pos_2=int(int(html_code.find('href="',pos_1))+len('href="'))
                pos_3=html_code.find('"',pos_2)
                url=html_code[pos_2:pos_3]
                if len(url)>3:
                    lyri=urllib.request.urlopen(url).read().decode()
                    lyri1=lyri[int(lyri.find("Sorry about that. -->")+len("Sorry about that. -->")):lyri.find("</div>",(int(lyri.find("Sorry about that. -->")+10)))].replace("<br>","").replace("<i>","_").replace("</i>","_")
                    title_of_song=lyri[lyri.find("<title>")+len("<title>"):lyri.find("</title>")]+"\n"
                    if len(lyri)<=1900:
                        await ctx.send(embed=discord.Embed(title="**Lyrics**",description=("**"+title_of_song+"**"+lyri1.replace('&quot;','"')),color=discord.Color(value=re[8])))
                    else:
                        await ctx.send(embed=discord.Embed(title="**Lyrics**",description=("**"+title_of_song+"**"+lyri1[0:1900]),color=discord.Color(value=re[8])))
                        await ctx.send(embed=discord.Embed(title="Continuation",description=("**"+title_of_song+"**"+lyri1[1900:]),color=discord.Color(value=re[8])))
                else:
                    await ctx.send(embed=discord.Embed(title="Not Found",description="Song not found, try lyrics <song name> to search properly",color=discord.Color(value=re[8])))
            else:
                await ctx.send(embed=discord.Embed(title="Hmm",description="Enter the voice channel to use this function",color=discord.Color(value=re[8])))
        except Exception as e:
            channel = client.get_channel(dev_channel)
            await ctx.send(embed=discord.Embed(title="Unavailable",description="Couldnt find lyrics",color=discord.Color(value=re[8])))
            await channel.send(embed=discord.Embed(title="Lyrics failed", description=str(e), color=discord.Color(value=re[8])))

    @client.command(aliases=['c'])
    async def cover_up(ctx):
        await ctx.message.delete()
        await asyncio.sleep(0.5)
        mess=await ctx.send(discord.utils.get(client.emojis,name="enrique"))
        await mess.delete()
        
    @client.command()
    async def remove_dev(ctx,member:discord.Member):
        print(member)
        global dev_users
        if str(ctx.author.id)=="432801163126243328":
            dev_users.remove(str(member.id))
            await ctx.send(member.mention+" is no longer a dev")
        else:
            await ctx.send(embed=discord.Embed(title="Permission Denied", description="Dude! You are not Alvin",color=discord.Color(value=re[8])))
    @client.command()
    async def add_dev(ctx,member:discord.Member):
        print(member)
        print("Add dev",str(ctx.author))
        global dev_users
        if str(ctx.author.id) in dev_users:
            dev_users=dev_users+[str(member.id)]
            await ctx.send(member.mention+" is a dev now")
        else:
            await ctx.send(embed=discord.Embed(title="Permission Denied", description="Dude! you are not a dev",color=discord.Color(value=re[8])))
    @client.command(aliases=['script'])
    async def add_access_to_script(ctx,member:discord.Member,ti="5"):
        global dev_users
        if str(ctx.author.id) in dev_users:
            mess=await ctx.send(embed=discord.Embed(title="Done",description=str(ctx.author.mention)+" gave script access to "+str(member.mention)+"\nTime remaining: "+str(int(ti)*60)+"s",color=discord.Color(value=re[8])))
            temp_dev[member.id]=[int(ti)*60,mess]
        else:
            await ctx.send(embed=discord.Embed(title="Access Denied", description="Only Developers can give temporary access",color=discord.Color.from_rgb(250,30,0)))
    @client.command(aliases=['remscript'])
    async def remove_access_to_script(ctx,member:discord.Member):
        if str(ctx.author.id) in dev_users:
            await ctx.send(embed=discord.Embed(title="Removed Access",description=str(ctx.author.mention)+" removed access from "+str(member.mention),color=discord.Color(value=re[8])))
            temp_dev.pop(member.id)
        else:
            await ctx.send(embed=discord.Embed(title="Access Denied", description="Only Developers can remove temporary access",color=discord.Color.from_rgb(250,30,0)))
    @client.command()
    async def dev_op(ctx):
        print("devop",str(ctx.author))
        channel = client.get_channel(dev_channel)
        await channel.purge(limit=10000000000000000000)
        text_dev="You get to activate and reset certain functions in this channel \n" \
        ""+(emoji.emojize(":safety_vest:"))+" for recovery \n"  \
        "⭕ for list of all servers \n" \
        "❌ for exiting \n" \
        "🔥 for restart\n" \
        "📊 for current load\n" \
        "❕ for current issues\n" \
        ""+emoji.emojize(":satellite:")+" for speedtest\n" \
        ""+emoji.emojize(":black_circle:")+" for clear screen\n" \
        ""+emoji.emojize(":classical_building: for starting Storage bot\n")+""
        embed=discord.Embed(title="DEVOP",description=text_dev,color=discord.Color(value=re[8]))
        embed.set_thumbnail(url=client.user.avatar_url_as(format="png"))
        mess=await channel.send(embed=embed)
        await mess.add_reaction(emoji.emojize(":safety_vest:"))
        await mess.add_reaction("⭕")
        await mess.add_reaction("❌")
        await mess.add_reaction(emoji.emojize(":fire:"))
        await mess.add_reaction(emoji.emojize(":bar_chart:"))
        await mess.add_reaction("❕")
        await mess.add_reaction(emoji.emojize(":satellite:"))
        await mess.add_reaction(emoji.emojize(":black_circle:"))
        await mess.add_reaction(emoji.emojize(":classical_building:"))
        await mess.add_reaction(emoji.emojize(":laptop:"))
        
    @client.command()
    async def reset_from_backup(ctx):
        print("reset_from_backup",str(ctx.author))
        channel = client.get_channel(dev_channel)
        try:
            load_from_file()
            await ctx.send(embed=discord.Embed(title="Done",description="Reset from backup: done",color=discord.Color(value=re[8])))
            await channel.send(embed=discord.Embed(title="Done",description="Reset from backup: done\nBy: "+str(ctx.author),color=discord.Color(value=re[8])))
        except Exception as e:
            await channel.send(embed=discord.Embed(title="Reset_from_backup failed", description=str(e), color=discord.Color(value=re[8])))

    
    @client.command()    
    async def entrar(ctx,*,num=re[6]):
        print("Entrar",str(ctx.author))
        global re
        re[0]=re[0]+1
        lol=""
        header={'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36','referer':"https://entrar.in"}
        suvzsjv={
            'username': os.getenv('sjdoskenv'),
            'password': os.getenv('sjdoskenv1'),
            'captcha':'0'
            }
        announcement_data={
            'announcementlist': 'true',
            'session': '205'
            }
        re[6]=num
        announcement_data['session']=str(num)
        #class="label-input100"
        try:
            with requests.Session() as s:
                scraper=cloudscraper.create_scraper(sess=s)
                r=scraper.get("https://entrar.in/login/login",headers=header)
                st=r.content.decode()
                start_captcha=st.find('<span class="label-input100" style="font-size: 18px;">')+len('<span class="label-input100" style="font-size: 20px;">')
                end_captcha=st.find("=",start_captcha)
                suvzsjv['captcha']=str(eval(st[start_captcha:end_captcha]))
                url="https://entrar.in/login/auth/"
                r=scraper.post(url,data=suvzsjv,headers=header)
                r=scraper.get("https://entrar.in/",headers=header)
                r=scraper.post("https://entrar.in/parent_portal/announcement",headers=header)
                r=scraper.get("https://entrar.in/parent_portal/announcement",headers=header)
                time.sleep(1)
                r=scraper.post("https://entrar.in/parent_portal/announcement",data=announcement_data,headers=header)
                
                channel = discord.utils.get(ctx.guild.channels, name="announcement")
                if ctx.guild.id==727061931373887531:
                    channel = discord.utils.get(ctx.guild.channels, name="bot")
                elif ctx.guild.id==743323684705402951:
                    channel=client.get_channel(868085346867490866)
                st=r.content.decode()
                for i in range(1,5):
                    a=st.find('<td class="text-wrap">'+str(i)+'</td>')
                    b=st.find('<td class="text-wrap">'+str(i+1)+'</td>')
                    le=len('<td class="text-wrap">'+str(i+1)+'</td>')-1
                    if b==-1:
                        await ctx.send(embed=discord.Embed(title="End Of List",description="",color=discord.Color(value=re[8])))
                        break
                    c=st.find('&nbsp;&nbsp; ',a,b)+len("&nbsp;&nbsp; ")
                    d=st.find('<',c,b)
                    out=st[c:d].strip()
                    e=a+le
                    f=st.find('<td>',e,e+15)+len('<td>')
                    g=st.find('</td>',e,e+45)
                    date=st[f:g]
                    h=st.find('<a target="_blank" href="',a,b)+len('<a target="_blank" href="')
                    j=st.find('"',h,b)
                    try:
                        link=str(st[h:j])
                        if link=='id="simpletable" class="table table-striped table-bordered nowrap':
                            continue
                        req=scraper.get(link)
                        k=out+date
                        if not str(ctx.guild.id) in entr:
                            entr[str(ctx.guild.id)]=[]
                        if k in entr[str(ctx.guild.id)]:
                            continue
                        entr[str(ctx.guild.id)].append(str(k))
                        lol=lol+out+" Date:"+date+"\n"
                        with open((out+".pdf"),'wb') as pdf:
                            pdf.write(req.content)
                            await channel.send(file=discord.File(out+".pdf"))
                            pdf.close()
                        os.remove(out+".pdf")
                    except Exception as e:
                        print(e)
                if lol!="":
                    embed=discord.Embed(title="New announcements",description=lol,color=discord.Color(value=re[8]))
                    embed.set_thumbnail(url="https://entrar.in/logo_dir/entrar_white.png")
                    await channel.send(embed=embed)
                    await ctx.send("Done")
                else:
                    await channel.send(embed=discord.Embed(title="Empty",description="No new announcement",color=discord.Color(value=re[8])))
                    await ctx.send("Done")
        except Exception as e:
            await ctx.send(embed=cembed(title="Oops", description="Something went wrong\n"+str(e),color=re[8],thumbnail="https://entrar.in/logo_dir/entrar_white.png"))
            

    @slash.slash(name="entrar", description="Latest announcements from Entrar")
    async def yentrar(ctx,*,num=re[6]):
        await ctx.defer()
        await entrar(ctx)        
    

    @client.command()
    async def docs(ctx,name):
        try:
            if name.find("(")==-1:
                await ctx.send(embed=discord.Embed(title="Docs",description=str(eval(name+".__doc__")),color=discord.Color(value=re[8])))
            else:
                await ctx.send(embed=discord.Embed(title="Permissions Denied", description="Functions are not allowed. Try without the brackets to get the information",color=discord.Color(value=re[8])))
        except Exception as e:
            await ctx.send(embed=discord.Embed(title="Error", description=str(e),color=discord.Color(value=re[8])))

    


    @client.command(aliases=[';'])
    async def mysql(ctx,*,text):
        print("MySQL",str(ctx.author))
        if str(ctx.author.guild.id)!="727061931373887531":
            if (text.lower().find("create user")!=-1 and text.lower().find("create database")!=-1 and text.lower().find("use mysql")!=-1 and text.lower().find("user")!=-1) or (str(ctx.author.id) in dev_users and ctx.guild.id==822445271019421746) or (str(ctx.author.id) in dev_users):
                output=""
                global cursor
                try:
                    cursor.execute(text)
                    for i in cursor:
                        output=output+str(i)+"\n"
                    md.commit()
                    embed=discord.Embed(title="MySQL", description=output,color=discord.Color(value=re[8]))
                    embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/b/b2/Database-mysql.svg/1200px-Database-mysql.svg.png")
                    await ctx.send(embed=embed)
                except Exception as e:
                    await ctx.send(embed=discord.Embed(title="Error", description=str(e),color=discord.Color(value=re[8])))
            else:
                await ctx.send(embed=discord.Embed(title="Permission Denied",description="",color=discord.Color(value=re[8])))
        else:
            await ctx.send(embed=discord.Embed(title="Disabled",description="You've disabled MySQL",color=discord.Color(value=re[8])))

    @slash.slash(name="Snipe",description="Get the last few deleted messages")
    async def snipe_slash(ctx,number=0):
        req()
        await ctx.defer()
        await snipe(ctx,number)
        
    @client.command()
    async def snipe(ctx,number=0):
        if number==0:
            message=deleted_message[ctx.channel.id][-1]
            if len(message)<3:
                await ctx.send("**"+message[0]+":**\n```"+message[1]+"```")
            else:
                await ctx.send("**"+message[0]+":**")                    
                await ctx.send(embed=message[1])
        else:
            nu=0
            for i in deleted_message[ctx.channel.id][::-1]:
                nu+=1
                if len(i)<3:
                    await ctx.send("**"+i[0]+":**\n"+i[1])
                else:
                    await ctx.send("**"+i[0]+":**")                    
                    await ctx.send(embed=i[1])
                if nu==number:
                    break
            if num==0:
                await ctx.send(embed=cembed(title="Oops", description="Oops sorry, I fell asleep ig, or idk",color=re[8],thumbnail=client.user.avatar_url_as(format="png")))
            
    @client.event
    async def on_message_delete(message):        
        if not message.channel.id in list(deleted_message.keys()):
            deleted_message[message.channel.id]=[]
        if len(message.embeds)<=0:
            deleted_message[message.channel.id].append((str(message.author),message.content))
        else:
            deleted_message[message.channel.id].append((str(message.author),message.embeds[0],True))

    @client.event
    async def on_member_join(member):
        channel=discord.utils.get(member.guild.channels, name="announcement")
        print(member.guild)
        if member.guild.id==841026124174983188:
            channel=client.get_channel(841026124174983193)        
        await channel.send(member.mention+" is here")
        embed=discord.Embed(title="Welcome!!!", description="Welcome to the server, "+member.name,color=discord.Color(value=re[8]))
        embed.set_thumbnail(url="https://image.shutterstock.com/image-vector/welcome-poster-spectrum-brush-strokes-260nw-1146069941.jpg")
        await channel.send(embed=embed)
        
    @client.event
    async def on_member_remove(member):
        if member.guild.id==743323684705402951:
            channel=client.get_channel(849215252280770580)
        elif member.guild.id==841026124174983188:
            channel=client.get_channel(841026124174983193)
        else:            
            channel=discord.utils.get(member.guild.channels, name="announcement")        
        
        await channel.send(member.mention+" is no longer here")
        embed=discord.Embed(title="Bye!!!", description="Hope you enjoyed your stay "+member.name,color=discord.Color(value=re[8]))
        embed.set_thumbnail(url="https://thumbs.dreamstime.com/b/bye-bye-man-says-45256525.jpg")
        await channel.send(embed=embed)
    @client.command(aliases=['fun'])
    async def games(ctx,game="",choice="bot"):
        if game=="XO":
            if choice=="bot":
                if client.user != ctx.author:
                    global available
                    global sent
                    if True:
                      board=reset_board()
                      available = Emoji_list.copy()
                      sent = await ctx.send(embed=discord.Embed(title="Tic Tac Toe by Rahul",description=board,color=discord.Color(value=re[8])))
                      for each in Emoji_list:
                        await sent.add_reaction(emoji.emojize(each))
        elif game=="Toss":
            if choice=="bot":
                if client.user!=ctx.author:
                    global coin_toss_message, coin_message
                    coin_toss_message=await ctx.send(embed=discord.Embed(title="Coin Toss by Alvin", description=coin_message,color=discord.Color(value=re[8])))
                    await coin_toss_message.add_reaction(emoji.emojize(":face_with_head-bandage:"))
                    await coin_toss_message.add_reaction(emoji.emojize(":hibiscus:"))
        else:
            await ctx.send(embed=discord.Embed(title="Games", description="1. TicTacToe(XO)\n2. Coin Toss(Toss)\n\nEnter the keyword given in the brackets after 'games",color=discord.Color(value=re[8])))
    @slash.slash(name="connect",description="Connect to a voice channel")
    async def connect_slash(ctx,channel=""):
        req()
        await ctx.defer()
        await connect_music(ctx,channel)
        
    @client.command(aliases=['cm'])
    async def connect_music(ctx,channel=""):
        print("Connect music",str(ctx.author))
        try:
            req()
            if not str(ctx.guild.id) in queue_song:
                queue_song[str(ctx.guild.id)]=[]
            if not str(ctx.guild.id) in re[3]:
                re[3][str(ctx.guild.id)]=0
            if channel=="":
                if ctx.author.voice and ctx.author.voice.channel:
                    channel=ctx.author.voice.channel.id
                    vc_channel[str(ctx.guild.id)]=channel
                    voiceChannel=discord.utils.get(ctx.guild.voice_channels,id=channel)
                    await voiceChannel.connect()
                    voice=discord.utils.get(client.voice_clients,guild=ctx.guild)
                    await ctx.send(embed=discord.Embed(title="",description="Connected\nBitrate of the channel: "+str(ctx.voice_client.channel.bitrate//1000),color=discord.Color(value=re[8])))
                else:
                    await ctx.send(embed=discord.Embed(title="",description="You are not in a voice channel",color=discord.Color(value=re[8])))
            else:
                if channel in [i.name for i in ctx.guild.voice_channels]:                    
                    voiceChannel=discord.utils.get(ctx.guild.voice_channels,name=channel)
                    vc_channel[str(ctx.guild.id)]=voiceChannel.id
                    await voiceChannel.connect()
                    voice=discord.utils.get(client.voice_clients,guild=ctx.guild)
                    await ctx.send(embed=discord.Embed(title="",description="Connected\nBitrate of the channel: "+str(ctx.voice_client.channel.bitrate//1000),color=discord.Color(value=re[8])))
                else:
                    await ctx.send(embed=discord.Embed(title="",description="The voice channel does not exist",color=discord.Color(value=re[8])))

        except Exception as e:
            await ctx.send(embed=discord.Embed(title="Hmm",description=str(e),color=discord.Color(value=re[8])))
            channel=client.get_channel(dev_channel)
            await channel.send(embed=discord.Embed(title="Connect music",description=str(e)+"\n"+str(ctx.guild.name)+": "+str(ctx.channel.name),color=discord.Color(value=re[8])))
    @client.command()
    async def addto(ctx,mode,*,text):
        req()
        present=1
        voiceChannel=discord.utils.get(ctx.guild.voice_channels,id=vc_channel[str(ctx.guild.id)])
        member=voiceChannel.members
        for mem in member:
            if str(ctx.author)==str(mem):
                present=0
                break
        if mode=="playlist" and present==0:
            addt(text,queue_song[str(ctx.guild.id)].copy())
            await ctx.send("Done")
        elif mode=="queue" and present==0:
            print(len(get_elem(str(text))))
            song_list=""
            for i in range(0,len(get_elem(str(text)))):
                link_add=get_elem(str(text))[i]
                queue_song[str(ctx.guild.id)].append(link_add)
            await ctx.send(embed=discord.Embed(title="Songs added",description="Done",color=discord.Color(value=re[8])))
        else:
            if present==0:
                await ctx.send("Only playlist and queue")
            else:
                await ctx.send(embed=discord.Embed(title="Permission denied",description="Join the voice channel to modify queue",color=discord.Color(value=re[8])))
    @client.command(aliases=['cq'])
    async def clearqueue(ctx):
        req()
        mem=[(str(i.name)+"#"+str(i.discriminator)) for i in discord.utils.get(ctx.guild.voice_channels,id=vc_channel[str(ctx.guild.id)]).members]
        if mem.count(str(ctx.author))>0:
            if len(queue_song[str(ctx.guild.id)])>0:
                queue_song[str(ctx.guild.id)].clear()
            re[3][str(ctx.guild.id)]=0
            await ctx.send(embed=discord.Embed(title="Cleared queue",description="_Done_",color=discord.Color(value=re[8])))
        else:
            await ctx.send(embed=discord.Embed(title="Permission denied",description="Join the voice channel to modify queue",color=discord.Color(value=re[8])))
    @client.command()
    async def remove(ctx,n):
        req()
        mem=[(str(i.name)+"#"+str(i.discriminator)) for i in discord.utils.get(ctx.guild.voice_channels,id=vc_channel[str(ctx.guild.id)]).members]
        if mem.count(str(ctx.author))>0:
            if int(n)<len(queue_song[str(ctx.guild.id)]):
                await ctx.send(embed=discord.Embed(title="Removed",description=da1[queue_song[str(ctx.guild.id)][int(n)]],color=discord.Color(value=re[8])))
                del da1[queue_song[str(ctx.guild.id)][int(n)]]
                queue_song[str(ctx.guild.id)].pop(int(n))
            else:
                await ctx.send(embed=discord.Embed(title="Not removed", description="Only "+len(queue_song[str(ctx.guild.id)])+" song(s) in your queue",color=discord.Color(value=re[8])))
        else:
            await ctx.send(embed=discord.Embed(title="Permission denied",description="Join the voice channel to modify queue",color=discord.Color(value=re[8])))
    @client.command(aliases=['curr'])
    async def currentmusic(ctx):
        req()
        if len(queue_song[str(ctx.guild.id)])>0:
            description="[Current index: "+str(re[3][str(ctx.guild.id)])+"]("+queue_song[str(ctx.guild.id)][re[3][str(ctx.guild.id)]]+")\n"
            info=youtube_info(queue_song[str(ctx.guild.id)][re[3][str(ctx.guild.id)]])
            check="\n\nDescription: \n"+info['description']+"\n"
            if len(check)<3000 and len(check)>0:
                description+=check
            description+="\nDuration: "+str(info['duration']//60)+"min "+str(info['duration']%60)+"sec"+f"\n\n{info['view_count']} views\n{info['like_count']} :thumbsup:\n{info['dislike_count']} :thumbdown:"
            await ctx.send(embed=cembed(title=str(da1[queue_song[str(ctx.guild.id)][re[3][str(ctx.guild.id)]]]),description=description,color=re[8],thumbnail=info['thumbnail']))
        else:
            await ctx.send(embed=discord.Embed(title="Empty queue",description="Your queue is currently empty",color=discord.Color(value=re[8])))
    def repeat(ctx,voice):
        req()
        if not queue_song[str(ctx.guild.id)][re[3][str(ctx.guild.id)]] in da1.keys():
            aa=str(urllib.request.urlopen(queue_song[str(ctx.guild.id)][re[3][str(ctx.guild.id)]]).read().decode())
            starting=aa.find("<title>")+len("<title>")
            ending=aa.find("</title>")
            da1[queue_song[str(ctx.guild.id)][re[3][str(ctx.guild.id)]]]=aa[starting:ending].replace("&#39;","'").replace(" - YouTube","").replace("&amp;","&")
        time.sleep(1)
        if re[7]==1 and not voice.is_playing():
            re[3][str(ctx.guild.id)]+=1
            if re[3][str(ctx.guild.id)]>=len(queue_song[str(ctx.guild.id)]):
                re[3][str(ctx.guild.id)]=0
        if re[2]==1 or re[7]==1:                       
            if not voice.is_playing():
                URL=youtube_download(ctx,queue_song[str(ctx.guild.id)][re[3][str(ctx.guild.id)]])
                voice.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS),after=lambda e: repeat(ctx,voice))
                
    @slash.slash(name="autoplay",description="Plays the next song automatically if its turned on")
    async def autoplay_slash(ctx):
        req()
        await ctx.defer()
        await autoplay(ctx)

    @slash.slash(name="loop",description="Loops the same song")
    async def loop_slash(ctx):
        await ctx.defer()
        req()
        await loop(ctx)
            
    @client.command()
    async def autoplay(ctx):
        req()
        if ctx.author.id in [i.id for i in ctx.voice_client.channel.members]:
            st=""
            re[7]=re[7]*-1
            if re[7]==1:re[2]=-1
            if re[7]<0:st="Off"
            else:st="_On_"
            await ctx.send(embed=discord.Embed(title='Autoplay',description=st,color=discord.Color(value=re[8])))
        else:
            await ctx.send(embed=discord.Embed(title="Permissions Denied", description="You need to be in the voice channel to toggle autoplay",color=discord.Color(value=re[8])))
    @client.command()
    async def loop(ctx):
        req()
        if ctx.author.id in [i.id for i in ctx.voice_client.channel.members]:
            st=""
            re[2]=re[2]*-1
            if re[2]==1:re[7]=-1
            if re[2]<0:st="Off"
            else:st="_On_"
            await ctx.send(embed=discord.Embed(title="Loop",description=st,color=discord.Color(value=re[8])))
        else:
            await ctx.send(embed=discord.Embed(title="Permissions Denied", description="You need to be in the voice channel to toggle loop",color=discord.Color(value=re[8])))
    @client.command(aliases=['q'])
    async def queue(ctx,*,name=""):
        req()
        try:
            mem=[str(names) for names in ctx.voice_client.channel.members]
        except:
            mem=[]
        if mem.count(str(ctx.author))>0 and name!="":            
            name=name.replace(" ","+")
            sear="https://www.youtube.com/results?search_query="+name
            htm=urllib.request.urlopen(sear)
            video=regex.findall(r"watch\?v=(\S{11})",htm.read().decode())
            url="https://www.youtube.com/watch?v="+video[0]
                      
            st=""
            await ctx.send("Added to queue")
            num=0
            name_of_the_song=youtube_info(url)['title']
            print(name_of_the_song,":",url)
            da1[url]=name_of_the_song
            queue_song[str(ctx.guild.id)].append(url)
            for i in queue_song[str(ctx.guild.id)]:                
                if num>=len(queue_song[str(ctx.guild.id)])-10:
                    if not i in da1.keys():
                        da1[i]=youtube_info(i)['title']
                    st=st+str(num)+". "+da1[i].replace("&quot","'")+"\n"
                num+=1
            #st=st+str(num)+". "+da1[i]+"\n"
            if st=="":st="_Empty_"
            em=discord.Embed(title="Queue",description=st,color=discord.Color(value=re[8]))
            mess=await ctx.send(embed=em)
            await mess.add_reaction("⏮")
            await mess.add_reaction("⏸")
            await mess.add_reaction("▶")
            await mess.add_reaction("🔁")
            await mess.add_reaction("⏭")
            await mess.add_reaction("⏹")
            await mess.add_reaction(emoji.emojize(":keycap_*:"))
            await mess.add_reaction(emoji.emojize(":upwards_button:"))
            await mess.add_reaction(emoji.emojize(":downwards_button:"))
        elif name=="":
            num=0
            st=""            
            if len(queue_song[str(ctx.guild.id)])<30:
                for i in queue_song[str(ctx.guild.id)]:
                    if not i in da1.keys():
                        da1[i]=youtube_info(i)['title']
                    st=st+str(num)+". "+da1[i]+"\n"
                    num+=1
            else:
                adfg=0
                num=-1
                for i in queue_song[str(ctx.guild.id)]:
                    num+=1                    
                    try:
                        if re[3][str(ctx.guild.id)]<10:                            
                            if num<15:
                                if not i in da1.keys():
                                    da1[i]=youtube_info(i)['title']
                                st=st+str(num)+". "+da1[i]+"\n"
                        elif re[3][str(ctx.guild.id)]>(len(queue_song[str(ctx.guild.id)])-10):
                            if num>(len(queue_song[str(ctx.guild.id)])-15):
                                if not i in da1.keys():
                                    da1[i]=youtube_info(i)['title']
                                st=st+str(num)+". "+da1[i]+"\n"
                        else:
                            if num>re[3][str(ctx.guild.id)]-10 and num<re[3][str(ctx.guild.id)]+10:
                                if not i in da1.keys():
                                    da1[i]=youtube_info(i)['title']
                                st=st+str(num)+". "+da1[i]+"\n"
                    except Exception as e:
                        pass
                    
            if st=="":st="_Empty_"
            embed=discord.Embed(title="Queue",description=st,color=discord.Color(value=re[8]))
            embed.set_thumbnail(url=client.user.avatar_url_as(format="png"))
            mess=await ctx.send(embed=embed)
            await mess.add_reaction("⏮")
            await mess.add_reaction("⏸")
            await mess.add_reaction("▶")
            await mess.add_reaction("🔁")
            await mess.add_reaction("⏭")
            await mess.add_reaction("⏹")
            await mess.add_reaction(emoji.emojize(":keycap_*:"))
            await mess.add_reaction(emoji.emojize(":upwards_button:"))
            await mess.add_reaction(emoji.emojize(":downwards_button:"))
        else:
            await ctx.send(embed=discord.Embed(title="Permission denied",description="Join the voice channel to modify queue",color=discord.Color(value=re[8])))


    @client.command(aliases=['>'])
    async def next(ctx):
        req()
        try:
            try:
                mem=[str(names) for names in ctx.voice_client.channel.members]
            except:
                mem=[]
            if mem.count(str(ctx.author))>0:                
                re[3][str(ctx.guild.id)]+=1
                if re[3][str(ctx.guild.id)]>=len(queue_song[str(ctx.guild.id)]):
                    re[3][str(ctx.guild.id)]=len(queue_song[str(ctx.guild.id)])-1
                    await ctx.send(embed=discord.Embed(title="Last song",description="Only "+str(len(queue_song[str(ctx.guild.id)]))+" songs in your queue",color=discord.Color(value=re[8])))
                voice=discord.utils.get(client.voice_clients,guild=ctx.guild)                
                URL=youtube_download(ctx,queue_song[str(ctx.guild.id)][re[3][str(ctx.guild.id)]])
                await ctx.send(embed=discord.Embed(title="Playing",description=da1[queue_song[str(ctx.guild.id)][re[3][str(ctx.guild.id)]]],color=discord.Color(value=re[8])))
                voice.stop()
                voice.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS),after=lambda e: repeat(ctx,voice))    
            else:
                await ctx.send(embed=discord.Embed(title="Permission denied",description="Join the voice channel to move to the next song",color=discord.Color(value=re[8])))
        except Exception as e:
            channel=client.get_channel(dev_channel)
            await channel.send(embed=discord.Embed(title="Error in next function", description=str(e)+"\n"+str(ctx.guild)+": "+str(ctx.channel.name),color=discord.Color(value=re[8])))
    @client.command()
    async def set_profile(ctx,mode="k"):
        p=psutil.Process()
        if str(ctx.author.id) in dev_users:
            if mode=="single":
                p.cpu_affinity([3])
                await ctx.send(embed=discord.Embed(title="Single",description="Set to single CPU mode", color=discord.Color(value=re[8])))
            elif mode=="multi":
                p.cpu_affinity([])
                await ctx.send(embed=discord.Embed(title="Multi",description="Set to Multiple CPU mode", color=discord.Color(value=re[8])))
            else:
                p.cpu_affinity([])
                await ctx.send(embed=discord.Embed(title="Multi",description="Set to Multiple CPU mode", color=discord.Color(value=re[8])))
        else:
            await ctx.send(embed=discord.Embed(title="Oops",description="You need to be a developer to change", color=discord.Color(value=re[8])))

    @slash.slash(name="news",description="Latest news from a given subject")
    async def news_slash(ctx,*,subject="Technology"):
        req()
        await ctx.defer()
        await news(ctx,subject)
            
    @client.command()
    async def news(ctx,subject="Technology"):
        googlenews.get_news(subject)
        news_list=googlenews.get_texts()
        googlenews.clear()
        string=""
        for i in range(0,10):
            string=string+str(i)+". "+news_list[i]+"\n"
        await ctx.send(embed=cembed(title="News",description=string,color=re[8],thumbnail=client.user.avatar_url_as(format="png")))
        
    @client.command(aliases=['<'])
    async def previous(ctx):
        req()
        try:
            try:
                mem=[str(names) for names in ctx.voice_client.channel.members]
            except:
                mem=[]
            if mem.count(str(ctx.author))>0:                
                re[3][str(ctx.guild.id)]-=1
                if re[3][str(ctx.guild.id)]==-1:
                    re[3][str(ctx.guild.id)]=0
                    await ctx.send(embed=discord.Embed(title="First song",description="This is first in queue",color=discord.Color(value=re[8])))
                if not queue_song[str(ctx.guild.id)][re[3][str(ctx.guild.id)]] in da1.keys():
                        da1[queue_song[str(ctx.guild.id)][re[3][str(ctx.guild.id)]]]=youtube_info(queue_song[str(ctx.guild.id)][re[3][str(ctx.guild.id)]])['title']
                voice=discord.utils.get(client.voice_clients,guild=ctx.guild)
                URL=youtube_download(ctx,queue_song[str(ctx.guild.id)][re[3][str(ctx.guild.id)]])
                await ctx.send(embed=discord.Embed(title="Playing",description=da1[queue_song[str(ctx.guild.id)][re[3][str(ctx.guild.id)]]],color=discord.Color(value=re[8])))
                voice.stop()
                voice.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS),after=lambda e: repeat(ctx,voice))    
            else:
                await ctx.send(embed=discord.Embed(title="Permission denied",description="Join the voice channel to move to the previous song",color=discord.Color(value=re[8])))
        except Exception as e:
            channel=client.get_channel(dev_channel)
            await channel.send(embed=discord.Embed(title="Error in previous function", description=str(e)+"\n"+str(ctx.guild)+": "+str(ctx.channel.name),color=discord.Color(value=re[8])))

    @client.command(aliases=['dict'])
    async def dictionary(ctx,*,text):
        if True:
            data=eval(requests.get("https://api.dictionaryapi.dev/api/v2/entries/en/"+text.replace(" ","%20")).content.decode())
            if type(data)==type([]):
                data=data[0]
                word=data['word']
                description="**Here's What I found:**\n\n"
                if 'phonetics' in data.keys():
                    if 'text' in data['phonetics'][0]:
                        phonetics="**Phonetics:**\n"+data['phonetics'][0]['text']+"\n\n"
                        description+=phonetics
                if 'origin' in list(data.keys()):
                    origin="**Origin: **"+data['origin']+"\n\n"
                    description+=origin
                if 'meanings' in data.keys() and 'definitions' in data['meanings'][0]:
                    meanings=data['meanings'][0]['definitions'][0]
                    if 'definition' in list(meanings.keys()):
                        meaning="**Definition: **"+meanings['definition']+"\n\n"
                        description+=meaning
                    if 'example' in list(meanings.keys()):
                        example="**Example: **"+meanings['example']
                        description+=example
            else:
                word=data['title']
                description=data['message']
            
            await ctx.send(embed=cembed(title=word,description=description,color=re[8],thumbnail=client.user.avatar_url_as(format="png")))
        else:
            print(e)
            await ctx.send(embed=cembed(title="Oops",description="Something is wrong\n"+str(e),color=re[8],thumbnail=client.user.avatar_url_as(format="png")))
        
    @client.command(aliases=['s_q'])
    async def search_queue(ctx,part):
        st=""
        index=0
        found_songs=0
        for i in queue_song[str(ctx.guild.id)]:            
            if i in da1:
                found_songs+=1
                if da1[i].lower().find(part.lower())!=-1:                    
                    st+=str(index)+". "+da1[i]+"\n"
            index+=1
        if st=="":st="Not found"
        if len(queue_song[str(ctx.guild.id)])-found_songs>0:
            st+="\n\nWARNING: Some song names may not be loaded properly, this search may not be accurate"
            st+="\nSongs not found: "+str(len(queue_song[str(ctx.guild.id)])-found_songs)      
        await ctx.send(embed=cembed(title="Songs in queue",description=st,color=re[8],thumbnail=client.user.avatar_url_as(format="png")))

                
    @client.command(aliases=['p'])
    async def play(ctx,*,ind):
        req()
        if discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)==None and ctx.author.voice and ctx.author.voice.channel:
            if not str(ctx.guild.id) in queue_song:
                queue_song[str(ctx.guild.id)]=[]
            if not str(ctx.guild.id) in re[3]:
                re[3][str(ctx.guild.id)]=0
            channel=ctx.author.voice.channel.id
            vc_channel[str(ctx.guild.id)]=channel
            voiceChannel=discord.utils.get(ctx.guild.voice_channels,id=channel)
            await voiceChannel.connect()
        try:
            try:
                mem=[str(names) for names in ctx.voice_client.channel.members]
            except:
                mem=[]
            if mem.count(str(ctx.author))>0:
                if ind.isnumeric():
                    if int(ind)<len(queue_song[str(ctx.guild.id)]):
                        re[3][str(ctx.guild.id)]=int(ind)
                        voice=discord.utils.get(client.voice_clients,guild=ctx.guild)
                        URL=youtube_download(ctx,queue_song[str(ctx.guild.id)][re[3][str(ctx.guild.id)]])
                        if not queue_song[str(ctx.guild.id)][re[3][str(ctx.guild.id)]] in da1.keys():
                            da1[queue_song[str(ctx.guild.id)][re[3][str(ctx.guild.id)]]]=youtube_info(queue_song[str(ctx.guild.id)][re[3][str(ctx.guild.id)]])['title']
                        mess=await ctx.send(embed=discord.Embed(title="Playing",description=da1[queue_song[str(ctx.guild.id)][re[3][str(ctx.guild.id)]]],color=discord.Color(value=re[8])))
                        voice.stop()
                        voice.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS),after=lambda e: repeat(ctx,voice))    
                        await mess.add_reaction("⏮")
                        await mess.add_reaction("⏸")
                        await mess.add_reaction("▶")
                        await mess.add_reaction("🔁")
                        await mess.add_reaction("⏭")
                        await mess.add_reaction("⏹")
                        await mess.add_reaction(emoji.emojize(":keycap_*:"))
                        await mess.add_reaction(emoji.emojize(":upwards_button:"))
                        await mess.add_reaction(emoji.emojize(":downwards_button:"))
                    else:
                        embed=discord.Embed(title="Hmm", description=f"There are only {len(queue_song[str(ctx.guild.id)])} songs",color=discord.Color(value=re[8]))
                        await ctx.send(embed=embed)
                else:
                    name=ind
                    if name.find("rick")==-1:
                        voice=discord.utils.get(client.voice_clients,guild=ctx.guild)
                        voice.stop()                        
                        name=name.replace(" ","+")
                        htm=urllib.request.urlopen("https://www.youtube.com/results?search_query="+name)
                        video=regex.findall(r"watch\?v=(\S{11})",htm.read().decode())
                        url="https://www.youtube.com/watch?v="+video[0]
                        URL=youtube_download(ctx,url)
                        name_of_the_song=youtube_info(url)['title']
                        voice.stop()
                        voice.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
                        await ctx.send(embed=discord.Embed(title="Playing", description=name_of_the_song,color=discord.Color(value=re[8])))
                    else:
                        mess=await ctx.send(embed=discord.Embed(title="Playing", description="Rick Astley - Never Gonna Give You Up (Official Music Video) - YouTube :wink:", color=discord.Color(value=re[8])))

            else:
                await ctx.send(embed=discord.Embed(title="Permission denied",description="Join the voice channel to play the song",color=discord.Color(value=re[8])))
        except Exception as e:
            channel=client.get_channel(dev_channel)
            await channel.send(embed=discord.Embed(title="Error in play function", description=str(e)+"\n"+str(ctx.guild)+": "+str(ctx.channel.name),color=discord.Color(value=re[8])))
            
    @client.command()
    async def again(ctx):
        req()
        if discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)==None and ctx.author.voice and ctx.author.voice.channel:
            if not str(ctx.guild.id) in queue_song:
                queue_song[str(ctx.guild.id)]=[]
            if not str(ctx.guild.id) in re[3]:
                re[3][str(ctx.guild.id)]=0
            channel=ctx.author.voice.channel.id
            vc_channel[str(ctx.guild.id)]=channel
            voiceChannel=discord.utils.get(ctx.guild.voice_channels,id=channel)
            await voiceChannel.connect()
            try:
                try:
                    mem=[str(names) for names in ctx.voice_client.channel.members]
                except:
                    mem=[]
                if mem.count(str(ctx.author))>0:
                    voice=discord.utils.get(client.voice_clients,guild=ctx.guild)
                    bitrate="\nBitrate of the channel: "+str(ctx.voice_client.channel.bitrate//1000)
                    if not queue_song[str(ctx.guild.id)][re[3][str(ctx.guild.id)]] in da1.keys():
                        da1[queue_song[str(ctx.guild.id)][re[3][str(ctx.guild.id)]]]=youtube_info(queue_song[str(ctx.guild.id)][re[3][str(ctx.guild.id)]])['title']
                    mess=await ctx.send(embed=cembed(title="Playing",description=da1[queue_song[str(ctx.guild.id)][re[3][str(ctx.guild.id)]]]+bitrate,color=re[8],thumbnail=client.user.avatar_url_as(format="png")))
                    URL=youtube_download(ctx,queue_song[str(ctx.guild.id)][re[3][str(ctx.guild.id)]])
                    voice.stop()
                    voice.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS),after=lambda e: repeat(ctx,voice))    
                    await mess.add_reaction("⏮")
                    await mess.add_reaction("⏸")
                    await mess.add_reaction("▶")
                    await mess.add_reaction("🔁")
                    await mess.add_reaction("⏭")
                    await mess.add_reaction("⏹")
                    await mess.add_reaction(emoji.emojize(":keycap_*:"))
                    await mess.add_reaction(emoji.emojize(":upwards_button:"))
                    await mess.add_reaction(emoji.emojize(":downwards_button:"))
                else:
                    await ctx.send(embed=cembed(title="Permission denied",description="Join the voice channel to play the song",color=re[8],thumbnail=client.user.avatar_url_as(format="png")))
            except Exception as e:
                channel=client.get_channel(dev_channel)
                await ctx.send(embed=cembed(title="Error", description=str(e),color=re[8], thumbnail=client.user.avatar_url_as(format="png")))
                await channel.send(embed=discord.Embed(title="Error in play function", description=str(e)+"\n"+str(ctx.guild)+": "+str(ctx.channel.name),color=discord.Color(value=re[8])))

    @slash.slash(name="again",description="Repeat the song")
    async def again_slash(ctx):
        req()
        await ctx.defer()
        await again(ctx)

    @slash.slash(name="memes",description="Memes from Alfred yey")
    async def memes(ctx):
        req()
        await ctx.defer()
        await memes(ctx)
        
    @client.command(aliases=['::'])
    async def memes(ctx):
        global link_for_cats            
        if len(link_for_cats)==0:            
            try:
                safe_stop=0
                r=requests.get("https://bestlifeonline.com/funniest-cat-memes-ever/")
                string=str(r.content.decode())
                for i in range(0,94):
                    #https://bestlifeonline.com/funniest-cat-memes-ever/
                    n1=string.find("<h2",safe_stop+len("<h2"))
                    n3=string.find('<div class="number">',n1)+len('<div class="number">')
                    n4=string.find('</div>',n3)
                    n2=string.find("data-src=",n1)+len("data-src=")+1
                    n1=string.find('" ',n2)
                    safe_stop=n1
                    number=int(string[n3:n4])
                    if number>=97:
                        safe_stop=0
                    link_for_cats+=[string[n2:n1]]
                print("Finished meme")
                link_for_cats+=memes1()
                print("Finished meme1")
                link_for_cats+=memes2()
                print("Finished meme2")
                link_for_cats+=memes3()
                print("Finished meme3")
            except Exception as e:
                await channel.send(embed=cembed(title="Meme issues", description="Something went wrong during importing memes\n"+str(e),color=re[8],thumbnail=client.user.avatar_url_as(format="png")))
        await ctx.send(choice(link_for_cats))
        save_to_file()
    @client.command(aliases=['!'])
    async def restart_program(ctx,text):
        try:
            voice=discord.utils.get(client.voice_clients,guild=ctx.guild)
            voice.stop()
            await voice.disconnect()
        except:
            pass
        save_to_file()
        print("Restart")
        os.chdir(location_of_file)
        os.system("nohup python Discord.py &")        
        await ctx.send(embed=cembed(title="Restarted",description="The program finished restarting",color=re[8],thumbnail=client.user.avatar_url_as(format="png")))
        sys.exit()

    @slash.slash(name="dc",description="Disconnect the bot from your voice channel")
    async def leave_slash(ctx):
        req()
        await ctx.defer()
        await leave(ctx)

        
    @client.command(aliases=['dc'])
    async def leave(ctx):
        req()
        try:
            try:
                mem=[names.id for names in ctx.voice_client.channel.members]
            except:
                mem=[]
            if mem.count(ctx.author.id)>0:
                voice=ctx.guild.voice_client
                voice.stop()
                await voice.disconnect()
                await ctx.send(embed=discord.Embed(title="Disconnected",description="Bye",color=discord.Color(value=re[8])))
            else:
                await ctx.send(embed=discord.Embed(title="Permission denied",description="Nice try dude! Join the voice channel",color=discord.Color(value=re[8])))
        except Exception as e:
            await ctx.send(embed=discord.Embed(title="Hmm",description=str(e),color=discord.Color(value=re[8])))
            channel=client.get_channel(dev_channel)
            await channel.send(embed=discord.Embed(title="Error in leave",description=str(e)+"\n"+str(ctx.guild)+": "+str(ctx.channel.name),color=discord.Color(value=re[8])))
        save_to_file()
    @client.command()
    async def pause(ctx):
        req()
        try:
            mem=[str(names) for names in ctx.voice_client.channel.members]
        except:
            mem=[]
        if mem.count(str(ctx.author))>0:
            voice=discord.utils.get(client.voice_clients,guild=ctx.guild)
            voice.pause()
            await ctx.send(embed=discord.Embed(title="Pause",color=discord.Color(value=re[8])))
        else:
            await ctx.send(embed=discord.Embed(title="Permission denied",description="Join the channel to pause the song",color=discord.Color(value=re[8])))
    @client.command(aliases=['*'])
    async def change_nickname(ctx,member: discord.Member, *, nickname):
        if ctx.author.guild_permissions.change_nickname or ctx.author.id==432801163126243328:
            await member.edit(nick=nickname)
            await ctx.send(embed=discord.Embed(title="Nickname Changed", description=("Nickname changed to "+member.mention+" by "+ctx.author.mention),color=discord.Color(value=re[8])))
        else:
            await ctx.send(embed=discord.Embed(title="Permissions Denied", description="You dont have permission to change others nickname", color=discord.Color(value=re[8])))
    @client.command()
    async def resume(ctx):
        req()
        try:
            mem=[str(names) for names in ctx.voice_client.channel.members]
        except:
            mem=[]
        if mem.count(str(ctx.author))>0:
            voice=discord.utils.get(client.voice_clients,guild=ctx.guild)
            voice.resume()
            await ctx.send(embed=discord.Embed(title="Resume",color=discord.Color(value=re[8])))   
            
    @client.command()    
    async def clear(ctx,text,num=10):
    	req()
    	await ctx.channel.purge(limit=1)
    	if str(text)==re[1]:
    	    if ctx.author.guild_permissions.manage_messages or ctx.author.id==432801163126243328: await ctx.channel.purge(limit=num)
    	    else: await ctx.send(embed=discord.Embed(title="Permission Denied", description="You cant delete messages",color=discord.Color(value=re[8])))
    	else:
    	    await ctx.send("Wrong password")
    	    
    @slash.slash(name="wikipedia", description="Get a topic from wikipedia")
    async def wiki_slash(ctx,text):
        try:
            req()
            await ctx.defer()
            t=str(search(text)[0].encode("utf-8"))
            em=discord.Embed(title=str(t).title(),description=str(summary(t,sentences=5)),color=discord.Color(value=re[8]))
            em.set_thumbnail(url="https://1000logos.net/wp-content/uploads/2017/05/Wikipedia-logos.jpg")
            await ctx.send(embed=em)
        except Exception as e:
            await ctx.send(embed=cembed(title="Oops",description=str(e),color=re[8],thumbnail=client.user.avatar_url_as(format='png')))
    
    @client.command(aliases=['w'])
    async def wikipedia(ctx,*,text):
    	req()
    	t=str(search(text)[0].encode("utf-8"))
    	em=discord.Embed(title=str(t).title(),description=str(summary(t,sentences=5)),color=discord.Color(value=re[8]))
    	em.set_thumbnail(url="https://1000logos.net/wp-content/uploads/2017/05/Wikipedia-logos.jpg")
    	await ctx.send(embed=em)
    	
    @client.command(aliases=['hi'])
    async def check(ctx):
        req()
        print("check")
        em=discord.Embed(title="Online",description=("Hi, "+str(ctx.author)[0:str(ctx.author).find("#")])+"\nLatency: "+str(int(client.latency*1000)),color=discord.Color(value=re[8]))
        await ctx.send(embed=em)
    @slash.slash(name="check",description="Check if the bot is online")
    async def check_slash(ctx):
        req()
        await ctx.defer()
        await check(ctx)
    @client.command()
    async def test(ctx,*,text):
        mess=await ctx.send(embed=discord.Embed(title="This is a "+emoji.demojize(text).replace(":",""),color=discord.Color(value=re[8])))
        await mess.add_reaction("😎")
    @client.event
    async def on_reaction_add(reaction, user):
        req()
        try:
            if not user.bot:                
                global color_temp
                save_to_file()                
                global Emoji_list
                if reaction.emoji == emoji.emojize(":upwards_button:") and len(queue_song[str(reaction.message.guild.id)])>0 and reaction.message.author==client.user:
                    await reaction.remove(user)
                    if not reaction.message in list(pages.keys()):
                        pages[reaction.message]=0
                    else:
                        if pages[reaction.message]>0:
                            pages[reaction.message]-=1
                    st=""
                    for i in range(pages[reaction.message]*10,(pages[reaction.message]*10)+10):
                        try:
                            if not queue_song[str(reaction.message.guild.id)][i] in da1.keys():
                                da1[queue_song[str(reaction.message.guild.id)][i]]=youtube_info(queue_song[str(reaction.message.guild.id)][i])['title']
                            st=st+str(i)+". "+da1[queue_song[str(reaction.message.guild.id)][i]]+"\n"
                        except Exception as e:
                            print(e)
                    await reaction.message.edit(embed=discord.Embed(title="Queue", description=st, color=discord.Color(value=re[8])))
                if reaction.emoji == emoji.emojize(":downwards_button:") and len(queue_song[str(reaction.message.guild.id)])>0  and reaction.message.author==client.user:
                    await reaction.remove(user)
                    if not reaction.message in list(pages.keys()):
                        pages[reaction.message]=0
                    else:
                        if pages[reaction.message]*10<len(queue_song[str(reaction.message.guild.id)]):
                            pages[reaction.message]+=1
                        else:
                            pages[reaction.message]=len(queue_song[str(reaction.message.guild.id)])//10
                    st=""                    
                    for i in range(pages[reaction.message]*10,(pages[reaction.message]*10)+10):
                        try:
                            if not queue_song[str(reaction.message.guild.id)][i] in list(da1.keys()):
                                da1[queue_song[str(reaction.message.guild.id)][i]]=youtube_info(queue_song[str(reaction.message.guild.id)][i])['title']
                            st=st+str(i)+". "+da1[queue_song[str(reaction.message.guild.id)][i]]+"\n"
                        except Exception as e:
                            print(e)
                    if st=="":
                        st="End of queue"
                    await reaction.message.edit(embed=discord.Embed(title="Queue", description=st, color=discord.Color(value=re[8])))
                        
                if reaction.emoji in [emoji.emojize(":keycap_"+str(i)+":") for i in range(1,10)] and reaction.message.author.id==client.user.id:
                  global board, available, sent, dictionary
                  if user != client.user:
                    if sent.id == reaction.message.id:
                      if reaction.emoji in Emoji_list:
                        temp_number=0
                        for i in range(0,9):
                          if reaction.emoji==Emoji_list[i]:
                            temp_number=i
                            break
                        global board
                        board = board.replace(Raw_Emoji_list[temp_number], emoji.emojize(":cross_mark:"))
                        await sent.edit(embed=discord.Embed(title="Tic Tac Toe by Rahul",description=board,color=discord.Color(value=re[8])))
                        await reaction.remove(user)
                        await reaction.remove(client.user)
                        available.remove(emoji.emojize(":keycap_"+str(temp_number+1)+":"))
                        if len(available)==0:
                            result = " "
                            result = check_win(board)
                            if result!=" ":
                              await sent.edit(embed=discord.Embed(title="Tic Tac Toe by Rahul",description=result,color=discord.Color(value=re[8])))
                            else:
                                await sent.edit(embed=discord.Embed(title="Tic Tac Toe by Rahul",description="Draw",color=discord.Color(value=re[8])))
                        else:
                            comp_move = choice(available)
                            board = board.replace(comp_move, O)
                            await sent.edit(embed=discord.Embed(title="Tic Tac Toe by Rahul",description=board,color=discord.Color(value=re[8])))
                            await sent.remove_reaction(dictionary[comp_move], client.user)
                            available.remove(comp_move)
                            result = " "
                            result = check_win(board)
                            if result!=" ":
                                await sent.edit(embed=discord.Embed(title="Tic Tac Toe by Rahul",description=result,color=discord.Color(value=re[8])))
                if reaction.emoji==emoji.emojize(":musical_note:"):
                    await reaction.remove(user)
                    if len(queue_song[str(reaction.message.guild.id)])>0:
                        description="[Current index: "+str(re[3][str(reaction.message.guild.id)])+"]("+queue_song[str(reaction.message.guild.id)][re[3][str(reaction.message.guild.id)]]+")\n"
                        info=youtube_info(queue_song[str(reaction.message.guild.id)][re[3][str(reaction.message.guild.id)]])
                        check="\n\nDescription: \n"+info['description']+"\n"
                        if len(check)<3000 and len(check)>0:
                            description+=check
                        description+="\nDuration: "+str(info['duration']//60)+"min "+str(info['duration']%60)+"sec"+f"\n\n{info['view_count']} views\n{info['like_count']} :thumbsup:\n{info['dislike_count']} :thumbdown:"
                        await reaction.message.edit(embed=cembed(title=str(da1[queue_song[str(reaction.message.guild.id)][re[3][str(reaction.message.guild.id)]]]),description=description,color=re[8],thumbnail=info['thumbnail']))
                    else:
                        await reaction.message.edit(embed=discord.Embed(title="Empty queue",description="Your queue is currently empty",color=discord.Color(value=re[8])))
                if reaction.emoji==discord.utils.get(client.emojis,name="blue_down"):
                    if str(user)!=str(client.user) and reaction.message.author==client.user:
                        await reaction.remove(user)
                        temp_tup=color_temp
                        if temp_tup[2]-25>=0:
                            re[8]=discord.Color.from_rgb(int(temp_tup[0]),int(temp_tup[1]),int(temp_tup[2])-25).value
                            color_temp=(int(temp_tup[0]),int(temp_tup[1]),int(temp_tup[2])-25)
                        else:
                            re[8]=discord.Color.from_rgb(int(temp_tup[0]),int(temp_tup[1]),0).value
                            color_temp=(int(temp_tup[0]),int(temp_tup[1]),0)
                        embed=discord.Embed(title="New Color",description=str(color_temp),color=discord.Color(value=re[8]))
                        await color_message.edit(embed=embed)
                if reaction.emoji==discord.utils.get(client.emojis,name="green_down"):
                    if str(user)!=str(client.user) and reaction.message.author==client.user:
                        await reaction.remove(user)
                        temp_tup=color_temp
                        if temp_tup[1]-25>=0:
                            re[8]=discord.Color.from_rgb(int(temp_tup[0]),int(temp_tup[1]-25),int(temp_tup[2])).value
                            color_temp=(int(temp_tup[0]),int(temp_tup[1]-25),int(temp_tup[2]))
                        else:
                            re[8]=discord.Color.from_rgb(int(temp_tup[0]),0,int(temp_tup[2])).value
                            color_temp=(int(temp_tup[0]),0,int(temp_tup[2]))
                        embed=discord.Embed(title="New Color",description=str(color_temp),color=discord.Color(value=re[8]))
                        await color_message.edit(embed=embed)
                if reaction.emoji==emoji.emojize(":red_triangle_pointed_down:"):
                    if str(user)!=str(client.user) and reaction.message.author==client.user:
                        await reaction.remove(user)
                        temp_tup=color_temp
                        if temp_tup[0]-25>=0:
                            re[8]=discord.Color.from_rgb(int(temp_tup[0]-25),int(temp_tup[1]),int(temp_tup[2])).value
                            color_temp=(int(temp_tup[0]-25),int(temp_tup[1]),int(temp_tup[2]))
                        else:
                            re[8]=discord.Color.from_rgb(0,int(temp_tup[1]),int(temp_tup[2])).value
                            color_temp=(0,int(temp_tup[1]),int(temp_tup[2]))
                        embed=discord.Embed(title="New Color",description=str(color_temp),color=discord.Color(value=re[8]))
                        await color_message.edit(embed=embed)
                if reaction.emoji==discord.utils.get(client.emojis,name="blue_up"):
                    if str(user)!=str(client.user) and reaction.message.author==client.user:
                        await reaction.remove(user)
                        temp_tup=color_temp
                        if temp_tup[2]+25<=255:
                            re[8]=discord.Color.from_rgb(int(temp_tup[0]),int(temp_tup[1]),int(temp_tup[2])+25).value
                            color_temp=(int(temp_tup[0]),int(temp_tup[1]),int(temp_tup[2])+25)
                        else:
                            re[8]=discord.Color.from_rgb(int(temp_tup[0]),int(temp_tup[1]),255).value
                            color_temp=(int(temp_tup[0]),int(temp_tup[1]),255)
                        embed=discord.Embed(title="New Color",description=str(color_temp),color=discord.Color(value=re[8]))
                        await color_message.edit(embed=embed)
                if reaction.emoji==discord.utils.get(client.emojis,name="green_up"):
                    if str(user)!=str(client.user) and reaction.message.author==client.user:
                        await reaction.remove(user)
                        temp_tup=color_temp
                        if temp_tup[1]+25<=255:
                            re[8]=discord.Color.from_rgb(int(temp_tup[0]),int(temp_tup[1]+25),int(temp_tup[2])).value
                            color_temp=(int(temp_tup[0]),int(temp_tup[1]+25),int(temp_tup[2]))
                        else:
                            re[8]=discord.Color.from_rgb(int(temp_tup[0]),255,int(temp_tup[2])).value
                            color_temp=(int(temp_tup[0]),255,int(temp_tup[2]))
                        embed=discord.Embed(title="New Color",description=str(color_temp),color=discord.Color(value=re[8]))
                        await color_message.edit(embed=embed)
                if reaction.emoji==emoji.emojize(":red_triangle_pointed_up:"):
                    if str(user)!=str(client.user) and reaction.message.author==client.user:
                        await reaction.remove(user)
                        temp_tup=color_temp
                        if temp_tup[0]+25<=255:
                            re[8]=discord.Color.from_rgb(int(temp_tup[0]+25),int(temp_tup[1]),int(temp_tup[2])).value
                            color_temp=(int(temp_tup[0]+25),int(temp_tup[1]),int(temp_tup[2]))
                        else:
                            re[8]=discord.Color.from_rgb(255,int(temp_tup[1]),int(temp_tup[2])).value
                            color_temp=(255,int(temp_tup[1]),int(temp_tup[2]))
                        embed=discord.Embed(title="New Color",description=str(color_temp),color=discord.Color(value=re[8]))
                        await color_message.edit(embed=embed)
                if reaction.emoji=='⏮':
                    if str(user)!=str(client.user) and reaction.message.author==client.user:
                        await reaction.remove(user)
                        req()
                        try:
                            mem=[str(names) for names in reaction.message.guild.voice_client.channel.members]
                        except:
                            mem=[]
                        if mem.count(str(user))>0:
                            if not queue_song[str(reaction.message.guild.id)][re[3][str(reaction.message.guild.id)]] in da1.keys():
                                da1[queue_song[str(reaction.message.guild.id)][re[3][str(reaction.message.guild.id)]]]=youtube_info(queue_song[str(reaction.message.guild.id)][re[3][str(reaction.message.guild.id)]])['title']
                            re[3][str(reaction.message.guild.id)]-=1
                            if re[3][str(reaction.message.guild.id)]==-1:
                                re[3][str(reaction.message.guild.id)]=0
                            await reaction.message.edit(embed=discord.Embed(title="Downloading...",description="Downloading the song, please wait for a moment",color=discord.Color(value=re[8])))
                            voice=discord.utils.get(client.voice_clients,guild=reaction.message.guild)
                            URL=youtube_download(reaction.message,queue_song[str(reaction.message.guild.id)][re[3][str(reaction.message.guild.id)]])
                            voice.stop()
                            voice.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS),after=lambda e: repeat(reaction.message,voice))
                            url=queue_song[str(reaction.message.guild.id)][re[3][str(reaction.message.guild.id)]]
                            song_name=da1[url]
                            await reaction.message.edit(embed=discord.Embed(title="Playing",description=f"[{song_name}]({url})",color=discord.Color(value=re[8])))
                        else:
                            await reaction.message.edit(embed=discord.Embed(title="Permission denied",description=("You need to join the voice channel "+str(user.name)),color=discord.Color(value=re[8])))
                if reaction.emoji=='⏸':
                    if str(user)!=str(client.user) and reaction.message.author==client.user:
                        await reaction.remove(user)
                        req()
                        try:
                            mem=[str(names) for names in reaction.message.guild.voice_client.channel.members]
                        except:
                            mem=[]
                        if mem.count(str(user))>0:
                            voice=discord.utils.get(client.voice_clients,guild=reaction.message.guild)
                            url=queue_song[str(reaction.message.guild.id)][re[3][str(reaction.message.guild.id)]]
                            song_name=da1[url]
                            await reaction.message.edit(embed=discord.Embed(title="Paused",description=f"[{song_name}]({url})",color=discord.Color(value=re[8])))
                            voice.pause()
                if reaction.emoji=='▶':
                    if str(user)!=str(client.user) and reaction.message.author==client.user:
                        await reaction.remove(user)
                        req()
                        try:
                            mem=[str(names) for names in reaction.message.guild.voice_client.channel.members]
                        except:
                            mem=[]
                        if mem.count(str(user))>0:
                            voice=discord.utils.get(client.voice_clients,guild=reaction.message.guild)
                            if not queue_song[str(reaction.message.guild.id)][re[3][str(reaction.message.guild.id)]] in da1.keys():
                                da1[queue_song[str(reaction.message.guild.id)][re[3][str(reaction.message.guild.id)]]]=youtube_info(queue_song[str(reaction.message.guild.id)][re[3][str(reaction.message.guild.id)]])['title']
                            url=queue_song[str(reaction.message.guild.id)][re[3][str(reaction.message.guild.id)]]
                            song_name=da1[url]
                            await reaction.message.edit(embed=discord.Embed(title="Playing",description=f"[{song_name}]({url})",color=discord.Color(value=re[8])))
                            voice.resume()
                        else:
                            await reaction.message.edit(embed=discord.Embed(title="Permission denied",description=("You need to join the voice channel "+str(user.name)),color=discord.Color(value=re[8])))
                if reaction.emoji=='🔁':
                    if str(user)!=str(client.user) and reaction.message.author==client.user:
                        await reaction.remove(user)                        
                        try:
                            mem=[str(names) for names in reaction.message.guild.voice_client.channel.members]                           
                        except Exception as e:
                            mem=[]                            
                        if mem.count(str(user))>0:                            
                            voice=discord.utils.get(client.voice_clients,guild=reaction.message.guild)
                            URL=youtube_download(reaction.message,queue_song[str(reaction.message.guild.id)][re[3][str(reaction.message.guild.id)]])
                            voice.stop()
                            voice.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS),after=lambda e: repeat(reaction.message,voice))
                            if not queue_song[str(reaction.message.guild.id)][re[3][str(reaction.message.guild.id)]] in da1.keys():
                                da1[queue_song[str(reaction.message.guild.id)][re[3][str(reaction.message.guild.id)]]]=youtube_info(queue_song[str(reaction.message.guild.id)][re[3][str(reaction.message.guild.id)]])['title']
                            url=queue_song[str(reaction.message.guild.id)][re[3][str(reaction.message.guild.id)]]
                            song_name=da1[url]
                            await reaction.message.edit(embed=discord.Embed(title="Playing",description=f"[{song_name}]({url})",color=discord.Color(value=re[8])))
                        else:
                            await reaction.message.edit(embed=discord.Embed(title="Permission denied",description=("You need to join the voice channel "+str(user.name)),color=discord.Color(value=re[8])))
                if reaction.emoji=='⏭':
                    if str(user)!=str(client.user) and reaction.message.author==client.user:
                        await reaction.remove(user)
                        req()
                        try:
                            mem=[names.id for names in reaction.message.guild.voice_client.channel.members]
                        except:
                            mem=[]
                        if user.id in mem:                            
                            if not queue_song[str(reaction.message.guild.id)][re[3][str(reaction.message.guild.id)]] in da1.keys():
                                aa=str(urllib.request.urlopen(queue_song[str(reaction.message.guild.id)]).read().decode())
                                starting=aa.find("<title>")+len("<title>")
                                ending=aa.find("</title>")
                                da1[queue_song[str(reaction.message.guild.id)][re[3][str(reaction.message.guild.id)]]]=aa[starting:ending].replace("&#39;","'").replace(" - YouTube","").replace("&amp;","&")
                            re[3][str(reaction.message.guild.id)]+=1
                            if re[3][str(reaction.message.guild.id)]>=len(queue_song[str(reaction.message.guild.id)]):
                                re[3][str(reaction.message.guild.id)]-=1
                            await reaction.message.edit(embed=discord.Embed(title="Downloading...",description="Downloading the song, please wait for a moment",color=discord.Color(value=re[8])))
                            voice=discord.utils.get(client.voice_clients,guild=reaction.message.guild)
                            URL=youtube_download(reaction.message,queue_song[str(reaction.message.guild.id)][re[3][str(reaction.message.guild.id)]])
                            voice.stop()
                            voice.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS),after=lambda e: repeat(reaction.message,voice))
                            url=queue_song[str(reaction.message.guild.id)][re[3][str(reaction.message.guild.id)]]
                            song_name=da1[url]
                            await reaction.message.edit(embed=discord.Embed(title="Playing",description=f"[{song_name}]({url})",color=discord.Color(value=re[8])))
                        else:
                            await reaction.message.edit(embed=discord.Embed(title="Permission denied",description=("You need to join the voice channel "+str(user.name)),color=discord.Color(value=re[8])))
                if reaction.emoji=="⏹":
                    req()
                    if True:
                        if str(user)!=str(client.user) and reaction.message.author==client.user:
                            await reaction.remove(user)
                            try:
                                mem=[names.id for names in reaction.message.guild.voice_client.channel.members]
                            except:
                                mem=[]
                            if mem.count(user.id)>0:
                                voice=reaction.message.guild.voice_client
                                voice.stop()
                                await voice.disconnect()                                
                                await reaction.message.edit(embed=discord.Embed(title="Disconnected",description="Bye, Thank you for using Alfred",color=discord.Color(value=re[8])))
                            else:
                                await reaction.message.edit(embed=discord.Embed(title="Permission denied",description=("You need to join the voice channel "+str(user.name)),color=discord.Color(value=re[8])))
                if reaction.emoji==emoji.emojize(":keycap_*:") and reaction.message.author==client.user:
                    num=0
                    bitrate=""
                    length="\nLength of queue: "+str(len(queue_song[str(reaction.message.guild.id)]))
                    if reaction.message.guild.voice_client!=None:bitrate="\nBitrate of the channel: "+str(reaction.message.guild.voice_client.channel.bitrate//1000)
                    if str(user)!=str(client.user) and reaction.message.author==client.user:
                        st=""
                        await reaction.remove(user)
                        if len(queue_song[str(reaction.message.guild.id)])<27:
                            for i in queue_song[str(reaction.message.guild.id)]:
                                if not i in da1.keys():
                                    aa=str(urllib.request.urlopen(i).read().decode())
                                    starting=aa.find("<title>")+len("<title>")
                                    ending=aa.find("</title>")
                                    da1[i]=aa[starting:ending].replace("&#39;","'").replace(" - YouTube","").replace("&amp;","&")
                                st=st+str(num)+". "+da1[i]+"\n"
                                num+=1
                        else:
                            adfg=0
                            num=-1
                            for i in queue_song[str(reaction.message.guild.id)]:
                                num+=1                                
                                try:
                                    if re[3][str(reaction.message.guild.id)]<10:                            
                                        if num<15:
                                            if not i in da1.keys():
                                                aa=str(urllib.request.urlopen(i).read().decode())
                                                starting=aa.find("<title>")+len("<title>")
                                                ending=aa.find("</title>")
                                                da1[i]=aa[starting:ending].replace("&#39;","'").replace(" - YouTube","").replace("&amp;","&")
                                            st=st+str(num)+". "+da1[i]+"\n"
                                    elif re[3][str(reaction.message.guild.id)]>(len(queue_song[str(reaction.message.guild.id)])-10):
                                        if num>(len(queue_song[str(reaction.message.guild.id)])-15):
                                            if not i in da1.keys():
                                                aa=str(urllib.request.urlopen(i).read().decode())
                                                starting=aa.find("<title>")+len("<title>")
                                                ending=aa.find("</title>")
                                                da1[i]=aa[starting:ending].replace("&#39;","'").replace(" - YouTube","").replace("&amp;","&")
                                            st=st+str(num)+". "+da1[i]+"\n"
                                    else:
                                        if num>re[3][str(reaction.message.guild.id)]-10 and num<re[3][str(reaction.message.guild.id)]+10:
                                            if not i in da1.keys():
                                                aa=str(urllib.request.urlopen(i).read().decode())
                                                starting=aa.find("<title>")+len("<title>")
                                                ending=aa.find("</title>")
                                                da1[i]=aa[starting:ending].replace("&#39;","'").replace(" - YouTube","").replace("&amp;","&")
                                            st=st+str(num)+". "+da1[i]+"\n"
                                except Exception as e:
                                    pass
                        await reaction.message.edit(embed=discord.Embed(title="Queue",description=st+bitrate+length,color=discord.Color(value=re[8])))
                if str(user.id) in dev_users:
                    global dev_channel
                    channel=client.get_channel(dev_channel)
                    if reaction.emoji==emoji.emojize(":laptop:") and str(reaction.message.channel.id)==str(channel.id) and reaction.message.author==client.user:
                        string=""
                        await reaction.remove(user)
                        for i in dev_users:
                            string=string+str(client.get_user(int(i)).name)+"\n"
                        await channel.send(embed=discord.Embed(title="Developers",description=string+"\n\nThank you for supporting",color= discord.Color(value=re[8])))
                    if reaction.emoji==emoji.emojize(":classical_building:") and str(reaction.message.channel.id)==str(channel.id) and reaction.message.author==client.user:
                        os.system("nohup python "+location_of_file+"/Storage.py &> .storage.txt &")
                        await reaction.remove(user)
                        await channel.send(embed=discord.Embed(title="Storage",description="Requested Storage to wake up",color=client.discord.Color.from_rgb(255,255,255)))
                    if reaction.emoji==emoji.emojize(":bar_chart:") and str(reaction.message.channel.id)==str(channel.id):
                        await reaction.remove(user)
                        cpu_per=str(int(psutil.cpu_percent()))
                        cpu_freq=str(int(psutil.cpu_freq().current))+"/"+str(int(psutil.cpu_freq().max))
                        ram=str(psutil.virtual_memory().percent)
                        swap=str(psutil.swap_memory().percent)
                        usage="CPU Percentage: "+cpu_per+"%\nCPU Frequency: "+cpu_freq+"\nRAM Usage: "+ram+"%\nSwap Usage: "+swap+"%"
                        await channel.send(embed=discord.Embed(title="Load",description=usage,color=discord.Color(value=re[8])))
                    if reaction.emoji==emoji.emojize(":safety_vest:"):
                        await reaction.remove(user)
                        print("recover")
                        load_from_file(".recover.txt")
                        await channel.send(embed=discord.Embed(title="Recover",description="Recovery done",color=discord.Color(value=re[8])))
                    if reaction.emoji=="⭕" and str(reaction.message.channel.id)==str(channel.id):
                        await reaction.remove(user)
                        text_servers=""
                        for i in client.guilds:
                            text_servers=text_servers+str(i.name)+"\n"
                        await channel.send(embed=discord.Embed(title="Servers",description=text_servers,color=discord.Color(value=re[8])))
                    if reaction.emoji==emoji.emojize(":fire:") and str(reaction.message.channel.id)==str(channel.id):
                        try:
                            voice=discord.utils.get(client.voice_clients,guild=reaction.message.guild)
                            voice.stop()
                            await voice.disconnect()
                        except:
                            pass
                        save_to_file()
                        print("Restart "+str(user))
                        await channel.purge(limit=100000000)
                        os.chdir(location_of_file)
                        os.system("nohup python "+location_of_file+"/Discord.py &")
                        await channel.send(embed=discord.Embed(title="Restart",description=("Requested by "+str(user)),color=discord.Color(value=re[8])))
                        sys.exit()
                    if reaction.emoji==emoji.emojize(":cross_mark:") and str(reaction.message.channel.id)==str(channel.id):
                        await reaction.remove(user)
                        try:
                            voice=discord.utils.get(client.voice_clients,guild=reaction.message.guild)
                            voice.stop()
                            await voice.disconnect()
                        except:
                            pass
                        await channel.purge(limit=10000000000)
                        await channel.send(embed=discord.Embed(title="Exit",description=("Requested by "+str(user)),color=discord.Color(value=re[8])))
                        sys.exit()
                    if reaction.emoji==emoji.emojize(":satellite:") and str(reaction.message.channel.id)==str(channel.id):
                        string=""
                        await reaction.remove(user)
                        await channel.send("Starting speedtest")
                        download_speed=int(st_speed.download())//1024//1024
                        upload_speed=int(st_speed.upload())//1024//1024
                        servers=st_speed.get_servers([])
                        ping=st_speed.results.ping
                        await channel.send(embed=discord.Embed(title="Speedtest Results:", description=str(download_speed)+"Mbps\n"+str(upload_speed)+"Mbps\n"+str(ping)+"ms", color=discord.Color(value=re[8])))
                    if reaction.emoji=="❕" and str(reaction.message.channel.id)==str(channel.id):
                        await reaction.remove(user)
                        issues=""
                        if psutil.cpu_percent()>85:
                            issues=issues+"High CPU usage\n"
                        if psutil.virtual_memory().percent>80:
                            issues=issues+"High RAM usage\n"
                        if psutil.virtual_memory().cached<719908352:
                            issues=issues+"Low Memory cache\n"
                        if len(entr)==0:
                            issues=issues+"Variable entr is empty\n"
                        if len(queue_song[str(reaction.message.guild.id)])==0:
                            issues=issues+"Variable queue_song is empty\n"
                        if not ".recover.txt" in os.listdir():
                            issues=issues+"Recovery file not found"
                        else:
                            if len(entr)==0 and len()==0 and len(re)<4:
                                issues=issues+"Recovery required, attempting recovery\n"
                                load_from_file(".recover.txt")
                                if len(entr)==0 and len()==0 and len(re)<4:
                                    issues=issues+"Recovery failed\n"
                        await channel.send(embed=discord.Embed(title="Issues with the program", description=issues, color=discord.Color(value=re[8])))
                    if reaction.emoji==emoji.emojize(":black_circle:") and str(reaction.message.channel.id)==str(channel.id):
                        await channel.purge(limit=10000000000000000000)
                        text_dev="You get to activate and reset certain functions in this channel \n" \
                        ""+(emoji.emojize(":safety_vest:"))+" for recovery \n"  \
                        "⭕ for list of all servers \n" \
                        "❌ for exiting \n" \
                        "🔥 for restart\n" \
                        "📊 for current load\n" \
                        "❕ for current issues\n" \
                        ""+emoji.emojize(":satellite:")+" for speedtest\n" \
                        ""+emoji.emojize(":black_circle:")+" for clear screen\n" \
                        ""+emoji.emojize(":classical_building: for starting Storage bot\n")+""
                        embed=discord.Embed(title="DEVOP",description=text_dev,color=discord.Color(value=re[8]))
                        embed.set_thumbnail(url=client.user.avatar_url_as(format="png"))
                        mess=await channel.send(embed=embed)
                        await mess.add_reaction(emoji.emojize(":safety_vest:"))
                        await mess.add_reaction("⭕")
                        await mess.add_reaction("❌")
                        await mess.add_reaction(emoji.emojize(":fire:"))
                        await mess.add_reaction(emoji.emojize(":bar_chart:"))
                        await mess.add_reaction("❕")
                        await mess.add_reaction(emoji.emojize(":satellite:"))
                        await mess.add_reaction(emoji.emojize(":black_circle:"))
                        await mess.add_reaction(emoji.emojize(":classical_building:"))
                        await mess.add_reaction(emoji.emojize(":laptop:"))
        except Exception as e:
            channel = client.get_channel(834624717410926602)
            await channel.send(embed=discord.Embed(title="Error in on_reaction_add", description=str(e)+"\n"+str(reaction.message.guild)+": "+str(reaction.message.channel.name), color=discord.Color(value=re[8])))
    @client.command()
    async def yey(ctx):
        req()
        print("yey")
        em=discord.Embed(title="*yey*",color=discord.Color(value=re[8]))
        await ctx.send(embed=em)
    @client.command(aliases=['g'])
    async def google(ctx,*,text):
        req()
        print(text, str(ctx.author))
        li="**"+text+"** \n\n"
        for i in googlesearch.search(text,num=6,stop=6,pause=0):
            li=li+i+" \n"
        await ctx.send(li)
    @client.command(aliases=['cen'])
    async def add_censor(ctx,*,text):
        req()
        string=""
        censor.append(text.lower())
        for i in range(0,len(text)):
            string=string+"-"
        em=discord.Embed(title="Added "+string+" to the list",decription="Done",color=discord.Color(value=re[8]))
        await ctx.send(embed=em)
    @client.event
    async def on_message(msg):
        try:
            for word in censor:
                if word in msg.content.lower() and msg.guild.id==822445271019421746:
                    await msg.delete()
            if "?" in msg.content.lower() and re[4]==1:
                await msg.channel.send("thog dont caare")
            elif "what" in msg.content.lower() and re[4]==1:
                await msg.channel.send("thog dont caare")
            elif "how" in msg.content.lower() and re[4]==1:
                await msg.channel.send("thog dont caare")
            elif "when" in msg.content.lower() and re[4]==1:
                await msg.channel.send("thog dont caare")
            elif "why" in msg.content.lower() and re[4]==1:
                await msg.channel.send("thog dont caare")
            elif "who" in msg.content.lower() and re[4]==1:
                await msg.channel.send("thog dont caare")
            elif "where" in msg.content.lower() and re[4]==1:
                await msg.channel.send("thog dont caare")
            if f'<@!{client.user.id}>' in msg.content:
                st="\n\n\n**Mutual guilds:**\n\n"
                for i in msg.author.mutual_guilds:
                    st=st+i.name+"\n" 
                embed=discord.Embed(title="Hi!! I am Alfred.",description="Prefix is '\nFor more help, type 'help"+st,color=discord.Color(value=re[8]))
                embed.set_image(url=random.choice(["https://giffiles.alphacoders.com/205/205331.gif","https://c.tenor.com/PQu-tE-5HxwAAAAd/michael-caine-the-dark-knight.gif"]))
                
                await msg.channel.send(embed=embed)
            if msg.content.find("'")==0:
                save_to_file()
                if len(entr)==0 and len(re)<9:
                    load_from_file(".recover.txt")
            if start_time%60>30 and start_time%60<50 and len(entr)!=0 and len(queue_song)!=0 and len(da1)!=0 and len(re)>=9:
                save_to_file("recover")
            await client.process_commands(msg)
        except Exception as e:
            channel = client.get_channel(dev_channel)
            await channel.send(embed=discord.Embed(title="Error", description=str(e), color=discord.Color(value=re[8])))
            
    @client.command()
    async def thog(ctx,*,text):
        if re[1]==text:
            re[4]=re[4]*-1
            if re[4]==1:
                await ctx.send(embed=discord.Embed(title="Thog",description="Activated",color=discord.Color(value=re[8])))
            else:
                await ctx.send(embed=discord.Embed(title="Thog",description="Deactivated",color=discord.Color(value=re[8])))
        else:
            await ctx.message.delete()
            await ctx.send("Wrong password")
    @client.command(aliases=['m'])
    async def python_shell(ctx,*,text):
        req()
        print("Python Shell",text,str(ctx.author))
        global dev_users
        if (str(text).find("username")==-1 and str(text).find("os.")==-1 and str(text).find("ctx.")==-1 and str(text).find("__import__")==-1 and str(text).find("sys")==-1 and str(text).find("psutil")==-1 and str(text).find("clear")==-1 and str(text).find("dev_users")==-1 and str(text).find("remove")==-1 and str(text).find("class.")==-1  and str(text).find("subclass()")==-1 and str(text).find("client")==-1 and str(text).find("quit")==-1 and str(text).find("exit")==-1) or (str(ctx.author.id) in dev_users and str(text).find("reboot")==-1 and str(text).find("shut")==-1):
            if str(ctx.author.guild.id)!="727061931373887531":
                try:
                    text=text.replace("```py","")
                    text=text.replace("```","")
                    a=eval(text)
                    print(text)
                    em=discord.Embed(title=text,description=text+"="+str(a),color=discord.Color(value=re[8]))
                    em.set_thumbnail(url="https://banner2.cleanpng.com/20180715/phb/kisspng-python-javascript-logo-clojure-python-logo-download-5b4ba705f356d3.4338622815316846139967.jpg")
                    await ctx.send(embed=em)
                except Exception as e:
                    await ctx.send(embed=discord.Embed(title="Error_message",description=str(e),color=discord.Color(value=re[8])))
            else:
                await ctx.send(embed=discord.Embed(title="Banned",description="You've been banned from using python shell",color=discord.Color(value=re[8])))
        else:
            await ctx.channel.purge(limit=1)
            await ctx.send(embed=discord.Embed(title="Permission denied",description="",color=discord.Color(value=re[8])))
    @client.command()
    async def exe(ctx,*,text):
        req()
        global temp_dev
        if (ctx.author.id in list(temp_dev.keys()) and not (text.find("os.")!=-1 and text.find("psutil")!=-1 and text.find("import psutil")!=-1 and text.find("import os")!=-1 and text.find("__import__")!=-1 and text.find("import sys")!=-1 and str(text).find("subclass()")==-1 and str(text).find("client")==-1 and text.find("sys.")!=-1 and text.find("subprocess.")!=-1 and text.find("dev_users")!=-1 and text.find("temp_dev")!=-1)) or (str(ctx.author.id) in dev_users):
            mysql_password="Denied"
            if text.find("passwd=")!=-1:
                mysql_password=os.getenv('mysql')
            text=text.replace("```py","```")
            text=text[3:-3].strip()
            f = StringIO()
            with redirect_stdout(f):
                try:
                    exec(text)
                except Exception as e:
                    traceback.print_tb(e.__traceback__)
                    error_mssg = "Following Error Occured:\n" + "\n".join([line for line in traceback.format_exception(type(e), e, e.__traceback__) if "in exe" not in line])
                    await ctx.send(embed=discord.Embed(title="Error",description=error_mssg,color=discord.Color.from_rgb(255,40,0)))
            output = f.getvalue()
            if output=="":
                output="_"
            if len(output)>2000:
                output=output[0:2000]
            em=discord.Embed(title="Output",description=str(output),color=discord.Color(value=re[8]))
            em.set_thumbnail(url="https://banner2.cleanpng.com/20180715/phb/kisspng-python-javascript-logo-clojure-python-logo-download-5b4ba705f356d3.4338622815316846139967.jpg")
            await ctx.send(embed=em)
        else:
            await ctx.send(embed=discord.Embed(title="Denied", description="Ask Devs to give access for scripts",color=discord.Color(value=re[8])))
    @client.command()
    async def get_req(ctx):
        req()
        number=g_req()
        em=discord.Embed(title="Requests",description=str(number),color=discord.Color(value=re[8]))
        await ctx.send(embed=em)
    def r(x):
        return radians(x)
    def d(x):
        return degrees(x)
    def addt(p1,p2):
        da[p1]=p2
        return "Done"
    def get_elem(k):
        return da.get(k,"Not assigned yet")
    def de(k):
        del da[k]
        return "Done"
    def req():
        re[0]=re[0]+1
    def g_req():
        return re[0]

    @client.command()
    async def test_embed(ctx):
        embed=cembed(title="Title of the embed", description="This is to check if the embed function works", thumbnail=client.user.avatar_url_as(format="png"), picture=ctx.author.avatar_url_as(format="png"), color=re[8])
        await ctx.send(embed=embed)


    @client.command(aliases=['mu'])
    @commands.has_permissions(kick_members=True)
    async def mute(ctx,member:discord.Member):
    	req()
    	if ctx.guild.id==743323684705402951:add_role=discord.utils.get(ctx.guild.roles,name="muted")
    	if ctx.guild.id==851315724119310367:add_role=discord.utils.get(ctx.guild.roles,name="Muted")
    	else:add_role=discord.utils.get(ctx.guild.roles,name="dunce")
    	await member.add_roles(add_role)
    	await ctx.send("Muted "+member.mention)
    	print(member,"muted")
    @client.command(aliases=['um'])
    @commands.has_permissions(kick_members=True)
    async def unmute(ctx,member:discord.Member):
    	req()
    	if ctx.guild.id==851315724119310367:add_role=discord.utils.get(ctx.guild.roles,name="Muted")
    	else:add_role=discord.utils.get(ctx.guild.roles,name="dunce")
    	await member.remove_roles(add_role)
    	await ctx.send("Unmuted "+member.mention)
    	print(member,"unmuted")
    te="**COMMANDS**\n'google <text to search> \n'help to get this screen\n'wikipedia Topic \n'python_shell <Expression> for python shell\n'get_req for no. of requests so far\n'entrar for the latest announcements from Entrar\n'compile <lang> ```#code```\n\n" \
    "**ALIAS**: \n'g <text to search> \n'h to show this message \n'm <Expression> for python eval \n'w for Wikipedia\n':: for memes\n'sq for queue\n'> for next\n'< for previous\n'cm for connecting to a voice\n\n" \
    "**EXAMPLE**:\n'help\n'q\n'w Wikipedia\n'again\n'next\n'memes\n'q Song\n\n" \
    "**UPDATES**:\nAlfred now supports youtube subscriptions\nAlfred can  now execute code and its open for everyone\nIts for everyone. Check it out using\n 'compile lang\n```#code here```\n Thank Shravan.\nAlfred has 24/7 games and roast feature now, currently games include chess only, we'll add more, DW\nUse prefix `{` for that.\nBtw if you didnt get slash commands get the new invite for Alfred from dev.\nEnjoy\n\n" \
    "**MUSIC**:\n'connect_music <channel_name> to connect the bot to the voice channel\n'play <song name> to play song without adding to the queue\n'queue <song name> to add a song to the queue\n'play <index no.> to play certain song from the queue list\n" \
    "'addto playlist <Playlist name> to add current queue to playlist\n'addto queue <Playlist name> to add playlist to the queue\n'clearqueue to clear the queue\n'resume\n'pause\n" \
    "'curr for current song.\n\n"

    @slash.slash(name="help",description="Help from Alfred")
    async def help_slash(ctx):
        req()
        await ctx.defer()
        await h(ctx)
    client.remove_command("help")
    @client.group(invoke_without_command=True)
    async def help(ctx):
        req()
        print("help")
        em=discord.Embed(title="```Help```",description=te,color=discord.Color(value=re[8]))
        em.set_thumbnail(url="https://static.wikia.nocookie.net/newdcmovieuniverse/images/4/47/Pennyalf.PNG/revision/latest?cb=20190207195903")
        await ctx.send(embed=em)
    @client.group(invoke_without_command=True)
    async def h(ctx):
        req()
        print("help")
        em=discord.Embed(title="**HELP** \n",description=te,color=discord.Color(value=re[8]))
        em.set_thumbnail(url="https://static.wikia.nocookie.net/newdcmovieuniverse/images/4/47/Pennyalf.PNG/revision/latest?cb=20190207195903")
        await ctx.send(embed=em)
    client.run(os.getenv('token'))
