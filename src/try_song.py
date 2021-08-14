def requirements():
    return "queue_song, da1, re"
def main(client, queue_song, da1 ,re):
    import discord
    from discord.ext import commands
    import ffmpeg
    import urllib.request
    import re as regex
    import youtube_dl
    import os
    ydl_op={'format':'bestaudio/best','postprocessors':[{'key':'FFmpegExtractAudio','preferredcodec':'mp3','preferredquality':'320',}],}
    @client.command()
    async def song(ctx,*,name):
        re[0]=re[0]+1
        try:
            mem=[str(names) for names in ctx.voice_client.channel.members]
        except:
            mem=[]
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
            await ctx.send(embed=discord.Embed(title="Song",description="Playing "+name_of_the_song,color=discord.Color(value=re[8])))
            for file in os.listdir("./"):
                if file.endswith(".mp3"):
                    os.rename(file,"."+str(ctx.guild.id)+".mp3")        
            voice.play(discord.FFmpegOpusAudio("."+str(ctx.guild.id)+".mp3",bitrate=320))
        else:
            await ctx.send(embed=discord.Embed(title="Permission denied",description="Join the voice channel to play a song",color=discord.Color(value=re[8])))
