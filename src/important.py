def requirements():
    return ["re","dev_users"]


def main(client, re, dev_users):
    import nextcord as discord
    import random
    import External_functions as ef
    import io
    # from gi.repository import Notify
    @client.command()
    async def f(ctx):
        urls = [
            "https://c.tenor.com/BaJDchtzSMQAAAAC/f-letter-f-burts.gif",
            "https://c.tenor.com/rtnshG9YFykAAAAd/rick-astley-rick-roll.gif",
            "https://c.tenor.com/Mk3HGIMZ0mcAAAAC/fairy-oddparents-f-dancing.gif",
            "https://c.tenor.com/J4bVExaxn5oAAAAd/efemann-efe.gif",
            "https://c.tenor.com/H8DA2jkNgtwAAAAC/team-fortress2-pay-respects.gif",
            "https://c.tenor.com/L68DS0H7Mp8AAAAC/triggered-letter-f.gif",
        ]
        embed = discord.Embed(color=discord.Color(re[8]))
        url = random.choice(urls)
        print(urls.index(url))
        print(url)
        embed.set_image(url=url)
        await ctx.send(embed=embed)

    @client.command(aliases=["s_e"])
    async def search_emoji(ctx, name):
        try:
            emoji_names = [i.name for i in client.emojis]
            st = ""
            for i in emoji_names:
                if i.lower().find(name.lower()) != -1:
                    st += i + "\n"
            if st == "":
                st = "Not found"
            embed = discord.Embed(
                title="Emojis found", description=st, color=discord.Color(value=re[8])
            )
            embed.set_thumbnail(url=client.user.avatar.url)
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(
                embed=discord.Embed(
                    description=str(e), color=discord.Color(value=re[8])
                )
            )

    @client.command(aliases=["src", "github", "source_code", "sc", "source"])
    async def repo(ctx):
        embed = discord.Embed(
            title="Source Code for Alfred",
            description="[Here you go, click this link and it'll redirect you to the github page](https://github.com/alvinbengeorge/alfred-discord-bot)",
            color=discord.Color(value=re[8]),
        )
        embed.set_thumbnail(
            url="https://github.githubassets.com/images/modules/open_graph/github-octocat.png"
        )
        embed.set_image(url=client.user.avatar.url)
        await ctx.send(embed=embed)

    @client.command()
    async def batsignal(ctx):
        # https://c.tenor.com/0GJ-XEcYLfcAAAAd/wongwingchun58.gif
        alvin = client.get_user(432801163126243328).mention
        await ctx.send(str(alvin) + " You've been summoned by " + ctx.author.name)
        await ctx.send("https://c.tenor.com/0GJ-XEcYLfcAAAAd/wongwingchun58.gif")

    @client.command()
    async def get_invite(ctx, time=300):
        link = await ctx.channel.create_invite(max_age=int(time))
        await ctx.send(
            embed=discord.Embed(
                title="Invitation link",
                description=str(link),
                color=discord.Color(value=re[8]),
            )
        )
    
    @client.command()
    async def yey(ctx):
        re[0]+=1
        print("yey")
        em = ef.cembed(title="*yey*", color=re[8])
        await ctx.send(embed=em)
    
    @client.command()
    async def lol(ctx):
        re[0]+=1
        em = ef.cembed(title="***L😂L***", color=re[8])
        await ctx.send(embed=em)


    @client.command()
    async def reply(ctx, channel, user, *, repl):
        if str(ctx.author.id) in dev_users and ctx.guild.id == 822445271019421746:
            channel = client.get_channel(int(channel))
            if not channel:
                await ctx.send(
                    embed=ef.cembed(
                        description="This channel does not exist",
                        color=re[8]
                    )
                )
                return
            await channel.send(f"<@{user}>",
                embed=ef.cembed(
                    description = repl,
                    color=re[8]
                )
            )
        else:
            await ctx.send(
                embed=ef.cembed(
                    title="Permissions Denied",
                    description="You cannot execute this command here" if ctx.guild.id != 822445271019421746 else "You're not a developer to do this",
                    color=re[8]
                )
            )

    @client.command(aliases = ['developers','dev','contributors'])
    async def contribution(ctx):
        embed=ef.cembed(
            title="Contributors and Contributions",
            description="Hey guys, if you've been Developers of Alfred, Thank you very much for your contribution in this project. Our intend for this project was openness and we've gained it, I would like to thank everyone who is seeing this message, and thank you for accepting Alfred. Alfred crossed 90 servers recently, has more than 90,000 users.\n\nIf you want to take part in this, go to our [github page](https://www.github.com), here you can check our code and fork the repository and add a function and send us a PR. If you wish to know more about Alfred, use the feedback command",
            color = re[8],
            footer = "Have a great day",
            thumbnail = client.user.avatar.url,
            image="attachment://contrib.png"
        )
        fp = ef.svg2png("https://contrib.rocks/image?repo=alvinbengeorge/alfred-discord-bot")
        file = discord.File(io.BytesIO(fp), 'contrib.png')
        await ctx.send(file=file, embed=embed)
