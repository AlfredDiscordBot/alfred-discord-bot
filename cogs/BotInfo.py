import nextcord
import time
import io
import traceback
import utils.assets as assets
import utils.External_functions as ef
import utils.helping_hand as helping_hand
from nextcord.ext import commands

# Use nextcord.slash_command()


def requirements():
    return ['dev_channel', 'start_time']


class BotInfo(commands.Cog):
    def __init__(self, client, dev_channel, start_time):
        self.client = client
        self.start_time = start_time
        self.re = self.client.re
        self.dev_channel = dev_channel
        self.embe = []
        self.index = []

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
                description="I left this guild",
                footer=f"Currently in {len(self.client.guilds)} servers | {len(self.client.users)} Users",
                color=self.client.re[8],
                thumbnail=self.client.user.avatar.url
            )
        )

    @commands.command(aliases=["hi", "ping"])
    @commands.check(ef.check_command)
    async def check(self, ctx):
        self.client.re[0]+=1
        print("check")
        emo = assets.Emotes(self.client)
        r = self.client.re[0]
        em = ef.cembed(
            title=f"Online {emo.check}",
            description=f"Hi, {getattr(ctx, 'author', getattr(ctx, 'user', None)).name}\nLatency: \t{int(self.client.latency*1000)}ms\nRequests: \t{r:,}\nUptime: {int(time.time()-self.start_time):,}s\nReady: {self.client.is_ready()}",
            color=self.client.re[8],
            footer="Have fun, bot has many features, check out /help",
            thumbnail=self.client.user.avatar.url,
            author=self.client.user
        )
        permissions1 = "`"*3+"diff\n+ "+'\n+ '.join(
            [i[0] for i in ctx.guild.get_member(self.client.user.id).guild_permissions if i[1]]
        )+"\n"+"`"*3+"\n\n"        
        permissions2 = "`"*3+"diff\n- "+'\n- '.join(
            [i[0] for i in ctx.guild.get_member(self.client.user.id).guild_permissions if not i[1]]
        )+"\n"+"`"*3+"\n\n"
        
        em.add_field(name="Allowed", value=permissions1, inline=False)
        em.add_field(name="Denied", value=permissions2, inline=False)
        await ctx.send(embed=em)

    @nextcord.slash_command(name="bot", description="Contains information about the bot")
    async def botinfo(self, inter):
        print(inter.user)    
    
    @nextcord.slash_command(name="check", description="Check if the bot is online")
    async def check_slash(self, inter):
        await self.check(inter)

    @botinfo.subcommand(name="neofetch", description="Get Status of the bot")
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
        await ctx.send(
            embed=assets.vote_embed(self.client)
        )
    
    @botinfo.subcommand("vote",description="Vote for Alfred in Bot Listing servers")
    async def vo(self, inter):
        await self.vote_alfred(inter)

    @commands.command(aliases=['h','alfred'])
    async def help(self, ctx, *, text = "<Optional>"):
        self.client.re[0]+=1
        try:
            if len(self.embe) < 30:
                self.embe = helping_hand.help_him(self.client, self.client.re)
                new_embed = ef.cembed(
                    title='Index',
                    description="Type `help <section>` to get to the help page\n```diff\n"+"\n+ ".join([i.title for i in self.embe])+"\n```",
                    color=self.client.re[8]
                )
                self.embe.insert(1, new_embed)
                self.index = [i.title for i in self.embe]
            if text in self.index:                
                n  = self.index.index(text)
                await assets.pa(ctx,[self.embe[n]],restricted=True)
            elif text in [i.name for i in self.client.commands]:
                prefix = self.client.prefix_dict.get(ctx.guild.id, "'")
                i=self.client.get_command(text)
                embed=ef.cembed(
                    title=i.name,
                    description=f"`{prefix}{i.name} {i.signature}`",
                    color=self.client.re[8]
                )
                embed.set_author(name=self.client.user.name, icon_url = self.client.user.avatar.url)
                await ctx.send(embed=embed)
            else:
                n = 0
                await assets.pa(ctx, self.embe, start_from=n, restricted=True)
        except Exception:
            print(traceback.format_exc())
    
    @nextcord.slash_command(name="help", description="Help from Alfred")
    async def help_slash(self, inter, text = None):    
        await inter.response.defer()        
        await self.help(inter, text = text)

    @help_slash.on_autocomplete("text")
    async def auto_com(self, inter, text):
        if len(self.embe) < 30:
            self.embe = helping_hand.help_him(self.client, self.client.re)
            new_embed = ef.cembed(
                title='Index',
                description="Type `help <section>` to get to the help page\n```diff\n"+"\n+ ".join([i.title for i in self.embe])+"\n```",
                color=self.client.re[8],
                thumbnail=self.client.user.avatar.url
            )
            self.embe.insert(1, new_embed)
            self.index = [i.title for i in self.embe]
        autocomp_help = [str(i) for i in list(self.index)+list(self.client.commands) if text.lower() in str(i).lower()][:25]
        await inter.response.send_autocomplete(autocomp_help)

    @botinfo.subcommand(name="serverinfo",description="Get your server information")
    async def serverinfo(self, inter):
        await inter.response.defer()
        g = inter.guild
        b = f"{len(g.bots)} Bots"
        h = f"{len(g.humans)} Humans"
        m = f"{len(g.members)} Total members"
        r = "\n\n**Roles:**\n"+', '.join([i.mention for i in g.roles])
        emos = "\n\n**Emojis:**\n"+''.join([str(i) for i in g.emojis])
        description=g.description if g.description else ""
        embed=ef.cembed(
            title=g.name,
            description=description+emos,
            thumbnail=ef.safe_pfp(g),
            image=g.banner if g.banner else "",
            color=self.client.re[8],
            footer=f"{b} | {h} | {m}"
        )
        boost = assets.Emotes(self.client).boost
        boosts = str(boost)*inter.guild.premium_tier + f" {inter.guild.premium_subscription_count}"
        embed.add_field(name="Owner", value=str(g.owner))
        embed.add_field(name="Server ID", value=str(g.id))
        created = nextcord.utils.format_dt(g.created_at,"r").replace(":r","")
        embed.add_field(name="Created at", value=created)
        embed.add_field(name="Boosts", value=boosts)
        embed1 = ef.cembed(
            title=g.name,
            description=r,
            color=self.client.re[8],
            thumbnail=ef.safe_pfp(g),
            footer=f"{len(g.roles)} Roles"
        )
        await assets.pa(inter, [embed, embed1])

    @commands.Cog.listener()
    async def on_message(self, msg):        
        if f"<@{self.client.user.id}>" in msg.content:
            print("Listening")
            prefi = self.client.prefix_dict.get(msg.guild.id if msg.guild is not None else None, "'")
            embed = nextcord.Embed(
                title="Hi!! I am Alfred.",
                description=f"""Prefix is {prefi}\nFor more help, type {prefi}help""",
                color=nextcord.Color(value=self.client.re[8]),
            )
            await msg.channel.send(embed=embed)

    @nextcord.message_command()
    async def view_raw(self, inter, message):
        a = message.clean_content.replace("`","\\`")
        await inter.response.send_message(
            f"```\n{a}\n```",
            ephemeral = True
        )

    @commands.command(name="view_raw", aliases = ['vr'])
    async def raw(self, ctx):
        a = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        a = a.clean_content.replace("`","\\`")
        
        all_embeds = ['']
        for i in a.split("\n"):
            if i[0]%30:
                all_embeds.append('')
            all_embeds[-1]+=i[1]+"\n"
            
        for i in all_embeds:
            await ctx.send(f"```\n{a}\n```")

    @botinfo.subcommand(name="learn", description="How alfred works")
    async def learn_slash(self, inter):
        await self.learn(inter)
        
    @commands.command()
    async def learn(self, ctx):
        embeds = []
        with open("Learn.md", "r") as f:
            l = f.read().replace(
                "- ",
                "⋅ "
            ).split("\n\n")
            j = l[:8]
            j.append("\n\n".join(l[8:]))
            a=0
            for i in j:
                a+=1
                embed = ef.cembed(
                    title="Learn", 
                    color=self.client.re[8], 
                    description=i, 
                    footer=f"{a} of {len(j)}"
                )
                embeds.append(embed)
        await assets.pa(ctx, embeds)

    @nextcord.slash_command(
        name="license", 
        description="View Alfred's Open Source License"
    )
    async def license(self, inter):
        with open("LICENSE", "r") as f:
            await inter.response.send_message(
                ephemeral=True,
                embed=ef.cembed(
                    title="LICENSE",
                    description=f"```\n{f.read()}\n```",
                    color=self.client.re[8],
                    thumbnail=self.client.user.avatar.url,
                    url="https://www.github.com/alvinbengeorge/alfred-discord-bot"
                )
            )

    @botinfo.subcommand(name="contribution", description="Alfred contributors")
    async def contrib_slash(self, inter):
        await inter.response.defer()
        await self.contribution(inter)

    @commands.command(aliases = ['developers','dev','contributors'])
    @commands.check(ef.check_command)
    async def contribution(self, ctx):
        embed=ef.cembed(
            title="Contributors and Contributions",
            description="Hey guys, if you've been Developers of Alfred, Thank you very much for your contribution in this project. Our intend for this project was openness and we've gained it, I would like to thank everyone who is seeing this message, and thank you for accepting Alfred. Alfred crossed 250 servers recently, has more than 250,000 users.\n\nIf you want to take part in this, go to our [github page](https://www.github.com), here you can check our code and fork the repository and add a function and send us a PR. If you wish to know more about Alfred, use the feedback command",
            color = self.client.re[8],
            footer = "Have a great day",
            thumbnail = self.client.user.avatar.url,
            image="attachment://contrib.png"
        )
        fp = ef.svg2png("https://contrib.rocks/image?repo=alvinbengeorge/alfred-discord-bot")
        file = nextcord.File(io.BytesIO(fp), 'contrib.png')
        await ctx.send(file=file, embed=embed)

    @commands.command()
    async def get_invite(self, ctx, time:int=300):
        link = await ctx.channel.create_invite(max_age=time)
        await ctx.send(
            embed=ef.cembed(
                title="Invitation link",
                description=str(link),
                color=self.client.re[8],
            )
        )

    @commands.command(aliases=["s_e"])
    @commands.check(ef.check_command)
    async def search_emoji(self, ctx, name):
        try:
            st = ""
            for i in self.client.emojis:
                if name in i.name:
                    st += f"{i.name} -> {str(i)} -> `{i.id}`\n"
            embed=ef.cembed(
                title="Emojis found",
                description=st,
                color=self.re[8],
                thumbnail=self.client.user.avatar.url,
                footer=f"Search results for {name}"
            )
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(
                embed=ef.cembed(
                    description=str(e), 
                    color=self.client.re[8]
                )
            )

            
def setup(client, **i):
    client.add_cog(BotInfo(client, **i))
    