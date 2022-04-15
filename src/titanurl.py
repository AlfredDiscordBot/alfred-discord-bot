def requirements():
    return ["re"]


def main(client, re):
    import nextcord as discord
    from discord.ext import commands
    import External_functions as ef
    import requests

    @client.command()
    @commands.check(ef.check_command)
    async def titan(ctx, url, mode="random", preference="blah"):
        with requests.Session() as s:
            true = True
            false = False
            payload = {
                "alias-type": str(mode),
                "original-url": str(url),
                "slug": str(preference),
            }
            header = {
                "user-agent": "Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.115 Safari/537.36",
                "referer": "https://titan-url.herokuapp.com/",
            }
            t = s.post(
                "https://titan-url.herokuapp.com/shorten",
                json=payload,
                headers=header,
            )
            await ctx.send(
                embed=discord.Embed(
                    title="TitanURL",
                    description=eval(str(t.content.decode()))["message"],
                    color=discord.Color(value=re[8]),
                )
            )
