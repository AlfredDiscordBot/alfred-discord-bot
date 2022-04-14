import nextcord
import assets
import time
import helping_hand
import External_functions as ef
import emoji
import asyncio

from nextcord.abc import GuildChannel
from nextcord import Interaction, SlashOption, ChannelType
from nextcord.ext import commands, tasks
from random import choice

#Use nextcord.slash_command() and commands.command()

def requirements():
    return ['dev_channel']

class Music(commands.Cog):
    def __init__(self, client, dev_channel):
        self.client = client
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
    async def pause(self, ctx):
        self.re[0]+=1
        user = getattr(ctx, 'author', getattr(ctx, 'user', None))
        mem = [i.id for i in ctx.guild.voice_client.channel.members] if ctx.guild.voice_client else []
        embed = None
        if mem.count(user.id) > 0:
            voice = nextcord.utils.get(self.client.voice_clients, guild=ctx.guild)
            voice.pause()
            url = self.queue_song[str(ctx.guild.id)][re[3][str(ctx.guild.id)]]
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
    async def leave_slash(inter):        
        await self.leave(inter)
    
    
    @commands.command(aliases=["dc"])
    async def leave(self, ctx):
        self.client.re[0]+=1
        mem = [names.id for names in ctx.guild.voice_client.channel.members] if ctx.guild.voice_client else []
        user = getattr(ctx, 'author', getattr(ctx, 'user', None))
        if len(mem) == 1 and mem[0] == client.user.id:
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
            await ef.pa1(embeds,inter,self.client)

    @nextcord.slash_command(name="connect", description="Connect to a voice channel")
    async def connect_slash(self, inter, channel: GuildChannel = ef.defa(ChannelType.voice)):
        await self.connect_music(inter, channel)
    
    
    @commands.command(aliases=["cm",'join','cn','connect'])
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
                    voice = nextcord.utils.get(client.voice_clients, guild=ctx.guild)
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
                    title="Hmm", description=str(e), color=nextcord.Color(value=self.re[8])
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

                
def setup(client,**i):
    client.add_cog(Music(client,**i))