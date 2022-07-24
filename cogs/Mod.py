import nextcord, asyncio, traceback
import utils.assets as assets
import utils.External_functions as ef
from nextcord.ext import commands

# Use nextcord.slash_command()

def requirements():
    return []

class Mod(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.deleted_message = {}

    @commands.Cog.listener()
    async def on_bulk_message_delete(self, messages):
        for i in messages:
            await self.on_message_delete(i)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.guild.id in self.client.config['commands'].get('snipe',[]):
            return
        if not message.channel.id in list(self.deleted_message.keys()):
            self.deleted_message[message.channel.id] = []
        if len(message.embeds) <= 0:
            if not message.author.bot:
                self.deleted_message[message.channel.id].append(
                    (str(message.author), message.content)
                )
        else:
            if not message.author.bot:
                self.deleted_message[message.channel.id].append(
                    (str(message.author), message.embeds[0], True)
                )

    @nextcord.slash_command(name="snipe", description="Get the last few deleted messages")
    async def snipe_slash(self, inter, number = 50):
        await self.snipe(inter, number)


    @commands.command()
    @commands.check(ef.check_command)
    async def snipe(self, ctx, number:int=50):
        number = int(number)
        if (
            getattr(ctx, 'author', getattr(ctx, 'user', None)).guild_permissions.administrator
            or ctx.guild.id not in self.client.config['snipe']
        ):
            message = self.deleted_message.get(ctx.channel.id,[("Empty","Nothing here lol")])[::-1]
            count=0
            embeds = []
            s = ""
            for i in message[:number]:
                count+=1            
                if len(i) < 3:
                    s+="**" + i[0] + ":**\n" + i[1]+"\n\n"     
                    if count%5==0 or count == len(message) or count == number:
                        embed=ef.cembed(
                            title="Snipe",
                            description=s,
                            color=self.client.re[8],
                            thumbnail=ef.safe_pfp(ctx.guild)
                        )
                        embeds.append(embed)
                        s=""                        
                else:
                    await ctx.send("**" + i[0] + ":**",embed=i[1])
            if len(embeds)>0: 
                await assets.pa(ctx, embeds, start_from=0, restricted=True, delete_after=20)
        else:
            await ctx.send(
                embed=ef.cembed(
                    title="Permissions Denied",
                    description="Sorry guys, only admins can snipe now",
                    color=self.client.re[8],
                    thumbnail=self.client.avatar.url,
                    author=ctx.author
                )
            )

    @commands.command(aliases=["ban"])
    @commands.check(ef.check_command)
    @commands.cooldown(1,10,commands.BucketType.guild)
    async def ban_member(self, ctx, member: ef.nextcord.Member, *, reason=None):
        if ctx.author.guild_permissions.ban_members:
            await member.ban(reason = reason)
            await ctx.send(
                embed = ef.cembed(
                    title="That dude's gone forever",
                    description=f"{member.name} was banned by {ctx.author.name}",
                    color=self.client.re[8],
                )
            )
        else:
            await ctx.send(
                embed = ef.cembed(
                    title="Permissions Denied",
                    description="You cant ban members, you dont have the permission to do it",
                    color=self.client.re[8],
                )
            )

    @commands.command(aliases=["kick"])
    @commands.check(ef.check_command)
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def kick_member(self, ctx, member: ef.nextcord.Member, *, reason=None):
        if ctx.author.guild_permissions.ban_members:
            await member.kick(reason=reason)
            await ctx.send(
                embed=ef.cembed(
                    title="Kicked",
                    description=member.name + " was kicked by " + ctx.author.name,
                    color=self.client.re[8],
                )
            )
        else:
            await ctx.send(
                embed=ef.cembed(
                    title="Permissions Denied",
                    description="You cant kick members, you dont have the permission to do it",
                    color=self.client.re[8],
                )
            )
            
    @commands.command(aliases=["mu"])
    @commands.check(ef.check_command)
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def mute(self, ctx, member: ef.nextcord.Member, time:int=10):
        self.client.re[0]+=1
        if not getattr(ctx, 'author', getattr(ctx, 'user', None)).guild_permissions.mute_members:
            await ctx.send(
                embed=ef.cembed(
                    title="Permissions Denied",
                    description = "You dont have enough permission to execute this command",
                    color=self.client.re[8]
                )
            )
            return
        print("Member id: ", member.id)
        await member.edit(timeout = ef.datetime.timedelta(minutes = time))
        await ctx.send(
            embed=ef.cembed(
                title="Done",
                description=f"Muted {member.mention}",
                color=self.client.re[8]
            )
        )




    @commands.command(aliases=["um"])
    @commands.check(ef.check_command)
    async def unmute(self, ctx, member: ef.nextcord.Member):
        self.client.re[0]+=1
        if not getattr(ctx, 'author', getattr(ctx, 'user', None)).guild_permissions.mute_members:
            await ctx.send(
                embed=ef.cembed(
                    title="Permissions Denied",
                    description = "You dont have enough permission to execute this command",
                    color=self.client.re[8]
                )
            )
            return
        print("Member id: ", member.id)
        await member.edit(timeout = None)
        await ctx.send(
            embed=ef.cembed(
                title="Done",
                description=f"Unmuted {member.mention}",
                color=self.client.re[8]
            )
        )

    @commands.command(aliases=["*"])
    @commands.check(ef.check_command)
    async def change_nickname(self, ctx, member: nextcord.Member, *, nickname=None):
        user = getattr(ctx, 'author', getattr(ctx, 'user', None))
        if user.guild_permissions.change_nickname and user.top_role.position > member.top_role.position:
            await member.edit(nick=nickname)
            await ctx.send(
                embed=ef.cembed(
                    title="Nickname Changed",
                    description=f"Nickname changed to {member.nick or member.name} by {user.mention}",
                    color=self.client.re[8],
                )
            )
        else:
            await ctx.send(
                embed=ef.cembed(
                    title="Permissions Denied",
                    description="You dont have permission to change others nickname",
                    color=self.client.re[8],
                )
            )

    @commands.command(aliases=['purge'])
    @commands.check(ef.check_command)
    async def clear(self, ctx, text, num:int=10):
        self.client.re[0]+=1
        await ctx.message.delete()
        if str(text) == self.client.re[1]:
            user = getattr(ctx, 'author', getattr(ctx, 'user', None))
            if user.guild_permissions.manage_messages or user.id == 432801163126243328:
                confirmation = True
                if int(num) > 10:
                    confirmation = await ef.wait_for_confirm(
                        ctx, self.client, 
                        f"Do you want to delete {num} messages",
                        color=self.client.re[8]
                    )
                if confirmation:
                    await ctx.channel.delete_messages(
                        [i async for i in ctx.channel.history(limit=num) if not i.pinned][:100]
                    )
            else:
                await ctx.send(
                    embed=ef.cembed(
                        title="Permission Denied",
                        description="You cant delete messages",
                        color=self.client.re[8],
                    )
                )
        else:
            await ctx.send("Wrong password")

    def has_role(self, member: nextcord.Member, role: nextcord.Role):
        if role in member.roles:
            return True

    @nextcord.slash_command(name="autoaddrole", description="Add roles to all")
    async def autoadd(self, inter):
        print(inter.user)

    @autoadd.subcommand(name="tobots", description="Bots")
    async def bots(self, inter, role: nextcord.Role):
        await inter.response.defer()
        if not inter.user.id == inter.guild.owner.id:
            await inter.send(
                embed=ef.cembed(
                    title="Permission Denied",
                    description="You cannot execute this command, only server owners can",
                    color=nextcord.Color.red(),
                    thumbnail=self.client.user.avatar.url,
                    author=inter.user,
                    footer="Please ask your owner to execute this command"
                )
            )
            return
        confirm = await ef.wait_for_confirm(
            inter, self.client, "Are you Sure you want to do this", color=self.client.re[8]
        )
        if not confirm:
            await inter.send("Aborting")
            return 
        to_be_added = [_ for _ in inter.guild.bots if not self.has_role(_, role)]
        await inter.send(
            embed=ef.cembed(
                title="All right",
                description="This may take a while to process, please be patient",
                color=self.client.re[8],
                author=inter.user,
                footer=f"This will be applied to {len(to_be_added)} bots"
            )
        )
        for bot in to_be_added: 
            try:
                await bot.add_roles(role)
                await asyncio.sleep(2)
            except:
                print(traceback.format_exc())   

    @autoadd.subcommand(name="toeveryone", description="Bots")
    async def everyone(self, inter, role: nextcord.Role):
        await inter.response.defer()
        if not inter.user.id == inter.guild.owner.id:
            await inter.send(
                embed=ef.cembed(
                    title="Permission Denied",
                    description="You cannot execute this command, only server owners can",
                    color=nextcord.Color.red(),
                    thumbnail=self.client.user.avatar.url,
                    author=inter.user,
                    footer="Please ask your owner to execute this command"
                )
            )
            return
        confirm = await ef.wait_for_confirm(
            inter, self.client, "Are you Sure you want to do this", color=self.client.re[8]
        )
        if not confirm:
            await inter.send("Aborting")
            return 
        to_be_added = [_ for _ in inter.guild.members if not self.has_role(_, role)]
        await inter.send(
            embed=ef.cembed(
                title="All right",
                description="This may take a while to process, please be patient",
                color=self.client.re[8],
                author=inter.user,
                footer=f"This will be applied to {len(to_be_added)} members"
            )
        )
        for member in to_be_added: 
            try:
                await member.add_roles(role)
                await asyncio.sleep(2)
            except:
                print(traceback.format_exc())  

    @commands.command()
    async def get_invite(self, ctx, time:int=600):
        link = await ctx.channel.create_invite(max_age=time)
        await ctx.send(
            embed=ef.cembed(
                title="Invitation link",
                description=str(link),
                color=self.client.re[8],
            )
        )    

    @autoadd.subcommand(name="tohumans", description="Bots")
    async def humans(self, inter, role: nextcord.Role):
        await inter.response.defer()
        if not inter.user.id == inter.guild.owner.id:
            await inter.send(
                embed=ef.cembed(
                    title="Permission Denied",
                    description="You cannot execute this command, only server owners can",
                    color=nextcord.Color.red(),
                    thumbnail=self.client.user.avatar.url,
                    author=inter.user,
                    footer="Please ask your owner to execute this command"
                )
            )
            return
        confirm = await ef.wait_for_confirm(
            inter, self.client, "Are you Sure you want to do this", color=self.client.re[8]
        )
        if not confirm:
            await inter.send("Aborting")
            return 
        to_be_added = [_ for _ in inter.guild.humans if not self.has_role(_, role)]
        await inter.send(
            embed=ef.cembed(
                title="All right",
                description="This may take a while to process, please be patient",
                color=self.client.re[8],
                author=inter.user,
                footer=f"This will be applied to {len(to_be_added)} humans"
            )
        )
        for member in to_be_added: 
            try:
                await member.add_roles(role)
                await asyncio.sleep(2)
            except:
                print(traceback.format_exc())        


def setup(client,**i):
    client.add_cog(Mod(client,**i))