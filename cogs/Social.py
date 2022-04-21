import nextcord
import assets
import time
import helping_hand
import External_functions as ef
import emoji
import asyncio
import traceback
import urllib

from nextcord.abc import GuildChannel
from nextcord import Interaction, SlashOption, ChannelType
from nextcord.ext import commands, tasks
from random import choice
from wikipedia import search, summary

def requirements():
    return []

class Social(commands.Cog):
    def __init__(self, client):
        self.client = client
        

    @commands.command()
    @commands.check(ef.check_command)
    async def quote(self, ctx):
        embed = await ef.quo(self.client.re[8])
        await ctx.send(embed=embed)
    
    @nextcord.slash_command(name="quote",description="Get a random quote")
    async def quo_slash(self, inter):
        await inter.response.defer()
        await self.quote(inter)

    @nextcord.slash_command(
        name="reddit",
        description="Gives you a random reddit post from the account you specify",
    )
    async def reddit_slash(self, inter, account="wholesomememes"):
        self.client.re[0]+=1
        await inter.response.defer()
        await self.reddit_search(inter, account)
    
    
    @commands.command(aliases=["reddit"])
    @commands.check(ef.check_command)
    async def reddit_search(self, ctx, account="wholesomememes", number=1):
        if number == 1:
            embeds = []
            a = await ef.redd(account, number = 40, single=False)
            if a[2]:
                for i in a:
                    embeds += [
                        ef.cembed(
                            description="**" + i[0] + "**",
                            picture=i[1],
                            color=self.client.re[8],
                            thumbnail=self.client.user.avatar.url,
                        )
                    ]
                await assets.pa(ctx, embeds, start_from=0, restricted=False)
            else:
                await ctx.send(embed=ef.cembed(title=a[0], color=self.client.re[8], description=a[1]))

    @nextcord.slash_command(name="wikipedia", description="Get a topic from wikipedia")
    async def wiki_slash(self, inter, text):
        await inter.response.defer()
        await self.wikipedia(inter, text = text)
    
    
    @commands.command(aliases=["w"])
    @commands.check(ef.check_command)
    async def wikipedia(self, ctx, *, text):
        embeds = []
        if not ctx.channel.nsfw:
            await ctx.send(
                embed=ef.cembed(
                    title="New update",
                    description="After an update from a Discord Bot Listing Website, I found out that NSFW content can be found in Wikipedia. Doesn't mean that we purged the entire wikipedia command, it's now only allowed in NSFW channel",
                    footer="Sorry for the inconvenience",
                    color=self.client.re[8],
                    thumbnail=self.client.user.avatar.url
                )
            )
            return
        for i in search(text):
            t = str(i.encode("utf-8"))
            em = ef.cembed(
                title=t.decode().title(),
                description=str(summary(t, sentences=5)),
                color=nextcord.Color(value=re[8]),
                thumbnail="https://1000logos.net/wp-content/uploads/2017/05/Wikipedia-logos.jpg"
            )
            embeds.append(em)
        await assets.pa(ctx, embeds, start_from=0, restricted=False)
    
        

def setup(client, **i):
    client.add_cog(Social(client,**i))