from __future__ import annotations


def requirements():
    return ["re"]


import nextcord
from nextcord.ext import commands
import datetime
from utils import External_functions as ef
from typing import TYPE_CHECKING
import typing_extensions  # type: ignore

if TYPE_CHECKING:
    from typing_extensions import Self
    from nextcord import Member, Interaction
    from typing import Union, Optional


class Moderation(commands.Cog):
    def __init__(self: Self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @commands.command(aliases=["ban"])
    @ef.check_command
    @commands.cooldown(1, 10, commands.BucketType.guild)
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def ban(
        self: Self,
        ctx: commands.Context,
        member: Member,
        *,
        reason: Optional[str] = "No reason provided.",
    ) -> None:
        if member.top_role > ctx.author.top_role:
            embed: nextcord.Embed = nextcord.Embed(
                title="Nah.",
                description="Why are you trying to ban your boss?",
                color=nextcord.Color.red(),
            )
        elif member.top_role > ctx.guild.me.top_role:
            embed: nextcord.Embed = nextcord.Embed(
                title="Nah.",
                description="He has higher hierachy than me, so...",
                color=nextcord.Color.red(),
            )
        elif ctx.guild.owner_id == member.id:
            embed: nextcord.Embed = nextcord.Embed(
                title="Nah.",
                description="He's the owner, I can't do it.",
                color=nextcord.Color.red(),
            )
        else:
            await member.ban(
                reason=f"Invoked by {str(ctx.author)} (ID {ctx.author.id}): {reason}"
            )
            embed: nextcord.Embed = nextcord.Embed(
                title="That dude has gone forever...",
                description=f"{member.name} was banned by {ctx.author.name}",
                color=nextcord.Color.red(),
            )
        await ctx.send(embed=embed)


def main(client, re):
    import nextcord as discord
    import nextcord.ext.commands as commands
    import datetime
    from utils import External_functions as ef

    @client.command(aliases=["kick"])
    @commands.check(ef.check_command)
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def kick_member(ctx, member: discord.Member, *, reason=None):
        if ctx.author.guild_permissions.ban_members:
            await member.kick(reason=reason)
            await ctx.send(
                embed=discord.Embed(
                    title="Kicked",
                    description=member.name + " was kicked by " + ctx.author.name,
                    color=discord.Color(value=re[8]),
                )
            )
        else:
            await ctx.send(
                embed=discord.Embed(
                    title="Permissions Denied",
                    description="You cant kick members, you dont have the permission to do it",
                    color=discord.Color(value=re[8]),
                )
            )

    @client.command(aliases=["mu"])
    @commands.check(ef.check_command)
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def mute(ctx, member: discord.Member, time=10):
        re[0] += 1
        if not getattr(
            ctx, "author", getattr(ctx, "user", None)
        ).guild_permissions.mute_members:
            await ctx.send(
                embed=ef.cembed(
                    title="Permissions Denied",
                    description="You dont have enough permission to execute this command",
                    color=re[8],
                )
            )
            return
        print("Member id: ", member.id)
        await member.edit(timeout=datetime.timedelta(minutes=time))
        await ctx.send(
            embed=ef.cembed(
                title="Done", description=f"Muted {member.mention}", color=re[8]
            )
        )

    @client.command(aliases=["um"])
    @commands.check(ef.check_command)
    async def unmute(ctx, member: discord.Member, time=100):
        re[0] += 1
        if not getattr(
            ctx, "author", getattr(ctx, "user", None)
        ).guild_permissions.mute_members:
            await ctx.send(
                embed=ef.cembed(
                    title="Permissions Denied",
                    description="You dont have enough permission to execute this command",
                    color=re[8],
                )
            )
            return
        print("Member id: ", member.id)
        await member.edit(timeout=None)
        await ctx.send(
            embed=ef.cembed(
                title="Done", description=f"Unmuted {member.mention}", color=re[8]
            )
        )
