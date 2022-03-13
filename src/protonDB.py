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
        for i in report[:3]:            
            details  = f"{i['notes'] if i['notes'] else ''}\n\nCompatibility: {i['rating']}\nOperating System: {i['os']}\nGPU Driver: {i['gpuDriver']}\n Proton: {i['protonVersion']}\nSpecs: {i['specs']}\n"            
            reports.append({
                'title': str(id),
                'description': details,
                'footer': self.ef.timestamp(int(i['timestamp'])),
                'thumbnail': "https://live.mrf.io/statics/i/ps/www.muylinux.com/wp-content/uploads/2019/01/ProtonDB.png?width=1200&enable=upscale",
                'image': "https://pcgw-community.sfo2.digitaloceanspaces.com/monthly_2020_04/chrome_a3Txoxr2j5.jpg.4679e68e37701c9fbd6a0ecaa116b8e5.jpg"
            })
        return reports
        
        
        

def main(client, re):
    import nextcord as discord
    import External_functions as ef    
    DB = Proton(ef)
    
    @client.command()
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

            await pa1(embeds, ctx)
        else:
            li = await DB.search_game(text)
            length = len(li)
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
            
    async def pa1(embeds, ctx, start_from=0, restricted = False):
        message = await ctx.send(embed=embeds[start_from])
        pag = start_from
        await message.add_reaction("◀️")
        await message.add_reaction("▶️")
        
    
        def check(reaction, user):
            if not restricted:            
                return (
                    user.id != client.user.id
                    and str(reaction.emoji) in ["◀️", "▶️"]
                    and reaction.message.id == message.id
                )
            else:
                a = (
                    user.id != client.user.id
                    and str(reaction.emoji) in ["◀️", "▶️"]
                    and reaction.message.id == message.id
                    and user.id == getattr(ctx, 'author', getattr(ctx,'user',None)).id
                )
                return a
    
        while True:
            try:
                reaction, user = await client.wait_for(
                    "reaction_add", timeout=720, check=check
                )            
                if str(reaction.emoji) == "▶️" and pag + 1 != len(embeds):
                    pag += 1
                    await message.edit(embed=embeds[pag])
                elif str(reaction.emoji) == "◀️" and pag != 0:
                    pag -= 1
                    await message.edit(embed=embeds[pag])
                try:
                    await message.remove_reaction(reaction, user)
                except:
                    pass
            except asyncio.TimeoutError:
                await message.remove_reaction("◀️", client.user)
                await message.remove_reaction("▶️", client.user)
                break
