from wolframalpha import *


def requirements():
    return [
        "re",
        "wolfram",
        "dev_channel",
    ]


def main(client, re, AiD, dev_channel):
    import discord
    import io
    import requests
    import urllib.parse

    w = Client(AiD)

    def get_answer(question=""):
        if question == "":
            embed = discord.Embed(
                title="Oops",
                description="You need to enter a question",
                color=discord.Color(value=re[8]),
            )
            embed.set_thumbnail(url=client.user.avatar_url_as(format="png"))
            return embed
        else:
            res = w.query(question)
            st = ""
            pic = ""
            for i in res["pod"]:
                try:
                    a = (str(i["@title"]), str(i["subpod"]["img"]["@alt"]))
                    if a[0] == "Number line" or a[0] == "Plot":
                        a = ("\n", "\n")
                        pic = str(i["subpod"]["img"]["@src"])
                    st += f"**{a[0]}**\n{a[1]}\n\n"
                except Exception as e:
                    print(e)
            embed = discord.Embed(
                title=question, description=st, color=discord.Color(value=re[8])
            )
            embed.set_thumbnail(url=client.user.avatar_url_as(format="png"))
            embed.set_image(url=pic)
            return (embed, None)

    @client.command()
    async def wolf(ctx, *, question):
        out = get_answer1(question)
        await ctx.send(embed=out[0], file=out[1])

    def get_answer1(question=""):
        if question == "":
            embed = discord.Embed(
                title="Oops",
                description="You need to enter a question",
                color=discord.Color(value=re[8]),
            )
            embed.set_thumbnail(url=client.user.avatar_url_as(format="png"))
            return (embed, None)
        else:
            question = urllib.parse.quote(question)
            a = requests.get(
                f"http://api.wolframalpha.com/v1/simple?appid={AiD}&i={question}&layout=labelbar&width=1500"
            ).content
            file = open("output.png", "wb")
            file.write(a)
            file.close()
            embed = discord.Embed(
                title="Wolfram",
                description="This result is from Wolfram",
                color=discord.Color(value=re[8]),
            )
            embed.set_thumbnail(
                url="https://www.wolfram.com/homepage/img/carousel-wolfram-alpha.png"
            )
            file = discord.File("output.png")
            embed.set_image(url="attachment://output.png")
            return (embed, file)
