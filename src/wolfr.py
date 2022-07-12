import utils.External_functions as ef

def requirements():
    return [
        "re",
        "wolfram"
    ]


def main(client, re, AiD):
    import nextcord
    import urllib.parse
    from nextcord.ext import commands
    
    @client.command()
    @commands.check(ef.check_command)
    async def wolf(ctx, *, question=""):
        embed, file = await get_answer1(question)
        await ctx.send(embed=embed, file=file)

    async def get_answer1(question=""):
        if question == "":
            embed = ef.cembed(
                title="Oops",
                description="You need to enter a question",
                color=re[8],
                thumbnail = client.user.avatar.url
            )
            return (embed, None)
        else:
            question = urllib.parse.quote(question)
            a = await ef.get_async(
                f"http://api.wolframalpha.com/v1/simple?appid={AiD}&i={question}&layout=labelbar&width=1000",kind="fp"
            )
            file = nextcord.File(a, "output.png")
            embed = ef.cembed(
                title="Wolfram",
                description="This result is from Wolfram",
                color=re[8],
                thumbnail= "https://www.wolfram.com/homepage/img/carousel-wolfram-alpha.png",
                image="attachment://output.png"
            )            
            return (embed, file)