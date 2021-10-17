def requirements():
    return ["re"]


def main(client, re):
    import discord

    @client.command(aliases=["ban"])
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
