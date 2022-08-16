import nextcord, asyncio, traceback
import utils.assets as assets
import datetime
import utils.External_functions as ef
from nextcord.ext import commands

# Use nextcord.slash_command()


def requirements():
    return []


def has_role(member: nextcord.Member, role: nextcord.Role):
    if role in member.roles:
        return True
    return False


class Mod(commands.Cog):
    def __init__(self, CLIENT: commands.Bot):
        self.CLIENT = CLIENT
        self.DELETED_MESSAGE = {}

    @commands.Cog.listener()
    async def on_bulk_message_delete(self, messages):
        for i in messages:
            await self.on_message_delete(i)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if (
            message.guild.id in self.CLIENT.config["commands"].get("snipe", [])
            or message.author.bot
        ):
            return
        if message.channel.id not in self.DELETED_MESSAGE:
            self.DELETED_MESSAGE[message.channel.id] = []
        self.DELETED_MESSAGE[message.channel.id].append(
            (message.author, message.content)
        )

    @nextcord.slash_command(
        name="snipe", description="Get the last few deleted messages"
    )
    async def snipe_slash(self, inter, number: int = 50):
        await inter.response.defer()
        await self.snipe(inter, number)

    @commands.command(description="Snipe Deleted messages")
    @commands.check(ef.check_command)
    async def snipe(self, ctx, number: int = 50):
        """
        Snipe command, prefix rewritten
        """
        user = getattr(ctx, "author", getattr(ctx, "user", None))
        if not (
            user.guild_permissions.administrator
            or ctx.guild.id not in self.CLIENT.config["snipe"]
        ):
            await ctx.send(
                embed=ef.cembed(
                    title="Permission Denied",
                    description="You're not allowed to use snipe command, please ask an admin to do it",
                    color=self.CLIENT.color(ctx.guild),
                    author=user,
                    thumbnail=self.CLIENT.user.avatar,
                    footer={
                        "text": "If you think something is wrong, please report to our support server",
                        "icon_url": self.CLIENT.user.avatar,
                    },
                )
            )
            return

        embeds, count, strings = [], 0, [[]]
        for m in self.DELETED_MESSAGE.get(ctx.channel.id, [])[::-1]:
            strings[-1].append("**{}:**\n{}".format(*m))
            if count % 5 == 0 and count != 0:
                strings.append([])
            if count >= number:
                break
            count += 1

        if strings == [[]]:
            strings = [
                [
                    "**Hmmmm:**\nNothing here lol",
                    "**Well Maybe**\nThe bot may have restarted",
                ]
            ]

        for description in strings:
            embeds.append(
                ef.cembed(
                    title="Snipe",
                    description=description,
                    color=self.CLIENT.color(ctx.guild),
                    thumbnail=ctx.guild.icon,
                    author=user,
                    footer={
                        "text": "This message will be deleted in 30 seconds",
                        "icon_url": self.CLIENT.user.avatar,
                    },
                )
            )

        await assets.pa(ctx, embeds=embeds, restricted=True, delete_after=30)

    @commands.command(aliases=["ban"])
    @commands.check(ef.check_command)
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def ban_member(self, ctx, member: ef.nextcord.Member, *, reason=None):
        if ctx.author.guild_permissions.ban_members:
            await member.ban(reason=reason)
            await ctx.send(
                embed=ef.cembed(
                    title="That dude's gone forever",
                    description=f"{member.name} was banned by {ctx.author.name}",
                    color=self.CLIENT.color(ctx.guild),
                )
            )
        else:
            await ctx.send(
                embed=ef.cembed(
                    title="Permissions Denied",
                    description="You cant ban members, you dont have the permission to do it",
                    color=self.CLIENT.color(ctx.guild),
                )
            )

    @commands.command(aliases=["kick"])
    @commands.check(ef.check_command)
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def kick_member(self, ctx, member: ef.nextcord.Member, *, reason=None):
        if ctx.author.guild_permissions.ban_members:
            await member.kick(reason=reason)
            await ctx.send(
                embed=ef.cembed(
                    title="Kicked",
                    description=member.name + " was kicked by " + ctx.author.name,
                    color=self.CLIENT.color(ctx.guild),
                )
            )
        else:
            await ctx.send(
                embed=ef.cembed(
                    title="Permissions Denied",
                    description="You cant kick members, you dont have the permission to do it",
                    color=self.CLIENT.color(ctx.guild),
                )
            )

    @commands.command(aliases=["mu"])
    @commands.check(ef.check_command)
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def mute(self, ctx, member: ef.nextcord.Member, time: int = 10):
        self.CLIENT.re[0] += 1
        if not getattr(
            ctx, "author", getattr(ctx, "user", None)
        ).guild_permissions.mute_members:
            await ctx.send(
                embed=ef.cembed(
                    title="Permissions Denied",
                    description="You dont have enough permission to execute this command",
                    color=self.CLIENT.color(ctx.guild),
                )
            )
            return
        print("Member id: ", member.id)
        await member.edit(timeout=datetime.timedelta(minutes=time))
        await ctx.send(
            embed=ef.cembed(
                title="Done",
                description=f"Muted {member.mention}",
                color=self.CLIENT.color(ctx.guild),
            )
        )

    @commands.command(aliases=["um"])
    @commands.check(ef.check_command)
    async def unmute(self, ctx, member: ef.nextcord.Member):
        self.CLIENT.re[0] += 1
        if not getattr(
            ctx, "author", getattr(ctx, "user", None)
        ).guild_permissions.mute_members:
            await ctx.send(
                embed=ef.cembed(
                    title="Permissions Denied",
                    description="You dont have enough permission to execute this command",
                    color=self.CLIENT.color(ctx.guild),
                )
            )
            return
        print("Member id: ", member.id)
        await member.edit(timeout=None)
        await ctx.send(
            embed=ef.cembed(
                title="Done",
                description=f"Unmuted {member.mention}",
                color=self.CLIENT.color(ctx.guild),
            )
        )

    @commands.command(aliases=["*"])
    @commands.check(ef.check_command)
    async def change_nickname(self, ctx, member: nextcord.Member, *, nickname=None):
        user = getattr(ctx, "author", getattr(ctx, "user", None))
        if (
            user.guild_permissions.change_nickname
            and user.top_role.position > member.top_role.position
        ):
            await member.edit(nick=nickname)
            await ctx.send(
                embed=ef.cembed(
                    title="Nickname Changed",
                    description=f"Nickname changed to {member.nick or member.name} by {user.mention}",
                    color=self.CLIENT.color(ctx.guild),
                )
            )
        else:
            await ctx.send(
                embed=ef.cembed(
                    title="Permissions Denied",
                    description="You dont have permission to change others nickname",
                    color=self.CLIENT.color(ctx.guild),
                )
            )

    @commands.command(aliases=["purge"])
    @commands.check(ef.check_command)
    async def clear(self, ctx, text, num: int = 10):
        self.CLIENT.re[0] += 1
        await ctx.message.delete()
        if str(text) == self.CLIENT.re[1]:
            user = getattr(ctx, "author", getattr(ctx, "user", None))
            if user.guild_permissions.manage_messages or user.id == 432801163126243328:
                confirmation = True
                if int(num) > 10:
                    confirmation = await ef.wait_for_confirm(
                        ctx,
                        self.CLIENT,
                        f"Do you want to delete {num} messages",
                        color=self.CLIENT.color(ctx.guild),
                    )
                if confirmation:
                    await ctx.channel.delete_messages(
                        [
                            i
                            async for i in ctx.channel.history(limit=num)
                            if not i.pinned
                        ][:100]
                    )
            else:
                await ctx.send(
                    embed=ef.cembed(
                        title="Permission Denied",
                        description="You cant delete messages",
                        color=self.CLIENT.color(ctx.guild),
                    )
                )
        else:
            await ctx.send("Wrong password")

    @nextcord.slash_command(name="autoaddrole", description="Add roles to all")
    async def autoadd(self, inter):
        print(inter.user)

    @autoadd.subcommand(name="tobots", description="Bots")
    async def bots(self, inter, role: nextcord.Role):
        await inter.response.defer()
        if not inter.user.id == inter.guild.owner.id:
            await inter.send(
                embed=ef.cembed(
                    title="Permission Denied",
                    description="You cannot execute this command, only server owners can",
                    color=nextcord.Color.red(),
                    thumbnail=self.CLIENT.user.avatar.url,
                    author=inter.user,
                    footer="Please ask your owner to execute this command",
                )
            )
            return
        confirm = await ef.wait_for_confirm(
            inter,
            self.CLIENT,
            "Are you Sure you want to do this",
            color=self.CLIENT.color(inter.guild),
        )
        if not confirm:
            await inter.send("Aborting")
            return
        to_be_added = [_ for _ in inter.guild.bots if not has_role(_, role)]
        await inter.send(
            embed=ef.cembed(
                title="All right",
                description="This may take a while to process, please be patient",
                color=self.CLIENT.color(inter.guild),
                author=inter.user,
                footer=f"This will be applied to {len(to_be_added)} bots",
            )
        )
        for bot in to_be_added:
            try:
                await bot.add_roles(role)
                await asyncio.sleep(2)
            except Exception:
                print(traceback.format_exc())

    @autoadd.subcommand(name="toeveryone", description="Bots")
    async def everyone(self, inter, role: nextcord.Role):
        await inter.response.defer()
        if not inter.user.id == inter.guild.owner.id:
            await inter.send(
                embed=ef.cembed(
                    title="Permission Denied",
                    description="You cannot execute this command, only server owners can",
                    color=nextcord.Color.red(),
                    thumbnail=self.CLIENT.user.avatar.url,
                    author=inter.user,
                    footer="Please ask your owner to execute this command",
                )
            )
            return
        confirm = await ef.wait_for_confirm(
            inter,
            self.CLIENT,
            "Are you Sure you want to do this",
            color=self.CLIENT.color(inter.guild),
        )
        if not confirm:
            await inter.send("Aborting")
            return
        to_be_added = [_ for _ in inter.guild.members if not has_role(_, role)]
        await inter.send(
            embed=ef.cembed(
                title="All right",
                description="This may take a while to process, please be patient",
                color=self.CLIENT.color(inter.guild),
                author=inter.user,
                footer=f"This will be applied to {len(to_be_added)} members",
            )
        )
        for member in to_be_added:
            try:
                await member.add_roles(role)
                await asyncio.sleep(2)
            except Exception:
                print(traceback.format_exc())

    @commands.command()
    async def get_invite(self, ctx, time: int = 600):
        link = await ctx.channel.create_invite(max_age=time)
        await ctx.send(
            embed=ef.cembed(
                title="Invitation link",
                description=str(link),
                color=self.CLIENT.color(ctx.guild),
            )
        )

    @autoadd.subcommand(name="tohumans", description="Bots")
    async def humans(self, inter, role: nextcord.Role):
        await inter.response.defer()
        if not inter.user.id == inter.guild.owner.id:
            await inter.send(
                embed=ef.cembed(
                    title="Permission Denied",
                    description="You cannot execute this command, only server owners can",
                    color=nextcord.Color.red(),
                    thumbnail=self.CLIENT.user.avatar.url,
                    author=inter.user,
                    footer="Please ask your owner to execute this command",
                )
            )
            return
        confirm = await ef.wait_for_confirm(
            inter,
            self.CLIENT,
            "Are you Sure you want to do this",
            color=self.CLIENT.color(inter.guild),
        )
        if not confirm:
            await inter.send("Aborting")
            return
        to_be_added = [_ for _ in inter.guild.humans if not has_role(_, role)]
        await inter.send(
            embed=ef.cembed(
                title="All right",
                description="This may take a while to process, please be patient",
                color=self.CLIENT.color(inter.guild),
                author=inter.user,
                footer=f"This will be applied to {len(to_be_added)} humans",
            )
        )
        for member in to_be_added:
            try:
                await member.add_roles(role)
                await asyncio.sleep(2)
            except Exception:
                print(traceback.format_exc())


def setup(CLIENT, **i):
    CLIENT.add_cog(Mod(CLIENT, **i))
