def requirements():
    return ["re"]


def main(client, re):
    import nextcord as discord
    import nextcord.ext.commands as commands
    import datetime
    import External_functions as ef

    @client.command(aliases=["ban"])
    @commands.cooldown(1,10,commands.BucketType.guild)
    async def ban_member(ctx, member: discord.Member, *, reason=None):
        if ctx.author.guild_permissions.ban_members:
            await member.ban(reason=reason)
            await ctx.send(
                embed=discord.Embed(
                    title="That dude's gone forever",
                    description=member.name + " was banned by " + ctx.author.name,
                    color=discord.Color(value=re[8]),
                )
            )
        else:
            await ctx.send(
                embed=discord.Embed(
                    title="Permissions Denied",
                    description="You cant ban members, you dont have the permission to do it",
                    color=discord.Color(value=re[8]),
                )
            )

    @client.command(aliases=["kick"])
    @commands.cooldown(1,10,commands.BucketType.guild)
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
    @commands.cooldown(1,10,commands.BucketType.guild)
    async def mute(ctx, member: discord.Member, time=10):
        re[0]+=1
        if not getattr(ctx, 'author', getattr(ctx, 'user', None)).guild_permissions.mute_members:
            await ctx.send(
                embed=ef.cembed(
                    title="Permissions Denied",
                    description = "You dont have enough permission to execute this command",
                    color=re[8]
                )
            )
            return
        print("Member id: ", member.id)
        await member.edit(timeout = datetime.timedelta(minutes = time))
        await ctx.send(
            embed=ef.cembed(
                title="Done",
                description=f"Muted {member.mention}",
                color=re[8]
            )
        )




    @client.command(aliases=["um"])
    async def unmute(ctx, member: discord.Member, time=100):
        re[0]+=1
        if not getattr(ctx, 'author', getattr(ctx, 'user', None)).guild_permissions.mute_members:
            await ctx.send(
                embed=ef.cembed(
                    title="Permissions Denied",
                    description = "You dont have enough permission to execute this command",
                    color=re[8]
                )
            )
            return
        print("Member id: ", member.id)
        await member.edit(timeout = None)
        await ctx.send(
            embed=ef.cembed(
                title="Done",
                description=f"Unmuted {member.mention}",
                color=re[8]
            )
        )
    