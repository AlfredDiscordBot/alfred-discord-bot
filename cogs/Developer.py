
import nextcord
import utils.External_functions as ef
from nextcord.ext import commands

# Use nextcord.slash_command()

def requirements():
    return []

class Developer(commands.Cog):
    def __init__(self, client):
        self.client = client

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