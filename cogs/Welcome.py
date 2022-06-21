
import nextcord
import assets
import time
import traceback
import helping_hand
import assets
import random
import time
import External_functions as ef
import helping_hand
from nextcord.ext import commands, tasks

#Use nextcord.slash_command()

def requirements():
    return []

class Card:
    def __init__(
        self,
        guild,
        background=None
    ):
        self.BASE_URL = "https://api.popcat.xyz/welcomecard?"
        self.background = background if background else ef.safe_pfp(guild)
        self.query = self.BASE_URL+"background="+ef.convert_to_url(self.background)

    def set_text1(self, text):
        if text:
            self.query+"&text1="+ef.convert_to_url(text)
        return self.query
    def set_text2(self, text):
        if text:
            self.query+"&text2="+ef.convert_to_url(text)
        return self.query
    def set_text3(self, text):
        if text:
            self.query+"&text3="+ef.convert_to_url(text)
        return self.query
    def set_avatar(self, avatar):
        if avatar:
            self.query+"&avatar="+avatar
        return self.query

class Welcome(commands.Cog):
    def __init__(self, client):
        self.client = client

    def cleanup_data(self):
        if not client.is_ready(): return
        for i in self.client.config['welcome']:
            if not self.client.get_guild(i):
                self.client.config['welcome'].remove(i)
                break

    def preset(self, member, text):
        presets = {
            '<mention>': member.mention,
            '<name>': member.name[:10],
            '<server>': member.guild.name
        }
        for i in presets:
            text.replace(i, presets[i])
        return text

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if not self.client.is_ready(): return
        if member.guild.id not in self.client.config['welcome']:
            return
        c = self.client.config['welcome'][member.guild.id]
        image = Card(member.guild, background=c.get('background'))
        image.set_text1(self.preset(c.get('text1')))
        image.set_text2(self.preset(c.get('text2')))
        image.set_text3(self.preset(c.get('text3')))
        image.set_avatar(ef.safe_pfp(member))
        self.cleanup_data()
        embed = ef.cembed(
            title=self.preset(member, c.get("title","Welcome to <server>")),
            description=self.preset(member, c.get("description", "Hello <name>, welcome to <server>")),
            color=self.client.re[8],
            thumbnail=ef.safe_pfp(member.guild),
            image=image.query
        )
        await self.client.get_channel(c['channel']).send(
            content=f"{member.mention} is here",
            embed=embed
        )

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if not self.client.is_ready(): return
        if member.guild.id not in self.client.config['welcome']:
            return
        c = self.client.config['welcome'][member.guild.id]
        await self.client.get_channel(c.get('channel')).send(
            content=f"{member.name} left the server",
            embed=ef.cembed(
                title="GoodBye",
                description=f"{member.name} left {member.guild.name} at <t:{int(time.time())}\nHope you enjoyed your stay {member.name}",
                color=self.client.re[8],
                thumbnail=ef.safe_pfp(member)
            )
        )

        

    
        


def setup(client,**i):
    client.add_cog(Welcome(client,**i))
