import discord
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
if True:
    client=commands.Bot(command_prefix="'")
    @client.event
    async def on_ready():
        print("Prepared")
    censor=[] 
    da={}
    da1={}
    queue_song=[]
    re=[0,"OK",1,0,-1]
    @client.command(aliases=['cm'])
    async def connect_music(ctx,channel):
        req()
        voiceChannel=discord.utils.get(ctx.guild.voice_channels,name=channel)
        await voiceChannel.connect()
        voice=discord.utils.get(client.voice_clients,guild=ctx.guild)
        await ctx.send("Connected")    
    @client.command()
    async def addto(ctx,mode,*,text):
        req()
        if mode=="playlist":
            add(text,queue_song.copy())
            await ctx.send("Done")
        elif mode=="queue":
            print(len(get_elem(str(text))))
            for i in range(0,len(get_elem(str(text)))):
                link_add=get_elem(str(text))[i]
                aa=str(urllib.request.urlopen(link_add).read().decode())
                starting=aa.find("<title>")+len("<title>")
                ending=aa.find("</title>")        
                name_of_the_song=aa[starting:ending].replace("&#39;","'").replace("Youtube","")
                da1[link_add]=name_of_the_song
                queue_song.append(link_add)
                await ctx.send(embed=discord.Embed(title=name_of_the_song+" added",description="",color=ctx.author.color))
            await ctx.send("Done")
        else:
            await ctx.send("Only playlist and queue")
    @client.command(aliases=['cq'])
    async def clearqueue(ctx):
        req()
        queue_song.clear()
        da1.clear()
        re[3]=0
    @client.command()
    async def remove(ctx,n):
        req()
        await ctx.send(embed=discord.Embed(title="Removed",description=da1[queue_song[int(n)]],color=ctx.author.color))
        del da1[queue_song[int(n)]]
        queue_song.pop(int(n))
    @client.command(aliases=['curr'])
    async def currentmusic(ctx):
        req()
        await ctx.send(embed=discord.Embed(title=str(da1[queue_song[re[3]]]),description="Current index: "+str(re[3]),color=ctx.author.color))
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
        name=name.replace(" ","+")
        sear="https://www.youtube.com/results?search_query="+name
        htm=urllib.request.urlopen(sear)
        video=regex.findall(r"watch\?v=(\S{11})",htm.read().decode())
        url="https://www.youtube.com/watch?v="+video[0]
        aa=str(urllib.request.urlopen(url).read().decode())
        starting=aa.find("<title>")+len("<title>")
        ending=aa.find("</title>")        
        name_of_the_song=aa[starting:ending].replace("&#39;","'").replace("Youtube","")
        print(name_of_the_song,":",url)
        da1[url]=name_of_the_song
        queue_song.append(url)
        st=""
        await ctx.send("Added to queue")
        num=0
        for i in queue_song:
            st=st+str(num)+"."+da1[i]+":"+i+"\n"
            num+=1
        if st=="":st="_Empty_"
        em=discord.Embed(title="Queue",description=st,color=ctx.author.color)
        await ctx.send(embed=em)
    @client.command()
    async def song(ctx,*,name):
        req()
        name=name.replace(" ","+")
        htm=urllib.request.urlopen("https://www.youtube.com/results?search_query="+name)
        video=regex.findall(r"watch\?v=(\S{11})",htm.read().decode())
        url="https://www.youtube.com/watch?v="+video[0]
        aa=str(urllib.request.urlopen(url).read().decode())
        starting=aa.find("<title>")+len("<title>")
        ending=aa.find("</title>")        
        name_of_the_song=aa[starting:ending].replace("&#39;","'").replace("Youtube","")
        print(url)
        song=os.path.isfile("song.mp3")
        try:
             if song:
                 os.remove("song.mp3")
        except PermissionError:
            await ctx.send("Wait or use stop")
        voice=discord.utils.get(client.voice_clients,guild=ctx.guild)

        ydl_op={'format':'bestaudio/best','postprocessors':[{'key':'FFmpegExtractAudio','preferredcodec':'mp3','preferredquality':'320',}],}
        with youtube_dl.YoutubeDL(ydl_op) as ydl:
            ydl.download([url])
        await ctx.send(embed=discord.Embed(title="Song",description="Playing"+name_of_the_song,color=ctx.author.color))
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                os.rename(file,"song.mp3")        
        voice.play(discord.FFmpegOpusAudio("song.mp3",bitrate=320))
    @client.command()
    async def next(ctx):
        req()
        re[3]+=1
        if re[3]>=len(queue_song):
            re[3]=len(queue_song)-1
            await ctx.send(embed=discord.Embed(title="Last song",description="Only "+str(len(queue_song))+" songs in your queue",color=ctx.author.color))                          
        song=os.path.isfile("song.mp3")
        try:
             if song:
                 os.remove("song.mp3")
        except PermissionError:
            await ctx.send("Wait or use stop")
        voice=discord.utils.get(client.voice_clients,guild=ctx.guild)
        voice.stop()
        ydl_op={'format':'bestaudio/best','postprocessors':[{'key':'FFmpegExtractAudio','preferredcodec':'mp3','preferredquality':'320',}],}
        with youtube_dl.YoutubeDL(ydl_op) as ydl:
            ydl.download([queue_song[re[3]]])
        await ctx.send(embed=discord.Embed(title="Playing",description=da1[queue_song[re[3]]],color=ctx.author.color))
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                os.rename(file,"song.mp3")        
        voice.play(discord.FFmpegOpusAudio("song.mp3",bitrate=320))
    @client.command()
    async def previous(ctx):
        req()
        re[3]-=1
        if re[3]==-1:
            re[3]=0
            await ctx.send(embed=discord.Embed(title="First song",description="This is first in queue",color=ctx.author.color))   
        song=os.path.isfile("song.mp3")
        try:
             if song:
                 os.remove("song.mp3")
        except PermissionError:
            await ctx.send("Wait or use stop")
        voice=discord.utils.get(client.voice_clients,guild=ctx.guild)
        voice.stop()
        ydl_op={'format':'bestaudio/best','postprocessors':[{'key':'FFmpegExtractAudio','preferredcodec':'mp3','preferredquality':'320',}],}
        with youtube_dl.YoutubeDL(ydl_op) as ydl:
            ydl.download([queue_song[re[3]]])
        await ctx.send(embed=discord.Embed(title="Playing",description=da1[queue_song[re[3]]],color=ctx.author.color))
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                os.rename(file,"song.mp3")        
        voice.play(discord.FFmpegOpusAudio("song.mp3",bitrate=320))
    @client.command()
    async def play(ctx,ind):
        req()
        re[3]=int(ind)
        song=os.path.isfile("song.mp3")
        try:
             if song:
                 os.remove("song.mp3")
        except PermissionError:
            await ctx.send("Wait or use stop")
        voice=discord.utils.get(client.voice_clients,guild=ctx.guild)
        voice.stop()
        ydl_op={'format':'bestaudio/best','postprocessors':[{'key':'FFmpegExtractAudio','preferredcodec':'mp3','preferredquality':'320',}],}
        with youtube_dl.YoutubeDL(ydl_op) as ydl:
            ydl.download([queue_song[re[3]]])
        await ctx.send(embed=discord.Embed(title="Playing",description=da1[queue_song[re[3]]],color=ctx.author.color))
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                os.rename(file,"song.mp3")        
        voice.play(discord.FFmpegOpusAudio("song.mp3",bitrate=320))
    @client.command()
    async def cont(ctx):
        req()
        await ctx.send(embed=discord.Embed(title="Playing",description=da1[queue_song[re[3]]],color=ctx.author.color))
        voice=discord.utils.get(client.voice_clients,guild=ctx.guild)
        voice.play(discord.FFmpegOpusAudio("song.mp3",bitrate=320))        
    @client.command()
    async def leave(ctx):
        req()
        voice=discord.utils.get(client.voice_clients,guild=ctx.guild)
        await voice.disconnect()
    @client.command()
    async def pause(ctx):
        req()
        voice=discord.utils.get(client.voice_clients,guild=ctx.guild)
        voice.pause()
    @client.command()
    async def resume(ctx):
        req()
        voice=discord.utils.get(client.voice_clients,guild=ctx.guild)
        voice.resume()
    @client.command()
    async def stop(ctx):
        req()
        voice=discord.utils.get(client.voice_clients,guild=ctx.guild)
        voice.stop()
    @client.command()
    async def clear(ctx,*,text):
    	req()
    	await ctx.channel.purge(limit=1)
    	if str(text)==re[1]:    		
    		await ctx.channel.purge(limit=100000)
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
        em=discord.Embed(title="Online",description="Dormammu, I've come to bargain",color=ctx.author.color)
        await ctx.send(embed=em)
    @client.command()
    async def yey(ctx):
        req()
        print("yey")
        em=discord.Embed(title="*yey*")
        await ctx.send(embed=em)    
    @client.command(aliases=['g'])
    async def google(ctx,*,text):
        req()
        print(text)
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
        for word in censor:
            if word in msg.content.lower():
                await msg.delete()
        if "?" in msg.content and re[4]==1:
            await msg.channel.send("thog dont caare")
        await client.process_commands(msg)
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
        pi=ma.pi
        a=eval(text)
        text=text.replace("ma.","")
        text=text.replace("s.","")        
        print(text)
        em=discord.Embed(title=text,description=text+"="+str(a),color=ctx.author.color)
        await ctx.send(embed=em)
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
    def get_q():
        return queue_song
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
    	try:
    		add_role=discord.utils.get(ctx.guild.roles,name="dunce")
    		await member.add_roles(add_role)
    		await ctx.send("Muted "+member.mention)
    		print(member,"muted")
    	except:
    		await ctx.send("Not Done")
    @client.command(aliases=['um'])
    @commands.has_permissions(kick_members=True)
    async def unmute(ctx,member:discord.Member):
    	req()
    	try:
    		add_role=discord.utils.get(ctx.guild.roles,name="dunce")
    		await member.remove_roles(add_role)
    		await ctx.send("Unmuted "+member.mention)
    		print(member,"unmuted")
    	except:
    		await ctx.send("Not Done")     	
    te="**Commands**\n'google <text to search> \n'help to get this screen\n'c (n,r) for *combination* \n'p (n,r) for *permutation* \n**Leave space between p/c and the bracket'('** \n'meth <Expression> for any math calculation *(includes statistic)*\n'get_req for no. of requests\n"
    te=te+"**Modules**:\n**ma** for math module\n**s** for statistics module \n\nr(angle in degree) to convert angle to radian \nd(angle in radian) to convert angle to radian\n\n"
    te=te+"**Alias**: \n'g <text to search> \n'h to show this message \n'm <Expression> for any math calculation *(includes statistic)*\n\n"
    te=te+"**Example**:\n'm quad('4x^2+2x-3')\n'p (10,9) \n'm ma.sin(r(45))\n'm ma.cos(pi)\n'help\n**Use small letters only**"
    te=te+"\n\n\n\n **MUSIC**:\n'connect_music <channel_name> to connect the bot to the voice channel\n'song <song name> to play song without adding to the queue\n'queue <song name> to add a song to the queue 'play <index no.> to play certain song from the queue list\n"
    te=te+"'addplaylist <Playlist name> to append the current queue to the playlist\n'addqueue <Playlist name> to add\n'clearqueue to clear the queue\n'resume,'pause\n"
    te=te+"'currentmusic for current song's index\nI think thats pretty much it."
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
    client.run("ODExNTkxNjIzMjQyMTU0MDQ2.YC0bmQ.4oW1hyppcaQJpRfKFRJCiddZ5aI")
else:
    print("Something has occured")
