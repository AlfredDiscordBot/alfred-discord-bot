import discord
import random
from discord.ext import commands
from googlesearch import search
from math import *
from statistics import*
from wikipedia import *
import wikipedia
import math as ma
import statistics as s
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
import mysql.connector as m
import speedtest
if True:
    st_speed=speedtest.Speedtest()
    if os.getcwd()!="default/path":
        os.chdir("default/path")
    start_time=time.time()
    md=m.connect(host="localhost", user="root", passwd="password for mysql", database="database name")
    cursor=md.cursor()
    intents=discord.Intents.default()
    intents.members=True
    client=commands.Bot(command_prefix="'",intents=intents)
    censor=[] 
    da={}
    entr={}
    da1={}
    queue_song={}
    dev_channel=834624717410926602
    re=[0,"OK",1,{},-1,'','205']
    vc_channel={}
    dev_users=['Alvin#6115']
    ydl_op={'format':'bestaudio/best','postprocessors':[{'key':'FFmpegExtractAudio','preferredcodec':'mp3','preferredquality':'96',}],}
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
            file.write("entr="+str(entr)+"\n")
            file.write("queue_song="+str(queue_song)+"\n")
            file.write("re="+str(re)+"\n")
            file.write("dev_users="+str(dev_users)+"\n")
            file.close()
        if a=="recover":
            file = open(".recover.txt", "w")
            file.write("censor="+str(censor)+"\n")
            file.write("da="+str(da)+"\n")
            file.write("da1="+str(da1)+"\n")
            file.write("entr="+str(entr)+"\n")
            file.write("queue_song="+str(queue_song)+"\n")
            file.write("re="+str(re)+"\n")
            file.write("dev_users="+str(dev_users)+"\n")
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
            print(txt_from_file)
            #censor list
            a1=txt_from_file.find("censor=")+len("censor")
            a2=txt_from_file.find("]",(a1+1))+1
            a1=txt_from_file.find("[",a1,a2)
            k_censor=eval(txt_from_file[a1:a2])
            censor=k_censor
            #da dictionary
            a1=txt_from_file.find("da=")+len("da")
            a2=txt_from_file.find("}",(a1+1))+1
            a1=txt_from_file.find("{",a1,a2)
            k_da=eval(txt_from_file[a1:a2])
            da=k_da
            #da1 dictionary
            a1=txt_from_file.find("da1=")+len("da1")
            a2=txt_from_file.find("}",(a1+1))+1
            a1=txt_from_file.find("{",a1,a2)
            k_da1=eval(txt_from_file[a1:a2])
            da1=k_da1
            #entr list
            a1=txt_from_file.find("entr=")+len("entr")
            a2=txt_from_file.find("}",(a1+1))+1
            a1=txt_from_file.find("{",a1,a2)
            k_entr=eval(txt_from_file[a1:a2])
            entr=k_entr
            #re list
            a1=txt_from_file.find("re=")+len("re")
            a2=txt_from_file.find("]",(a1+1))+1
            a1=txt_from_file.find("[",a1,a2)
            k_re=eval(txt_from_file[a1:a2])
            re=k_re
            #dev_users list
            a1=txt_from_file.find("dev_users=")+len("dev_users")
            a2=txt_from_file.find("]",(a1+1))+1
            a1=txt_from_file.find("[",a1,a2)
            k_dev_users=eval(txt_from_file[a1:a2])
            dev_users=k_dev_users
            #queue_song list
            a1=txt_from_file.find("queue_song=")+len("queue_song")            
            a2=txt_from_file.find("}",(a1))+1            
            a1=txt_from_file.find("{",a1,a2)            
            k_queue_song=eval(txt_from_file[a1:a2])
            queue_song=k_queue_song            
        save_to_file()    
    @client.event
    async def on_ready():
        channel = client.get_channel(dev_channel)
        try:
            load_from_file()
            print(re)
            print(dev_users)        
            await channel.purge(limit=10000000000000000000)
            text_dev="You get to activate and reset certain functions in this channel \n" \
            ""+(emoji.emojize(":safety_vest:"))+" for recovery \n"  \
            "⭕ for list of all servers \n" \
            "❌ for exiting \n" \
            "🔥 for restart\n" \
            "📊 for current load\n" \
            "❕ for current issues\n" \
            ""+emoji.emojize(":satellite:")+" for speedtest\n" \
            ""+emoji.emojize(":black_circle:")+" for clear screen\n"
            mess=await channel.send(embed=discord.Embed(title="DEVOP",description=text_dev,color=discord.Color.from_rgb(255,255,255)))
            await mess.add_reaction(emoji.emojize(":safety_vest:"))
            await mess.add_reaction("⭕")
            await mess.add_reaction("❌")
            await mess.add_reaction("🔥")
            await mess.add_reaction("📊")
            await mess.add_reaction("❕")
            await mess.add_reaction(emoji.emojize(":satellite:"))
            await mess.add_reaction(emoji.emojize(":black_circle:"))
        except Exception as e:
            await channel.send(embed=discord.Embed(title="Error in the function on_ready", description=e,color=discord.Color.from_rgb(255,0,0)))
        print("Prepared")        
    @client.command(aliases=['$$'])
    async def recover(ctx):
        try:
            load_from_file(".recover.txt")
        except Exception as e:
            channel = discord.utils.get(ctx.guild.channels, name="devop")
            await channel.send(embed=discord.Embed(title="Recovery failed", description=e, color=ctx.author.color))
            
    @client.command()
    async def load(ctx):
        req()
        try:
            cpu_per=str(int(psutil.cpu_percent()))
            cpu_freq=str(int(psutil.cpu_freq().current))+"/"+str(int(psutil.cpu_freq().max))
            ram=str(psutil.virtual_memory().percent)
            swap=str(psutil.swap_memory().percent)
            usage="CPU Percentage: "+cpu_per+"%\nCPU Frequency: "+cpu_freq+"\nRAM Usage: "+ram+"%\nSwap Usage: "+swap+"%"
            await ctx.send(embed=discord.Embed(title="Current load",description=usage,color=ctx.author.color))
        except Exception as e:
            channel = discord.utils.get(ctx.guild.channels, name="devop")
            await channel.send(embed=discord.Embed(title="Load failed", description=e, color=ctx.author.color))
    @client.command()
    async def pr(ctx,*,text):
        await ctx.send(text)
    @client.command(aliases=['l'])
    async def lyrics(ctx,*,string=""):
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
                pos_1=html_code.find('text-left')            
                pos_2=int(int(html_code.find(".href='",pos_1))+len('.href="'))
                pos_3=html_code.find("'",pos_2)
                url=html_code[pos_2:pos_3]
                if len(url)>3:
                    lyri=urllib.request.urlopen(url).read().decode()
                    lyri1=lyri[int(lyri.find("Sorry about that. -->")+len("Sorry about that. -->")):lyri.find("</div>",(int(lyri.find("Sorry about that. -->")+10)))].replace("<br>","").replace("<i>","_").replace("</i>","_") 
                    title_of_song=lyri[lyri.find("<title>")+len("<title>"):lyri.find("</title>")]+"\n"
                    if len(lyri)<=1900:
                        await ctx.send(embed=discord.Embed(title="**Lyrics**",description=("**"+title_of_song+"**"+lyri1.replace('&quot;','"')),color=ctx.author.color))
                    else:
                        await ctx.send(embed=discord.Embed(title="**Lyrics**",description=("**"+title_of_song+"**"+lyri1[0:1900]),color=ctx.author.color))
                        await ctx.send(embed=discord.Embed(title="Continuation",description=("**"+title_of_song+"**"+lyri1[1900:]),color=ctx.author.color))
                else:
                    await ctx.send(embed=discord.Embed(title="Not Found",description="Song not found, try lyrics <song name> to search properly",color=ctx.author.color))
            else:
                await ctx.send(embed=discord.Embed(title="Hmm",description="Enter the voice channel to use this function",color=ctx.author.color))
        except Exception as e:
            channel = discord.utils.get(ctx.guild.channels, name="devop")
            await channel.send(embed=discord.Embed(title="Lyrics failed", description=e, color=ctx.author.color))
    @client.command()
    async def remove_dev(ctx,member:discord.Member):
        print(member)
        global dev_users
        if str(ctx.author)=="Alvin#6115":
            dev_users.remove(str(member))
            await ctx.send(member.mention+" is no longer a dev")
        else:
            await ctx.send(embed=discord.Embed(title="Permission Denied", description="Dude! You are not Alvin",color=ctx.author.color))
    @client.command()
    async def add_dev(ctx,member:discord.Member):
        print(member)
        global dev_users
        if str(ctx.author) in dev_users:
            dev_users=dev_users+[str(member)]
            await ctx.send(member.mention+" is a dev now")
        else:
            await ctx.send(embed=discord.Embed(title="Permission Denied", description="Dude! you are not a dev",color=ctx.author.color))
    @client.command()
    async def dev_op(ctx):
        channel = discord.utils.get(ctx.guild.channels, name="devop")
        await channel.purge(limit=10000000000000000000)
        text_dev="You get to activate and reset certain functions in this channel \n" \
        ""+(emoji.emojize(":safety_vest:"))+" for recovery \n"  \
        "⭕ for list of all servers \n" \
        "❌ for exiting \n" \
        "🔥 for restart\n" \
        "📊 for current load\n" \
        "❕ for current issues\n" \
        ""+emoji.emojize(":satellite:")+" for speedtest\n" \
        ""+emoji.emojize(":black_circle:")+" for clear screen\n"
        mess=await channel.send(embed=discord.Embed(title="DEVOP",description=text_dev,color=ctx.author.color))
        await mess.add_reaction(emoji.emojize(":safety_vest:"))
        await mess.add_reaction("⭕")
        await mess.add_reaction("❌")
        await mess.add_reaction("🔥")
        await mess.add_reaction("📊")
        await mess.add_reaction("❕")
        await mess.add_reaction(emoji.emojize(":satellite:"))
        await mess.add_reaction(emoji.emojize(":black_circle:"))
    @client.command()
    async def reset_from_backup(ctx):
        try:
            load_from_file()
        except Exception as e:
            channel = discord.utils.get(ctx.guild.channels, name="devop")
            await channel.send(embed=discord.Embed(title="Reset_from_backup failed", description=e, color=ctx.author.color))
    @client.command()
    async def entrar(ctx,*,num=re[6]):
        global re
        re[0]=re[0]+1
        lol=""
        header={'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36','referer':"https://entrar.in"}
        suvzsjv={
            'username': "username",
            'password': "password"
            }
        announcement_data={
            'announcementlist': 'true',
            'session': '205'
            }
        re[6]=num
        announcement_data['session']=str(num)        
        with requests.Session() as s:
            url="https://entrar.in/login/authenticate1/"
            r=s.post(url,data=suvzsjv,headers=header)
            r=s.get("https://entrar.in/",headers=header)
            r=s.post("https://entrar.in/parent_portal/announcement",headers=header)
            r=s.get("https://entrar.in/parent_portal/announcement",headers=header)
            time.sleep(1)
            r=s.post("https://entrar.in/parent_portal/announcement",data=announcement_data,headers=header)
            channel = discord.utils.get(ctx.guild.channels, name="announcement")
            st=r.content.decode()
            for i in range(1,5):
                a=st.find('<td class="text-wrap">'+str(i)+'</td>')
                b=st.find('<td class="text-wrap">'+str(i+1)+'</td>')
                le=len('<td class="text-wrap">'+str(i+1)+'</td>')-1
                if b==-1:
                    await ctx.send(embed=discord.Embed(title="End Of List",description="",color=ctx.author.color))
                    break
                c=st.find('&nbsp;&nbsp; ',a,b)+len("&nbsp;&nbsp; ")
                d=st.find('<',c,b)
                out=st[c:d].strip()
                e=a+le
                f=st.find('<td>',e,e+15)+len('<td>')
                g=st.find('</td>',e,e+45)
                date=st[f:g]
                h=st.find('<a href="',a,b)+len('<a href="')
                j=st.find('">',h,b)
                link=str(st[h:j])
                req=s.get(link)
                k=out+link+date
                if not str(ctx.guild.id) in entr:
                    entr[str(ctx.guild.id)]=[]
                if k in entr[str(ctx.guild.id)]:
                    break          
                entr[str(ctx.guild.id)].append(str(k))
                lol=lol+out+" Date:"+date+"\n"
                with open((out+".pdf"),'wb') as pdf:
                    pdf.write(req.content)                    
                    await channel.send(file=discord.File(out+".pdf"))
                    pdf.close()
                os.remove(out+".pdf")
            if lol!="":
                await channel.send(embed=discord.Embed(title="New announcements",description=lol,color=discord.Color.from_rgb(128,20,0)))
            else:
                await channel.send(embed=discord.Embed(title="Empty",description="No new announcement",color=discord.Color.from_rgb(128,20,0)))

    @client.command(aliases=[';'])
    async def mysql(ctx,*,text):        
        output=""
        global cursor
        try:
            cursor.execute(text)
            for i in cursor:
                output=output+str(i)+"\n"
            await ctx.send(embed=discord.Embed(title="MySQL", description=output,color=ctx.author.color))
        except Exception as e:
            await ctx.send(embed=discord.Embed(title="Error", description=e,color=discord.Color.from_rgb(255,0,0)))
        
    @client.event
    async def on_member_join(member):
        channel=discord.utils.get(member.guild.channels, name="announcement")
        await channel.send(member.mention+" is here")
        await channel.send(embed=discord.Embed(title="Welcome!!!", description="Welcome to the channel, "+member.name,color=discord.Color.from_rgb(255,255,255)))
    @client.command(aliases=['cm'])
    async def connect_music(ctx,channel):
        try:
            req()
            if not str(ctx.guild.id) in queue_song:
                queue_song[str(ctx.guild.id)]=[]
            if not str(ctx.guild.id) in re[3]:
                re[3][str(ctx.guild.id)]=0
            vc_channel[str(ctx.guild.id)]=channel
            voiceChannel=discord.utils.get(ctx.guild.voice_channels,name=channel)
            await voiceChannel.connect()
            voice=discord.utils.get(client.voice_clients,guild=ctx.guild)
            await ctx.send("Connected")
        except Exception as e:
            await ctx.send(embed=discord.Embed(title="Hmm",description=e,color=ctx.author.color))
            await channel.send(embed=discord.Embed(title="Connect music",description=e,color=ctx.author.color))
    @client.command()
    async def addto(ctx,mode,*,text):
        req()
        present=1
        voiceChannel=discord.utils.get(ctx.guild.voice_channels,name=vc_channel[str(ctx.guild.id)])
        member=voiceChannel.members
        for mem in member:
            if str(ctx.author)==str(mem):
                present=0
                break
        if mode=="playlist" and present==0:
            add(text,queue_song[str(ctx.guild.id)].copy())
            await ctx.send("Done")
        elif mode=="queue" and present==0:
            print(len(get_elem(str(text))))
            song_list=""
            for i in range(0,len(get_elem(str(text)))):
                link_add=get_elem(str(text))[i]
                aa=str(urllib.request.urlopen(link_add).read().decode())
                starting=aa.find("<title>")+len("<title>")
                ending=aa.find("</title>")        
                name_of_the_song=aa[starting:ending].replace("&#39;","'").replace(" - YouTube","").replace("&amp;","&")
                da1[link_add]=name_of_the_song
                queue_song[str(ctx.guild.id)].append(link_add)
                song_list=song_list+name_of_the_song+"\n"
            await ctx.send(embed=discord.Embed(title="Songs added",description=song_list,color=ctx.author.color))            
        else:
            if present==0:
                await ctx.send("Only playlist and queue")
            else:
                await ctx.send(embed=discord.Embed(title="Permission denied",description="Join the voice channel to modify queue",color=ctx.author.color))
    @client.command(aliases=['cq'])
    async def clearqueue(ctx):
        req()
        mem=[(str(i.name)+"#"+str(i.discriminator)) for i in discord.utils.get(ctx.guild.voice_channels,name=vc_channel[str(ctx.guild.id)]).members]
        if mem.count(str(ctx.author))>0:
            if len(queue_song[str(ctx.guild.id)])>0:
                queue_song[str(ctx.guild.id)].clear()
                da1.clear()
            re[3][str(ctx.guild.id)]=0
            await ctx.send(embed=discord.Embed(title="Cleared queue",description="_Done_",color=ctx.author.color))
        else:
            await ctx.send(embed=discord.Embed(title="Permission denied",description="Join the voice channel to modify queue",color=ctx.author.color))
    @client.command()
    async def remove(ctx,n):        
        req()
        mem=[(str(i.name)+"#"+str(i.discriminator)) for i in discord.utils.get(ctx.guild.voice_channels,name=vc_channel[str(ctx.guild.id)]).members]
        if mem.count(str(ctx.author))>0:
            if int(n)<len(queue_song[str(ctx.guild.id)]):
                await ctx.send(embed=discord.Embed(title="Removed",description=da1[queue_song[str(ctx.guild.id)][int(n)]],color=ctx.author.color))
                del da1[queue_song[str(ctx.guild.id)][int(n)]]
                queue_song[str(ctx.guild.id)].pop(int(n))                
            else:
                await ctx.send(embed=discord.Embed(title="Not removed", description="Only "+len(queue_song[str(ctx.guild.id)])+" song(s) in your queue",color=ctx.author.color))
        else:
            await ctx.send(embed=discord.Embed(title="Permission denied",description="Join the voice channel to modify queue",color=ctx.author.color))
    @client.command(aliases=['curr'])
    async def currentmusic(ctx):
        req()
        if len(queue_song[str(ctx.guild.id)])>0:
            await ctx.send(embed=discord.Embed(title=str(da1[queue_song[str(ctx.guild.id)][re[3][str(ctx.guild.id)]]]),description="Current index: "+str(re[3][str(ctx.guild.id)]),color=ctx.author.color))
        else:
            await ctx.send(embed=discord.Embed(title="Empty queue",description="Your queue is currently empty",color=ctx.author.color))
    @client.command()
    async def loop(ctx):
        req()
        st=""
        re[2]=re[2]*-1
        if re[2]<0:st="Off"
        else:st="_On_"
        await ctx.send(embed=discord.Embed(title="Loop",description=st,color=ctx.author.color))
    @client.command(aliases=['q'])
    async def queue(ctx,*,name):
        req()
        mem=[(str(ps.name)+"#"+str(ps.discriminator)) for ps in discord.utils.get(ctx.guild.voice_channels,name=vc_channel[str(ctx.guild.id)]).members]
        if mem.count(str(ctx.author))>0:
            name=name.replace(" ","+")
            sear="https://www.youtube.com/results?search_query="+name
            htm=urllib.request.urlopen(sear)
            video=regex.findall(r"watch\?v=(\S{11})",htm.read().decode())
            url="https://www.youtube.com/watch?v="+video[0]
            aa=str(urllib.request.urlopen(url).read().decode())
            starting=aa.find("<title>")+len("<title>")
            ending=aa.find("</title>")        
            name_of_the_song=aa[starting:ending].replace("&#39;","'").replace(" - YouTube","").replace("&amp;","&")
            print(name_of_the_song,":",url)
            da1[url]=name_of_the_song
            queue_song[str(ctx.guild.id)].append(url)
            st=""
            await ctx.send("Added to queue")
            num=0
            for i in queue_song[str(ctx.guild.id)]:
                st=st+str(num)+". "+da1[i]+"\n"
                num+=1
            if st=="":st="_Empty_"
            em=discord.Embed(title="Queue",description=st,color=ctx.author.color)
            mess=await ctx.send(embed=em)
            await mess.add_reaction("⏮")
            await mess.add_reaction("⏸")
            await mess.add_reaction("▶")
            await mess.add_reaction("🔁")
            await mess.add_reaction("⏭")
            await mess.add_reaction("⏹")
        else:
            await ctx.send(embed=discord.Embed(title="Permission denied",description="Join the voice channel to modify queue",color=ctx.author.color))
    @client.command(aliases=['sq'])
    async def show_q(ctx):
        if True:
            mem=[(str(ps.name)+"#"+str(ps.discriminator)) for ps in discord.utils.get(ctx.guild.voice_channels,name=vc_channel[str(ctx.guild.id)]).members]
            if mem.count(str(ctx.author))>0:
                num=0
                st=""
                for i in queue_song[str(ctx.guild.id)]:
                    st=st+str(num)+". "+da1[i]+"\n"
                    num+=1
                mess=await ctx.send(embed=discord.Embed(title="Queue",description=st,color=ctx.author.color))
                await mess.add_reaction("⏮")
                await mess.add_reaction("⏸")
                await mess.add_reaction("▶")
                await mess.add_reaction("🔁")
                await mess.add_reaction("⏭")
                await mess.add_reaction("⏹")
            else:
                await ctx.send(embed=discord.Embed(title="Permission denied",description="Join the voice channel to show queue",color=ctx.author.color))
    @client.command()
    async def show_playlist(ctx,*,key):
        req()
        mem=[(str(ps.name)+"#"+str(ps.discriminator)) for ps in discord.utils.get(ctx.guild.voice_channels,name=vc_channel[str(ctx.guild.id)]).members]
        if mem.count(str(ctx.author))>0:
            li=da.get(key,["This Playlist does not exist"])
            st=""
            num=0
            for i in li:
                num+=1
                if i=="This Playlist does not exist":
                    await ctx.send(embed=discord.Embed(title="No Playlist named "+key,description=li,color=ctx.author.color))
                    break
                else:
                    aa=str(urllib.request.urlopen(i).read().decode())
                    starting=aa.find("<title>")+len("<title>")
                    ending=aa.find("</title>")        
                    name_of_the_song=aa[starting:ending].replace("&#39;","'").replace(" - YouTube","").replace("&amp;","&")
                    st=st+"*"+str(num)+"*. "+name_of_the_song+"\n"
            else:
                await ctx.send(embed=discord.Embed(title=key,description=st,color=ctx.author.color))
        else:
            await ctx.send(embed=discord.Embed(title="Permission denied",description="Join the voice channel to see the playlist",color=ctx.author.color))
    
    @client.command()
    async def song(ctx,*,name):
        req()
        mem=[(str(ps.name)+"#"+str(ps.discriminator)) for ps in discord.utils.get(ctx.guild.voice_channels,name=vc_channel[str(ctx.guild.id)]).members]
        if mem.count(str(ctx.author))>0:
            name=name.replace(" ","+")
            htm=urllib.request.urlopen("https://www.youtube.com/results?search_query="+name)
            video=regex.findall(r"watch\?v=(\S{11})",htm.read().decode())
            url="https://www.youtube.com/watch?v="+video[0]
            aa=str(urllib.request.urlopen(url).read().decode())
            starting=aa.find("<title>")+len("<title>")
            ending=aa.find("</title>")        
            name_of_the_song=aa[starting:ending].replace("&#39;","'").replace("&amp;","&")
            print(url)
            song=os.path.isfile("."+str(ctx.guild.id)+".mp3")
            try:
                 if song:
                     os.remove("."+str(ctx.guild.id)+".mp3")
            except PermissionError:
                await ctx.send("Wait or use stop")
            voice=discord.utils.get(client.voice_clients,guild=ctx.guild)
            with youtube_dl.YoutubeDL(ydl_op) as ydl:
                ydl.download([url])
            await ctx.send(embed=discord.Embed(title="Song",description="Playing "+name_of_the_song,color=ctx.author.color))
            for file in os.listdir("./"):
                if file.endswith(".mp3"):
                    os.rename(file,"."+str(ctx.guild.id)+".mp3")        
            voice.play(discord.FFmpegOpusAudio("."+str(ctx.guild.id)+".mp3",bitrate=96))
        else:
            await ctx.send(embed=discord.Embed(title="Permission denied",description="Join the voice channel to play a song",color=ctx.author.color))
    @client.command(aliases=['>'])
    async def next(ctx):
        req()
        mem=[(str(ps.name)+"#"+str(ps.discriminator)) for ps in discord.utils.get(ctx.guild.voice_channels,name=vc_channel[str(ctx.guild.id)]).members]
        if mem.count(str(ctx.author))>0:
            re[3][str(ctx.guild.id)]+=1
            if re[3][str(ctx.guild.id)]>=len(queue_song[str(ctx.guild.id)]):
                re[3][str(ctx.guild.id)]=len(queue_song[str(ctx.guild.id)])-1
                await ctx.send(embed=discord.Embed(title="Last song",description="Only "+str(len(queue_song))+" songs in your queue",color=ctx.author.color))                          
            song=os.path.isfile("."+str(ctx.guild.id)+".mp3")
            try:
                 if song:
                     os.remove("."+str(ctx.guild.id)+".mp3")
            except PermissionError:
                await ctx.send("Wait or use stop")
            voice=discord.utils.get(client.voice_clients,guild=ctx.guild)
            voice.stop()
            with youtube_dl.YoutubeDL(ydl_op) as ydl:
                ydl.download([queue_song[str(ctx.guild.id)][re[3][str(ctx.guild.id)]]])
            await ctx.send(embed=discord.Embed(title="Playing",description=da1[queue_song[str(ctx.guild.id)][re[3][str(ctx.guild.id)]]],color=ctx.author.color))
            for file in os.listdir("./"):
                if file.endswith(".mp3"):
                    os.rename(file,"."+str(ctx.guild.id)+".mp3")        
            voice.play(discord.FFmpegOpusAudio("."+str(ctx.guild.id)+".mp3",bitrate=96))
        else:
            await ctx.send(embed=discord.Embed(title="Permission denied",description="Join the voice channel to move to the next song",color=ctx.author.color))  
    @client.command(aliases=['<'])
    async def previous(ctx):
        req()
        mem=[(str(ps.name)+"#"+str(ps.discriminator)) for ps in discord.utils.get(ctx.guild.voice_channels,name=vc_channel[str(ctx.guild.id)]).members]
        if mem.count(str(ctx.author))>0:
            re[3][str(ctx.guild.id)]-=1
            if re[3][str(ctx.guild.id)]==-1:
                re[3][str(ctx.guild.id)]=0
                await ctx.send(embed=discord.Embed(title="First song",description="This is first in queue",color=ctx.author.color))   
            song=os.path.isfile("."+str(ctx.guild.id)+".mp3")
            try:
                 if song:
                     os.remove("."+str(ctx.guild.id)+".mp3")
            except PermissionError:
                await ctx.send("Wait or use stop")
            voice=discord.utils.get(client.voice_clients,guild=ctx.guild)
            voice.stop()
            with youtube_dl.YoutubeDL(ydl_op) as ydl:
                ydl.download([queue_song[str(ctx.guild.id)][re[3][str(ctx.guild.id)]]])
            await ctx.send(embed=discord.Embed(title="Playing",description=da1[queue_song[str(ctx.guild.id)][re[3][str(ctx.guild.id)]]],color=ctx.author.color))
            for file in os.listdir("./"):
                if file.endswith(".mp3"):
                    os.rename(file,"."+str(ctx.guild.id)+".mp3")        
            voice.play(discord.FFmpegOpusAudio("."+str(ctx.guild.id)+".mp3",bitrate=96))
    @client.command()
    async def play(ctx,ind):
        req()
        mem=[(str(ps.name)+"#"+str(ps.discriminator)) for ps in discord.utils.get(ctx.guild.voice_channels,name=vc_channel[str(ctx.guild.id)]).members]
        if mem.count(str(ctx.author))>0:
            re[3][str(ctx.guild.id)]=int(ind)
            song=os.path.isfile("."+str(ctx.guild.id)+".mp3")
            try:
                 if song:
                     os.remove("."+str(ctx.guild.id)+".mp3")
            except PermissionError:
                await ctx.send("Wait or use stop")
            voice=discord.utils.get(client.voice_clients,guild=ctx.guild)
            voice.stop()            
            with youtube_dl.YoutubeDL(ydl_op) as ydl:
                ydl.download([queue_song[str(ctx.guild.id)][re[3][str(ctx.guild.id)]]])
            mess=await ctx.send(embed=discord.Embed(title="Playing",description=da1[queue_song[str(ctx.guild.id)][re[3][str(ctx.guild.id)]]],color=ctx.author.color))
            await mess.add_reaction("⏮")
            await mess.add_reaction("⏸")
            await mess.add_reaction("▶")
            await mess.add_reaction("🔁")
            await mess.add_reaction("⏭")
            await mess.add_reaction("⏹")
            for file in os.listdir("./"):
                if file.endswith(".mp3"):
                    os.rename(file,"."+str(ctx.guild.id)+".mp3")        
            voice.play(discord.FFmpegOpusAudio("."+str(ctx.guild.id)+".mp3",bitrate=96))
        else:
            await ctx.send(embed=discord.Embed(title="Permission denied",description="Join the voice channel to play the song",color=ctx.author.color))
    @client.command()
    async def again(ctx):
        req()
        if not "."+str(ctx.guild.id)+".mp3" in os.listdir():
            await ctx.send("You might need to wait a while since its not loaded")
            with youtube_dl.YoutubeDL(ydl_op) as ydl:
                ydl.download([queue_song[str(ctx.guild.id)][re[3][str(ctx.guild.id)]]])
            for file in os.listdir("./"):
                if file.endswith(".mp3"):
                    os.rename(file,"."+str(ctx.guild.id)+".mp3")
        mem=[(str(ps.name)+"#"+str(ps.discriminator)) for ps in discord.utils.get(ctx.guild.voice_channels,name=vc_channel[str(ctx.guild.id)]).members]
        if mem.count(str(ctx.author))>0:
            mess=await ctx.send(embed=discord.Embed(title="Playing",description=da1[queue_song[str(ctx.guild.id)][re[3][str(ctx.guild.id)]]],color=ctx.author.color))
            await mess.add_reaction("⏮")
            await mess.add_reaction("⏸")
            await mess.add_reaction("▶")
            await mess.add_reaction("🔁")
            await mess.add_reaction("⏭")
            await mess.add_reaction("⏹")
            voice=discord.utils.get(client.voice_clients,guild=ctx.guild)
            voice.stop()
            voice.play(discord.FFmpegOpusAudio("."+str(ctx.guild.id)+".mp3",bitrate=96))
        else:
            await ctx.send(embed=discord.Embed(title="Permission denied",description="Join the voice channel to play the song",color=ctx.author.color))
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
        os.system("nohup python path/to/python/file &")                
        await ctx.send(embed=discord.Embed(title="Restarted",description="The program finished restarting",color=ctx.author.color))
        sys.exit()
    @client.command(aliases=['dc'])
    async def leave(ctx):
        req()
        mem=[(str(ps.name)+"#"+str(ps.discriminator)) for ps in discord.utils.get(ctx.guild.voice_channels,name=vc_channel[str(ctx.guild.id)]).members]
        if mem.count(str(ctx.author))>0:
            vc_channel[str(ctx.guild.id)]=""
            voice=discord.utils.get(client.voice_clients,guild=ctx.guild)
            voice.stop()
            await voice.disconnect()
            try:
                os.remove("./."+str(ctx.guild.id)+".mp3")
            except:
                pass            
            await ctx.send(embed=discord.Embed(title="Disconnected",description="Bye",color=ctx.author.color))            
        else:
            await ctx.send(embed=discord.Embed(title="Permission denied",description="Nice try dude! Join the voice channel",color=ctx.author.color))
        save_to_file()
    @client.command()
    async def pause(ctx):
        req()
        mem=[(str(ps.name)+"#"+str(ps.discriminator)) for ps in discord.utils.get(ctx.guild.voice_channels,name=vc_channel[str(ctx.guild.id)]).members]
        if mem.count(str(ctx.author))>0:
            voice=discord.utils.get(client.voice_clients,guild=ctx.guild)
            voice.pause()
            await ctx.send(embed=discord.Embed(title="Pause",color=ctx.author.color))
        else:
            await ctx.send(embed=discord.Embed(title="Permission denied",description="Join the channel to pause the song",color=ctx.author.color))
    @client.command(aliases=['*'])
    async def change_nickname(ctx,member: discord.Member, *, nickname):
        await member.edit(nick=nickname)
        await ctx.send(embed=discord.Embed(title="Nickname Changed", description=("Nickname changed to "+member.mention+" by "+ctx.author.mention),color=ctx.author.color))
    @client.command()
    async def resume(ctx):
        req()
        mem=[(str(ps.name)+"#"+str(ps.discriminator)) for ps in discord.utils.get(ctx.guild.voice_channels,name=vc_channel[str(ctx.guild.id)]).members]
        if mem.count(str(ctx.author))>0:
            voice=discord.utils.get(client.voice_clients,guild=ctx.guild)
            voice.resume()            
    @client.command()
    async def stop(ctx):
        req()
        mem=[(str(ps.name)+"#"+str(ps.discriminator)) for ps in discord.utils.get(ctx.guild.voice_channels,name=vc_channel[str(ctx.guild.id)]).members]
        if mem.count(str(ctx.author))>0:
            voice=discord.utils.get(client.voice_clients,guild=ctx.guild)
            voice.stop()
            await ctx.send(embed=discord.Embed(title="Stop",color=ctx.author.color))
        else:
            await ctx.send(embed=discord.Embed(title="Permission denied",description="Join the channel to resume the song",color=ctx.author.color))
    @client.command()
    async def clear(ctx,text,num=1000000000000000):
    	req()
    	await ctx.channel.purge(limit=1)
    	if str(text)==re[1]:    		
    		await ctx.channel.purge(limit=num)
    	else:
    		await ctx.send("Wrong password")
    @client.command(aliases=['w'])
    async def wikipedia(ctx,*,text):
    	req()
    	t=str(search(text)[0].encode("utf-8"))    	
    	em=discord.Embed(title=text,description=str(summary(t,sentences=5)),color=ctx.author.color)
    	await ctx.send(embed=em)
    @client.command()
    async def check(ctx):
        req()
        print("check")
        em=discord.Embed(title="Online",description=("Hi, "+str(ctx.author)[0:str(ctx.author).find("#")]),color=ctx.author.color)
        await ctx.send(embed=em)
    @client.command()
    async def test(ctx,*,text):
        mess=await ctx.send("This is a test "+emoji.demojize(text).replace(":",""))
        print()
        await mess.add_reaction("😎")
    @client.event
    async def on_reaction_add(reaction, user):
        req()
        try:
            if reaction.emoji=='😎':
                print("reaction added by "+str(user))
                if str(user)!=str(client.user):
                    await reaction.remove(user)
            if reaction.emoji=='⏮':
                if str(user)!=str(client.user):
                    await reaction.remove(user)
                    req()
                    mem=[(str(ps.name)+"#"+str(ps.discriminator)) for ps in discord.utils.get(reaction.message.guild.voice_channels,name=vc_channel[str(reaction.message.guild.id)]).members]
                    if mem.count(str(user))>0:
                        re[3][str(reaction.message.guild.id)]-=1
                        if re[3][str(reaction.message.guild.id)]==-1:
                            re[3][str(reaction.message.guild.id)]=0                          
                        song=os.path.isfile("."+str(ctx.guild.id)+".mp3")
                        try:
                             if song:
                                 os.remove("."+str(ctx.guild.id)+".mp3")
                        except PermissionError:
                            pass
                        voice=discord.utils.get(client.voice_clients,guild=reaction.message.guild)
                        voice.stop()
                        with youtube_dl.YoutubeDL(ydl_op) as ydl:
                            ydl.download([queue_song[str(reaction.message.guild.id)][re[3][str(reaction.message.guild.id)]]])                    
                        for file in os.listdir("./"):
                            if file.endswith(".mp3"):
                                os.rename(file,"."+str(ctx.guild.id)+".mp3")        
                        voice.play(discord.FFmpegOpusAudio("."+str(reaction.message.guild.id)+".mp3",bitrate=96))
            if reaction.emoji=='⏸':
                if str(user)!=str(client.user):
                    await reaction.remove(user)
                    req()
                    mem=[(str(ps.name)+"#"+str(ps.discriminator)) for ps in discord.utils.get(reaction.message.guild.voice_channels,name=vc_channel[str(reaction.message.guild.id)]).members]
                    if mem.count(str(user))>0:
                        voice=discord.utils.get(client.voice_clients,guild=reaction.message.guild)
                        voice.pause()
            if reaction.emoji=='▶':
                if str(user)!=str(client.user):
                    await reaction.remove(user)
                    req()
                    mem=[(str(ps.name)+"#"+str(ps.discriminator)) for ps in discord.utils.get(reaction.message.guild.voice_channels,name=vc_channel[str(reaction.message.guild.id)]).members]
                    if mem.count(str(user))>0:
                        voice=discord.utils.get(client.voice_clients,guild=reaction.message.guild)
                        voice.resume()
            if reaction.emoji=='🔁':            
                if str(user)!=str(client.user):
                    await reaction.remove(user)
                    mem=[(str(ps.name)+"#"+str(ps.discriminator)) for ps in discord.utils.get(reaction.message.guild.voice_channels,name=vc_channel[str(reaction.message.guild.id)]).members]
                    if mem.count(str(user))>0:
                        if not "."+str(reaction.message.guild.id)+".mp3" in os.listdir():                        
                            with youtube_dl.YoutubeDL(ydl_op) as ydl:
                                ydl.download([queue_song[str(reaction.message.guild.id)][re[3][str(reaction.message.guild.id)]]])
                            for file in os.listdir("./"):
                                if file.endswith(".mp3"):
                                    os.rename(file,"."+str(reaction.message.guild.id)+".mp3")                
                        voice=discord.utils.get(client.voice_clients,guild=reaction.message.guild)
                        voice.stop()
                        voice.play(discord.FFmpegOpusAudio("."+str(reaction.message.guild.id)+".mp3",bitrate=96))
            if reaction.emoji=='⏭':
                if str(user)!=str(client.user):                
                    await reaction.remove(user)
                    req()
                    mem=[(str(ps.name)+"#"+str(ps.discriminator)) for ps in discord.utils.get(reaction.message.guild.voice_channels,name=vc_channel[str(reaction.message.guild.id)]).members]
                    if mem.count(str(user))>0:
                        re[3][str(reaction.message.guild.id)]+=1
                        if re[3][str(reaction.message.guild.id)]>=len(queue_song[str(reaction.message.guild.id)]):
                            re[3][str(reaction.message.guild.id)]=len(queue_song[str(reaction.message.guild.id)])-1                                                  
                        song=os.path.isfile("."+str(reaction.message.guild.id)+".mp3")
                        try:
                             if song:
                                 os.remove("."+str(reaction.message.guild.id)+".mp3")
                        except PermissionError:
                            await ctx.send("Wait or use stop")
                        voice=discord.utils.get(client.voice_clients,guild=reaction.message.guild)
                        voice.stop()
                        with youtube_dl.YoutubeDL(ydl_op) as ydl:
                            ydl.download([queue_song[str(reaction.message.guild.id)][re[3][str(reaction.message.guild.id)]]])
                        
                        for file in os.listdir("./"):
                            if file.endswith(".mp3"):
                                os.rename(file,"."+str(reaction.message.guild.id)+".mp3")        
                        voice.play(discord.FFmpegOpusAudio("."+str(reaction.message.guild.id)+".mp3",bitrate=96))
            if reaction.emoji=="⏹":
                req()                    
                try:
                    if str(user)!=str(client.user):
                        await reaction.remove(user)
                        mem=[(str(ps.name)+"#"+str(ps.discriminator)) for ps in discord.utils.get(reaction.message.guild.voice_channels,name=vc_channel[str(reaction.message.guild.id)]).members]
                        if mem.count(str(user))>0:
                            vc_channel[str(reaction.message.guild.id)]=""
                            voice=discord.utils.get(client.voice_clients,guild=reaction.message.guild)
                            voice.stop()
                            await voice.disconnect()
                            try:
                                os.remove("./."+str(reaction.message.guild.id)+".mp3")
                            except:
                                pass
                except Exception as e:
                    channel=discord.utils.get(reaction.message.guild.channels,name='devop')
                    await channel.send(embed=discord.Embed(title="Error", description=e,color=discord.Color.from_rgb(255,0,0)))
            if str(user) in dev_users:
                global dev_channel
                channel=client.get_channel(dev_channel)
                if reaction.emoji=="📊":
                    await reaction.remove(user)
                    cpu_per=str(int(psutil.cpu_percent()))
                    cpu_freq=str(int(psutil.cpu_freq().current))+"/"+str(int(psutil.cpu_freq().max))
                    ram=str(psutil.virtual_memory().percent)
                    swap=str(psutil.swap_memory().percent)
                    usage="CPU Percentage: "+cpu_per+"%\nCPU Frequency: "+cpu_freq+"\nRAM Usage: "+ram+"%\nSwap Usage: "+swap+"%"
                    await channel.send(embed=discord.Embed(title="Load",description=usage,color=discord.Color.from_rgb(0,0,0)))
                if reaction.emoji==emoji.emojize(":safety_vest:"):
                    await reaction.remove(user)
                    print("recover")
                    load_from_file(".recover.txt")
                    await channel.send(embed=discord.Embed(title="Recover",description="Recovery done",color=discord.Color.from_rgb(0,0,0)))
                if reaction.emoji=="⭕":
                    await reaction.remove(user)
                    text_servers=""
                    for i in client.guilds:
                        text_servers=text_servers+str(i.name)+"\n"                
                    await channel.send(embed=discord.Embed(title="Servers",description=text_servers,color=discord.Color.from_rgb(0,0,0)))
                if reaction.emoji=="🔥":
                    try:
                        voice=discord.utils.get(client.voice_clients,guild=reaction.message.guild)
                        voice.stop()
                        await voice.disconnect()
                    except:
                        pass                    
                    save_to_file()
                    print("Restart "+str(user))
                    await channel.purge(limit=100000000)
                    os.system("nohup python /home/alvinbengeorge/OneDrive/Desktop/others/F/Python/Discord/Discord.py &")           
                    await channel.send(embed=discord.Embed(title="Restart",description=("Requested by "+str(user)),color=discord.Color.from_rgb(255,255,255)))
                    sys.exit()
                if reaction.emoji=="❌":
                    await reaction.remove(user)
                    try:
                        voice=discord.utils.get(client.voice_clients,guild=reaction.message.guild)
                        voice.stop()
                        await voice.disconnect()
                    except:
                        pass
                    await channel.purge(limit=10000000000)
                    await channel.send(embed=discord.Embed(title="Exit",description=("Requested by "+str(user)),color=discord.Color.from_rgb(255,255,255)))                
                    sys.exit()
                if reaction.emoji==emoji.emojize(":satellite:"):
                    string=""
                    await reaction.remove(user)
                    await channel.send("Starting speedtest")
                    download_speed=int(st_speed.download())//1024//1024
                    upload_speed=int(st_speed.upload())//1024//1024
                    servers=st_speed.get_servers([])
                    ping=st_speed.results.ping
                    await channel.send(embed=discord.Embed(title="Speedtest Results:", description=str(download_speed)+"Mbps\n"+str(upload_speed)+"Mbps\n"+str(ping)+"ms", color=discord.Color.from_rgb(255,255,255)))
                if reaction.emoji=="❕":
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
                    await channel.send(embed=discord.Embed(title="Issues with the program", description=issues, color=discord.Color.from_rgb(255,255,255)))
                if reaction.emoji==emoji.emojize(":black_circle:"):
                    await channel.purge(limit=10000000000000000000)
                    text_dev="You get to activate and reset certain functions in this channel \n" \
                    ""+(emoji.emojize(":safety_vest:"))+" for recovery \n"  \
                    "⭕ for list of all servers \n" \
                    "❌ for exiting \n" \
                    "🔥 for restart\n" \
                    "📊 for current load\n" \
                    "❕ for current issues\n" \
                    ""+emoji.emojize(":satellite:")+" for speedtest\n" \
                    ""+emoji.emojize(":black_circle:")+" for clear screen\n"
                    mess=await channel.send(embed=discord.Embed(title="DEVOP",description=text_dev,color=discord.Color.from_rgb(255,255,255)))
                    await mess.add_reaction(emoji.emojize(":safety_vest:"))
                    await mess.add_reaction("⭕")
                    await mess.add_reaction("❌")
                    await mess.add_reaction("🔥")
                    await mess.add_reaction("📊")
                    await mess.add_reaction("❕")
                    await mess.add_reaction(emoji.emojize(":satellite:"))
                    await mess.add_reaction(emoji.emojize(":black_circle:"))
        except Exception as e:
            channel = client.get_channel(834624717410926602)
            await channel.send(embed=discord.Embed(title="Error", description=e, color=discord.Color.from_rgb(255,255,255)))
    @client.command()
    async def yey(ctx):
        req()
        print("yey")
        em=discord.Embed(title="*yey*")
        await ctx.send(embed=em)    
    @client.command(aliases=['g'])
    async def google(ctx,*,text):
        req()
        print(text, str(ctx.author))
        li="**"+text+"** \n\n"
        for i in googlesearch.search(text,num=7,stop=7,pause=0):
            li=li+i+" \n\n"
        text=text.replace(' ','%20')
        li=li+"**Query link:**https://www.google.com/search?q="+text+"\n"
        await ctx.send(li)    
    @client.command(aliases=['cen'])
    async def add_censor(ctx,*,text):
        req()
        string=""
        censor.append(text.lower())
        for i in range(0,len(text)):
            string=string+"-"
        em=discord.Embed(title="Added "+string+" to the list",decription="Done",color=ctx.author.color)
        await ctx.send(embed=em)
    @client.event
    async def on_message(msg):
        try:
            for word in censor:
                if word in msg.content.lower():
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
            if msg.content.find("'")==0:
                save_to_file()
                if len(entr)==0:
                    load_from_file(".recover.txt")
            if start_time%60>30 and start_time%60<50 and len(entr)!=0 and len(queue_song)!=0 and len(da1)!=0:
                save_to_file("recover")
            await client.process_commands(msg)
        except Exception as e:
            channel = discord.utils.get(ctx.guild.channels, name="devop")
            await channel.send(embed=discord.Embed(title="Error", description=e, color=ctx.author.color))
    @client.command()
    async def thog(ctx,*,text):
        if re[1]==text:
            re[4]=re[4]*-1
            if re[4]==1:
                await ctx.send(embed=discord.Embed(title="Thog",description="Activated",color=ctx.author.color))
            else:
                await ctx.send(embed=discord.Embed(title="Thog",description="Deactivated",color=ctx.author.color))
        else:
            await ctx.channel.purge(limit=1)
            await ctx.send("Wrong password")
    @client.command(aliases=['m'])
    async def meth(ctx,*,text):
        req()
        global dev_users
        if (str(text).find("username")==-1 and str(text).find("os")==-1 and str(text).find("ctx")==-1 and str(text).find("import")==-1 and str(text).find("sys")==-1 and str(text).find("psutil")==-1 and str(text).find("clear")==-1 and str(text).find("dev_users")==-1 and str(text).find("remove")==-1) or (str(ctx.author) in dev_users and str(text).find("reboot")==-1 and str(text).find("shut")==-1):
            pi=ma.pi
            try:
                a=eval(text)
                text=text.replace("ma.","")
                text=text.replace("s.","")        
                print(text)
                em=discord.Embed(title=text,description=text+"="+str(a),color=ctx.author.color)
                await ctx.send(embed=em)
            except Exception as e:
                await ctx.send(embed=discord.Embed(title="Error_message",description=str(e),color=ctx.author.color))            
        else:
            await ctx.channel.purge(limit=1)
            await ctx.send(embed=discord.Embed(title="Permission denied",description="",color=ctx.author.color))
    @client.command()
    async def get_req(ctx):
        req()
        number=g_req()
        em=discord.Embed(title="Requests",description=str(number),color=ctx.author.color)
        await ctx.send(embed=em)    
    def r(x):
        return ma.radians(x)
    def d(x):
        return ma.degrees(x)
    def add(p1,p2):
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
    def quad(eq):
        if "x^2" not in eq:
            return "x^2 not found, try again"
        print(eq)
        eq=eq.replace("2+","2 + ")
        eq=eq.replace("2-","2 - ")
        eq=eq.replace("x+","x + ")
        eq=eq.replace("x-","x - ")
        
        #try to get correct equation
        parts = [x.strip() for x in eq.split(" ")]
        a, b, c = 0, 0, 0
        for i in parts:
            if i==' ':
                parts.remove(' ')
        
        for index, part in enumerate(parts):
            if part in ["+", "-"]:
                continue
            
            symbol = -1 if index - 1 >= 0 and parts[index - 1] == "-" else 1

            if part.endswith("x^2"):
                coeff = part[:-3]
                a = float(coeff) if coeff != '' else 1
                a *= symbol
            elif part.endswith("x"):
                coeff = part[:-1]
                b = float(coeff) if coeff != '' else 1
                b *= symbol
            elif part.isdigit():
                c = symbol * float(part)

        determinant = b**2 - (4 * a * c)

        if determinant < 0:
            return "Not Real"
        if determinant == 0:
            root = -b / (2 * a)
            return "Equation has one root:"+str(root) 
 
        if determinant > 0:
            determinant = determinant ** 0.5
            root1 = (-b + determinant) / (2 * a)
            root2 = (-b - determinant) / (2 * a)
            return "This equation has two roots: "+str(root1)+","+str(root2)
	
        
    @client.command()
    async def p(ctx,*,text):
        req()
        print("P"+text)
        a=eval(text)
        ans=ma.factorial(a[0])/ma.factorial(a[0]-a[1])
        em=discord.Embed(title="P"+text+":",description=str(ans),color=ctx.author.color)
        await ctx.send(embed=em)
    @client.command()
    async def c(ctx,*,text):
        req()
        print("c"+text)
        a=eval(text)
        ans=ma.factorial(a[0])/(ma.factorial(a[1])*ma.factorial(a[0]-a[1]))
        em=discord.Embed(title="C"+text+":",description=str(ans),color=ctx.author.color)
        await ctx.send(embed=em)
    @client.command(aliases=['mu'])
    @commands.has_permissions(kick_members=True)
    async def mute(ctx,member:discord.Member):
    	req()
    	add_role=discord.utils.get(ctx.guild.roles,name="dunce")
    	await member.add_roles(add_role)
    	await ctx.send("Muted "+member.mention)
    	print(member,"muted")
    @client.command(aliases=['um'])
    @commands.has_permissions(kick_members=True)
    async def unmute(ctx,member:discord.Member):
    	req()
    	add_role=discord.utils.get(ctx.guild.roles,name="dunce")
    	await member.remove_roles(add_role)
    	await ctx.send("Unmuted "+member.mention)
    	print(member,"unmuted")	
    te="**Commands**\n'google <text to search> \n'help to get this screen\n'c (n,r) for *combination* \n'p (n,r) for *permutation* \n**Leave space between p/c and the bracket'('** \n'meth <Expression> for any math calculation *(includes statistic)*\n'get_req for no. of requests\n" \
    "**Modules**:\n**ma** for math module\n**s** for statistics module \n\nr(angle in degree) to convert angle to radian \nd(angle in radian) to convert angle to radian\n\n" \
    "**Alias**: \n'g <text to search> \n'h to show this message \n'm <Expression> for any math calculation *(includes statistic)*\n'> for next\n'< for previous\n'cm for connecting to a voice\n\n" \
    "**Example**:\n'm quad('4x^2+2x-3')\n'p (10,9) \n'm ma.sin(r(45))\n'm ma.cos(pi)\n'help\n**Use small letters only**\n" \
    "**Updates**:\n Alfred now supports MySQL\n\n" \
    "**MUSIC**:\n'connect_music <channel_name> to connect the bot to the voice channel\n'song <song name> to play song without adding to the queue\n'queue <song name> to add a song to the queue 'play <index no.> to play certain song from the queue list\n" \
    "'addplaylist <Playlist name> to append the current queue to the playlist\n'addqueue <Playlist name> to add\n'clearqueue to clear the queue\n'resume,'pause\n" \
    "'currentmusic for current song's index.\n\n" \
    "_Note: 'again' command does not support 'song' command._"
    client.remove_command("help")
    @client.group(invoke_without_command=True)
    async def help(ctx):
        req()
        print("help")
        em=discord.Embed(title="**HELP** \n",description=te,color=ctx.author.color)   
        await ctx.send(embed=em)
    @client.group(invoke_without_command=True)
    async def h(ctx):
        req()
        print("help")
        em=discord.Embed(title="**HELP** \n",description=te,color=ctx.author.color)
        await ctx.send(embed=em)
    client.run("token")
