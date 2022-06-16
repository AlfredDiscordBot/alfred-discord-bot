import nextcord
import assets
import time
import helping_hand
import External_functions as ef
import emoji
import asyncio
import traceback
import urllib
import inshort

from nextcord.abc import GuildChannel
from nextcord import Interaction, SlashOption, ChannelType
from nextcord.ext import commands, tasks
from random import choice
from wikipedia import search, summary

def requirements():
    return ["dev_channel"]

class Social(commands.Cog):
    def __init__(self, client, dev_channel):
        self.client = client
        self.dev_channel = dev_channel
        self.link_for_cats = []
        

    @commands.command()
    @commands.check(ef.check_command)
    async def quote(self, ctx):
        embed = await ef.quo(self.client.re[8])
        await ctx.send(embed=embed)
    
    @nextcord.slash_command(name="quote",description="Get a random quote")
    async def quo_slash(self, inter):
        await inter.response.defer()
        await self.quote(inter)

    @nextcord.slash_command(name="reddit")
    async def reddit_slash(self, inter, account="wholesomememes", number=1):
        self.client.re[0]+=1
        await inter.response.defer()
        await self.reddit_search(inter, account, number)
    
    
    @commands.command(aliases=["reddit"])
    @commands.check(ef.check_command)
    async def reddit_search(self, ctx, account="wholesomememes", number=1):
        a = await ef.redd(ctx, account, number)
        await assets.pa(ctx, a)

    @nextcord.slash_command(name="imdb", description="Give a movie name")
    async def imdb_slash(self, inter, movie):
        await inter.response.defer()
        try:
            await inter.send(embed = ef.imdb_embed(movie, self.client.re))
        except Exception as e:
            await inter.send(
                embed=ef.cembed(
                    title="Oops",
                    description=str(e),
                    color=self.client.re[8],
                    thumbnail=self.client.user.avatar.url,
                )
            )

    @commands.command()
    @commands.check(ef.check_command)
    async def imdb(self, ctx, *, movie):
        await ctx.send(embed=ef.imdb_embed(movie,self.client.re))

    @commands.command(aliases = ['zoo','animals'])
    @commands.check(ef.check_command)
    async def animal(self,ctx):        
        embeds=await ef.animals(self.client,ctx,self.client.re[8])
        await assets.pa(ctx, embeds)

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
                title=str(t).title(),
                description=str(summary(t, sentences=5)),
                color=nextcord.Color(value=self.client.re[8]),
                thumbnail="https://1000logos.net/wp-content/uploads/2017/05/Wikipedia-logos.jpg"
            )
            embeds.append(em)
        await assets.pa(ctx, embeds, start_from=0, restricted=False)

    @commands.command(aliases=["::"])
    @commands.check(ef.check_command)
    async def memes(self, ctx):
        if len(self.link_for_cats) == 0:
            try:            
                print("Finished meme")
                self.link_for_cats += await ef.memes1()
                print("Finished meme1")
                self.link_for_cats += await ef.memes2()
                print("Finished meme2")
                self.link_for_cats += await ef.memes3()
                print("Finished meme3")
                self.link_for_cats += await ef.memes4()
                print("Finished meme4")
            except Exception as e:
                await ctx.channel.send(
                    embed=ef.cembed(
                        title="Meme issues",
                        description="Something went wrong during importing memes\n"
                        + str(e),
                        color=self.client.re[8],
                        thumbnail=self.client.user.avatar.url,
                    )
                )
        await ctx.send(choice(self.link_for_cats))

    @nextcord.slash_command(name="memes", description="Memes from Alfred yey")
    async def memes_slash(self, inter):
        await inter.response.defer()
        await self.memes(inter)

    @nextcord.slash_command(name="news", description="Latest news from a given subject")
    async def news_slash(self, inter, subject="all"):
        self.client.re[0]+=1  
        await inter.response.defer()
        await self.news(inter, subject)
    
    @commands.command()
    @commands.check(ef.check_command)
    async def news(self, ctx, subject="all"):
        d = await inshort.getNews(subject)
        if not d['success']:
            await ctx.send(
                embed=ef.cembed(
                    title="Error",
                    description=d['error'],
                    color=self.client.re[8]
                )
            )
            return
        embeds = []
        for i in d['data']:
            embed=ef.cembed(
                title=i['title'],
                image=i['imageUrl'],
                description=i['content'],
                url=i['url'],
                footer=i['date']+ "|" +" From Inshorts",
                color=self.client.re[8]
            )
            embed.set_author(name = i['author'], icon_url = "https://pbs.twimg.com/profile_images/627085479268126720/k4Wwj-lS_400x400.png")
            embed.add_field(name = "ReadMore", value = f"[Here]({i['readMoreUrl']})")
            embeds.append(embed)
        await assets.pa(ctx,embeds)
            

    @nextcord.slash_command(name="instagram",description="get recent instagram posts of the account")
    async def insta_slash(self, ctx, account):
        await ctx.response.defer()
        await self.instagram(ctx, account = account)

    @commands.command(alias=['insta'])
    @commands.check(ef.check_command)
    async def instagram(self, ctx, account):    
        embeds = []
        pop_in = await ef.get_async(f"https://api.popcat.xyz/instagram?user={ef.convert_to_url(account)}", kind="json")
        if pop_in.get('error'):
            await ctx.send(
                embed=ef.cembed(
                    title="Error",
                    description=pop_in['error'],
                    color=self.client.re[8]
                )
            )
            return
        elif pop_in.get('private'):
            embed=ef.cembed(
                title=pop_in.get("full_name"),
                description=pop_in.get("biography"),
                color=self.client.re[8],
                thumbnail=pop_in.get("profile_pic"),
                footer="This user has a private account, cannot share his posts, sorry for the inconvenience"
            )
            for i in ("followers", "following"):
                embed.add_field(name=i, value=pop_in.get(i))
            await ctx.send(embed=embed)
            return
        embed=ef.cembed(
            title=pop_in.get("full_name"),
            description=pop_in.get("biography"),
            color=self.client.re[8],
            thumbnail=pop_in.get("profile_pic")
        )
        for i in ("followers", "following", "posts", "reels", "private", "verified"):
            embed.add_field(name=i, value=str(pop_in.get(i)))
        embeds.append(embed)
        try:
            links = ef.instagram_get1(
                account,
                self.client.re[8],
                self.client.re[9]
            )
            if links == "User Not Found, please check the spelling":
                await ctx.send(
                    embed=ef.cembed(
                        title="Hmm",
                        description=links,
                        color=self.client.re[8],
                        thumbnail=self.client.user.avatar.url
                    )
                )
                return
            if type(links) == str:
                self.client.re[9]=links
                links=ef.instagram_get1(
                    account,
                    self.client.re[8],
                    self.client.re[9]
                )            
            for a in links:
                if a is not None and type(a) != str:
                    embeds.append(a[0])
                elif type(a) != str:
                    self.client.re[9] = links
                else:                
                    await ctx.send(
                        embed=nextcord.Embed(
                            description="Oops!, something is wrong.",
                            color=nextcord.Color(value=self.client.re[8]),
                        )
                    )
                    break
            await assets.pa(ctx, embeds, start_from=0, restricted=False)
        except IndexError:
            embed = ef.cembed(
                title="Error in instagram",
                description=f"Sorry, we couldnt find posts in {account}, please check again if it's private or if {account} has posted anything",
                color=self.client.re[8],
                thumbnail=self.client.user.avatar.url,
            )
            await ctx.send(embed=embed)
            await self.client.get_channel(self.dev_channel).send(embed=embed)
    
        

def setup(client, **i):
    client.add_cog(Social(client,**i))
