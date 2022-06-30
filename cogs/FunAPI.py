import nextcord
import assets
import time
import traceback
import helping_hand
import asyncio
import assets
import requests
import External_functions as ef
from nextcord.ext import commands, tasks

#Use nextcord.slash_command()

def requirements():
    return []

class Proton:
    def __init__(self):
        loop = asyncio.get_event_loop()
        m = requests.get("https://protondb.max-p.me/games").json()
        self.games = []
        for i in m:
            t = list(i.items())
            self.games.append((t[0][1],t[1][1]))

    def search_game(self, name):
        search_results = []
        name = name.lower()
        for i in self.games:
            if name in i[1].lower():
                search_results.append(i)
        return search_results

    async def report(self, name):
        print(self.search_game(name))
        id = self.search_game(name)[0][0]
        
        report = await ef.get_async(f'https://protondb.max-p.me/games/{id}/reports', kind ="json")        
        reports = []
        for i in report:            
            details  = f"```\n{i['notes'] if i['notes'] else '-'}\n```\n\n```yml\nCompatibility: {i['rating']}\nOperating System: {i['os']}\nGPU Driver: {i['gpuDriver']}\n Proton: {i['protonVersion']}\nSpecs: {i['specs']}\n```"    
            
            reports.append({
                'title': str([j[1] for j in self.games if j[0]==id][0]),
                'description': details,
                'footer': ef.timestamp(int(i['timestamp'])),
                'thumbnail': "https://live.mrf.io/statics/i/ps/www.muylinux.com/wp-content/uploads/2019/01/ProtonDB.png?width=1200&enable=upscale",
                'image': "https://pcgw-community.sfo2.digitaloceanspaces.com/monthly_2020_04/chrome_a3Txoxr2j5.jpg.4679e68e37701c9fbd6a0ecaa116b8e5.jpg"
            })
        return reports

class FunAPI(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.space = ef.SpaceX(self.client.re[8])
        self.proton = Proton()

    @nextcord.slash_command(name="protondb", description="Check a game for linux compatibility in proton")
    async def protondb(self, inter, game):
        await inter.response.defer()
        reports = await self.proton.report(game)
        embeds = [ef.cembed(**i, color=self.client.re[8]) for i in reports]
        if len(embeds) == 0: embeds = [
            ef.cembed(
                description="Not Found, please try again", 
                color=self.client.re[8]
            )
        ]
        await assets.pa(inter, embeds)

    @protondb.on_autocomplete("game")
    async def auto(self, inter, game):
        autocom = [i[1] for i in self.proton.search_game(game)][:25]
        await inter.response.send_autocomplete(autocom)
        

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
