import nextcord
import utils.assets as assets
import traceback
import utils.External_functions as ef

from nextcord.ext import commands
from nextcord import Interaction, ChannelType
from nextcord.abc import GuildChannel
from .Roles import setup_view

# Use nextcord.slash_command()


def requirements():
    return ["DEV_CHANNEL"]


class Configuration(
    commands.Cog,
    description="This is where you get to configure Alfred's features, disable prefix commands and respond features",
):
    text_slash_ = ef.defa(ChannelType.text)

    def __init__(self, CLIENT: commands.Bot, DEV_CHANNEL):
        self.CLIENT: commands.Bot = CLIENT
        self.DEV_CHANNEL = DEV_CHANNEL
        self.command_list = []
        with open("commands.txt", "r") as f:
            self.command_list = f.read().split("\n")[:-1]

    @commands.Cog.listener()
    async def on_ready(self):
        for i in ef.get_all_slash_commands(self.CLIENT).values():
            if c := getattr(i, "children", False):
                for j in c.values():
                    j.add_check(ef.check_slash)
            else:
                i.add_check(ef.check_slash)

    @commands.command()
    @commands.check(ef.check_command)
    async def sniper(self, ctx):
        user = getattr(ctx, "author", getattr(ctx, "user", None))
        if user.guild_permissions.administrator:
            output = ""
            if ctx.guild.id in self.CLIENT.config["snipe"]:
                self.CLIENT.config["snipe"].remove(ctx.guild.id)
                output = "All people can use the snipe command"

            else:
                self.CLIENT.config["snipe"].append(ctx.guild.id)
                output = "Only admins can use snipe command"

            await ctx.send(
                embed=ef.cembed(
                    title="Done",
                    description=output,
                    color=self.CLIENT.re[8],
                    thumbnail=self.CLIENT.user.avatar.url,
                )
            )
        else:
            await ctx.send(
                embed=ef.cembed(
                    title="Permission Denied",
                    description="Only an admin can toggle this setting",
                    color=nextcord.Color.red(),
                    thumbnail=self.CLIENT.user.avatar.url,
                )
            )

    @nextcord.slash_command(
        name="config", description="Configure Alfred the way you want"
    )
    async def config(self, inter: Interaction):
        print(inter.user)

    @config.subcommand(name="prefix", description="Set Prefix here")
    async def prefix_setting(self, inter, prefix: str = None):
        await self.set_prefix(inter, pref=prefix)

    @config.subcommand(name="color", description="Set color (R, G, B)")
    async def set_color(self, inter, r: int, g: int, b: int):
        if not inter.user.guild_permissions.administrator:
            await inter.response.send_message(
                "You do not have enough permission", ephemeral=True
            )
            return

        if not 0 <= r <= 255:
            await inter.send("Your Red Value must be in the range of (0, 255)")
            return

        if not 0 <= g <= 255:
            await inter.send("Your Green Value must be in the range of (0, 255)")
            return

        if not 0 <= b <= 255:
            await inter.send("Your Blue Value must be in the range of (0, 255)")
            return

        self.CLIENT.re[5][inter.guild.id] = nextcord.Color.from_rgb(r, g, b).value
        await inter.send(
            embed=ef.cembed(
                title="Done",
                description="Set color as ({r}, {g}, {b})".format(r=r, g=g, b=b),
                color=self.CLIENT.color(inter.guild),
                thumbnail=inter.guild.icon,
                author=inter.user,
            )
        )

    @commands.command(aliases=["prefix", "setprefix"])
    @commands.check(ef.check_command)
    async def set_prefix(self, ctx, *, pref=None):
        default_prefix = "'"
        if pref == None:
            await ctx.send(
                embed=ef.cembed(
                    description=f"My Prefix is `{self.CLIENT.prefix_dict.get(ctx.guild.id,default_prefix)}`",
                    color=self.CLIENT.color(ctx.guild),
                )
            )
            return
        if getattr(
            ctx, "author", getattr(ctx, "user", None)
        ).guild_permissions.administrator:
            if pref.startswith('"') and pref.endswith('"') and len(pref) > 1:
                pref = pref[1:-1]
            self.CLIENT.prefix_dict[ctx.guild.id] = pref
            await ctx.send(
                embed=ef.cembed(
                    title="Done",
                    description=f"Prefix set as {pref}",
                    color=self.CLIENT.color(ctx.guild),
                )
            )
            if pref == default_prefix:
                del self.CLIENT.prefix_dict[ctx.guild.id]
        else:
            await ctx.send(
                embed=ef.cembed(
                    title="Permissions Denied",
                    description="You cannot change the prefix, you need to be an admin"
                    + str(assets.Emotes(self.CLIENT).animated_wrong),
                    color=self.CLIENT.color(ctx.guild),
                )
            )

    @commands.command()
    @commands.check(ef.check_command)
    async def remove_prefix(self, ctx):
        if getattr(
            ctx, "author", getattr(ctx, "user", None)
        ).guild_permissions.administrator:
            if self.CLIENT.prefix_dict.get(ctx.guild.id):
                self.CLIENT.prefix_dict.pop(ctx.guild.id)
            await ctx.send(
                embed=ef.cembed(
                    title="Done", description=f"Prefix removed", color=self.CLIENT.re[8]
                )
            )
        else:
            await ctx.send(
                embed=ef.cembed(
                    title="Permissions Denied",
                    description="You cannot change the prefix, you need to be an admin"
                    + str(assets.Emotes(self.CLIENT).animated_wrong),
                    color=self.CLIENT.re[8],
                )
            )

    @commands.command(aliases=["response"])
    async def toggle_response(self, ctx):
        user = getattr(ctx, "author", getattr(ctx, "user", None))
        if user.guild_permissions.administrator:
            output = ""
            if ctx.guild.id in self.CLIENT.config["respond"]:
                self.CLIENT.config["respond"].remove(ctx.guild.id)
                output = "Auto respond turned on"

            else:
                self.CLIENT.config["respond"].append(ctx.guild.id)
                output = "Auto respond turned off"

            await ctx.send(
                embed=ef.cembed(
                    title="Enabled",
                    description=output,
                    color=self.CLIENT.color(ctx.guild),
                    thumbnail=self.CLIENT.user.avatar.url,
                )
            )
        else:
            await ctx.reply(
                embed=ef.cembed(
                    title="Permissions Denied",
                    description="You need admin permissions to toggle this"
                    + str(assets.Emotes(self.CLIENT).animated_wrong),
                    color=nextcord.Color.red(),
                    thumbnail=self.CLIENT.user.avatar.url,
                )
            )

    @commands.command(aliases=["suicide"])
    @commands.check(ef.check_command)
    async def toggle_suicide(self, ctx):
        if getattr(
            ctx, "author", getattr(ctx, "user", None)
        ).guild_permissions.administrator:
            output = ""
            if ctx.guild.id in self.CLIENT.observer:
                self.CLIENT.observer.remove(ctx.guild.id)
                output = "disabled"
            else:
                self.CLIENT.observer.append(ctx.guild.id)
                output = "enabled"
            await ctx.reply(
                embed=ef.cembed(
                    title="Done",
                    description=f"I've {output} the suicide observer",
                    color=self.CLIENT.color(ctx.guild),
                )
            )
        else:
            await ctx.send(
                embed=ef.cembed(
                    title="Permission Denied",
                    description="Only an admin can toggle this setting"
                    + str(assets.Emotes(self.CLIENT).animated_wrong),
                    color=nextcord.Color.red(),
                )
            )

    @config.subcommand(name="slash", description="Enable and Disable slash commands")
    async def slash_control(self, inter):
        print(inter.user)

    @slash_control.subcommand(name="enable", description="Enable this slash command")
    async def slash_enable(self, inter: nextcord.Interaction, command):
        if command not in ef.slash_and_sub(Client=self.CLIENT):
            await inter.send(
                embed=ef.cembed(
                    title="Not a command",
                    description="Please choose from the commands",
                    color=nextcord.Color.red(),
                    footer={
                        "text": "If something seems wrong, please use /feedback",
                        "icon_url": self.CLIENT.user.avatar,
                    },
                )
            )
            return
        if not inter.user.guild_permissions.administrator:
            await inter.send(
                embed=ef.cembed(
                    title="Permission Denied",
                    color=nextcord.Color.red(),
                    description="You do not have Enough permission to execute this command, please ask one of the administrator to",
                    author=inter.user,
                )
            )
            return
        if command not in self.CLIENT.config["slash"]:
            self.CLIENT.config["slash"][command] = set()
        if inter.guild.id in self.CLIENT.config["slash"][command]:
            self.CLIENT.config["slash"][command].remove(inter.guild.id)
        await inter.send(
            embed=ef.cembed(
                title="Done",
                description=f"Enabled {command} in this server, to disable it, use `/config slash disable`",
                color=self.CLIENT.color(inter.guild),
                thumbnail=self.CLIENT.user.avatar,
                author=inter.user,
            )
        )

    @slash_control.subcommand(name="disable", description="Disable this slash command")
    async def slash_disable(self, inter, command):
        if command not in ef.slash_and_sub(Client=self.CLIENT):
            await inter.send(
                embed=ef.cembed(
                    title="Not a command",
                    description="Please choose from the commands",
                    color=nextcord.Color.red(),
                    footer={
                        "text": "If something seems wrong, please use /feedback",
                        "icon_url": self.CLIENT.user.avatar,
                    },
                )
            )
            return
        if not inter.user.guild_permissions.administrator:
            await inter.send(
                embed=ef.cembed(
                    title="Permission Denied",
                    color=nextcord.Color.red(),
                    description="You do not have Enough permission to execute this command, please ask one of the administrator to",
                    author=inter.user,
                )
            )
            return
        if command not in self.CLIENT.config["slash"]:
            self.CLIENT.config["slash"][command] = set()

        self.CLIENT.config["slash"][command].add(inter.guild.id)

        await inter.send(
            embed=ef.cembed(
                title="Done",
                description=f"Disabled {command} in this server, to enable it, use `/config slash enable`",
                color=self.CLIENT.re[8],
                thumbnail=self.CLIENT.user.avatar,
                author=inter.user,
            )
        )

    @slash_enable.on_autocomplete("command")
    @slash_disable.on_autocomplete("command")
    async def slash_autocomplete(self, inter: nextcord.Interaction, command):
        await inter.response.send_autocomplete(
            [i for i in ef.slash_and_sub(self.CLIENT) if i.startswith(command)][:25]
        )

    @config.subcommand(
        name="commands", description="Enable and Disable commands, only for admins"
    )
    async def comm(
        self,
        inter,
        mode=ef.defa(choices=["enable", "disable", "show"], required=True),
        command="-",
    ):
        await inter.response.defer()
        command = command.lower()
        if not inter.user.guild_permissions.administrator:
            await inter.send(
                embed=ef.cembed(
                    title="Permissions Denied",
                    description="Only an admin can use this command, please ask an admin to enable this"
                    + str(assets.Emotes(self.CLIENT).animated_wrong),
                    color=nextcord.Color.red(),
                )
            )
            return
        if command.lower() not in [
            i.name.lower() for i in self.CLIENT.commands
        ] and mode in ["enable", "disable"]:
            await inter.send("This is not a command, check the spelling")
            return
        if command not in self.CLIENT.config["commands"] and command != "-":
            self.CLIENT.config["commands"][command] = []
        if mode == "enable" and command != "-":
            if inter.guild.id in self.CLIENT.config["commands"][command]:
                self.CLIENT.config["commands"][command].remove(inter.guild.id)
                await inter.send(
                    embed=ef.cembed(
                        title="Done",
                        description=f"Enabled {command} in this server",
                        color=self.CLIENT.re[8],
                        thumbnail=self.CLIENT.user.avatar.url,
                    )
                )
                return
            await inter.send("Already Enabled")
        elif mode == "disable" and command != "-":
            if inter.guild.id not in self.CLIENT.config["commands"][command]:
                self.CLIENT.config["commands"][command].append(inter.guild.id)
                await inter.send(
                    embed=ef.cembed(
                        title="Done",
                        description=f"Disabled {command} in this server",
                        color=self.CLIENT.re[8],
                        thumbnail=self.CLIENT.user.avatar.url,
                    )
                )
                return
            await inter.send("Already Disabled")
        else:
            disabled_commands = []
            enabled_commands = []
            for i in [j.name for j in self.CLIENT.commands]:
                if inter.guild.id in self.CLIENT.config["commands"].get(i, []):
                    disabled_commands.append(i)
                else:
                    enabled_commands.append(i)

            disabled_commands = "**Disabled commands**\n" + ", ".join(disabled_commands)
            enabled_commands = "**Enabled commands**\n" + ", ".join(enabled_commands)
            await inter.send(
                embed=ef.cembed(
                    title="Commands",
                    description=enabled_commands + "\n\n" + disabled_commands,
                    color=self.CLIENT.re[8],
                    thumbnail=self.CLIENT.user.avatar.url,
                    footer="Everything is enabled by default",
                )
            )

    @comm.on_autocomplete("command")
    async def auto(self, inter, command):
        autocomp_command = [
            i for i in self.command_list if command.lower() in i.lower()
        ][:25]
        await inter.response.send_autocomplete(autocomp_command)

    @config.subcommand(name="welcome", description="set welcome channel")
    async def wel(
        self,
        inter,
        channel: GuildChannel = ef.defa(ChannelType.text, required=True),
        background_url=None,
        description=None,
        title=None,
        text1=None,
        text2=None,
        text3=None,
    ):
        await inter.response.defer()
        self.CLIENT.config["welcome"][inter.guild.id] = {
            "channel": channel.id,
            "description": description,
            "title": title,
            "background": background_url,
            "text1": text1,
            "text2": text2,
            "text3": text3,
        }
        await inter.send("Done")

    @nextcord.slash_command(name="youtube", description="Controls youtube")
    async def youtube(self, inter):
        print(inter.user)

    @youtube.subcommand(name="subscribe", description="Subscribe to a youtube channel")
    async def sub_slash(
        self,
        inter,
        channel: GuildChannel = ef.defa(ChannelType.text, required=True),
        url=None,
        message="",
    ):
        await inter.response.defer()
        await self.subscribe(inter, channel=channel, url=url, message=message)

    @youtube.subcommand(
        name="unsubscribe", description="remove a youtube channel from a textchannel"
    )
    async def unsub_slash(self, ctx, channel: GuildChannel = None, url=None):
        await ctx.response.defer()
        await self.unsubscribe(ctx, channel=channel, url=url)

    @commands.command()
    @commands.check(ef.check_command)
    async def subscribe(
        self, ctx, channel: nextcord.TextChannel = None, url=None, *, message=""
    ):
        if getattr(
            ctx, "author", getattr(ctx, "user", None)
        ).guild_permissions.administrator:
            if "youtube" not in self.CLIENT.config:
                self.CLIENT.config["youtube"] = {}
            if channel.id not in self.CLIENT.config["youtube"]:
                self.CLIENT.config["youtube"][channel.id] = set()
            if url is not None:
                url = ef.check_end(url)
                if not ef.validate_url(url):
                    await ctx.send(
                        embed=ef.cembed(
                            title="Huh",
                            description="That's an invalid url form id",
                            color=self.CLIENT.re[8],
                            thumbnail=self.CLIENT.user.avatar.url,
                        )
                    )
                    return
                self.CLIENT.config["youtube"][channel.id].add((url, message))
                await ctx.send(
                    embed=ef.cembed(
                        title="Done",
                        description=f"Added {url} to the list and it'll be displayed in {channel.mention}",
                        color=self.CLIENT.re[8],
                        thumbnail=self.CLIENT.user.avatar.url,
                    )
                )
            else:
                all_links = "\n".join(
                    [i[0] for i in self.CLIENT.config["youtube"][channel.id]]
                )
                await ctx.send(
                    embed=ef.cembed(
                        title="All youtube subscriptions in this channel",
                        description=all_links,
                        color=self.CLIENT.re[8],
                        thumbnail=self.CLIENT.user.avatar.url,
                    )
                )
        else:
            await ctx.send(
                embed=ef.cembed(
                    title="Permission Denied",
                    description="Only an admin can set it",
                    color=self.CLIENT.re[8],
                    thumbnail=self.CLIENT.user.avatar.url,
                )
            )

    @commands.command()
    @commands.check(ef.check_command)
    async def unsubscribe(self, ctx, channel: nextcord.TextChannel = None, url=None):
        if getattr(
            ctx, "author", getattr(ctx, "user", None)
        ).guild_permissions.administrator:
            if "youtube" not in self.CLIENT.config:
                self.CLIENT.config["youtube"] = {}
            if channel.id not in self.CLIENT.config["youtube"]:
                self.CLIENT.config["youtube"][channel.id] = set()
            if url is None:
                all_links = "\n".join(
                    [i[0] for i in self.CLIENT.config["youtube"][channel.id]]
                )
                await ctx.send(
                    embed=ef.cembed(
                        title="All youtube subscriptions in this channel",
                        description=all_links,
                        color=self.CLIENT.re[8],
                        thumbnail=self.CLIENT.user.avatar.url,
                    )
                )
                return
            try:
                url = ef.check_end(url)
                for u, m in self.CLIENT.config["youtube"][channel.id]:
                    if u == url:
                        self.CLIENT.config["youtube"][channel.id].remove((u, m))
                        break

                await ctx.send(
                    embed=ef.cembed(
                        title="Done",
                        description=f"Removed {url} from the list",
                        color=self.CLIENT.re[8],
                        thumbnail=self.CLIENT.user.avatar.url,
                    )
                )
            except KeyError:
                print(traceback.format_exc())
                await ctx.reply(
                    embed=ef.cembed(
                        title="Hmm",
                        description=f"The URL provided is not in {channel.name}'s subscriptions",
                        color=self.CLIENT.re[8],
                    )
                )
        else:
            await ctx.send(
                embed=ef.cembed(
                    title="Permission Denied",
                    description="Only an admin can remove subscriptions",
                    color=self.CLIENT.re[8],
                    thumbnail=self.CLIENT.user.avatar.url,
                )
            )

    @config.subcommand(name="message", description="Set your configuration")
    async def config_slash(
        self,
        inter: Interaction,
        mode=ef.defa(choices=["enable", "disable", "show"], required=True),
        feature=ef.defa(choices=["snipe", "response", "suicide_detector"]),
    ):
        await inter.response.defer()
        if mode == "show":
            su = inter.guild.id in self.CLIENT.observer
            rs = not inter.guild.id in self.CLIENT.config["respond"]
            sn = not inter.guild.id in self.CLIENT.config["snipe"]
            if not sn:
                sn = "Only Admins"
            else:
                sn = "All people"
            embed = ef.cembed(
                title="Features",
                description="This shows all the extra features in alfred",
                color=self.CLIENT.re[8],
                thumbnail=ef.safe_pfp(inter.guild),
                fields=ef.dict2fields(
                    {
                        "Suicide detector": str(su),
                        "Auto Response": str(rs),
                        "Snipe": str(sn),
                    }
                ),
            )
            await inter.send(embed=embed)
            return

        if not inter.user.guild_permissions.administrator:
            await inter.send(
                embed=ef.cembed(
                    title="Permissions Denied",
                    description="You need to be an admin to toggle settings",
                    color=self.CLIENT.re[8],
                    thumbnail=ef.safe_pfp(inter.guild),
                    author=inter.user,
                )
            )
            return

        try:
            output = ""
            if mode == "enable":
                if feature == "snipe":
                    if not inter.guild.id in self.CLIENT.config["snipe"]:
                        self.CLIENT.config["snipe"].append(inter.guild.id)
                    output = "Only admins can use snipe command"
                elif feature == "response":
                    if inter.guild.id in self.CLIENT.config["respond"]:
                        self.CLIENT.config["respond"].remove(inter.guild.id)
                    output = "Enabled Auto response, try saying `Alfred hello`"
                else:
                    if not inter.guild.id in self.CLIENT.observer:
                        self.CLIENT.observer.append(inter.guild.id)
                    output = "Enabled suicide observer"

            elif mode == "disable":
                if feature == "snipe":
                    if inter.guild.id in self.CLIENT.config["snipe"]:
                        self.CLIENT.config["snipe"].remove(inter.guild.id)
                    output = "All people can use snipe command"
                elif feature == "response":
                    if not inter.guild.id in self.CLIENT.config["respond"]:
                        self.CLIENT.config["respond"].append(inter.guild.id)
                    output = "Disabled Auto Response. You've decided to not talk to Alfred :sob:"
                else:
                    if inter.guild.id in self.CLIENT.observer:
                        self.CLIENT.observer.remove(inter.guild.id)
                        output = "Disabled Suicide observer"
            await inter.send(
                embed=ef.cembed(
                    description=output, title="Done", color=self.CLIENT.re[8]
                )
            )
        except:
            a = traceback.format_exc()
            d = self.CLIENT.get_channel(self.DEV_CHANNEL)
            await d.send(
                embed=ef.cembed(
                    title="Error in config",
                    description=str(a),
                    color=self.CLIENT.re[8],
                    footer=f"{inter.user.name} -> {inter.guild.name}",
                    thumbnail=self.CLIENT.user.avatar.url,
                )
            )

    @config.subcommand(
        name="sealfred",
        description="Checks for behaviours like kicking out or banning regularly",
    )
    async def SeCurity(self, inter, log_channel: GuildChannel = "delete"):
        await inter.response.defer()
        if not inter.permissions.administrator:
            await inter.send(
                embed=ef.cembed(
                    title="Permission",
                    description="You need admin permissions to do the security work, Ask your owner to execute this command for protection",
                    color=nextcord.Color.red(),
                    thumbnail=self.CLIENT.user.avatar.url,
                )
            )
            return
        if log_channel == "delete":
            if inter.guild.id in self.CLIENT.config["security"]:
                del self.CLIENT.config["security"][inter.guild.id]
            await inter.send(
                embed=ef.cembed(
                    description="Removed SEAlfred from this server, this server is now left unprotected",
                    color=self.CLIENT.re[8],
                )
            )
            return
        channel_id = log_channel.id
        self.CLIENT.config["security"][inter.guild.id] = channel_id
        await inter.send(
            embed=ef.cembed(
                title="Done",
                description=f"Set {log_channel.mention} as the log channel, all the updates will be pushed to this",
                color=self.CLIENT.re[8],
            )
        )

    @config.subcommand(
        name="autoreact",
        description="Automatically reacts to every message in a channel",
    )
    async def autoreactslash(
        self, inter, channel: GuildChannel = ef.defa(ChannelType.text), emojis: str = ""
    ):
        await inter.response.defer()
        await self.autoreact(inter, channel, Emojis=emojis)

    @config.subcommand(
        name="removereact", description="Clears autoreact from a channel"
    )
    async def removeautoreactslash(
        self, inter, channel: GuildChannel = ef.defa(ChannelType.text)
    ):
        await inter.response.defer()
        await self.remove_autoreact(inter, channel=channel)

    @commands.command(aliases=["autoreaction"])
    @commands.check(ef.check_command)
    async def autoreact(
        self, ctx, channel: nextcord.TextChannel = None, *, Emojis: str = ""
    ):
        if not getattr(
            ctx, "author", getattr(ctx, "user", None)
        ).guild_permissions.administrator:
            await ctx.send(
                embed=ef.cembed(
                    title="Permissions Denied",
                    description="You cannot set autoreact, you do not have admin privilege",
                    color=self.CLIENT.re[8],
                    thumbnail=self.CLIENT.user.avatar,
                )
            )
            return
        if not channel:
            await ctx.send(
                embed=ef.cembed(
                    title="Hmm",
                    description=ef.emoji.emojize(
                        "You need to mention a channel\n'autoreact #channel :one:|:two:|:three:"
                    ),
                    color=self.CLIENT.re[8],
                    author=getattr(ctx, "author", getattr(ctx, "user", None)),
                    thumbnail=self.CLIENT.user.avatar,
                )
            )
            return
        if Emojis == "":
            await ctx.send(
                embed=ef.cembed(
                    title="Hmm",
                    description="You need one or more emojis separated by |",
                    color=self.CLIENT.re[8],
                )
            )
            return
        if channel.id not in self.CLIENT.autor:
            self.CLIENT.autor[channel.id] = [
                i.strip() for i in ef.emoji.demojize(Emojis).split("|")
            ]
        else:
            self.CLIENT.autor[channel.id] += [
                i.strip() for i in ef.emoji.demojize(Emojis).split("|")
            ]
        await ctx.send(
            embed=ef.cembed(
                title="Done",
                description=f"For every message in {channel.mention} Alfred will add {Emojis} reaction",
                color=self.CLIENT.re[8],
            )
        )

    @commands.command()
    @commands.check(ef.check_command)
    async def remove_autoreact(self, ctx, channel: nextcord.TextChannel = None):
        if not getattr(
            ctx, "author", getattr(ctx, "user", None)
        ).guild_permissions.administrator:
            await ctx.send(
                embed=ef.cembed(
                    title="Permissions Denied",
                    description="You cannot remove autoreact, you do not have admin privilege",
                    color=self.CLIENT.re[8],
                    author=getattr(ctx, "author", getattr(ctx, "user", None)),
                )
            )
            return
        if not channel:
            await ctx.send(
                embed=ef.cembed(
                    title="This time",
                    description="Mention a channel, in the `channel` field",
                    color=self.CLIENT.re[8],
                    thumbnail=self.CLIENT.user.avatar,
                )
            )
        if not channel.id in self.CLIENT.autor:
            await ctx.send(
                embed=ef.cembed(
                    title="Hmm",
                    description="This channel does not have any reactions",
                    color=self.CLIENT.re[8],
                )
            )
            return
        confirmation = await ef.wait_for_confirm(
            ctx,
            self.CLIENT,
            "Do you want to remove every automatic reaction in this channel?",
            color=self.CLIENT.re[8],
            usr=getattr(ctx, "author", getattr(ctx, "user", None)),
        )
        if not confirmation:
            return
        self.CLIENT.autor.pop(channel.id)
        await ctx.send(
            embed=ef.cembed(
                title="Done",
                description=f"Removed every reaction in {channel.mention}",
                color=self.CLIENT.re[8],
            )
        )

    @nextcord.slash_command(name="roles", description="Setup Roles Selection")
    async def setup_roles(self, inter):
        print(inter.user)

    @setup_roles.subcommand(name="selection", description="Setup Roles using buttons")
    async def selection(
        self,
        inter,
        roles_with_comma,
        channel: GuildChannel = ef.defa(ChannelType.text, required=True),
    ):
        await inter.response.defer()
        roles = [
            inter.guild.get_role(int(i.strip()[3:-1]))
            for i in roles_with_comma.split(",")
        ]
        if not (
            channel.permissions_for(inter.user).send_messages
            and inter.user.guild_permissions.manage_guild
        ):
            await inter.send(content="You do not have enough permission to do that")
            return
        if not channel.permissions_for(inter.guild.me).send_messages:
            await inter.send(content="I do not have enough permissions to send message")
        await channel.send(
            embed=ef.cembed(
                title="Roles",
                description="\n".join([role.mention for role in roles]),
                color=self.CLIENT.re[8],
                author={"name": inter.guild.name, "icon_url": inter.guild.icon},
                footer={
                    "text": "This feature is still Beta",
                    "icon_url": self.CLIENT.user.avatar.url,
                },
                thumbnail=inter.guild.icon,
                image=assets.BLUE_LINE,
            ),
            view=setup_view(roles),
        )
        if inter.guild.id not in self.CLIENT.config["roles"]:
            self.CLIENT.config["roles"][inter.guild.id] = []
        self.CLIENT.config["roles"][inter.guild.id].append([role.id for role in roles])
        await inter.send(
            embed=ef.cembed(
                title="Done",
                description=f"Completed, the role selection can be seen in {channel.mention}",
                color=self.CLIENT.re[8],
                thumbnail=self.CLIENT.user.avatar.url,
                fields=[
                    {"name": "Roles", "value": "".join([i.mention for i in roles])}
                ],
            )
        )


def setup(CLIENT, **i):
    CLIENT.add_cog(Configuration(CLIENT, **i))
