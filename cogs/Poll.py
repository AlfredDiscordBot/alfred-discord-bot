import nextcord
import utils.External_functions as ef
from nextcord.ext import commands

# Use nextcord.slash_command()


def requirements():
    return []


class Poll(commands.Cog, description="Create a poll"):
    def __init__(self, CLIENT: commands.Bot):
        self.CLIENT = CLIENT

    @nextcord.slash_command(name="polling", description="Seperate options with |")
    async def polling_slash(self, inter, question, options="yes|no", image=None):
        await inter.response.defer()
        if not image:
            image = ef.safe_pfp(inter.guild)
        text = question + "\n\n"
        options = options.split("|")
        if len(options) >= 20:
            reply = "Use this if you want to redo\n\n"
            reply += f"Question: `{question}` \n"
            reply += f"Options: `{'|'.join(options)}`"
            await inter.send(
                embed=ef.cembed(
                    title="Sorry you can only give 20 options",
                    description=reply,
                    color=nextcord.Color.red(),
                    thumbnail=self.CLIENT.user.avatar.url,
                )
            )
        for i in range(len(options)):
            text += f"{ef.emoji.emojize(f':keycap_{i+1}:') if i<10 else ef.Emoji_alphabets[i-10]} | {options[i].strip()}\n"

        embed = ef.cembed(
            title="Poll",
            description=text,
            color=self.CLIENT.color(inter.guild),
            footer=f"from {inter.user.name} | {inter.guild.name}",
            picture=image,
            author=inter.user,
        )
        message = await inter.send(embed=embed)

        for i in range(len(options)):
            await message.add_reaction(
                ef.emoji.emojize(f":keycap_{i+1}:")
                if i < 10
                else ef.Emoji_alphabets[i - 10]
            )

    @nextcord.message_command(name="poll result")
    async def result(self, inter: nextcord.Interaction, message):
        check = any(
            [
                message.author.id != self.CLIENT.user.id,
                message.embeds[0].title != "Poll",
            ]
        )
        if check:
            await inter.response.send_message(content="Not my poll 🤨", ephemeral=True)
            return
        await inter.response.defer()
        P = ef.PollGraph(self.CLIENT, inter)
        P.extract_from_message(message=message)
        f, embed = P.generate_embed()
        await inter.send(embed=embed, file=f)


def setup(CLIENT, **i):
    CLIENT.add_cog(Poll(CLIENT, **i))
