
import nextcord
import utils.External_functions as ef
from nextcord.ext import commands
from subprocess import getoutput

# Use nextcord.slash_command()

def requirements():
    return ["DEV_CHANNEL"]

class Developer(commands.Cog):
    def __init__(self, client, DEV_CHANNEL):
        self.client = client
        self.SUPER_USERS = [
            "432801163126243328",
            "803855283821871154",
            "723539849969270894"
        ]
        self.DEV_CHANNEL = DEV_CHANNEL

    @commands.command()
    @commands.check(ef.check_command)
    async def reply(self, ctx, channel, user, *, repl):
        if str(ctx.author.id) in self.client.dev_users and ctx.guild.id == 822445271019421746:
            channel = self.client.get_channel(int(channel))
            if not channel:
                await ctx.send(
                    embed=ef.cembed(
                        description="This channel does not exist",
                        color=self.client.re[8]
                    )
                )
                return
            await channel.send(f"<@{user}>",
                embed=ef.cembed(
                    description = repl,
                    color=self.client.re[8]
                )
            )
            await ctx.send("Done")
        else:
            await ctx.send(
                embed=ef.cembed(
                    title="Permissions Denied",
                    description="You cannot execute this command here" if ctx.guild.id != 822445271019421746 else "You're not a developer to do this",
                    color=self.client.re[8]
                )
            )

           
    @commands.command()
    @commands.check(ef.check_command)
    async def dev_test(self, ctx, user:nextcord.Member=None):
        if not user:
            user = ctx.author
        if str(user.id) in self.client.dev_users:
            await ctx.send(f"{user} is a dev!")
        else:
            await ctx.send(f"{user} is not a dev!")

    @commands.command()
    @commands.check(ef.check_command)
    async def remove_dev(self, ctx, member: nextcord.Member):
        print(member)
        user = getattr(ctx, 'author', getattr(ctx, 'user', None))
        if str(user.id) in self.SUPER_USERS:
            self.client.dev_users.remove(str(member.id))
            await ctx.send(member.mention + " is no longer a dev")
        else:
            await ctx.send(
                embed=ef.cembed(
                    title="Permission Denied",
                    description="Dude! You are not Alvin",
                    color=self.client.re[8],
                )
            )


    @commands.command()
    @commands.check(ef.check_command)
    async def add_dev(self, ctx, member: nextcord.Member):
        print(member)
        user = getattr(ctx, 'author', getattr(ctx, 'user', None))
        print("Add dev", str(user))
        if str(user.id) in self.client.dev_users:
            self.client.dev_users.add(str(member.id))
            await ctx.send(member.mention + " is a dev now")
        else:
            await ctx.send(
                embed=ef.cembed(
                    title="Permission Denied",
                    description="Dude! you are not a dev",
                    color=self.client.re[8],
                )
            )

    @commands.command(name="update", description="Pulls new updates from Github")
    @commands.check(ef.check_command)
    async def update(self, ctx):
        if str(ctx.author.id) in self.client.dev_users:
            embed=ef.cembed(
                title="Update command",
                description="```bash\n"+getoutput("git pull")+"\n```",
                color=self.client.re[8],
                thumbnail=self.client.user.avatar,
                author=ctx.author,
                footer={
                    'text': 'A copy of this is send to Wayne Enterprise',
                    'icon_url': self.client.get_guild(822445271019421746).icon
                }
            )
            await ctx.send(embed=embed)
            await self.client.get_channel(946381704958988348).send(embed=embed)
        else:
            await ctx.send(
                embed=ef.cembed(
                    title="Permission Denied",
                    description="This is a developer only function, you cannot use this",
                    color=self.client.re[8],
                    author=ctx.author,
                    thumbnail=self.client.user.avatar
                )
            )


    @commands.command()
    @commands.check(ef.check_command)
    async def leave_server(self, ctx, *, server_name):
        if str(ctx.author.id) in self.client.dev_users:
            guild = nextcord.utils.get(self.client.guilds, name=server_name)
            if guild is None:
                await ctx.send(
                    embed=ef.cembed(
                        title="Hmm",
                        description="This server doesnt exist. Please check if the name is right",
                        color=self.client.re[8],
                    )
                )
            else:
                await guild.leave()
                await ctx.send(
                    embed=ef.cembed(
                        title="Done",
                        description="I left the server " + server_name,
                        color=self.client.re[8],
                    )
                )
        else:
            await ctx.send(
                embed=ef.cembed(
                    title="Permission Denied",
                    description="You dont have the permission to do this",
                    color=self.client.re[8],
                )
            )


def setup(client,**i):
    client.add_cog(Developer(client,**i))