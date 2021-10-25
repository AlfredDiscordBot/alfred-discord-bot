import asyncio
from random import choice

import discord
import requests
from discord.ext import commands
from discord_slash import cog_ext

from External_functions import cembed, reddit, memes3, memes2, memes1
from stuff import req, re, client, save_to_file


class Memes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.link_for_cats = ""

    async def pa1(self, embeds, ctx):
        message = await ctx.send(embed=embeds[0])
        pag = 0
        await message.add_reaction("◀️")
        await message.add_reaction("▶️")

        def check(reaction, user):
            return (
                    user != self.bot.user
                    and str(reaction.emoji) in ["◀️", "▶️"]
                    and reaction.message.id == message.id
            )

        while True:
            try:
                reaction, user = await self.bot.wait_for(
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

    @cog_ext.cog_slash(
        name="reddit",
        description="Gives you a random reddit post from the account you specify",
    )
    async def reddit_slash(self, ctx, account="wholesomememes"):
        req()
        try:
            await ctx.defer()
            await self.reddit_search(ctx, account)
        except Exception as e:
            print(e)
            await ctx.send(
                embed=cembed(title="Oops", description="Something went wrong", color=re[8])
            )

    @commands.command(aliases=["reddit"])
    async def reddit_search(self, ctx, account="wholesomememes", number=1):
        req()
        if number == 1:
            embeds = []
            a = reddit(account, single=False)
            if a[2]:
                for i in a:
                    embeds += [
                        cembed(
                            description="**" + i[0] + "**",
                            picture=i[1],
                            color=re[8],
                            thumbnail=self.bot.user.avatar_url_as(format="png"),
                        )
                    ]
                await self.pa1(embeds, ctx)
            else:
                await ctx.send(embed=cembed(title=a[0], color=re[8], description=a[1]))

    @commands.command(aliases=["c"])
    async def cover_up(self, ctx):
        await ctx.message.delete()
        await asyncio.sleep(0.5)
        mess = await ctx.send(discord.utils.get(self.bot.emojis, name="enrique"))
        await mess.delete()

    @cog_ext.cog_slash(name="memes", description="Memes from Alfred yey")
    async def memes(self, ctx):
        req()
        await ctx.defer()
        await self.memes(ctx)

    @commands.command(aliases=["::"])
    async def memes(self, ctx):
        if len(self.link_for_cats) == 0:
            try:
                safe_stop = 0
                r = requests.get("https://bestlifeonline.com/funniest-cat-memes-ever/")
                string = str(r.content.decode())
                for i in range(0, 94):
                    # https://bestlifeonline.com/funniest-cat-memes-ever/
                    n1 = string.find("<h2", safe_stop + len("<h2"))
                    n3 = string.find('<div class="number">', n1) + len(
                        '<div class="number">'
                    )
                    n4 = string.find("</div>", n3)
                    n2 = string.find("data-src=", n1) + len("data-src=") + 1
                    n1 = string.find('" ', n2)
                    safe_stop = n1
                    number = int(string[n3:n4])
                    if number >= 97:
                        safe_stop = 0
                    self.link_for_cats += [string[n2:n1]]
                print("Finished meme")
                self.link_for_cats += memes1()
                print("Finished meme1")
                self.link_for_cats += memes2()
                print("Finished meme2")
                self.link_for_cats += memes3()
                print("Finished meme3")
            except Exception as e:
                await ctx.send(
                    embed=cembed(
                        title="Meme issues",
                        description="Something went wrong during importing memes\n"
                                    + str(e),
                        color=re[8],
                        thumbnail=self.bot.user.avatar_url_as(format="png"),
                    )
                )
        await ctx.send(choice(self.link_for_cats))
        save_to_file()


def setup(bot):
    bot.add_cog(Memes(bot))
