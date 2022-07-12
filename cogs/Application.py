from __future__ import (
    annotations,
)  # IMPORTANT: this must be placed in the top of the file
import nextcord
from . import assets
from . import External_functions as ef
from nextcord.ext import commands
from nextcord import ChannelType, ui, TextInputStyle
from nextcord.abc import GuildChannel
from Embed import filter_graves
from typing_extensions import Self
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from nextcord import Button, Interaction, Message, Embed
# Use nextcord.slash_command()


def requirements():
    return []


class ApplicationButton(ui.View):
    def __init__(self: Self, client: commands.Bot) -> None:
        self.client: commands.Bot = client
        super().__init__(timeout=None)

    @ui.button(label="Application", style=assets.color, custom_id="alfred_application")
    async def open_modal(self: Self, button: Button, inter: Interaction) -> None:
        if inter.message.author.id != self.client.user.id:
            await inter.response.send_message("Not for me", ephemeral=True)
            await inter.delete_original_message()
            return
        await inter.response.send_modal(ApplicationModel(self.client, inter.message))


class ApplicationModel(ui.Modal):
    def __init__(self: Self, client: commands.Bot, message: Message) -> None:
        super().__init__(
            "Application",
            timeout=600,
        )
        self.client: commands.Bot = client
        self.message: Message = message
        self.embed: Embed = self.message.embeds[0]
        self._embed_to_items()

    def _embed_to_items(self: Self):
        questions = filter_graves(self.embed.description).strip().split("\n")
        n = 0
        for q in questions:
            n += 1
            Input = ui.TextInput(
                label=q[:40], min_length=1, style=TextInputStyle.paragraph
            )
            setattr(self, f"field{n}", Input)
            self.add_item(getattr(self, f"field{n}"))

    async def callback(self, inter):
        channel = self.client.get_channel(int(self.message.embeds[0].footer.text))
        fields = []
        for attribute in dir(self):
            if attribute.startswith("field"):
                fields.append(
                    {
                        "name": getattr(self, attribute).label,
                        "value": f"```\n{filter_graves(getattr(self, attribute).value)}\n```",
                        "inline": False,
                    }
                )
        await channel.send(
            embed=ef.cembed(
                title=f"Application By {inter.user.name}",
                author=inter.user,
                color=self.client.re[8],
                description=f"This was done in the {inter.channel.mention}",
                footer={
                    "text": "This is still in Beta",
                    "icon_url": self.client.user.avatar.url,
                },
                fields=fields,
            )
        )
        await inter.response.send_message(ephemeral=True, content="Done")


class ApplicationCreate(ui.Modal):
    def __init__(self: Self, channel: GuildChannel, log_channel: GuildChannel) -> None:
        super().__init__("Create Application", timeout=1200)
        self.question = ui.TextInput(
            label="Enter your question",
            min_length=1,
            placeholder="Seperate questions by line",
            style=TextInputStyle.paragraph,
        )
        self.add_item(self.question)
        self.channel = channel
        self.log_channel = log_channel

    async def callback(self: Self, inter: Interaction) -> None:
        if len(self.question.value.split("\n")) > 5:
            await inter.response.send_message(
                "Cannot have more than 5 questions", ephemeral=True
            )
            return
        await self.channel.send(
            embed=ef.cembed(
                title="Application",
                description=f"```\n{filter_graves(self.question.value)}\n```",
                color=inter.client.re[8],
                thumbnail=ef.safe_pfp(inter.guild),
                footer=str(self.log_channel.id),
            ),
            view=ApplicationButton(inter.client),
        )
        await inter.response.send_message(
            ephemeral=True,
            embed=ef.cembed(description="Done", color=inter.client.re[8]),
        )


class Application(commands.Cog):
    def __init__(self: Self, client: commands.Bot):
        self.client: commands.Bot = client

    @commands.Cog.listener()
    async def on_ready(self: Self):
        self.client.add_view(ApplicationButton(self.client))

    @nextcord.slash_command(
        name="application",
        description="Create An Application",
        default_member_permissions=32,
    )
    async def application(
        self: Self,
        inter: Interaction,
        channel: GuildChannel = ef.defa(ChannelType.text),
        log_channel: GuildChannel = ef.defa(ChannelType.text),
    ) -> None:
        if not inter.user.guild_permissions.manage_guild:
            await inter.response.send_message(
                ephemeral=True,
                embed=ef.cembed(
                    title="Permissions Denied",
                    description="You do not have manage server permission",
                    color=self.client.re[8],
                    thumbnail=self.client.user.avatar.url,
                ),
            )
            return
        await inter.response.send_modal(ApplicationCreate(channel, log_channel))


def setup(client: commands.Bot, **i) -> None:
    client.add_cog(Application(client, **i))
