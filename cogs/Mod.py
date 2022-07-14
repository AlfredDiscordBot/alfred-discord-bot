import utils.External_functions as ef
from nextcord.ext import commands

# Use nextcord.slash_command()

def requirements():
    return []

class Mod(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["ban"])
    @commands.check(ef.check_command)
    @commands.cooldown(1,10,commands.BucketType.guild)
    async def ban_member(self, ctx, member: ef.nextcord.Member, *, reason=None):
        if ctx.author.guild_permissions.ban_members:
            await member.ban(reason = reason)
            await ctx.send(
                embed = ef.cembed(
                    title="That dude's gone forever",
                    description=f"{member.name} was banned by {ctx.author.name}",
                    color=self.client.re[8],
                )
            )
        else:
            await ctx.send(
                embed = ef.cembed(
                    title="Permissions Denied",
                    description="You cant ban members, you dont have the permission to do it",
                    color=self.client.re[8],
                )
            )

    @commands.command(aliases=["kick"])
    @commands.check(ef.check_command)
    @commands.cooldown(1,10,commands.BucketType.guild)
    async def kick_member(self, ctx, member: ef.nextcord.Member, *, reason=None):
        if ctx.author.guild_permissions.ban_members:
            await member.kick(reason=reason)
            await ctx.send(
                embed=ef.cembed(
                    title="Kicked",
                    description=member.name + " was kicked by " + ctx.author.name,
                    color=self.client.re[8],
                )
            )
        else:
            await ctx.send(
                embed=ef.cembed(
                    title="Permissions Denied",
                    description="You cant kick members, you dont have the permission to do it",
                    color=self.client.re[8],
                )
            )
            
    @commands.command(aliases=["mu"])
    @commands.check(ef.check_command)
    @commands.cooldown(1,10,commands.BucketType.guild)
    async def mute(self, ctx, member: ef.nextcord.Member, time:int=10):
        self.client.re[0]+=1
        if not getattr(ctx, 'author', getattr(ctx, 'user', None)).guild_permissions.mute_members:
            await ctx.send(
                embed=ef.cembed(
                    title="Permissions Denied",
                    description = "You dont have enough permission to execute this command",
                    color=self.client.re[8]
                )
            )
            return
        print("Member id: ", member.id)
        await member.edit(timeout = ef.datetime.timedelta(minutes = time))
        await ctx.send(
            embed=ef.cembed(
                title="Done",
                description=f"Muted {member.mention}",
                color=self.client.re[8]
            )
        )




    @commands.command(aliases=["um"])
    @commands.check(ef.check_command)
    async def unmute(self, ctx, member: ef.nextcord.Member):
        self.client.re[0]+=1
        if not getattr(ctx, 'author', getattr(ctx, 'user', None)).guild_permissions.mute_members:
            await ctx.send(
                embed=ef.cembed(
                    title="Permissions Denied",
                    description = "You dont have enough permission to execute this command",
                    color=self.client.re[8]
                )
            )
            return
        print("Member id: ", member.id)
        await member.edit(timeout = None)
        await ctx.send(
            embed=ef.cembed(
                title="Done",
                description=f"Unmuted {member.mention}",
                color=self.client.re[8]
            )
        )


def setup(client,**i):
    client.add_cog(Mod(client,**i))