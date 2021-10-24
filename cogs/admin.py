import discord
from discord.ext import commands

from External_functions import cembed, wait_for_confirm
from main_program import mute_role, re, req


class Admin(commands.Cog):
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

    @commands.command()
    async def clear(self, ctx, text, num=10):
        req()
        await ctx.channel.purge(limit=1)
        if str(text) == re[1]:
            if (
                    ctx.author.guild_permissions.manage_messages
                    or ctx.author.id == 432801163126243328
            ):
                confirmation = True
                if int(num) > 10:
                    confirmation = await wait_for_confirm(
                        ctx, self.bot, f"Do you want to delete {num} messages", color=re[8]
                    )
                if confirmation:
                    await ctx.channel.delete_messages(
                        [i async for i in ctx.channel.history(limit=num) if not i.pinned][:100]
                    )
            else:
                await ctx.send(
                    embed=discord.Embed(
                        title="Permission Denied",
                        description="You cant delete messages",
                        color=discord.Color(value=re[8]),
                    )
                )
        else:
            await ctx.send("Wrong password")


def setup(bot):
    client.add_cog(Admin(bot))
