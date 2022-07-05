import nextcord
import assets
import traceback
import External_functions as ef
from nextcord.ext import commands

#Use nextcord.slash_command()

def requirements():
    return []

class FunAPI(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.space = ef.SpaceX(self.client.re[8])
        self.proton = ef.Proton()
        self.tt = ef.TechTerms()
        self.APIs = ef.PublicAPI(self.client)

    @nextcord.slash_command(name="tech", description="Get TechTerms from TechTerms.com")
    async def tech(self, inter, query = "Python"):
        await inter.response.defer()
        e = await self.tt.get_page_as_embeds(query)
        embeds = [ef.cembed(**i, color=self.client.re[8], author = inter.user) for i in e]
        await assets.pa(inter, embeds)

    @tech.on_autocomplete("query")
    async def auto_tech(self, inter, query):
        comp = await self.tt.search(query)
        await inter.response.send_autocomplete(comp)

    @nextcord.slash_command(name="protondb", description="Check a game for linux compatibility in proton")
    async def protondb(self, inter, game):
        await inter.response.defer()
        reports = await self.proton.report(game)
        embeds = [ef.cembed(**i, color=self.client.re[8], author = inter.user) for i in reports]
        if len(embeds) == 0: embeds = [
            ef.cembed(
                description="Not Found, please try again", 
                color=self.client.re[8]
            )
        ]
        await assets.pa(inter, embeds)

    @protondb.on_autocomplete("game")
    async def auto_proton(self, inter, game):
        autocom = [i[1] for i in self.proton.search_game(game)][:25]
        await inter.response.send_autocomplete(autocom)
        

    # @commands.group()
    # @commands.check(ef.check_command)
    async def spacex(self, ctx):        
        if not ctx.invoked_subcommand:
            await ctx.send(
                embed=ef.cembed(
                    title="Oops",
                    description="We couldnt find that sub-command, it's either history or latest",
                    image="https://thumbs.gfycat.com/CoarseAdventurousIbis-max-1mb.gif",
                    color=self.client.re[8]
                )
            )
            return

    # @spacex.command()
    async def history(self, ctx):
        embeds = await self.space.history()
        await assets.pa(ctx, embeds, start_from=0, restricted=False)

    # @spacex.command()
    async def latest(self, ctx):
        await self.space.setup()
        embed=ef.cembed(
            title=self.space.name,
            description=f"Time: {self.space.time}\nVisit the [official website](https://www.spacex.com/) for more",
            thumbnail=self.space.thumbnail, footer="This feature is still in its beta stage, sorry for inconvenience",color=self.space.color,
            image = "https://static01.nyt.com/images/2021/01/30/business/29musk-print/29musk-1-videoSixteenByNineJumbo1600.jpg"

        )
        embed.add_field(name="Youtube",value=f"[Link]({self.space.youtube})", inline=True)
        embed.add_field(name="Wikipedia", value=f"[Link]({self.space.wikipedia})", inline=True)
        await ctx.send(embed=embed)

    @commands.command()
    async def cute_cat(self, ctx, res="1920x1080"):
        query = "kitten"
        f = await ef.get_async(f"https://source.unsplash.com/{res}?{query}", kind="fp")
        file = nextcord.File(f, "cat.png")
        em = ef.cembed(
            title="Here's a picture of a Cute Cat",
            description="The Image you see here is collected from source.unsplash.com",
            color=self.client.re[8],
            author=ctx.author,
            thumbnail=self.client.user.avatar.url,
            image="attachment://cat.png"
        )
        await ctx.send(file=file, embed=em)

    @nextcord.slash_command(name="dictionary", description="Use the dictionary for meaning")
    async def dic(self, inter, word):
        await inter.response.defer()
        try:
            mean = ef.Meaning(word = word, color = self.client.re[8])
            await mean.setup()
            await assets.pa(inter, mean.create_texts(), start_from=0, restricted=False)
        except Exception as e:
            await inter.send(
                embed=ef.cembed(
                    title="Something is wrong",
                    description="Oops something went wrong, I gotta check this out real quick, sorry for the inconvenience",
                    color=nextcord.Color.red(),
                    thumbnail=self.client.user.avatar.url,
                    footer = str(e)
                )
            )
            print(traceback.format_exc())

    @commands.command(aliases=["cat"])
    @commands.check(ef.check_command)
    async def cat_fact(self, ctx):
        self.client.re[0]+=1
        a = await ef.get_async("https://catfact.ninja/fact", kind="json")
        embed = ef.cembed(
            title="Cat Fact", 
            description=a["fact"], 
            color=self.client.re[8],
            thumbnail="https://i.imgur.com/u1TPbIp.png?1"
        )
        await ctx.send(embed=embed)  

    @nextcord.slash_command(name="api", description="Get info about a public API")
    async def APis(self, inter, name):
        await inter.response.defer()
        await self.APIs.update(inter.user)
        embed = self.APIs.return_embed(
            self.APIs.find(name),
            self.client.re[8]
        )
        await inter.send(embed=embed)

    @APis.on_autocomplete("name")
    async def autocomplete_api(self, inter, name):
        await self.APIs.update(inter.user)
        await inter.response.send_autocomplete(
            self.APIs.search_result(name)[:25]
        )


def setup(client,**i):
    client.add_cog(FunAPI(client,**i))
