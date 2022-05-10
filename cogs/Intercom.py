import nextcord
import assets
import asyncio
import time
import helping_hand
import External_functions as ef
from nextcord.ext import commands, tasks
from io import BytesIO
from nextcord import Interaction, SlashOption, ChannelType
from nextcord.abc import GuildChannel


def requirements():
    return []

class Intercom(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.calls = {}

    @nextcord.slash_command(name="intercom", description="Set a channel for intercom, if not given removes the existing channel")
    async def intercom(self, inter, channel:GuildChannel = "-"):
        await inter.response.defer()
        if not inter.user.guild_permissions.manage_guild:
            await inter.send(
                embed=ef.cembed(
                    title="Permissions Denied",
                    description="You need Manage Server Permissions to use this command",
                    color=self.client.re[8]
                )
            )
            return
        if channel == "-":
            if inter.guild.id in self.client.config['connect']:
                del self.client.config['connect'][inter.guild.id]
            await inter.send("Removing existing intercom connection channel")
            return

        
        self.client.config['connect'][inter.guild.id] = channel.id
        await inter.send(
            embed=ef.cembed(
                description=f"Set {channel.mention} for intercom",
                color=self.client.re[8],
                footer="When you enable this command, you're allowing your server to be seen"
            )
        )

        
    @commands.command(aliases=['end','endcall'])
    @commands.check(ef.check_command)
    async def end_call(self, ctx):
        if not ctx.author.guild_permissions.manage_guild:
            await ctx.send("Permissions Denied")
            return
        if ctx.guild.id in self.calls:
            self.calls.pop(self.calls.pop(ctx.guild.id))
            await ctx.send("Ended call")
            return
        await ctx.send("No call in progress")

    @commands.command(aliases=['call'])
    @commands.check(ef.check_command)
    async def start_call(self, ctx, number = None):
        if not number:
            st = ""
            for i in list(self.client.config['connect']).copy():
                g = self.client.get_guild(i)
                if not g:
                    del self.client.config['connect'][i]
                else:
                    st+=f"`{i}` -> {g.name}\n"

            await ctx.send(
                embed=ef.cembed(
                    title="PhoneBook",
                    description=st,
                    picture="https://static1.srcdn.com/wordpress/wp-content/uploads/2021/04/Batman-Batphone-Gordon-Joker.jpg",
                    color=self.client.re[8]
                )
            )
            return

        if not ctx.author.guild_permissions.manage_guild:
            await ctx.send("Permissions Denied")
            return
            
        number = int(number)
        guild = self.client.get_guild(number)
        
        if not guild:
            await ctx.reply("Not a server ID, try again")
            return

        if number in self.calls:
            await ctx.reply("Busy at the moment, call again later")
            return

        if ctx.guild.id in self.calls:
            await ctx.reply("You're already in a call")
            return

        if number not in self.client.config['connect']:
            await ctx.reply("This Server has not set Intercom yet")
            return        

        if ctx.guild.id not in self.client.config['connect']:
            await ctx.reply("Your Server has not set Intercom yet\nUse `/intercom`")
            return

        ch = self.client.get_channel(self.client.config['connect'][number])
        ay = await ch.send(
            embed=ef.cembed(
                title="Intercom",
                description=f"Call from {ctx.guild.name}\nType `accept` or `decline`",
                color=self.client.re[8]
            )
        )
        await ctx.send("Call sent")
        while True:
            try:
                def check(m):
                    return m.content.lower() in ["accept","decline"] and m.author.guild_permissions.manage_guild
                message = await self.client.wait_for("message", check=check, timeout=720)
                if message.content.lower() == "accept":
                    break
                else:
                    await ctx.send("They declined the call")
                    return
            except asyncio.TimeoutError:
                await ctx.send("Timed out, no one answered")
                await ay.reply("Ending call")
                return
                

        self.calls[ctx.guild.id] = number
        self.calls[number] = ctx.guild.id

        await ctx.reply(
            embed=ef.cembed(
                title="Done",
                description=f'Connected to {guild.name}',
                color=self.client.re[8],
                footer="'end to end the call"
            )
        )
        
        

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.guild.id in self.calls:
            b = msg.guild.id
            a = self.calls[b]
            if msg.author.bot: return            
            if msg.guild.id == a:
                if not msg.channel.id == self.client.config['connect'][a]: return
                c = self.client.get_channel(self.client.config['connect'][b])
                embed = ef.cembed(
                    description = msg.content,
                    color=self.client.re[8],                    
                )
                embed.set_author(name = msg.author.name, icon_url = ef.safe_pfp(msg.author))
                await c.send(embed=embed)

            if msg.guild.id == b:
                if not msg.channel.id == self.client.config['connect'][b]: return
                c = self.client.get_channel(self.client.config['connect'][a])
                embed = ef.cembed(
                    description = msg.content,
                    color=self.client.re[8],   
                    footer=msg.guild.name + f'> {msg.guild.id}'
                )
                embed.set_author(name = msg.author.name, icon_url = ef.safe_pfp(msg.author))
                await c.send(embed=embed)
                await msg.add_reaction("✅")
            
            
            

def setup(client, **i):
    client.add_cog(Intercom(client, **i))