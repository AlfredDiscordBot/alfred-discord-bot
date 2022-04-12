import nextcord
import assets
import time
import helping_hand
import External_functions as ef
import emoji
import asyncio
from nextcord.ext import commands, tasks
from random import choice

#Use nextcord.slash_command()

def requirements():
    require = ['re']
    return ef.create_requirements(require)

class Games(commands.Cog):
    def __init__(self, client, re):
        self.client = client
        self.re = re
        self.choices = [
            emoji.emojize(":rock:"),
            emoji.emojize(":roll_of_paper:"),
            emoji.emojize(":scissors:")
        ]
        self.exit = emoji.emojize(":cross_mark_button:")
        self.victor = {
            self.choices[0]: self.choices[2],
            self.choices[1]: self.choices[0],
            self.choices[2]: self.choices[1]
        }

    @nextcord.slash_command(name="rps", description="play some rock paper scissors against me")
    async def rp(self, inter):
        await inter.response.defer()
        await self.rocpaperscissor(inter)

        
    @commands.command(aliases = ['rps','stonepaperscissor'])
    async def rockpaperscissor(self, ctx):
        s = {}
        embed = ef.cembed(
            title="Rock Paper Scissor",
            description="Hi, You will be playing rock paper scissor against me, please try not to delay it as discord hates me for waiting",
            color=self.re[8],
            thumbnail=self.client.user.avatar.url,
            footer="You can press X when you wanna stop or else it'll timeout after 10 minutes"
        )
        user = getattr(ctx,'user', ctx.author)
        s[user] = 0
        s[self.client.user] = 0
        embed.set_author(name=user.name, icon_url=ef.safe_pfp(user))
        embed.add_field(name="You",value=s[user],inline=True)
        embed.add_field(name="Alfred",value=s[self.client.user],inline=True)
        message = await ctx.send(embed=embed)
        for i in self.choices: await message.add_reaction(i)
        await message.add_reaction(self.exit)
        def check(reaction,r_user):
            return r_user == user and reaction.emoji in self.choices+[self.exit]
        while True:
            try:
                r,u = await self.client.wait_for("reaction_add", timeout=600, check = check)
                await r.remove(u)
                r = r.emoji                
                alfred = choice(self.choices)
                if r == self.exit:
                    embed=ef.cembed(
                        title="Bye",
                        description="Ig I'll see you later",
                        color=nextcord.Color.red(),
                        thumbnail=self.client.user.avatar.url
                    )
                    embed.add_field(name="You",value=s[user],inline=True)
                    embed.add_field(name="Alfred",value=s[self.client.user],inline=True)
                    await message.edit(embed=embed)
                    return
                if r in self.choices:
                    if r == alfred:
                        await message.edit(
                            embed=ef.cembed(
                                title="Draw",
                                description=f"You both put {r}",
                                color=self.re[8],
                                thumbnail=self.client.user.avatar.url,
                                footer="Try again"
                            )
                        )
                    elif r in self.victor and self.victor[r] == alfred:
                        embed=ef.cembed(
                            title="You won",
                            description=f"You put {r}, I put {alfred}",
                            color=self.re[8],
                            thumbnail=ef.safe_pfp(user)
                        )
                        s[user]+=1
                        embed.add_field(name="You",value=s[user],inline=True)
                        embed.add_field(name="Alfred",value=s[self.client.user],inline=True)
                        await message.edit(embed=embed)
                    else:
                        embed=ef.cembed(
                            title="You lost",
                            description=f"You put {r}, I put {alfred}",
                            color=self.re[8],
                            thumbnail=ef.safe_pfp(user)
                        )
                        s[self.client.user]+=1
                        embed.add_field(name="You",value=s[user],inline=True)
                        embed.add_field(name="Alfred",value=s[self.client.user],inline=True)
                        await message.edit(embed=embed)
            except asyncio.TimeoutError:
                await message.clear_reactions()
                await message.edit(
                    embed=cembed(
                        title="Timeout",
                        description="Sorry gtg, the reactions timed out",
                        color=nextcord.Color.red()
                    )
                )
                
            
        
        
def setup(client,**i):
    client.add_cog(Games(client,**i))