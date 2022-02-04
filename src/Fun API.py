from functools import lru_cache
import nextcord as discord
import os
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
    async def gen(ctx, *, text):
        print(ctx.guild.name)
        re[0]+=1
        API_URL2 = "https://api-inference.huggingface.co/models/EleutherAI/gpt-neo-2.7B"
        header2 = {"Authorization": f"Bearer {os.environ['transformers_auth']}"}
        payload2 = {
            "inputs": text,
            "parameters": {"max_new_tokens": 100, "return_full_text": True},
        }

        output = await ef.post_async(API_URL2, header2, payload2)
        print(output)
        o = output[0]["generated_text"]
        
        await ctx.reply(
            embed=ef.cembed(
                title="Generated text", description=o, color=re[8],thumbnail=client.user.avatar_url_as(format="png")
            )
        )
      
      
    @client.command()
    async def kanye(ctx):
        re[0] += 1
        text = await ef.get_async("https://api.kanye.rest", kind="json");text=text["quote"]
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
    async def apis(ctx, page: int = 0):
        a = await ef.get_async("https://api.publicapis.org/entries",kind="json")
        b=a['entries']
        embeds=[]
        for i in range(a['count']):
            text=f"{b[i]['Description']}\n\n\nAuth: {b[i]['Auth'] if b[i]['Auth']!='' else None}\nHTTPS: {b[i]['HTTPS']}\nCors: {b[i]['Cors']}\nCategory: {b[i]['Category']}"
            embed = ef.cembed(
                title=b[i]['API'],
                description=text,
                color=re[8],
                url=b[i]['Link'],
                footer=f"{i+1} of {a['count']}"
            )
            embeds.append(embed)

        await pa1(embeds,ctx,page)

        
    @client.command()
    async def pokemon(ctx, pokemon=None):
        re[0] + re[0] + 1
        try:
            a = await ef.get_async(f"https://pokeapi.co/api/v2/pokemon/{ef.convert_to_url(pokemon.lower())}",kind="json")
        except:
            a = "Not Found"
        if a != "Not Found":
            response = a
            title = response["name"]
            thumbnail = response["sprites"]["front_default"]
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
        a = await ef.get_async(f"https://ipinfo.io/{ip}/geo",kind="json")
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


    @client.command(aliases=["desktop"])
    async def gs_stat(ctx):
        a = await ef.get_async("https://gs.statcounter.com/os-market-share/desktop/worldwide/")
        start = a.find('og:image" content="')+len('og:image" content="')
        end = a.find(".png",start)+len(".png")
        url = a[start:end]
        await ctx.send(embed=ef.cembed(title="Gs.statcounter Desktop OS",description="This contains the market share of desktop operating systems worldwide", color=re[8], thumbnail="https://pbs.twimg.com/profile_images/918460707787681792/fMVNRhz4_400x400.jpg", picture=url))

    @client.command()
    async def csvoyager(ctx, edition):
        embeds=[]
        for i in range(1,20):
            embed = ef.cembed(title="CS Voyager",description=f"{i} of 20",color=re[8],picture=f"https://csvoyager.netlify.app/data/{edition}/{i}.jpg")
            embeds.append(embed)
        await pa1(embeds,ctx)

        
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
                              picture=f"https://render-tron.appspot.com/screenshot/{ef.convert_to_url(i)}/?width=600&height=400")
            embed.url = i
            li.append(embed)
        await pa1(li, ctx)

    @client.command()
    async def lyrics(ctx, *, song):
        j = await ef.get_async(f"https://api.popcat.xyz/lyrics?song={convert_to_url(song)}",kind="json")
        await ctx.send(embed=ef.cembed(title=j['title'],description=j['lyrics'],color=re[8],thumbnail=j['image'],footer=j['artist']))

        
    async def pa1(embeds, ctx, start_from=0):
        message = await ctx.send(embed=embeds[start_from])
        pag = start_from
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
                
