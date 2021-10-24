import discord
import emoji
from discord.ext import commands

from main_program import reset_board, Emoji_list, re, coin_toss_message, coin_message, set_coin_toss_message


class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["fun"])
    async def games(self, ctx, game="", choice="bot"):
        if game == "XO":
            if choice == "bot":
                if self.bot.user != ctx.author:
                    global available
                    global sent
                    board = reset_board()
                    available = Emoji_list.copy()
                    sent = await ctx.send(
                        embed=discord.Embed(
                            title="Tic Tac Toe by Rahul",
                            description=board,
                            color=discord.Color(value=re[8]),
                        )
                    )
                    for each in Emoji_list:
                        await sent.add_reaction(emoji.emojize(each))
        elif game == "Toss":
            if choice == "bot":
                if self.bot.user != ctx.author:
                    set_coin_toss_message(await ctx.send(
                        embed=discord.Embed(
                            title="Coin Toss by Alvin",
                            description=coin_message,
                            color=discord.Color(value=re[8]),
                        )
                    ))
                    await coin_toss_message.add_reaction(
                        emoji.emojize(":face_with_head-bandage:")
                    )
                    await coin_toss_message.add_reaction(emoji.emojize(":hibiscus:"))
        else:
            await ctx.send(
                embed=discord.Embed(
                    title="Games",
                    description="1. TicTacToe(XO)\n2. Coin Toss(Toss)\n\nEnter the keyword given in the brackets "
                                "after 'games",
                    color=discord.Color(value=re[8]),
                )
            )
def setup(client):
    client.add_cog(Games(client))
