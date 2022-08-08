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
    return ["DEV_CHANNEL", "start_time"]


class BotInfo(
    commands.Cog,
    description="Has Information about the Bot and other commands to see info about your current server, etc.",
):
    def __init__(self, CLIENT, DEV_CHANNEL, start_time):
        self.CLIENT = CLIENT
        self.start_time = start_time
        self.DEV_CHANNEL = DEV_CHANNEL
        self.embe = []
        self.index = []

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        channel = self.CLIENT.get_channel(self.DEV_CHANNEL)
        await channel.send(
            embed=ef.cembed(
                title=guild.name,
                description=f"{len(guild.members)-1} Lucky Member(s) Found",
                color=self.CLIENT.color(guild),
                thumbnail=self.CLIENT.user.avatar.url,
                footer=f"Currently in {len(self.CLIENT.guilds)} servers | {len(self.CLIENT.users)} Users",
                fields=ef.dict2fields({"Member": f"{len(guild.members)} members"}),
            )
        )

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        channel = self.CLIENT.get_channel(self.DEV_CHANNEL)
        await channel.send(
            embed=ef.cembed(
                title=guild.name,
                description="I left this guild",
                footer=f"Currently in {len(self.CLIENT.guilds)} servers | {len(self.CLIENT.users)} Users",
                color=self.CLIENT.color(guild),
                thumbnail=self.CLIENT.user.avatar.url,
                fields=ef.dict2fields({"Member": f"{len(guild.members)} members"}),
            )
        )

    @commands.command(aliases=["hi", "ping"])
    @commands.check(ef.check_command)
    async def check(self, ctx):
        self.CLIENT.re[0] += 1
        print("check")
        emo = assets.Emotes(self.CLIENT)
        r = self.CLIENT.re[0]
        permissions1 = (
            "`" * 3
            + "diff\n+ "
            + "\n+ ".join(
                [
                    i[0]
                    for i in ctx.guild.get_member(self.CLIENT.user.id).guild_permissions
                    if i[1]
                ]
            )
            + "\n"
            + "`" * 3
            + "\n\n"
        )
        permissions2 = (
            "`" * 3
            + "diff\n- "
            + "\n- ".join(
                [
                    i[0]
                    for i in ctx.guild.get_member(self.CLIENT.user.id).guild_permissions
                    if not i[1]
                ]
            )
            + "\n"
            + "`" * 3
            + "\n\n"
        )
        em = ef.cembed(
            title=f"Online {emo.check}",
            description=f"Hi, {getattr(ctx, 'author', getattr(ctx, 'user', None)).name}\nLatency: \t{int(self.CLIENT.latency*1000)}ms\nRequests: \t{r:,}\nUpFrom: <t:{int(self.start_time)}>\nReady: {self.CLIENT.is_ready()}",
            color=self.CLIENT.color(ctx.guild),
            footer="Have fun, bot has many features, check out /help",
            thumbnail=self.CLIENT.user.avatar.url,
            author=self.CLIENT.user,
            fields=ef.dict2fields(
                {"Allowed": permissions1, "Denied": permissions2}, inline=False
            ),
        )
        await ctx.send(embed=em)

    @nextcord.slash_command(
        name="bot", description="Contains information about the bot"
    )
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
        text += f"Name    : {self.CLIENT.user.name}\n"
        text += f"ID      : {self.CLIENT.user.id}\n"
        text += f"Users   : {len(self.CLIENT.users)}\n"
        text += f"Servers : {len(self.CLIENT.guilds)}\n"
        text += f"Uptime  : {int(time.time()-self.start_time)}\n"
        text += f"Nextcord: {nextcord.__version__}"
        await ctx.send("```yml\n" + text + "\n```")

    @commands.command(aliases=["vote", "top.gg", "v"])
    async def vote_alfred(self, ctx):
        await ctx.send(embed=assets.vote_embed(self.CLIENT))

    @botinfo.subcommand("vote", description="Vote for Alfred in Bot Listing servers")
    async def vo(self, inter):
        await self.vote_alfred(inter)

    @commands.command(aliases=["h", "alfred"])
    async def help(self, ctx, *, text="<Optional>"):
        self.CLIENT.re[0] += 1
        self.embe = helping_hand.help_him(self.CLIENT, ctx)
        new_embed = ef.cembed(
            title="Index",
            description="Type `help <section>` to get to the help page\n```diff\n"
            + "\n+ ".join([i.title for i in self.embe])
            + "\n```",
            color=self.CLIENT.color(ctx.guild),
            author=self.CLIENT.user,
            thumbnail=self.CLIENT.user.avatar,
            footer={
                "text": "Here's the list of Cogs in Alfred, why Dont you go through them",
                "icon_url": self.CLIENT.user.avatar,
            },
        )
        self.embe.insert(1, new_embed)
        self.index = [i.title for i in self.embe]
        if text in self.index:
            n = self.index.index(text)
            await assets.pa(ctx, [self.embe[n]], restricted=True)
        elif text in [i.name for i in self.CLIENT.commands]:
            prefix = self.CLIENT.prefix_dict.get(ctx.guild.id, "'")
            i = self.CLIENT.get_command(text)
            embed = ef.cembed(
                title=i.name,
                description=f"`{prefix}{i.name} {i.signature}`",
                color=self.CLIENT.color(ctx.guild),
                author=self.CLIENT.user,
            )
            await ctx.send(embed=embed)
        else:
            n = 0
            await assets.pa(ctx, self.embe, start_from=n, restricted=True, t="sb")

    @nextcord.slash_command(name="help", description="Help from Alfred")
    async def help_slash(self, inter, text=None):
        await inter.response.defer()
        await self.help(inter, text=text)

    @help_slash.on_autocomplete("text")
    async def auto_com(self, inter, text):
        if len(self.embe) < 30:
            self.embe = helping_hand.help_him(self.CLIENT)
            new_embed = ef.cembed(
                title="Index",
                description="Type `help <section>` to get to the help page\n```diff\n"
                + "\n+ ".join([i.title for i in self.embe])
                + "\n```",
                color=self.CLIENT.color(inter.guild),
                thumbnail=self.CLIENT.user.avatar.url,
            )
            self.embe.insert(1, new_embed)
            self.index = [i.title for i in self.embe]
        autocomp_help = [
            str(i)
            for i in list(self.index) + list(self.CLIENT.commands)
            if text.lower() in str(i).lower()
        ][:25]
        await inter.response.send_autocomplete(autocomp_help)

    @botinfo.subcommand(name="serverinfo", description="Get your server information")
    async def serverinfo(self, inter):
        await inter.response.defer()
        g = inter.guild
        b = f"{len(g.bots)} Bots"
        h = f"{len(g.humans)} Humans"
        m = f"{len(g.members)} Total members"
        r = "\n\n**Roles:**\n" + ", ".join([i.mention for i in g.roles])
        emos = "\n\n**Emojis:**\n" + "".join([str(i) for i in g.emojis[:50]])
        description = g.description if g.description else ""
        boost = assets.Emotes(self.CLIENT).boost
        boosts = (
            str(boost) * inter.guild.premium_tier
            + f" {inter.guild.premium_subscription_count}"
        )
        embed = ef.cembed(
            title=g.name,
            description=description,
            thumbnail=ef.safe_pfp(g),
            image=g.banner if g.banner else "",
            color=self.CLIENT.color(inter.guild),
            footer=f"{b} | {h} | {m}",
            fields=ef.dict2fields(
                {
                    "Owner": g.owner.mention,
                    "Server ID": g.id,
                    "Created_at": nextcord.utils.format_dt(g.created_at),
                    "Boosts": boosts,
                }
            ),
            author=g.owner,
        )
        embed1 = ef.cembed(
            title=g.name,
            description=r,
            color=self.CLIENT.color(g),
            thumbnail=ef.safe_pfp(g),
            footer=f"{len(g.roles)} Roles",
            author=g.owner,
        )
        embed2 = ef.cembed(
            title=f"Emojis of {g.name}",
            description=emos,
            color=self.CLIENT.color(g),
            author=g.owner,
            thumbnail=ef.safe_pfp(g),
            footer=f"{len(g.emojis)} Emojis",
        )
        await assets.pa(inter, [embed, embed1, embed2])

    @commands.Cog.listener()
    async def on_message(self, msg):
        if f"<@{self.CLIENT.user.id}>" in msg.content:
            print("Listening")
            prefi = self.CLIENT.prefix_dict.get(
                msg.guild.id if msg.guild is not None else None, "'"
            )
            embed = ef.cembed(
                title="Hi!! I am Alfred.",
                description=f"""Prefix is `{prefi}`\nFor more help, type `{prefi}help`""",
                color=self.CLIENT.color(msg.guild),
                author=self.CLIENT.user,
                thumbnail=self.CLIENT.user.avatar,
                fields={
                    "Stats": ef.dict2str(
                        {
                            "Servers ": len(self.CLIENT.guilds),
                            "Users   ": len(self.CLIENT.users),
                            "Nextcord": nextcord.__version__,
                        }
                    )
                },
            )
            await msg.channel.send(embed=embed)

    @botinfo.subcommand(name="learn", description="How alfred works")
    async def learn_slash(self, inter):
        await self.learn(inter)

    @commands.command()
    async def learn(self, ctx):
        embeds = []
        with open("Learn.md", "r", encoding=None) as f:
            l = f.read().replace("- ", "⋅ ").split("\n\n")
            j = l[:8]
            j.append("\n\n".join(l[8:]))
            a = 0
            for i in j:
                a += 1
                embed = ef.cembed(
                    title="Learn",
                    color=self.CLIENT.color(ctx.guild),
                    description=i,
                    footer=f"{a} of {len(j)}",
                )
                embeds.append(embed)
        await assets.pa(ctx, embeds)

    @botinfo.subcommand(name="license", description="View Alfred's Open Source License")
    async def license(self, inter):
        with open("LICENSE", "r") as f:
            await inter.response.send_message(
                ephemeral=True,
                embed=ef.cembed(
                    title="LICENSE",
                    description=f"```\n{f.read()}\n```",
                    color=self.CLIENT.color(inter.guild),
                    thumbnail=self.CLIENT.user.avatar.url,
                    url="https://www.github.com/alvinbengeorge/alfred-discord-bot",
                ),
            )

    @botinfo.subcommand(name="contribution", description="Alfred contributors")
    async def contrib_slash(self, inter):
        await inter.response.defer()
        await self.contribution(inter)

    @commands.command(aliases=["developers", "dev", "contributors"])
    @commands.check(ef.check_command)
    async def contribution(self, ctx):
        embed = ef.cembed(
            title="Contributors and Contributions",
            description="Hey guys, if you've been Developers of Alfred, Thank you very much for your contribution in this project. Our intend for this project was openness and we've gained it, I would like to thank everyone who is seeing this message, and thank you for accepting Alfred. Alfred crossed 250 servers recently, has more than 250,000 users.\n\nIf you want to take part in this, go to our [github page](https://www.github.com), here you can check our code and fork the repository and add a function and send us a PR. If you wish to know more about Alfred, use the feedback command",
            color=self.CLIENT.color(ctx.guild),
            footer="Have a great day",
            thumbnail=self.CLIENT.user.avatar.url,
            image="attachment://contrib.png",
        )
        fp = ef.svg2png(
            url="https://contrib.rocks/image?repo=alvinbengeorge/alfred-discord-bot"
        )
        file = nextcord.File(io.BytesIO(fp), "contrib.png")
        await ctx.send(file=file, embed=embed)

    @commands.command(aliases=["s_e"])
    @commands.check(ef.check_command)
    async def search_emoji(self, ctx, name):
        try:
            st = ""
            for i in self.CLIENT.emojis:
                if name in i.name:
                    st += f"{i.name} -> {str(i)} -> `{i.id}`\n"
            embed = ef.cembed(
                title="Emojis found",
                description=st,
                color=self.CLIENT.color(ctx.guild),
                thumbnail=self.CLIENT.user.avatar.url,
                footer=f"Search results for {name}",
            )
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(
                embed=ef.cembed(description=str(e), color=self.CLIENT.color(ctx.guild))
            )

    @botinfo.subcommand(name="emoji", description="Get Alfred's Emoji")
    async def emoji_slash(self, inter, emoji: str):
        self.CLIENT.re[0] += 1
        e = nextcord.utils.get(self.CLIENT.emojis, name=emoji)
        await inter.send(e)

    @emoji_slash.on_autocomplete("emoji")
    async def emoji_autocomplete(self, inter: nextcord.Interaction, emoji):
        await inter.response.send_autocomplete(
            [
                e.name
                for e in self.CLIENT.emojis
                if e.name.lower().startswith(emoji.lower())
            ][:25]
        )


def setup(CLIENT, **i):
    CLIENT.add_cog(BotInfo(CLIENT, **i))
