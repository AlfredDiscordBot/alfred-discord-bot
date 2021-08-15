def requirements():
    return "re"


def main(client, re):
    import discord
    from discord.ext import commands, tasks

    @client.command()
    async def f(ctx):
        embed = discord.Embed(color=discord.Color(re[8]))
        embed.set_image(
            url="https://c.tenor.com/BaJDchtzSMQAAAAC/f-letter-f-burts.gif")
        await ctx.send(embed=embed)

    @client.command(aliases=['s_e'])
    async def search_emoji(ctx, name):
        try:
            emoji_names = [i.name for i in client.emojis]
            st = ""
            for i in emoji_names:
                if i.lower().find(name.lower()) != -1:
                    st += i+"\n"
            if st == "":
                st = "Not found"
            embed = discord.Embed(
                title="Emojis found", description=st, color=discord.Color(value=re[8]))
            embed.set_thumbnail(url=client.user.avatar_url)
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(embed=discord.Embed(description=str(e), color=discord.Color(value=re[8])))
