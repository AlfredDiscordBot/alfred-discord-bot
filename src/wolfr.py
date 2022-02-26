from wolframalpha import *
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

    w = Client(AiD)

    def get_answer(question=""):
        if question == "":
            embed = nextcord.Embed(
                title="Oops",
                description="You need to enter a question",
                color=nextcord.Color(value=re[8]),
            )
            embed.set_thumbnail(url=client.user.avatar.url)
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
            embed = nextcord.Embed(
                title=question, description=st, color=nextcord.Color(value=re[8])
            )
            embed.set_thumbnail(url=client.user.avatar.url)
            embed.set_image(url=pic)
            return (embed, None)

    @client.command()
    async def wolf(ctx, *, question=""):
        out = get_answer1(question)
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
                f"http://api.wolframalpha.com/v1/simple?appid={AiD}&i={question}&layout=labelbar&width=1500"
            ).content
            file = open("output.png", "wb")
            file.write(a)
            file.close()
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
