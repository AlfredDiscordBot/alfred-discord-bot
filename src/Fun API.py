def requirements():
    return ["re"]


def main(client, re):
    import discord
    import requests
    import urllib.parse

    def convert_to_url(name):
        name = urllib.parse.quote(name)
        return name

    @client.command()
    async def kanye(ctx):
        re[0] += 1
        text = eval(requests.get("https://api.kanye.rest").content.decode())["quote"]
        embed = discord.Embed(
            title="Kanye Rest", description=text, color=discord.Color(value=re[8])
        )
        embed.set_thumbnail(
            url="https://i.pinimg.com/originals/3b/84/e1/3b84e1b85fb0a8068044df8b6cd8869f.jpg"
        )
        await ctx.send(embed=embed)

    @client.command()
    async def age(ctx, name):
        try:
            re[0] += 1
            text = eval(
                requests.get(f"https://api.agify.io/?name={name}").content.decode()
            )
            st = ""
            for i in text:
                st += i + ":" + str(text[i]) + "\n"
            await ctx.send(
                embed=discord.Embed(
                    title="Agify", description=st, color=discord.Color(value=re[8])
                )
            )
        except:
            await ctx.send(
                embed=discord.Embed(
                    title="Oops",
                    description="Something went wrong",
                    color=discord.Color(value=re[8]),
                )
            )

    @client.command()
    async def pokemon(ctx, pokemon):
        re[0] + re[0] + 1
        true = True
        false = False
        null = None
        a = requests.get(
            f"https://pokeapi.co/api/v2/pokemon/{pokemon.lower()}"
        ).content.decode()
        if a != "Not Found":
            response = eval(a)
            title = response["name"]
            thumbnail = response["sprites"]["back_default"]
            ability = "**ABILITIES:**\n"
            for i in response["abilities"]:
                ability += i["ability"]["name"] + "\n"
            weight = "\n**WEIGHT**\n" + str(response["weight"])
            embed = discord.Embed(
                title=title,
                description=ability + weight,
                color=discord.Color(value=re[8]),
            )
            embed.set_thumbnail(url=thumbnail)
            await ctx.send(embed=embed)
        else:
            await ctx.send(
                embed=discord.Embed(
                    title="Hmm",
                    description="Not found",
                    color=discord.Color(value=re[8]),
                )
            )

    @client.command()
    async def ip(ctx, *, ip):
        re[0] + re[0] + 1
        ip = convert_to_url(ip)
        print(ip)
        print(f"https://ipinfo.io/{ip}/geo")
        a = eval(requests.get(f"https://ipinfo.io/{ip}/geo").content.decode())
        st = ""
        if "status" not in list(a.keys()):
            for i in list(a.keys()):
                st += f"**{i}**:\n{a[i]}\n\n"
            embed = discord.Embed(
                title=ip, description=st, color=discord.Color(value=re[8])
            )
            embed.set_thumbnail(url=client.user.avatar_url_as(format="png"))
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Oops",
                description="Oops, couldnt find it :confused:",
                color=discord.Color(value=re[8]),
            )
            embed.set_thumbnail(url=client.user.avatar_url_as(format="png"))
            await ctx.send(embed=embed)

    @client.command(aliases=["cat"])
    async def cat_fact(ctx):
        re[0] + re[0] + 1
        a = eval(requests.get("https://catfact.ninja/fact").content.decode())
        embed = discord.Embed(
            title="Cat Fact", description=a["fact"], color=discord.Color(value=re[8])
        )
        embed.set_thumbnail(url="https://i.imgur.com/u1TPbIp.png?1")
        await ctx.send(embed=embed)
