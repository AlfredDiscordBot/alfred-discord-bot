import nextcord
import assets
import time
import helping_hand
import assets
import random
import External_functions as ef
import helping_hand
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

    @commands.command(aliases=["hi","ping"])
    @commands.check(ef.check_command)
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
    @commands.check(ef.check_command)
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

    @commands.command(aliases=['h'])
    async def help(self, ctx):
        self.client.re[0]+=1
        test_help = helping_hand.help_him(ctx, self.client, self.re)
        await assets.pa(ctx, test_help, start_from=0, restricted=True)
    
    @nextcord.slash_command(name="help", description="Help from Alfred")
    async def help_slash(self, inter):    
        await inter.response.defer()
        await self.help(inter)

    @commands.Cog.listener()
    async def on_message(self, msg):
        if f"<@!{self.client.user.id}>" in msg.content:
            prefi = self.client.prefix_dict.get(msg.guild.id if msg.guild is not None else None, "'")
            embed = nextcord.Embed(
                title="Hi!! I am Alfred.",
                description=f"""Prefix is {prefi}\nFor more help, type {prefi}help""",
                color=nextcord.Color(value=self.client.re[8]),
            )
            embed.set_image(
                url=random.choice(
                    [                        "https://giffiles.alphacoders.com/205/205331.gif",
                        "https://c.tenor.com/PQu-tE-5HxwAAAAd/michael-caine-the-dark-knight.gif",
                    ]
                )
            )
            await msg.channel.send(embed=embed)

        
def setup(client,**i):
    client.add_cog(BotInfo(client,**i))