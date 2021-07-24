def requirements():
    return "dev_users, re"
def main(client, dev_users, re):
    import discord
    from discord import commands
    @client.command()
    async def leave_server(ctx, *, server_name):
        if str(ctx.author.id) in dev_users:
            guild = discord.utils.get(bot.guilds, name=server_name)
            if guild is None:
                await ctx.send(embed=discord.Embed(title="Hmm", description="This server doesnt exist. Please check if the name is right", color=discord.Color(value=re[8])))
            else:
                await guild.leave()
                await ctx.send(embed=discord.Embed(title="Done", description="I left the server "+server_name, color=discord.Color(value=re[8])))
        else:
            await ctx.send(embed=discord.Embed(title="Permission Denied", description="You dont have the permission to do this", color=discord.Color(value=re[8])))
        
    