import nextcord
import os
import helping_hand
import External_functions as ef
from nextcord.ext import commands
from io import BytesIO
from wordcloud import WordCloud
from collections import Counter

# Use nextcord.slash_command()


def requirements():
    return []


class Image(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.re = self.client.re

    @nextcord.slash_command(name="pfp", description="Get a person's avatar")
    async def pfp_pic(self, inter, member: nextcord.User = "-"):
        if member == "-":
            member = inter.user
        await self.get_pfp(inter, member)

    @commands.command(aliases=["pfp"])
    @commands.check(ef.check_command)
    async def get_pfp(self, ctx, member: nextcord.Member = None):
        self.client.re[0] += 1
        user = getattr(ctx, "author", getattr(ctx, "user", None))
        if not member:
            member = user
        picture = member.guild_avatar or ef.safe_pfp(member)
        embed = ef.cembed(
            title=f"Profile Picture -> {member.name}",
            footer=f"Amazing picture | Requested by {user.name}",
            picture=picture,
            color=member.color,
        )
        await ctx.send(embed=embed)

    @nextcord.slash_command(
        name="blend", description="Blend your pfp with another picture"
    )
    async def blend(
        self, inter, url_of_picture: str, member: nextcord.Member = None, ratio=0.5
    ):
        await inter.response.defer()
        if not member:
            url = ef.safe_pfp(inter.user)
        else:
            url = ef.safe_pfp(member)
        json = {"url": url, "url2": url_of_picture, "ratio": ratio}
        byte = await ef.post_async(
            "https://suicide-detector-api-1.yashvardhan13.repl.co/style_predict",
            json=json,
        )
        await inter.send(file=nextcord.File(BytesIO(byte), "blend.png"))

    @nextcord.slash_command(
        name="effects", description="effects with your profile picture"
    )
    async def eff(
        self, inter, effect=helping_hand.effects_helper(), member: nextcord.Member = "-"
    ):
        await inter.response.defer()
        if member == "-":
            member = inter.user
        await self.effects(inter, effect=effect, member=member)

    @commands.command(aliases=["ef", "effect"])
    @commands.check(ef.check_command)
    async def effects(self, ctx, effect: str = None, member: nextcord.Member = None):
        self.client.re[0] += 1
        if not member:
            url = ef.safe_pfp(getattr(ctx, "author", getattr(ctx, "user", None)))
        else:
            print(member)
            url = ef.safe_pfp(member)
        url = str(url)

        if not effect:
            await ctx.send(
                embed=ef.cembed(
                    title="OOPS",
                    description="""Hmm You seem to be forgetting an argument \n `effects <effect> <member>` if member is none the users pfp will be modified \n The list of effects is \n- cartoonify \n- watercolor \n- canny \n- pencil \n- econify \n- negative \n- pen \n- candy \n- composition \n- feathers \n- muse \n- mosaic \n- night \n- scream \n- wave \n- udnie """,
                    color=self.client.re[8],
                )
            )
            return

        styles = [
            "candy",
            "composition",
            "feathers",
            "muse",
            "mosaic",
            "night",
            "scream",
            "wave",
            "udnie",
        ]

        effects = [
            "cartoonify",
            "watercolor",
            "canny",
            "pencil",
            "econify",
            "negative",
            "pen",
        ]

        if effect not in styles and effect not in effects and effect is not None:
            await ctx.send(
                embed=ef.cembed(
                    title="OOPS",
                    description="""hmm no such effect. The effects are given below. \n `effects <effect> <member> if member is none the users pfp will be modified \n The list of effects is \n- cartoonify \n- watercolor \n- canny \n- pencil \n- econify \n- negative \n- pen \n- candy \n- composition \n- feathers \n- muse \n- mosaic \n- night \n- scream \n- wave \n- udnie """,
                    color=self.client.re[8],
                )
            )
            return
        elif effect in styles:
            json = {"url": url, "effect": effect}
            byte = await ef.post_async(
                "https://suicide-detector-api-1.yashvardhan13.repl.co/style",
                json=json,
                output="content",
            )

        elif effect in effects:
            json = {"url": url, "effect": effect}
            byte = await ef.post_async(
                "https://suicide-detector-api-1.yashvardhan13.repl.co/cv", json=json
            )

        await ctx.send(file=nextcord.File(BytesIO(byte), "effect.png"))

    @nextcord.slash_command(name="wordcloud", description="Creates a wordcloud picture")
    async def word(self, inter, user: nextcord.Member = None):
        await inter.response.defer()
        if not user:
            user = inter.user
        a = await inter.channel.history(limit=3000).flatten()
        messages = [i.clean_content for i in a if i.author.id == user.id]
        text = " ".join(messages)
        WordCloud(height=1080, width=1920).generate(text).to_file("test.png")
        description = "**Most common words**```\n"
        count = Counter(text.lower().split())
        equalised = ef.equalise([i[:14] for i in count])
        for i in sorted(count.items(), key=lambda h: h[1], reverse=True)[:10]:
            description += f"\n{equalised[i[0][:14]]} -> {i[1]}"
        embed = ef.cembed(
            title="Word Cloud",
            image="attachment://test.png",
            color=self.client.re[8],
            footer=f"{len(messages)} Messages | {len(text)} Words",
            description=f"{description}\n```",
            thumbnail=ef.safe_pfp(inter.guild),
        )
        embed.set_author(name=user.name, icon_url=ef.safe_pfp(user))
        await inter.send(file=nextcord.File("test.png"), embed=embed)
        os.remove("test.png")


def setup(client, **i):
    client.add_cog(Image(client, **i))
