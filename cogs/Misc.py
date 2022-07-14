from random import choice
from nextcord.ext import commands

import utils.External_functions as ef
import utils.helping_hand as h

# Use nextcord.slash_command()

def requirements():
    return ["dev_channel"]

class Misc(commands.Cog):
    def __init__(self, client, dev_channel):
        self.client = client
        self.urls = [
            "https://c.tenor.com/BaJDchtzSMQAAAAC/f-letter-f-burts.gif",
            "https://c.tenor.com/rtnshG9YFykAAAAd/rick-astley-rick-roll.gif",
            "https://c.tenor.com/Mk3HGIMZ0mcAAAAC/fairy-oddparents-f-dancing.gif",
            "https://c.tenor.com/J4bVExaxn5oAAAAd/efemann-efe.gif",
            "https://c.tenor.com/H8DA2jkNgtwAAAAC/team-fortress2-pay-respects.gif",
            "https://c.tenor.com/L68DS0H7Mp8AAAAC/triggered-letter-f.gif",
        ]
        self.dev_channel = dev_channel

    @commands.command()
    @commands.check(ef.check_command)
    async def yey(self, ctx):
        self.client.re[0]+=1
        print("yey")
        em = ef.cembed(title="*yey*", color=self.client.re[8])
        await ctx.send(embed=em)

    @commands.command()
    @commands.check(ef.check_command)
    async def lol(self, ctx):
        self.client.re[0]+=1
        em = ef.cembed(title="***L😂L***", color=self.client.re[8])
        await ctx.send(embed=em)

    @commands.command()
    @commands.check(ef.check_command)
    async def f(self, ctx):
        embed=ef.cembed(
            color=self.client.re[8],
            image=choice(self.urls)
        )
        await ctx.send(embed=embed)
    
    @commands.command()
    async def src(self, ctx):
        await ctx.send(
            embed=h.help_him(self.client, self.client.re)[1]
        )

    @commands.command()
    @commands.check(ef.check_command)
    async def nay(self, ctx):
        await ctx.send(
            embed=ef.cembed(
                title="***nay***", 
                description="", 
                color=self.client.re[8]
            )
        )

    @commands.command()
    @commands.check(ef.check_command)
    async def eng2pig(self, ctx, *, data):
        output = ""
        for i in data.split(" "):
            a = str(i)
            a = a.lower()
            a = a + a[0] + "ay"
            a = list(a)
            a.remove(a[0])

            a = "".join(a)
            output += a + " "
        await ctx.send(
            embed=ef.cembed(
                title="igpay atinlay",
                description=str(output),
                color=self.client.re[8],
            )
        )

    @commands.command()
    @commands.check(ef.check_command)
    async def pig2eng(self, ctx, *, data):
        output = ""
        for i in data.split(" "):
            b = i.lower()
            for i in range(1, 3):
                b = b[:-1]

            b = b[len(b) - 1] + b[0 : len(b) - 1]
            output += b + " "
        await ctx.send(
            embed=ef.cembed(
                title="English Again",
                description=str(output),
                color=self.client.re[8],
            )
        )

    @commands.command()
    @commands.check(ef.check_command)
    async def batsignal(self, ctx, *, text="I'm guessing it's just a hello"):
        channel = self.client.get_channel(self.dev_channel)
        await channel.send(
            embed=ef.cembed(
                author=ctx.author,
                description=text,
                title="BatSignal",
                footer=f"This happened in {ctx.guild.name}",
                color=self.client.re[8],
                image="https://c.tenor.com/0GJ-XEcYLfcAAAAM/wongwingchun58.gif",
                thumbnail=self.client.user.avatar.url
            )
        )
        await ctx.send(
            embed=ef.cembed(
                title="BatSignal",
                author=ctx.author,
                color=self.client.re[8],
                image="https://c.tenor.com/0GJ-XEcYLfcAAAAM/wongwingchun58.gif",
                thumbnail=self.client.user.avatar.url
            )
        )


def setup(client,**i):
    client.add_cog(Misc(client,**i))