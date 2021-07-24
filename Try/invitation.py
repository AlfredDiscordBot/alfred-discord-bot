def requirements():
    return "re"
def main(client, re):
    import discord
    from discord.ext import commands
    @client.command()
    async def get_invite(ctx, time=300):
        link = await ctx.channel.create_invite(max_age = int(time))
        await ctx.send(embed=discord.Embed(title="Invitation link", description=link, color =discord.Color(value=re[8])))
