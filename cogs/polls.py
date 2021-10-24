from discord.ext import commands
from discord_slash import SlashContext, cog_ext, ButtonStyle
import discord
import random

from External_functions import cembed, equalise
from main_program import req, re


class Polls(commands.cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="polling", description="Seperate options with |")
    async def polling_slash(self, ctx, question, channel: discord.TextChannel, options):
        await ctx.defer()
        await self.poll(ctx, options, channel, question=question)

    @commands.command()
    async def poll(self, ctx, options, channel_to_send: discord.TextChannel = None, *, question):
        count = {}
        req()
        author_list = {}
        names = {}
        channel = channel_to_send
        print(type(channel_to_send))
        if type(channel_to_send) == str:
            channel = ctx.channel
            question = channel_to_send + question
        if ctx.guild.id == 858955930431258624:
            channel = ctx.channel

        options = options.replace("_", " ").split("|")
        components = []
        for i in options:
            components.append(
                Button(style=random.choice([ButtonStyle.green, ButtonStyle.blue]), label=i)
            )
            count[i] = 0
        await ctx.send("Done")
        mess = await channel.send(
            embed=cembed(
                title=f"Poll from {ctx.author.name}",
                description=f"```yaml\n{question}```",
                color=re[8],
                thumbnail=self.bot.user.avatar_url_as(format="png"),
            ),
            components=[components],
        )

        def check(res):
            return mess.id == res.message.id

        while True:
            res = await self.bot.wait_for("button_click", check=check)
            if res.component.label in count and res.author.id not in author_list:
                author_list[res.author.id] = res.component.label
                count[res.component.label] += 1
            else:
                count[author_list[res.author.id]] -= 1
                count[res.component.label] += 1
                author_list[res.author.id] = res.component.label
            description = question + "\n\n"
            avg = sum(list(count.values())) // len(options)
            avg = 1 if avg == 0 else avg
            copy_count = equalise(list(count.keys()))
            for i in list(count.keys()):
                description += f"{copy_count[i]} |" + chr(9606) * (count[i] // avg) + "\n"
            _ = [
                names.update({i: self.bot.get_user(i).name})
                for i in author_list
                if i not in names
            ]
            people = "\n" + "\n".join([names[i] for i in author_list])
            st = "\n"
            for i in list(count.keys()):
                st += f"{copy_count[i]}:  {(count[i] * 100) // len(author_list)}%\n"
            people = st + "\n" + people
            await res.edit_origin(
                embed=cembed(
                    title=f"Poll from {ctx.author.name}",
                    description=f"```yaml\n{description}```" + "\n" + people,
                    color=re[8],
                    thumbnail=self.bot.user.avatar_url_as(format="png"),
                )
            )
