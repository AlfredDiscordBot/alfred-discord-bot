import discord
from discord.ext import commands
from googlesearch import search
try:
    client=commands.Bot(command_prefix="'")
    @client.event
    async def on_ready():
        print("Prepared")

    @client.command()
    async def g(ctx,*,text):        
        print(text)
        li=""
        for i in search(text,num=7,stop=7,pause=0):
            li=li+i+" \n\n"
        await ctx.send(li)
    @client.command()
    async def google(ctx,*,text):        
        print(text)
        li=""
        for i in search(text,num=7,stop=7,pause=0):
            li=li+i+" \n\n"
        await ctx.send(li)
    client.remove_command("help")
    @client.group(invoke_without_command=True)
    async def help(ctx):
        text="'google <text to search> \n'help to get this screen \n\nAlias: \n'g <text to search>"
        em=discord.Embed(title="**HELP** \n",description=text,color=ctx.author.color)
        await ctx.send(embed=em)
    @client.group(invoke_without_command=True)
    async def h(ctx):
        text="'google <text to search> \n'help to show this message \n\nAlias: \n'g <text to search> \n'h to show this message"
        em=discord.Embed(title="**HELP** \n",description=text,color=ctx.author.color)
        await ctx.send(embed=em)   
    client.run("ODExNTkxNjIzMjQyMTU0MDQ2.YC0bmQ.4oW1hyppcaQJpRfKFRJCiddZ5aI")
except:
    print("Something has occured")

