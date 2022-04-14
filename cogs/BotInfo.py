import nextcord
import assets
import time
import helping_hand
import assets
import External_functions as ef
from nextcord.ext import commands, tasks

#Use nextcord.slash_command()

def requirements():
    return ['dev_channel', 'start_time']

class BotInfo(commands.Cog):
    def __init__(self, client, dev_channel, start_time):
        self.client = client
        self.start_time = start_time
        self.re = self.client.re
        self.dev_channel = dev_channel

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        channel = self.client.get_channel(self.dev_channel)
        await channel.send(
            embed=ef.cembed(
                title=guild.name,
                description=f"{len(guild.members)-1} Lucky Member(s) Found",
                color=self.client.re[8],
                thumbnail=self.client.user.avatar.url,
                footer=f"Currently in {len(self.client.guilds)} servers | {len(self.client.users)} Users"
            )
        )

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        channel = self.client.get_channel(self.dev_channel)
        await channel.send(
            embed=ef.cembed(
                title=guild.name,
                description=f"I left this guild",
                footer=f"Currently in {len(self.client.guilds)} servers | {len(self.client.users)} Users",
                color=self.client.re[8],
                thumbnail=self.client.user.avatar.url
            )
        )

    @commands.command()
    async def cogs_check(self, ctx):
        await ctx.reply("This works")

    @commands.command(aliases=["hi","ping"])
    async def check(self,ctx):
        self.client.re[0]+=1
        print("check")
        emo = assets.Emotes(self.client)
        r = self.client.re[0]
        em = ef.cembed(
            title=f"Online {emo.check}",
            description=f"Hi, {getattr(ctx, 'author', getattr(ctx, 'user', None)).name}\nLatency: \t{int(self.client.latency*1000)}ms\nRequests: \t{r:,}\nAwake time: {int(time.time()-self.start_time):,}s",
            color=self.client.re[8],
            footer="Have fun, bot has many features, check out /help",
            thumbnail = self.client.user.avatar.url
        )
        await ctx.send(embed=em)
    
    
    @nextcord.slash_command(name="check", description="Check if the bot is online")
    async def check_slash(self,inter):
        await self.check(inter)

    @nextcord.slash_command(name="neofetch", description="Get Status of the bot")
    async def neo(self, inter):
        await inter.response.defer()    
        await self.neofetch(inter)
        
    @commands.command()
    async def neofetch(self, ctx):
        text = helping_hand.neofetch
        text += f"Name    : {self.client.user.name}\n"
        text += f"ID      : {self.client.user.id}\n"
        text += f"Users   : {len(self.client.users)}\n"
        text += f"Servers : {len(self.client.guilds)}\n"
        text += f"Uptime  : {int(time.time()-self.start_time)}\n"
        text += f"Nextcord: {nextcord.__version__}"
        await ctx.send("```yml\n"+text+"\n```")

    @commands.command(aliases=["vote","top.gg",'v'])
    async def vote_alfred(self, ctx):
        upvote = assets.Emotes(self.client).upvote    
        await ctx.send(
            embed=ef.cembed(
                title="Vote for Alfred",
                description=f"`Top.gg:         `>>[{upvote}](https://top.gg/bot/811591623242154046/vote)<<\n`DiscordBotList: `>>[{upvote}](https://discordbotlist.com/bots/811591623242154046/upvote)<<\n`Botsfordiscord: `>>[{upvote}](https://botsfordiscord.com/bot/811591623242154046/vote)<<\n`Batcave Top.gg: `>>[{upvote}](https://top.gg/servers/822445271019421746/vote)<<",
                color=self.client.re[8],
                thumbnail=self.client.user.avatar.url,
                image = "https://previews.123rf.com/images/aquir/aquir1311/aquir131100570/24053063-voz-del-sello-del-grunge-rojo.jpg",
                footer="Stay Safe and be happy | Gotham Knights"
            )
        )
    
    @nextcord.slash_command("vote",description="Vote for Alfred in Bot Listing servers")
    async def vo(self, inter):
        await self.vote_alfred(inter)

        
def setup(client,**i):
    client.add_cog(BotInfo(client,**i))