import nextcord
import utils.External_functions as ef
import emoji
from nextcord.ext import commands
from random import choice


def requirements():
    return []


DEFAULT_TITLE = "__GIVEAWAY__"
DEFAULT_DESCRIPTION = (
    lambda e, user: f"""
New Giveaway, hosted by our very own {user.mention}, feel free to participate in this by reacting to the Emoji {e}
"""
)
DEFAULT_FOOTER = lambda picture: {
    "text": "All the best, I hope you win 🤞",
    "icon_url": str(picture),
}


class Giveaway(
    commands.Cog,
    description="Use `/giveaway` to create a giveaway, to roll, you can either use the prefix command `'roll <number>` or message command roll",
):
    def __init__(self, CLIENT: commands.Bot):
        self.CLIENT = CLIENT

    @nextcord.slash_command(
        name="giveaway", description="You can use this for giveaway"
    )
    async def giveaway(
        self,
        inter,
        donor: nextcord.User = None,
        required_role: nextcord.Role = " ",
        heading=DEFAULT_TITLE,
        description=None,
        emoji=emoji.emojize(":party_popper:"),
        giveaway_money: str = None,
        time: str = None,
        image="https://media.discordapp.net/attachments/960070023563603968/963041700996063282/standard_6.gif",
    ):
        await inter.response.defer()
        if donor is None:
            donor = inter.user
        if description is None:
            description = DEFAULT_DESCRIPTION(emoji, donor)
        fields = {}
        if giveaway_money:
            fields["Money"] = giveaway_money
        if time:
            fields["Time"] = time
        embed = ef.cembed(
            title=heading,
            description=description,
            color=self.CLIENT.color(inter.guild),
            thumbnail=self.CLIENT.user.avatar.url,
            image=image,
            footer=DEFAULT_FOOTER(self.CLIENT.user.avatar),
            fields=ef.dict2fields(fields, inline=True),
        )
        embed.set_author(name=donor.name, icon_url=ef.safe_pfp(donor))
        m = await inter.send(
            f"Giveaway!! Requirement: {required_role.mention if required_role !=' ' else required_role}",
            embed=embed,
        )
        await m.add_reaction(emoji)

    @commands.command()
    @commands.check(ef.check_command)
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def roll(self, ctx, number):
        if not ctx.author.guild_permissions.manage_channels:
            await ctx.send(
                embed=ef.cembed(
                    title="Permissions Denied",
                    description="You need manage channel permission to access this function",
                    color=self.CLIENT.color(ctx.guild),
                )
            )
            return
        if not ctx.message.reference:
            await ctx.send("You need to reply to a giveaway message by Alfred")
            return
        message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        if not message.author == self.CLIENT.user:
            await ctx.reply("Heyyyyy, wait a minute, that's not my giveaway mesage")
            return
        if not message.clean_content.startswith("Giveaway"):
            await ctx.reply(
                "Ok that's my messsage, but is that a giveaway message?????"
            )
            return
        if message.embeds[0].title == "Time up":
            await ctx.reply("That's an old giveaway message")
            return
        reaction = message.reactions[0]
        users = await reaction.users().flatten()
        users.remove(self.CLIENT.user)
        roles = message.raw_role_mentions
        if len(roles) > 0:
            roles = roles[0]
        if type(roles) == int:
            roles = ctx.guild.get_role(roles)
        for i in users.copy():
            if roles != [] and roles not in i.roles:
                users.remove(i)
                await reaction.remove(i)
        await message.edit(
            embed=ef.cembed(
                title="Time up",
                description="The giveaway has ended, hope you get it the next time",
                color=self.CLIENT.color(ctx.guild),
                thumbnail=self.CLIENT.user.avatar.url,
            )
        )
        if len(users) == 0:
            await ctx.send("No one participated in the giveaway :frown:")
            return
        l = ""
        if int(number) > len(users):
            number = len(users)
        for i in range(int(number)):
            lu = choice(users)
            await reaction.remove(lu)
            lu = lu.mention
            l = l + lu
        await ctx.send(f"Congratulations, {l} has won the giveaway")

    @nextcord.message_command(name="roll")
    async def roll_interaction(self, inter, message):
        if not inter.user.guild_permissions.manage_channels:
            await inter.response.send_message(
                "Permission Denied, you need manage channels permission", ephemeral=True
            )
            return
        if message.author.id != self.CLIENT.user.id:
            await inter.response.send_message("That's not my message", ephemeral=True)
            return
        if not message.content.startswith("Giveaway"):
            await inter.response.send_message(
                "Ok that's my messsage, but is that a giveaway message?????",
                ephemeral=True,
            )
            return
        reaction = message.reactions[0]
        users = await reaction.users().flatten()
        users.remove(self.CLIENT.user)
        roles = message.raw_role_mentions
        if len(roles) > 0:
            roles = roles[0]
        if type(roles) == int:
            roles = inter.guild.get_role(roles)
        for i in users.copy():
            if roles != [] and roles not in i.roles:
                users.remove(i)
                await reaction.remove(i)
        if not len(users):
            await inter.send("No one participated in the giveaway :frown:")
            return
        l = ""
        for i in range(int(1)):
            lu = choice(users)
            await reaction.remove(lu)
            lu = lu.mention
            l = l + lu
        await inter.channel.send(f"Congratulations, {l} has won the giveaway")
        await inter.response.send_message(content="Done", ephemeral=True)


def setup(CLIENT, **i):
    CLIENT.add_cog(Giveaway(CLIENT, **i))
