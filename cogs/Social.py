import nextcord
import utils.assets as assets
import utils.External_functions as ef
import utils.inshort as inshort

from nextcord.ext import commands
from wikipedia import search, summary

NEWS_CATEGORIES = inshort.get_categories() + ['all']


def requirements():
    return ["dev_channel"]

class Social(commands.Cog):
    def __init__(self, client, dev_channel):
        self.client = client
        self.dev_channel = dev_channel
        self.link_for_cats = []

    @nextcord.slash_command(name="social", description="Contains all the social cog slash commands")
    async def social(self, inter):
        print(inter.user)        

    @social.subcommand(name="reddit", description="Get posts from reddit")
    async def reddit_slash(self, inter, account="wholesomememes", number=1):
        self.client.re[0]+=1
        await inter.response.defer()
        await self.reddit_search(inter, account, number)    
    
    @commands.command(aliases=["reddit"])
    @commands.check(ef.check_command)
    async def reddit_search(self, ctx, account="wholesomememes", number=1):
        a = await ef.redd(ctx, account, number)
        await assets.pa(ctx, a)

    @social.subcommand(name="imdb", description="Give a movie name")
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
                    author=self.client.user,
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

    @social.subcommand(name="wikipedia", description="Get a topic from wikipedia")
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
        j = await ef.get_async("https://api.popcat.xyz/meme", kind="json")
        await ctx.send(
            embed=ef.cembed(
                title=j.get('title','Unavaiable'),
                image=j.get('image'),
                color=self.client.re[8],
                thumbnail=self.client.user.avatar.url,
                footer=f"{j.get('upvotes')} Upvotes | {j.get('comments')} Comments"
            )
        )

    @social.subcommand(name="memes", description="Memes from Alfred yey")
    async def memes_slash(self, inter):
        await inter.response.defer()
        await self.memes(inter)

    @social.subcommand(name="news", description="Latest news from a given subject from inshorts")
    async def news_slash(self, inter: nextcord.Interaction, subject: str = ef.defa(choices=NEWS_CATEGORIES, default="all")):
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
    
        

def setup(client, **i):
    client.add_cog(Social(client,**i))
