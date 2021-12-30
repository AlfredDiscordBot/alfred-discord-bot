from functools import lru_cache
import discord
from discord import Color
from discord.ext import commands
import aiohttp
import asyncio
from bs4 import BeautifulSoup
import datetime
import requests
import urllib.parse
from googlesearch import search
import External_functions as ef

def requirements():
    return ["re"]
  
  
def main(client, re):
    def convert_to_url(name):
        name = urllib.parse.quote(name)
        return name
      
      
    @client.command()
    async def kanye(ctx):
        re[0] += 1
        text = eval(requests.get(
            "https://api.kanye.rest").content.decode())["quote"]
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
                 requests.get(
                    f"https://api.agify.io/?name={name}").content.decode()
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

        
    @client.command(aliases=["g"])
    async def google(ctx, *, text):
        re[0] += 1
        li = []
        print(text, str(ctx.author))
        for i in search(text, num=5, stop=5, pause=0):
             # https://render-tron.appspot.com/screenshot/https://discord.com/?width=1458&height=690
            embed = ef.cembed(title="Google",
                              color=re[8],
                              thumbnail=client.user.avatar_url_as(
                                  format="png"),
                              picture=f"https://render-tron.appspot.com/screenshot/{i}/?width=1458&height=690")
            embed.url = i
            li.append(embed)
        await pa1(li, ctx)

        
    async def pa1(embeds, ctx):
        message = await ctx.send(embed=embeds[0])
        pag = 0
        await message.add_reaction("◀️")
        await message.add_reaction("▶️")
        def check(reaction, user):
            return (
                user != client.user
                and str(reaction.emoji) in ["◀️", "▶️"]
                and reaction.message.id == message.id
            )
        while True:
            try:
                reaction, user = await client.wait_for(
                    "reaction_add", timeout=360, check=check
                )
                await message.remove_reaction(reaction, user)
                if str(reaction.emoji) == "▶️" and pag + 1 != len(embeds):
                    pag += 1
                    await message.edit(embed=embeds[pag])
                elif str(reaction.emoji) == "◀️" and pag != 0:
                    pag -= 1
                    await message.edit(embed=embeds[pag])
            except asyncio.TimeoutError:
                break
                