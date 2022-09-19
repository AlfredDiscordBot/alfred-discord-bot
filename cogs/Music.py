import nextcord
import utils.External_functions as ef
from nextcord.ext import commands

# Use nextcord.slash_command()


def requirements():
    return []


class Music(commands.Cog):
    def __init__(self, CLIENT):
        self.CLIENT = CLIENT

    @nextcord.slash_command(
        name="music", description="No longer supports music, I'm sorry"
    )
    async def music(self, inter):
        await inter.response.send_message(
            embed=ef.cembed(
                title="You will be disappointed",
                description="I'm sorry to say this, but I've heard of Discord Bots losing verification, because it's source was from `Youtube`"
                + "Even though we are totally within the rules of youtube, `no monetizing`, we cannot lose the verification status",
                color=self.CLIENT.color(inter.guild),
                footer={
                    "text": 'I know you will be disappointed. But it is better than "No Alfred"',
                    "icon_url": self.CLIENT.user.avatar,
                },
                author=inter.user,
                thumbnail=self.CLIENT.user.avatar,
            )
        )


def setup(client, **i):
    client.add_cog(Music(client, **i))
