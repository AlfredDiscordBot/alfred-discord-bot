import nextcord
import assets
import time
import helping_hand
import asyncio
import External_functions as ef
from nextcord.ext import commands, tasks



def requirements():
    require = ['re', 'config']
    return ef.create_requirements(require)

class Ticket(commands.Cog):
    def __init__(self, client, re, config):
        self.client = client
        self.re = re
        self.ticket = client.config['ticket']

    @commands.Cog.listener()
    async def on_raw_reaction_add(self,payload):
        #0->channel id
        #1->message id
        if payload.member.bot: return    
        if payload.emoji.name == chr(127915):
            print("Check 1")
            if payload.guild_id not in self.ticket: return
            if not self.client.get_channel(self.ticket[payload.guild_id][0]):
                del self.ticket[payload.guild_id]
                return
            if payload.channel_id != self.ticket[payload.guild_id][0]: return
            msg = payload.message_id
            channel = self.client.get_channel(self.ticket[payload.guild_id][0])
            print(payload.emoji.name)
            ms = await channel.fetch_message(msg)
            if msg != self.ticket[payload.guild_id][1]: return
            await ms.remove_reaction(payload.emoji, payload.member)
            mess = await channel.send(
                embed=ef.cembed(description=f"Creating Ticket for {payload.member.name}", color=self.client.re[8])
            )
            
            th = await channel.create_thread(name = f"Ticket - {payload.member.name} {payload.member.id}", reason = f"Ticket - {payload.member.name}", auto_archive_duration = 60, message = mess)
            await mess.delete()
            await th.send(self.client.get_user(payload.user_id).mention)

    @commands.command()
    async def close_ticket(self, ctx):    
        if type(ctx.channel) != nextcord.Thread: return
        if ctx.channel.owner == self.client.user:
            confirm = await ef.wait_for_confirm(ctx,self.client,"Do you want to close this ticket?", self.client.re[8])
            if not confirm: return
            if not ctx.author.id == int(ctx.channel.name.split()[-1]):
                if not ctx.author.guild_permissions.administrator:
                    await ctx.send(
                        embed=ef.cembed(
                            title="Permission Denied",
                            description="You need to be the one who created the ticket or you need to be an admin to close this ticket",
                            color=nextcord.Color.red(),
                            thumbnail=self.client.user.avatar.url
                        )
                    )
                    return
            
            await ctx.send(
                embed=ef.cembed(
                    description="Deleting the ticket in 5 seconds",
                    color=self.client.re[8]
                )
            )
            await asyncio.sleep(5)
            await ctx.channel.delete()

def setup(client,**i):
    client.add_cog(Ticket(client,**i))