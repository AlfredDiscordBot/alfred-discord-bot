import nextcord
import assets
import time
import helping_hand
import External_functions as ef
import emoji
import asyncio
import traceback
import urllib

from nextcord.abc import GuildChannel
from nextcord import Interaction, SlashOption, ChannelType
from nextcord.ext import commands, tasks
from random import choice

#Use nextcord.slash_command() and commands.command()

def requirements():
    return ['dev_channel', 'FFMPEG_OPTIONS']

class Music(commands.Cog):
    def __init__(self, client, dev_channel, FFMPEG_OPTIONS):
        self.client = client
        self.FFMPEG_OPTIONS = FFMPEG_OPTIONS
        self.re = self.client.re
        self.da = self.client.da
        self.da1 = self.client.da1
        self.queue_song = self.client.queue_song
        self.dev_channel = dev_channel

    @nextcord.slash_command(
        name="autoplay",
        description="Plays the next song automatically if its turned on",
    )
    async def autoplay_slash(self, inter):
        await self.autoplay(inter)
    
    @nextcord.slash_command(name="loop", description="Loops the same song")
    async def loop_slash(self, inter):
        await self.loop(inter)

    @commands.command()
    @commands.check(ef.check_command)
    async def autoplay(self, ctx):
        user = getattr(ctx, 'author', getattr(ctx, 'user', None))
        if ctx.guild.voice_client and user.id in [i.id for i in ctx.guild.voice_client.channel.members]:
            st = ""
            self.re[7][ctx.guild.id] = self.re[7].get(ctx.guild.id,-1) * -1
            if self.re[7].get(ctx.guild.id,-1) == 1:
                self.re[2][ctx.guild.id] = -1
            if self.re[7][ctx.guild.id] < 0:
                st = "Off"
            else:
                st = "_On_"
            await ctx.send(
                embed=nextcord.Embed(
                    title="Autoplay", description=st, color=nextcord.Color(value=self.re[8])
                )
            )
        else:
            await ctx.send(
                embed=nextcord.Embed(
                    title="Permissions Denied",
                    description="You need to be in the voice channel with Alfred to toggle autoplay",
                    color=nextcord.Color(value=self.re[8]),
                )
            )
    
    
    @commands.command()
    @commands.check(ef.check_command)
    async def loop(self, ctx):
        user = getattr(ctx, 'author', getattr(ctx, 'user', None))
        if ctx.guild.voice_client and user.id in [i.id for i in ctx.guild.voice_client.channel.members]:
            st = ""
            self.re[2][ctx.guild.id] = self.re[2].get(ctx.guild.id,-1) * -1
            if self.re[2].get(ctx.guild.id,1) == 1:
                self.re[7][ctx.guild.id] = -1
            if self.re[2].get(ctx.guild.id,1) < 0:
                st = "Off"
            else:
                st = "_On_"
            await ctx.send(
                embed=nextcord.Embed(
                    title="Loop", description=st, color=nextcord.Color(value=self.re[8])
                )
            )
        else:
            await ctx.send(
                embed=nextcord.Embed(
                    title="Permissions Denied",
                    description="You need to be in the voice channel to toggle loop",
                    color=nextcord.Color(value=self.re[8]),
                )
            )
            
    @commands.command(aliases=["cq"])
    @commands.check(ef.check_command)
    async def clearqueue(self, ctx):
        mem = [names.id for names in ctx.guild.voice_client.channel.members] if ctx.guild.voice_client else []
        user = getattr(ctx, 'author', getattr(ctx, 'user', None))
        if mem.count(user.id) > 0:
            if len(self.queue_song.get(str(ctx.guild.id),[])) > 0:
                self.queue_song[str(ctx.guild.id)].clear()
            self.re[3][str(ctx.guild.id)] = 0
            await ctx.send(
                embed=ef.cembed(
                    title="Cleared queue",
                    description="_Done_",
                    color=self.re[8],
                    thumbnail=self.client.user.avatar.url
                )
            )
        else:
            await ctx.send(
                embed=nextcord.Embed(
                    title="Permission denied",
                    description="Join the voice channel to modify queue",
                    color=nextcord.Color(value=self.re[8]),
                )
            )

    @commands.command()
    @commands.check(ef.check_command)
    async def pause(self, ctx):
        self.re[0]+=1
        user = getattr(ctx, 'author', getattr(ctx, 'user', None))
        mem = [i.id for i in ctx.guild.voice_client.channel.members] if ctx.guild.voice_client else []
        embed = None
        if mem.count(user.id) > 0:
            voice = nextcord.utils.get(self.client.voice_clients, guild=ctx.guild)
            voice.pause()
            url = self.queue_song[str(ctx.guild.id)][self.client.re[3][str(ctx.guild.id)]]
            song = self.da1.get(url, "Unavailable")
            embed=nextcord.Embed(
                title="Paused",
                description=f"[{song}]({url})",
                color=nextcord.Color(value=self.re[8]),
            )
        else:
            embed=nextcord.Embed(
                title="Permission denied",
                description="Join the channel to pause the song",
                color=nextcord.Color(value=self.re[8]),
            )
        await ef.isReaction(ctx,embed)

    @nextcord.slash_command(name="disconnect", description="Disconnect the bot from your voice channel")
    async def leave_slash(self, inter):        
        await self.leave(inter)
    
    
    @commands.command(aliases=["dc"])
    @commands.check(ef.check_command)
    async def leave(self, ctx):
        self.client.re[0]+=1
        mem = [names.id for names in ctx.guild.voice_client.channel.members] if ctx.guild.voice_client else []
        user = getattr(ctx, 'author', getattr(ctx, 'user', None))
        if len(mem) == 1 and mem[0] == self.client.user.id:
            if user.guild_permissions.administrator:
                user = self.client.user
        if mem.count(user.id) > 0: 
            voice = ctx.guild.voice_client
            voice.stop()
            await voice.disconnect()
            embed=nextcord.Embed(
                title="Disconnected",
                description="Bye, Thank you for using Alfred",
                color=nextcord.Color(value=self.re[8]),
            )            
        else:
            embed=nextcord.Embed(
                title="Permission denied",
                description="Nice try dude! Join the voice channel",
                color=nextcord.Color(value=self.re[8]),
            )
        await ef.isReaction(ctx,embed,clear=True)

    @nextcord.slash_command(name="addto",description="put queue or playlist and it will add the songs to your playlist to queue or queue to playlist")
    async def addto(self, inter, mode = ef.defa(choices=['queue','playlist','show','clear']), from_user:nextcord.User = "-"):
        await inter.response.defer()
        if from_user == '-':
            from_user = inter.user
        if not (inter.user.voice and inter.guild.voice_client): 
            await inter.send("You need to connect to a voice channel")
            return
        if mode == "queue":        
            if from_user.id in list(self.da.keys()):
                self.queue_song[str(inter.guild.id)]+=self.da[from_user.id]
                await inter.send("Added your playlist to queue")
            else:
                await inter.send("You do not have a Playlist")
                return
        if mode == "playlist":
            if inter.user.id not in list(self.da.keys()):
                self.da[inter.user.id] = []
            for i in self.queue_song[str(inter.guild.id)]:
                if i not in self.da[inter.user.id]:
                    self.da[inter.user.id].append(i)
            await inter.send("Added songs in queue to playlist\n*Note: The songs are added uniquely, which means that if a song in queue is repeated in your playlist, then that song wont be added*")
        if mode == "clear":
            if self.da.get(inter.user.id): 
                del self.da[inter.user.id]
                await inter.send("Cleared your playlist")
            else:
                await inter.send("You had no playlist registered")
        if mode == "show":
            l = []
            thumbnail = ef.safe_pfp(from_user)
            songs = self.da.get(from_user.id,[])
            for i in songs:
                if not self.da1.get(i):
                    self.da1[i] = await ef.get_name(i)
                l.append(f"{self.da1.get(i)}\n")            
                
            st = []
            for i in range(len(songs)//10):
                s = i*10
                e = i*10+10
                if e > len(l): e = len(l)
                st.append(''.join(l[s:e]))

            if st == []:
                st = ['This person may not have set a playlist yet']
                
            embeds=[]
            for i in st:
                embed=ef.cembed(
                    title=f"Playlist of {inter.user.name}",
                    description=i,
                    color=self.re[8],
                    thumbnail=thumbnail
                )
                embeds.append(embed)
            await assets.pa(inter, embeds, start_from=0, restricted=False)

    @nextcord.slash_command(name="connect", description="Connect to a voice channel")
    async def connect_slash(self, inter, channel: GuildChannel = ef.defa(ChannelType.voice)):
        await self.connect_music(inter, channel)
    
    
    @commands.command(aliases=["cm",'join','cn','connect'])
    @commands.check(ef.check_command)
    async def connect_music(self, ctx, channel=None):
        if type(channel) == nextcord.channel.VoiceChannel: 
            channel = channel.name
        print("Connect music", str(getattr(ctx, 'author', getattr(ctx, 'user', None))))
        try:
            self.re[0]+=1
            user = getattr(ctx, 'author', getattr(ctx, 'user', None))
            if not str(ctx.guild.id) in self.queue_song:
                self.queue_song[str(ctx.guild.id)] = []
            if not str(ctx.guild.id) in self.re[3]:
                self.client.re[3][str(ctx.guild.id)] = 0
            if channel == None:
                if user.voice and user.voice.channel:
                    channel = user.voice.channel.id
                    voiceChannel = nextcord.utils.get(ctx.guild.voice_channels, id=channel)
                    await voiceChannel.connect()
                    voice = nextcord.utils.get(self.client.voice_clients, guild=ctx.guild)
                    await ctx.send(
                        embed=nextcord.Embed(
                            title="",
                            description="Connected\nBitrate of the channel: "
                            + str(ctx.guild.voice_client.channel.bitrate // 1000),
                            color=nextcord.Color(value=self.re[8]),
                        )
                    )
                else:
                    emo = assets.Emotes(self.client)
                    await ctx.send(
                        embed=nextcord.Embed(
                            description=f"You are not in a voice channel {emo.join_vc}",
                            color=nextcord.Color(value=self.re[8]),
                        )
                    )
            else:
                if channel in [i.name for i in ctx.guild.voice_channels]:
                    voiceChannel = nextcord.utils.get(ctx.guild.voice_channels, name=channel)
                    await voiceChannel.connect()
                    voice = nextcord.utils.get(self.client.voice_clients, guild=ctx.guild)
                    await ctx.send(
                        embed=ef.cembed(
                            title="Connected",
                            description=f"Connected to {voiceChannel.name} \nBitrate of the channel: "
                            + str(ctx.guild.voice_client.channel.bitrate // 1000),
                            color=nextcord.Color(value=self.re[8])
                        )
                    )
                else:
                    await ctx.send(
                        embed=ef.cembed(
                            description="The voice channel does not exist",
                            color=nextcord.Color(value=self.re[8])
                        )
                    )
    
        except Exception as e:
            await ctx.send(
                embed=nextcord.Embed(
                    title="Hmm", 
                    description=str(e), 
                    color=nextcord.Color(value=self.re[8])
                )
            )
            channel = self.client.get_channel(self.dev_channel)
            await channel.send(
                embed=ef.cembed(
                    title="Connect music",
                    description=traceback.format_exc(),
                    footer = f"{getattr(ctx, 'author', getattr(ctx, 'user', None)).name}: {ctx.guild}",
                    color=self.re[8],
                )
            )

    @commands.command(aliases=["s_q"])
    @commands.check(ef.check_command)
    async def search_queue(self,ctx, part):
        st = ""
        index = 0
        found_songs = 0
        for i in self.queue_song[str(ctx.guild.id)]:
            if i in self.da1:
                found_songs += 1
                if self.da1[i].lower().find(part.lower()) != -1:
                    st += str(index) + ". " + self.da1[i] + "\n"
            index += 1
        if st == "":
            st = "Not found"
        if len(self.queue_song[str(ctx.guild.id)]) - found_songs > 0:
            st += "\n\nWARNING: Some song names may not be loaded properly, this search may not be accurate"
            st += "\nSongs not found: " + str(
                len(self.queue_song[str(ctx.guild.id)]) - found_songs
            )
        await ctx.send(
            embed=ef.cembed(
                title="Songs in queue",
                description=st,
                color=self.re[8],
                thumbnail=self.client.user.avatar.url,
            )
        )

    @nextcord.slash_command(name="again", description="Repeat the song")
    async def again_slash(self, inter):
        await inter.response.defer()
        await self.again(inter)
        
    @commands.command()
    @commands.check(ef.check_command)
    async def again(self, ctx):
        self.client.re[0]+=1
        user = getattr(ctx, 'author', getattr(ctx, 'user', None))
        if user.voice and user.voice.channel:
            if not str(ctx.guild.id) in self.queue_song:
                self.queue_song[str(ctx.guild.id)] = []
            if not str(ctx.guild.id) in self.client.re[3]:
                self.client.re[3][str(ctx.guild.id)] = 0
                
            if ctx.guild.voice_client == None:
                voiceChannel = user.voice.channel
                await voiceChannel.connect()
            mem = []
            try:
                try:
                    mem = [i.id for i in ctx.guild.voice_client.channel.members]    
                except:
                    mem = []
                if mem.count(user.id) > 0:
                    voice = ctx.guild.voice_client
                    bitrate = "\nBitrate of the channel: " +str(voice.channel.bitrate // 1000)
                    song = self.queue_song[str(ctx.guild.id)][self.re[3][str(ctx.guild.id)]]
                    if song not in self.da1:
                        self.da1[song] = ef.youtube_info(song)["title"]                
                    URL = ef.youtube_download(ctx, song)
                    voice.stop()
                    voice.play(
                        nextcord.FFmpegPCMAudio(URL, **self.FFMPEG_OPTIONS),
                        after=lambda e: self.repeat(ctx, voice),
                    )
                    embed=ef.cembed(
                        title="Playing",
                        description=self.da1[song] + bitrate,
                        color=self.re[8],
                        thumbnail=self.client.user.avatar.url,
                    )
                    if type(ctx) != nextcord.message: 
                        mess = await ctx.channel.send(embed=embed)
                        await self.player_pages(mess)
                    else:
                        await ef.isReaction(ctx,embed)
                else:
                    emo = assets.Emotes(self.client)
                    embed=ef.cembed(
                        title="Permission denied",
                        description=f"{emo.animated_wrong} Join the voice channel to play the song",
                        color=self.re[8],
                        thumbnail=self.client.user.avatar.url,
                    )
            except Exception as e:
                channel = self.client.get_channel(self.dev_channel)
                await ctx.channel.send(
                    embed=ef.cembed(
                        title="Error",
                        description=str(e),
                        color=self.re[8],
                        thumbnail=self.client.user.avatar.url,
                    )
                )
                await channel.send(
                    embed=nextcord.Embed(
                        title="Error in play function",
                        description=f"{e}\n{ctx.guild.name}: {ctx.channel.name}",
                        color=nextcord.Color(value=self.re[8]),
                    )
                )

    async def player_pages(self, mess):
        await ef.player_reaction(mess)    
        emojis = emoji.emojize(":upwards_button:"),emoji.emojize(":downwards_button:")
        def check(reaction, user):
            return (
                user.id != self.client.user.id
                and str(reaction.emoji) in emojis
                and reaction.message.id == mess.id
            )
        page=self.re[3][str(mess.guild.id)]//10
        while True:
            songs = self.queue_song[str(mess.guild.id)]
            try:
                reaction, user = await self.client.wait_for("reaction_add", check = check, timeout=None)
                if reaction.emoji == emojis[0] and page>0:
                    page-=1
                elif reaction.emoji == emojis[1] and page<=len(songs):
                    page+=1
                cu = page * 10
                st = '\n'.join([f"{i}. {self.da1[songs[i]]}" for i in range(cu,cu+10) if len(songs)>i])
                await mess.edit(
                    embed=ef.cembed(
                        title="Queue",
                        description=st,
                        color=self.re[8],
                        footer='Amazing songs btw, keep going' if len(songs)!=0 else 'Use queue to add some songs'
                    )
                )
                await reaction.remove(user)
            except asyncio.TimeoutError:
                await mess.clear_reactions()

            
    def repeat(self, ctx, voice):
        songs = self.queue_song.get(str(ctx.guild.id),[])
        if len(songs) == 0: return
        index = self.re[3].get(str(ctx.guild.id),0)
        if len(songs)<index:
            index = 0
            self.re[3][str(ctx.guild.id)]=index
        song = songs[index]
        if not song in self.da1.keys():
            aa = str(urllib.request.urlopen(song).read().decode())
            starting = aa.find("<title>") + len("<title>")
            ending = aa.find("</title>")
            self.da1[song] = (
                aa[starting:ending]
                .replace("&#39;", "'")
                .replace(" - YouTube", "")
                .replace("&amp;", "&")
            )
        time.sleep(1)
        if self.re[7].get(ctx.guild.id,-1) == 1 and not voice.is_playing():
            self.re[3][str(ctx.guild.id)] += 1
            if self.re[3][str(ctx.guild.id)] >= len(self.queue_song[str(ctx.guild.id)]):
                self.re[3][str(ctx.guild.id)] = 0
        if self.client.re[2].get(ctx.guild.id,-1) == 1 or self.re[7].get(ctx.guild.id,-1) == 1:
            if not voice.is_playing():
                URL = ef.youtube_download(ctx, song)
                voice.play(
                    nextcord.FFmpegPCMAudio(URL, **self.FFMPEG_OPTIONS),
                    after=lambda e: self.repeat(ctx, voice),
                )    

    @nextcord.slash_command(name = "lyrics", description = "Gets lyrics of a song")
    async def lyrics_slash(self, inter, song):
        await inter.response.defer()
        await inter.send(embed=await ef.ly(song,self.re))
        
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user.bot: return
        if reaction.emoji == "⏸":
            if (
                str(user) != str(self.client.user)
                and reaction.message.author == self.client.user
            ):
                await reaction.remove(user)
                self.re[0]+=1
                reaction.message.author = user
                await self.pause(reaction.message)
        if reaction.emoji == "⏹":
            if (
                str(user) != str(self.client.user)
                and reaction.message.author == self.client.user
            ):
                await reaction.remove(user)
                reaction.message.author = user
                await self.leave(reaction.message)
        if reaction.emoji == "🔁":
            if (
                str(user) != str(self.client.user)
                and reaction.message.author == self.client.user
            ):
                await reaction.remove(user)
                reaction.message.author = user
                await self.again(reaction.message)

                
def setup(client,**i):
    client.add_cog(Music(client,**i))
    