import nextcord
import utils.assets as assets
import asyncio
import utils.External_functions as ef
from nextcord.ext import commands


def requirements():
    return []


class TicketView(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @nextcord.ui.button(
        label="Ticket", emoji="🎫", custom_id="alfred_ticket", style=assets.color
    )
    async def open_ticket(self, _, inter):
        message = inter.message
        embed = message.embeds[0]
        mess = await inter.channel.send(f"Creating Ticket for {inter.user.name}")
        th = await inter.channel.create_thread(
            name=f"Ticket - {inter.user.name} {inter.user.id}",
            reason=f"Ticket for {str(inter.user)}",
            message=mess,
        )
        await mess.delete()
        embed.set_footer(
            text="Close Ticket using 'close_ticket after you're done",
            icon_url=inter.client.user.avatar.url,
        )
        await th.send(content=inter.user.mention, embed=embed)


class Ticket(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        self.client.add_view(TicketView())

    @commands.command()
    async def close_ticket(self, ctx):
        if type(ctx.channel) != nextcord.Thread:
            return
        if ctx.channel.owner == self.client.user:
            confirm = await ef.wait_for_confirm(
                ctx,
                self.client,
                "Do you want to close this ticket?",
                self.client.color(ctx.guild),
            )
            if not confirm:
                return
            if not ctx.author.id == int(ctx.channel.name.split()[-1]):
                if not ctx.author.guild_permissions.administrator:
                    await ctx.send(
                        embed=ef.cembed(
                            title="Permission Denied",
                            description="You need to be the one who created the ticket or you need to be an admin to close this ticket",
                            color=nextcord.Color.red(),
                            thumbnail=self.client.user.avatar.url,
                        )
                    )
                    return

            await ctx.send(
                embed=ef.cembed(
                    description="Deleting the ticket in 5 seconds",
                    color=self.client.color(ctx.guild),
                )
            )
            await asyncio.sleep(5)
            await ctx.channel.delete()

    @nextcord.slash_command(name="ticket", description="create a ticket message")
    async def tick(self, inter, description="None"):
        await inter.response.defer()
        if not inter.user.guild_permissions.administrator:
            e = assets.Emotes(self.client)
            await inter.send(
                embed=ef.cembed(
                    title="Permissions Denied",
                    description=f"{e.animated_wrong}You're not an admin to create a ticket message",
                    color=self.client.color(inter.guild),
                ),
                ephemeral=True,
            )
            return
        if description == "None":
            description = "Open your tickets here"
        await inter.send("Done", ephemeral=True)
        message = await inter.channel.send(
            embed=ef.cembed(
                title="Ticket",
                description=description,
                color=self.client.color(inter.guild),
                thumbnail=ef.safe_pfp(inter.guild),
            ),
            view=TicketView(),
        )


def setup(client, **i):
    client.add_cog(Ticket(client, **i))
