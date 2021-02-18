import discord
from discord.ext import commands
from googlesearch import search
try:
    client=commands.Bot(command_prefix="'")
    @client.event
    async def on_ready():
        print("Prepared")

    @client.command()
    async def google(ctx,*,text):        
        print(text)
        li=""
        for i in search(text,num=10,stop=10,pause=0):
            li=li+i+" \n"
        await ctx.send(li)
    @client.command()
    async def g(ctx,*,text):        
        print(text)
        li=""
        for i in search(text,num=10,stop=10,pause=0):
            li=li+i+" \n"
        await ctx.send(li)
    client.run("ODExNTkxNjIzMjQyMTU0MDQ2.YC0bmQ.4oW1hyppcaQJpRfKFRJCiddZ5aI")
except:
    print("Something has occured")
