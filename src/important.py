def requirements():
    return "re"


def main(client, re):
    import discord

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
            
    @client.command(aliases=['github','source_code','sc','source'])
    async def repo(ctx):
        embed=discord.Embed(title="Source Code for Alfred",description="[Here you go, click this link and it'll redirect you to the github page](https://github.com/alvinbengeorge/alfred-discord-bot)",color=discord.Color(value=re[8]))
        embed.set_thumbnail(url="https://github.githubassets.com/images/modules/open_graph/github-octocat.png")
        embed.set_image(url=client.user.avatar_url_as(format="png"))
        await ctx.send(embed=embed)
        
