import nextcord
import utils.assets as assets
import utils.External_functions as ef
from nextcord.ext import commands
from nextcord import ChannelType, ui, TextInputStyle
from nextcord.abc import GuildChannel
from .Embed import filter_graves

# Use nextcord.slash_command()


def requirements():
    return []


class ApplicationButton(ui.View):
    def __init__(self, CLIENT: commands.Bot):
        self.CLIENT = CLIENT
        super().__init__(timeout=None)

    @ui.button(label="Application", style=assets.color, custom_id="alfred_application")
    async def open_modal(self, button, inter):
        if inter.message.author.id != self.CLIENT.user.id:
            await inter.response.send_message("Not for me", ephemeral=True)
            await inter.delete_original_message()
            return
        await inter.response.send_modal(ApplicationModel(self.CLIENT, inter.message))


class ApplicationModel(ui.Modal):
    def __init__(self, CLIENT, message):
        super().__init__(
            "Application",
            timeout=600,
        )
        self.CLIENT = CLIENT
        self.message = message
        self.embed = self.message.embeds[0]
        self.embed_to_items()

    def embed_to_items(self):
        questions = filter_graves(self.embed.description).strip().split("\n")
        for n, q in enumerate(questions):
            Input = ui.TextInput(
                label=q[:40], min_length=1, style=TextInputStyle.paragraph
            )
            setattr(self, f"field{n}", Input)
            self.add_item(getattr(self, f"field{n}"))

    async def callback(self, inter):
        channel = self.CLIENT.get_channel(int(self.message.embeds[0].footer.text))
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
                color=self.CLIENT.re[8],
                description=f"This was done in the {inter.channel.mention}",
                footer={
                    "text": f"UserID: {inter.user.id}",
                    "icon_url": ef.safe_pfp(inter.user),
                },
                fields=fields,
            )
        )
        await inter.response.send_message(ephemeral=True, content="Done")


class ApplicationCreate(ui.Modal):
    def __init__(self, channel, log_channel):
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

    async def callback(self, inter):
        if len(self.question.value.split("\n")) > 5:
            await inter.response.send_message(
                "Cannot have more than 5 questions", ephemeral=True
            )
            return
        await self.channel.send(
            embed=ef.cembed(
                title="Application",
                description=f"```\n{filter_graves(self.question.value)}\n```",
                color=inter.CLIENT.re[8],
                thumbnail=ef.safe_pfp(inter.guild),
                footer=str(self.log_channel.id),
            ),
            view=ApplicationButton(inter.CLIENT),
        )
        await inter.response.send_message(
            ephemeral=True,
            embed=ef.cembed(description="Done", color=inter.CLIENT.re[8]),
        )


class Application(
    commands.Cog,
    description="Used for Creating Easy Application\nIt is a very easy process and very convenient",
):
    def __init__(self, CLIENT: commands.Bot):
        self.CLIENT = CLIENT

    @commands.Cog.listener()
    async def on_ready(self):
        self.CLIENT.add_view(ApplicationButton(self.CLIENT))

    @nextcord.slash_command(name="application", description="Create An Application")
    async def application(
        self,
        inter,
        channel: GuildChannel = ef.defa(ChannelType.text),
        log_channel: GuildChannel = ef.defa(ChannelType.text),
    ):
        if not inter.user.guild_permissions.manage_guild:
            await inter.response.send_message(
                ephemeral=True,
                embed=ef.cembed(
                    title="Permissions Denied",
                    description="You do not have manage server permission",
                    color=self.CLIENT.re[8],
                    thumbnail=self.CLIENT.user.avatar.url,
                ),
            )
            return
        await inter.response.send_modal(ApplicationCreate(channel, log_channel))


def setup(CLIENT, **i):
    CLIENT.add_cog(Application(CLIENT, **i))
