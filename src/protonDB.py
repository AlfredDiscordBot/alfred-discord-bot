import asyncio 
import requests

def requirements():
    return ["re"]


class Proton:
    def __init__(self, ef):
        self.ef = ef
        loop = asyncio.get_event_loop()
        m = requests.get("https://protondb.max-p.me/games").json()
        self.games = []
        for i in m:
            t = list(i.items())
            self.games.append((t[0][1],t[1][1]))

    async def search_game(self, name):
        search_results = []
        name = name.lower()
        for i in self.games:
            if name in i[1].lower():
                search_results.append(i)
        return search_results

    async def report(self, id):
        report = await self.ef.get_async(f'https://protondb.max-p.me/games/{id}/reports',kind="json")        
        reports = []
        for i in report:            
            details  = f"{i['notes'] if i['notes'] else ''}\n\nCompatibility: {i['rating']}\nOperating System: {i['os']}\nGPU Driver: {i['gpuDriver']}\n Proton: {i['protonVersion']}\nSpecs: {i['specs']}\n"    
            reports.append({
                'title': str([j[1] for j in self.games if j[0]==id][0]),
                'description': details,
                'footer': self.ef.timestamp(int(i['timestamp'])),
                'thumbnail': "https://live.mrf.io/statics/i/ps/www.muylinux.com/wp-content/uploads/2019/01/ProtonDB.png?width=1200&enable=upscale",
                'image': "https://pcgw-community.sfo2.digitaloceanspaces.com/monthly_2020_04/chrome_a3Txoxr2j5.jpg.4679e68e37701c9fbd6a0ecaa116b8e5.jpg"
            })
        return reports
        
        
        

def main(client, re):
    import nextcord as discord
    import assets
    import External_functions as ef    
    from discord.ext import commands
    DB = Proton(ef)
    
    @client.command()
    @commands.check(ef.check_command)
    async def protonDB(ctx, *, text):        
        if text.isdigit():
            report = await DB.report(text)
            if report == []:
                await ctx.send(
                    embed=ef.cembed(
                        title = "Oops",
                        description = "You may have got the ID wrong, please recheck the ID by searching a name in this same command like `protonDB game name`",
                        thumbnail = "https://live.mrf.io/statics/i/ps/www.muylinux.com/wp-content/uploads/2019/01/ProtonDB.png?width=1200&enable=upscale",
                        color = re[8]
                    )
                )
                return
            embeds = []
            for i in report:  
                embed = ef.cembed(**i, color = re[8])
                embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
                embeds.append(embed)

            await assets.pa(ctx, embeds)
        else:
            li = await DB.search_game(text)
            st = ""
            for i in li[:10]:
                st += f"{i[0]}. {i[1]}\n"
            await ctx.send(
                embed=ef.cembed(
                    title = "Proton search",
                    description = st,
                    thumbnail = "https://live.mrf.io/statics/i/ps/www.muylinux.com/wp-content/uploads/2019/01/ProtonDB.png?width=1200&enable=upscale",
                    color=re[8]
                )
            )