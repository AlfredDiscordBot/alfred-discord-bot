import discord
from discord.ext import commands

from External_functions import cembed
from main_program import mute_role, re, req


class Admin(commands.cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['muter'])
    async def set_mute_role(self, ctx, role_for_mute: discord.Role):
        if ctx.author.guild_permissions.administrator:
            mute_role[ctx.guild.id] = role_for_mute.id
            await ctx.send(
                embed=cembed(title="Done", description=f"Mute role set as {role_for_mute.mention}", color=re[8]))
        else:
            await ctx.send(
                embed=cembed(title="Permissions Denied", description="You need to be an admin to set mute role",
                             color=re[8]))

    @commands.command(aliases=["mu"])
    @commands.has_permissions(kick_members=True)
    async def mute(self, ctx, member: discord.Member):
        req()
        print("Member id: ", member.id)
        add_role = None
        if ctx.guild.id in mute_role:
            add_role = [i for i in ctx.guild.roles if i.id == mute_role[ctx.guild.id]][0]
            await member.add_roles(add_role)
            await ctx.send("Muted " + member.mention)
        else:
            add_role = discord.utils.get(ctx.guild.roles, name="dunce")
            await member.add_roles(add_role)
            await ctx.send("Muted " + member.mention)

    @commands.command(aliases=["um"])
    @commands.has_permissions(kick_members=True)
    async def unmute(self, ctx, member: discord.Member):
        req()
        add_role = None
        if ctx.guild.id in mute_role:
            add_role = [i for i in ctx.guild.roles if i.id == mute_role[ctx.guild.id]][0]
            await member.remove_roles(add_role)
            await ctx.send("Unmuted " + member.mention)
        else:
            add_role = discord.utils.get(ctx.guild.roles, name="dunce")
            await member.remove_roles(add_role)
            await ctx.send("Unmuted " + member.mention)
            print(member, "unmuted")
