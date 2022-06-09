import External_functions as ef

def requirements():
    return [
        "re",
        "wolfram",
        "dev_channel",
    ]


def main(client, re, AiD, dev_channel):
    import nextcord
    import io
    import requests
    import urllib.parse
    from nextcord.ext import commands
    
    @client.command()
    @commands.check(ef.check_command)
    async def wolf(ctx, *, question=""):
        out = await get_answer1(question)
        await ctx.send(embed=out[0], file=out[1])
        if 'output.png' in os.listdir(): os.remove("output.png")

    async def get_answer1(question=""):
        if question == "":
            embed = ef.cembed(
                title="Oops",
                description="You need to enter a question",
                color=nextcord.Color(value=re[8]),
                thumbnail = client.user.avatar.url
            )
            return (embed, None)
        else:
            question = urllib.parse.quote(question)
            a = await ef.get_async(
                f"http://api.wolframalpha.com/v1/simple?appid={AiD}&i={question}&layout=labelbar&width=1500",kind="file>output.png"
            )
            embed = nextcord.Embed(
                title="Wolfram",
                description="This result is from Wolfram",
                color=nextcord.Color(value=re[8]),
            )
            embed.set_thumbnail(
                url="https://www.wolfram.com/homepage/img/carousel-wolfram-alpha.png"
            )
            file = nextcord.File("output.png")
            embed.set_image(url="attachment://output.png")
            return (embed, file)