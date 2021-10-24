import discord
from discord.ext import commands

from External_functions import cembed
from main_program import req, re


class Fun(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    @commands.command()
    async def yey(self, ctx):
        req()
        print("yey")
        em = discord.Embed(title="*yey*", color=discord.Color(value=re[8]))
        await ctx.send(embed=em)

    @commands.command()
    async def lol(self, ctx):
        req()
        em = discord.Embed(title="***L😂L***", color=discord.Color(value=re[8]))
        await ctx.send(embed=em)

    @commands.command()
    async def thog(self, ctx, *, text):
        if ctx.author.guild_permissions.administrator:
            if re[1] == text:
                re[4] = re[4] * -1
                if re[4] == 1:
                    await ctx.send(
                        embed=discord.Embed(
                            title="Thog",
                            description="Activated",
                            color=discord.Color(value=re[8]),
                        )
                    )
                else:
                    await ctx.send(
                        embed=discord.Embed(
                            title="Thog",
                            description="Deactivated",
                            color=discord.Color(value=re[8]),
                        )
                    )
            else:
                await ctx.message.delete()
                await ctx.send("Wrong password")
        else:
            await ctx.send(
                embed=cembed(
                    title="Permissions Denied",
                    description="You cannot toggle thog",
                    color=re[8],
                )
            )

def setup(bot):
    client.add_cog(Fun(bot))
