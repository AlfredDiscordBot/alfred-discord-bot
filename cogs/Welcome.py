import nextcord
import time
import utils.External_functions as ef
from nextcord.ext import commands


# Use nextcord.slash_command()


def requirements():
    return []


class Card:
    def __init__(self, background=None):
        DEFAULT_BACKGROUND = "https://static.vecteezy.com/system/resources/previews/001/557/683/original/abstract-overlapping-blue-background-free-vector.jpg"
        self.BASE_URL = "https://api.popcat.xyz/welcomecard?"
        self.background = background if background else DEFAULT_BACKGROUND
        self.query = self.BASE_URL + "background=" + (background or DEFAULT_BACKGROUND)

    def set_text1(self, text):
        if text:
            self.query += "&text1=" + text
        return self.query

    def set_text2(self, text):
        if text:
            self.query += "&text2=" + text
        return self.query

    def set_text3(self, text):
        if text:
            self.query += "&text3=" + text
        return self.query

    def set_avatar(self, avatar):
        if avatar:
            self.query += "&avatar=" + avatar
        return self.query


class Welcome(
    commands.Cog,
    description="Sends a Welcome message to the specified channel\nUse `/config welcome` to setup",
):
    def __init__(self, client):
        self.client = client

    def cleanup_data(self):
        if not self.client.is_ready():
            return
        for i in self.client.config["welcome"]:
            if not self.client.get_guild(i):
                self.client.config["welcome"].remove(i)
                break

    def preset(self, member, text):
        presets = {
            "<mention>": member.mention,
            "<name>": member.name[:20],
            "<server>": member.guild.name,
            "<count>": f"{len(member.guild.humans)}",
        }
        for i in presets:
            text = text.replace(i, presets[i])
        return text

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if not self.client.is_ready():
            return
        if member.guild.id not in self.client.config["welcome"]:
            return
        c = self.client.config["welcome"][member.guild.id]
        image = Card(background=c.get("background"))
        image.set_text1(self.preset(member, c.get("text1") or "<name>"))
        image.set_text2(self.preset(member, c.get("text2") or "Welcome To <server>"))
        image.set_text3(self.preset(member, c.get("text3") or "<count> members"))
        image.set_avatar(ef.safe_pfp(member))
        pic = await ef.get_async(image.query, kind="fp")
        file = nextcord.File(pic, "welcome.png")
        self.cleanup_data()
        embed = ef.cembed(
            title=self.preset(member, c.get("title") or "Welcome to <server>"),
            description=self.preset(
                member, c.get("description") or "Hello <name>, welcome to <server>"
            ),
            color=self.client.color(member.guild),
            thumbnail=ef.safe_pfp(member.guild),
            image="attachment://welcome.png",
        )
        await self.client.get_channel(c["channel"]).send(
            content=f"{member.mention} is here", embed=embed, file=file
        )

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if not self.client.is_ready():
            return
        if member.guild.id not in self.client.config["welcome"]:
            return
        c = self.client.config["welcome"][member.guild.id]
        await self.client.get_channel(c.get("channel")).send(
            content=f"{member.name} left the server",
            embed=ef.cembed(
                title="GoodBye",
                description=f"{member.name} left {member.guild.name} <t:{int(time.time())}:R>\nHope you enjoyed your stay {member.name}",
                color=self.client.color(member.guild),
                thumbnail=ef.safe_pfp(member),
            ),
        )

    @commands.command()
    async def test_welcome(self, ctx):
        if ctx.guild.id not in self.client.config["welcome"]:
            await ctx.send("You have not set welcome channel")
            return
        await self.on_member_join(ctx.author)
        await ctx.send("Done")


def setup(client, **i):
    client.add_cog(Welcome(client, **i))
