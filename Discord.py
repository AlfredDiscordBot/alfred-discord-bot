import discord
from discord.ext import commands
from googlesearch import search
import math as ma
import statistics as s

try:
    client=commands.Bot(command_prefix="'")
    @client.event
    async def on_ready():
        print("Prepared")
    
    @client.command()
    async def check(ctx):
        print("check")
        em=discord.Embed(title="*Online*")
        await ctx.send(embed=em)
    @client.command()
    async def yey(ctx):
        print("yey")
        em=discord.Embed(title="*yey*")
        await ctx.send(embed=em)
    @client.command()
    async def g(ctx,*,text):        
        print(text)
        li="**"+text+"** \n\n"
        for i in search(text,num=7,stop=7,pause=0):
            li=li+i+" \n\n"
        text=text.replace(' ','%20')
        li=li+"**Query link:**https://www.google.com/search?q="+text+"\n"
        await ctx.send(li)
    @client.command()
    async def google(ctx,*,text):        
        print(text)
        li="**"+text+"** \n\n"
        for i in search(text,num=7,stop=7,pause=0):
            li=li+i+" \n\n"
        text=text.replace(' ','%20')
        li=li+"**Query link:**https://www.google.com/search?q="+text+"\n"
        await ctx.send(li)
    @client.command()
    async def m(ctx,*,text):
        pi=ma.pi
        a=eval(text)
        text=text.replace("ma.","")
        text=text.replace("s.","")        
        print(text)
        em=discord.Embed(title=text,description=text+"="+str(a),color=ctx.author.color)
        await ctx.send(embed=em)
    @client.command()
    async def meth(ctx,*,text):
        pi=ma.pi
        a=eval(text)
        text=text.replace("ma.","")
        text=text.replace("s.","")        
        print(text)
        em=discord.Embed(title=text,description=text+"="+str(a),color=ctx.author.color)
        await ctx.send(embed=em)
    def r(x):
        return ma.radians(x)
    def d(x):
        return ma.degrees(x)
    @client.command()
    async def p(ctx,*,text):
        print("P"+text)
        a=eval(text)
        ans=ma.factorial(a[0])/ma.factorial(a[0]-a[1])
        em=discord.Embed(title="P"+text+":",description=str(ans),color=ctx.author.color)
        await ctx.send(embed=em)
    @client.command()
    async def c(ctx,*,text):
        print("c"+text)
        a=eval(text)
        ans=ma.factorial(a[0])/(ma.factorial(a[1])*ma.factorial(a[0]-a[1]))
        em=discord.Embed(title="C"+text+":",description=str(ans),color=ctx.author.color)
        await ctx.send(embed=em)
    
    
    client.remove_command("help")
    @client.group(invoke_without_command=True)
    async def help(ctx):
        text="'google <text to search> \n'help to get this screen\n'c (n,r) for *combination* \n'p (n,r) for *permutation* \n'meth <Expression> for any math calculation *(includes statistic)*\n**ma** for math module\n**s** for statistics module \nr(angle in degree) to convert angle to radians \nd(angle in radian) to convert angle to radian\n\n**Alias**: \n'g <text to search> \n'h to show this message \n'm <Expression> for any math calculation *(includes statistic)*\n"
        em=discord.Embed(title="**HELP** \n",description=text,color=ctx.author.color)   
        await ctx.send(embed=em)
    @client.group(invoke_without_command=True)
    async def h(ctx):
        text="'google <text to search> \n'help to get this screen\n'c (n,r) for *combination* \n'p (n,r) for *permutation* \n'meth <Expression> for any math calculation *(includes statistic)*\n**ma** for math module\n**s** for statistics module \nr(angle in degree) to convert angle to radians \nd(angle in radian) to convert angle to radian\n\n**Alias**: \n'g <text to search> \n'h to show this message \n'm <Expression> for any math calculation *(includes statistic)*\n"
        em=discord.Embed(title="**HELP** \n",description=text,color=ctx.author.color)
        await ctx.send(embed=em)   
    client.run("ODExNTkxNjIzMjQyMTU0MDQ2.YC0bmQ.4oW1hyppcaQJpRfKFRJCiddZ5aI")
except:
    print("Something has occured")
