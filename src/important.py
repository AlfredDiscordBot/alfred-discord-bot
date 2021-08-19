def requirements():
    return "re"


def main(client, re):
    import discord
    import random
    @client.command()
    async def f(ctx):
        urls = ["https://c.tenor.com/BaJDchtzSMQAAAAC/f-letter-f-burts.gif","https://tenor.com/view/rick-astley-rick-roll-dancing-dance-moves-gif-14097983","https://tenor.com/view/fairy-oddparents-f-dancing-dance-gif-14148380","https://tenor.com/view/efemann-efe-ff-f-in-the-chat-f-in-chat-gif-17919585","https://tenor.com/view/team-fortress2-pay-respects-press-f-gif-14764178","https://tenor.com/view/triggered-letter-f-respect-shake-gif-16962890"]
        embed = discord.Embed(color=discord.Color(re[8]))
        embed.set_image(
            url=random.choice(urls)
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
        
