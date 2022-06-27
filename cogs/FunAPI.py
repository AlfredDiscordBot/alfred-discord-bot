import nextcord
import assets
import time
import traceback
import helping_hand
import assets
import External_functions as ef
from nextcord.ext import commands, tasks

#Use nextcord.slash_command()

def requirements():
    return []

class FunAPI(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.space = ef.SpaceX(self.client.re[8])

    @commands.group()
    @commands.check(ef.check_command)
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

    @spacex.command()
    async def history(self, ctx):
        embeds = await self.space.history()
        await assets.pa(ctx, embeds, start_from=0, restricted=False)

    @spacex.command()
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


def setup(client,**i):
    client.add_cog(FunAPI(client,**i))
