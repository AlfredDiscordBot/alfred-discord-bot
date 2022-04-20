import nextcord
import assets
import time
import helping_hand
import traceback
import External_functions as ef
from nextcord.ext import commands, tasks
from nextcord import Interaction, SlashOption, ChannelType
from nextcord.abc import GuildChannel

#Use nextcord.slash_command()

def requirements():
    return []

class Configuration(commands.Cog):    
    def __init__(self, client):
        self.client = client
        self.re = self.client.re
        self.config = self.client.config
        self.command_list = open("commands.txt","r").read().split("\n")[:-1]

    @commands.command()
    @commands.check(ef.check_command)
    async def sniper(self, ctx):
        user = getattr(ctx, 'author', getattr(ctx, 'user', None))
        if user.guild_permissions.administrator:
            output=""
            if ctx.guild.id in self.client.config['snipe']:
                self.client.config['snipe'].remove(ctx.guild.id)
                output="All people can use the snipe command"
                
            else:
                self.client.config['snipe'].append(ctx.guild.id)
                output="Only admins can use snipe command"
    
            await ctx.send(embed=ef.cembed(
                title="Done",
                description=output,
                color=self.client.re[8],
                thumbnail=self.client.user.avatar.url)
            )
        else:
            await ctx.send(
                embed=ef.cembed(
                    title="Permission Denied",
                    description="Only an admin can toggle this setting",
                    color=nextcord.Color.red(),
                    thumbnail=self.client.user.avatar.url
                )
            )
            
    @commands.command()
    @commands.check(ef.check_command)
    async def set_prefix(self, ctx, *, pref):
        if getattr(ctx, 'author', getattr(ctx, 'user', None)).guild_permissions.administrator:
            if pref.startswith('"') and pref.endswith('"') and len(pref)>1:
                pref=pref[1:-1]
            self.client.prefix_dict[ctx.guild.id] = pref
            await ctx.send(
                embed=ef.cembed(title="Done", description=f"Prefix set as {pref}", color=self.client.re[8])
            )
        else:
            await ctx.send(
                embed=ef.cembed(
                    title="Permissions Denied",
                    description="You cannot change the prefix, you need to be an admin",
                    color=self.client.re[8],
                )
            )
    
    @commands.command()
    @commands.check(ef.check_command)
    async def remove_prefix(self, ctx):
        if getattr(ctx, 'author', getattr(ctx, 'user', None)).guild_permissions.administrator:
            if self.client.prefix_dict.get(ctx.guild.id):
                self.client.prefix_dict.pop(ctx.guild.id)
            await ctx.send(
                embed=ef.cembed(title="Done", description=f"Prefix removed", color=self.client.re[8])
            )
        else:
            await ctx.send(
                embed=ef.cembed(
                    title="Permissions Denied",
                    description="You cannot change the prefix, you need to be an admin",
                    color=self.client.re[8],
                )
            )

    @nextcord.slash_command('sniper', description='Toggle Snipe permissions')
    async def snipr(self, inter):
        await self.sniper(inter)

    @commands.command(aliases=['response'])
    async def toggle_response(self, ctx):
        user = getattr(ctx, 'author', getattr(ctx, 'user', None))
        if user.guild_permissions.administrator:
            output=""
            if ctx.guild.id in self.client.config['respond']:
                self.client.config['respond'].remove(ctx.guild.id)
                output="Auto respond turned on"
                
            else:
                self.client.config['respond'].append(ctx.guild.id)
                output="Auto respond turned off"
    
            await ctx.send(embed=ef.cembed(
                title="Enabled",
                description=output,
                color=self.client.re[8],
                thumbnail=self.client.user.avatar.url)
            )
        else:
            await ctx.reply(
                embed=ef.cembed(
                    title="Permissions Denied",
                    description="You need admin permissions to toggle this",
                    color=nextcord.Color.red(),
                    thumbnail=self.client.user.avatar.url
                )
            )

    @commands.command(aliases=['suicide'])
    @commands.check(ef.check_command)
    async def toggle_suicide(self, ctx):
        if getattr(ctx, 'author', getattr(ctx, 'user', None)).guild_permissions.administrator:
            output=""
            if ctx.guild.id in self.client.observer:
                self.client.observer.remove(ctx.guild.id)
                output="enabled"
            else:
                self.client.observer.append(ctx.guild.id)
                output="disabled"
            await ctx.reply(embed=ef.cembed(title="Done",description=f"I've {output} the suicide observer",color=self.client.re[8]))
        else:
            await ctx.send(
                embed=ef.cembed(
                    title="Permission Denied",
                    description="Only an admin can toggle this setting",
                    color=nextcord.Color.red()
                )
            )

    
    @nextcord.slash_command(name="commands", description="Enable and Disable commands, only for admins")
    async def comm(self, inter, mode = ef.defa(choices=['enable','disable','show']), command = "-"):
        await inter.response.defer()
        command = command.lower()        
        if not inter.user.guild_permissions.administrator:
            await inter.send(
                embed=ef.cembed(
                    title="Permissions Denied",
                    description="Only an admin can use this command, please ask an admin to enable this",
                    color=nextcord.Color.red(),
                    
                )
            )
            return
        if command.lower() not in [i.name.lower() for i in self.client.commands] and mode in ['enable','disable']:
            await inter.send("This is not a command, check the spelling")
            return
        if command not in self.client.config['commands'] and command!='-':
            self.client.config['commands'][command] = []
        if mode == 'enable' and command != '-':
            if inter.guild.id in self.client.config['commands'][command]:
                self.client.config['commands'][command].remove(inter.guild.id)
                await inter.send(
                    embed=ef.cembed(
                        title="Done",
                        description=f"Enabled {command} in this server",
                        color=self.client.re[8],
                        thumbnail=self.client.user.avatar.url
                    )
                )
                return
            await inter.send("Already Enabled")
        elif mode == 'disable' and command != '-':
            if inter.guild.id not in self.client.config['commands'][command]:
                self.client.config['commands'][command].append(inter.guild.id)
                await inter.send(
                    embed=ef.cembed(
                        title="Done",
                        description=f"Disabled {command} in this server",
                        color=self.client.re[8],
                        thumbnail=self.client.user.avatar.url
                    )
                )
                return
            await inter.send("Already Disabled")
        else:
            disabled_commands = []
            enabled_commands = []
            for i in [j.name for j in self.client.commands]:
                if inter.guild.id in self.client.config['commands'].get(i,[]):
                    disabled_commands.append(i)
                else:
                    enabled_commands.append(i)

            disabled_commands = "**Disabled commands**\n"+', '.join(disabled_commands)
            enabled_commands = "**Enabled commands**\n"+', '.join(enabled_commands)
            await inter.send(
                embed=ef.cembed(
                    title="Commands",
                    description=enabled_commands+"\n\n"+disabled_commands,
                    color=self.client.re[8],
                    thumbnail=self.client.user.avatar.url,
                    footer="Everything is enabled by default"
                )
            )
    @comm.on_autocomplete("command")
    async def auto(self, inter, command):
        autocomp_command = [i for i in self.command_list if command.lower() in i.lower()][:25]
        await inter.response.send_autocomplete(autocomp_command)

    @nextcord.slash_command(name = "welcome", description = "set welcome channel")
    async def wel(self, inter, channel: GuildChannel = "-"):
        await inter.response.defer()
        if inter.user.guild_permissions.administrator:
            if channel != "-":                
                self.client.config['welcome'][inter.guild.id] = channel.id
                await inter.send(
                    embed=ef.cembed(
                        title="Done",
                        description=f"Set {channel.mention} for welcome and exit messages.",
                        color=self.client.re[8],
                        thumbnail=self.client.user.avatar.url
                    )
                )
            else:
                if self.client.config['welcome'].get(inter.guild.id):
                    del self.client.config['welcome'][inter.guild.id]
                await inter.send(
                    embed=ef.cembed(
                        title="Done",
                        description="Removed welcome channel from config",
                        color=self.client.re[8],
                        thumbnail=self.client.user.avatar.url
                    )
                )
        else:
            await inter.send(
                embed=ef.cembed(
                    title="Permissions Denied",
                    description="You need to be an admin to do this",
                    thumbnail = self.client.user.avatar.url,
                    color=nextcord.Color.red()
                )
            )

    @nextcord.slash_command(name = "subscribe", description = "Subscribe to a youtube channel")
    async def sub_slash(self, inter, channel: GuildChannel = None, url = None, message = ""):
        await inter.response.defer()
        await self.subscribe(inter, channel = channel, url = url, message = message)
    
    @nextcord.slash_command(name = "unsubscribe", description = "remove a youtube channel from a textchannel")
    async def unsub_slash(ctx, channel: GuildChannel = None, url = None):
        await ctx.response.defer()
        await self.unsubscribe(ctx, channel = channel, url = url)
    
    @commands.command()
    @commands.check(ef.check_command)
    async def subscribe(self, ctx, channel: nextcord.TextChannel=None, url=None, *, message=""):
        if getattr(ctx, 'author', getattr(ctx, 'user', None)).guild_permissions.administrator:
            if 'youtube' not in self.client.config: 
                self.client.config['youtube']={}
            if channel.id not in self.client.config['youtube']: 
                self.client.config['youtube'][channel.id]=set()
            if url is not None:
                url = ef.check_end(url)
                self.client.config['youtube'][channel.id].add((url,message))
                await ctx.send(embed=ef.cembed(title="Done",description=f"Added {url} to the list and it'll be displayed in {channel.mention}",color=self.client.re[8],thumbnail=self.client.user.avatar.url))
            else:
                all_links = "\n".join([i[0] for i in self.client.config['youtube'][channel.id]])
                await ctx.send(embed=ef.cembed(
                    title="All youtube subscriptions in this channel",
                    description=all_links,
                    color=self.client.re[8],
                    thumbnail = self.client.user.avatar.url
                ))
        else:
            await ctx.send(
                embed=ef.cembed(
                    title="Permission Denied",
                    description="Only an admin can set it",
                    color=self.client.re[8],
                    thumbnail=self.client.user.avatar.url
                )
            )
    
    @commands.command()
    @commands.check(ef.check_command)
    async def unsubscribe(self, ctx, channel: nextcord.TextChannel=None, url=None):
        if getattr(ctx, 'author', getattr(ctx, 'user', None)).guild_permissions.administrator:
            if 'youtube' not in self.client.config:
                self.client.config['youtube']={}
            if channel.id not in self.client.config['youtube']: 
                self.client.config['youtube'][channel.id]=set()
            if url is None:   
                all_links = "\n".join([i[0] for i in self.client.config['youtube'][channel.id]])
                await ctx.send(embed=ef.cembed(
                    title="All youtube subscriptions in this channel",
                    description=all_links,
                    color=self.client.re[8],
                    thumbnail = self.client.user.avatar.url
                ))
                return
            try:
                url = ef.check_end(url)
                for u,m in self.client.config['youtube'][channel.id]:
                    if u == url:
                        self.client.config['youtube'][channel.id].remove((u,m))
                        break   
                
                await ctx.send(embed=ef.cembed(title="Done", description=f"Removed {url} from the list", color=self.client.re[8], thumbnail=self.client.user.avatar.url))
            except KeyError:
                print(traceback.format_exc())
                await ctx.reply(embed=ef.cembed(title="Hmm",description=f"The URL provided is not in {channel.name}'s subscriptions",color=self.client.re[8]))
        else:
            await ctx.send(
                embed=ef.cembed(
                    title="Permission Denied",
                    description="Only an admin can remove subscriptions",
                    color=self.client.re[8],
                    thumbnail=self.client.user.avatar.url
                )
            )

            
    @commands.command()
    @commands.check(ef.check_command)
    async def changeM(ctx, *, num):
        if str(getattr(ctx, 'author', getattr(ctx, 'user', None)).id) in self.client.dev_users:
            num = int(num)
            if num == 1:
                self.client.re[10] = 1
                await ctx.send(
                    embed=nextcord.Embed(
                        title="Model change",
                        description="Changed to blenderbot",
                        color=nextcord.Color(value=self.client.re[8]),
                    )
                )
            elif num == 2:
                self.client.re[10] = 2
                await ctx.send(
                    embed=ef.cembed(
                        title="Model change",
                        description="Changed to dialo-gpt",
                        color=self.client.re[8],
                    )
                )
            else:    
                await ctx.send(
                    embed=ef.cembed(
                        title="Model change",
                        description="Bruh thats not a valid option",
                        color=self.client.re[8],
                    )
                )
    
        else:
            await ctx.send(
                embed=nextcord.Embed(
                    title="Model change",
                    description="F off thout isn't un dev user",
                    color=nextcord.Color(value=self.client.re[8]),
                )
            )

    @nextcord.slash_command(name="sealfred", description="Checks for behaviours like kicking out or banning regularly")
    async def SeCurity(self, inter, log_channel: GuildChannel = "delete"):
        await inter.response.defer()        
        if not inter.permissions.administrator:
            await inter.send(
                embed=ef.cembed(
                    title="Permission",
                    description="You need admin permissions to do the security work, Ask your owner to execute this command for protection",
                    color=discord.Color.red(),
                    thumbnail=self.client.user.avatar.url
                )
            )
            return
        if log_channel == 'delete':
            if inter.guild.id in self.client.config['security']:
                del self.client.config['security'][inter.guild.id]
            await inter.send(
                embed=ef.cembed(
                    description="Removed SEAlfred from this server, this server is now left unprotected",
                    color=self.client.re[8]
                )
            )
            return
        channel_id = log_channel.id    
        self.client.config['security'][inter.guild.id] = channel_id
        await inter.send(
            embed=ef.cembed(
                title="Done",
                description=f"Set {log_channel.mention} as the log channel, all the updates will be pushed to this",
                color=self.client.re[8]
            )
        )
        
            

def setup(client,**i):
    client.add_cog(Configuration(client,**i))