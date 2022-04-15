import nextcord
import assets
import time
import helping_hand
import External_functions as ef
from nextcord.ext import commands, tasks

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
                color=self.re[8],
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
                color=self.re[8],
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
                        color=self.re[8],
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
                        color=self.re[8],
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
                    color=self.re[8],
                    thumbnail=self.client.user.avatar.url,
                    footer="Everything is enabled by default"
                )
            )
    @comm.on_autocomplete("command")
    async def auto(self, inter, command):
        autocomp_command = [i for i in self.command_list if command.lower() in i.lower()][:25]
        await inter.response.send_autocomplete(autocomp_command)
            
            

def setup(client,**i):
    client.add_cog(Configuration(client,**i))