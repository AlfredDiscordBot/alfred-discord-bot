import nextcord
import utils.External_functions as ef
import emoji
import asyncio

from .Music import Player
from nextcord.ext import commands, tasks
from random import choice

# Use nextcord.slash_command()


def requirements():
    return ["FFMPEG_OPTIONS", "ydl_op"]


class Games(commands.Cog, description="Very Simple Games"):
    def __init__(self, CLIENT: commands.Bot, FFMPEG_OPTIONS, ydl_op):
        self.CLIENT = CLIENT
        self.FFMPEG_OPTIONS = FFMPEG_OPTIONS
        self.choices = [
            emoji.emojize(":rock:"),
            emoji.emojize(":roll_of_paper:"),
            emoji.emojize(":scissors:"),
        ]
        self.exit = emoji.emojize(":cross_mark_button:")
        self.victor = {
            self.choices[0]: self.choices[2],
            self.choices[1]: self.choices[0],
            self.choices[2]: self.choices[1],
        }
        self.player = Player(CLIENT, FFMPEG_OPTIONS, ydl_op)

    @nextcord.slash_command(
        name="rps", description="play some rock paper scissors against me"
    )
    async def rp(self, inter):
        await inter.response.defer()
        s = {}
        embed = ef.cembed(
            title="Rock Paper Scissor",
            description="Hi, You will be playing rock paper scissor against me, please try not to delay it as discord hates me for waiting",
            color=self.CLIENT.color(inter.guild),
            thumbnail=self.CLIENT.user.avatar.url,
            footer="You can press X when you wanna stop or else it'll timeout after 10 minutes",
            author=inter.user,
        )
        user = inter.user
        s[user] = 0
        s[self.CLIENT.user] = 0
        embed.add_field(name="You", value=s[user], inline=True)
        embed.add_field(name="Alfred", value=s[self.CLIENT.user], inline=True)
        message = await inter.send(embed=embed)
        for i in self.choices:
            await message.add_reaction(i)
        await message.add_reaction(self.exit)

        def check(reaction, r_user):
            return r_user == user and reaction.emoji in self.choices + [self.exit]

        while True:
            print("Reaction Checking")
            try:
                r, u = await self.CLIENT.wait_for(
                    "reaction_add", timeout=600, check=check
                )
                print("Done reaction checking")
                try:
                    await r.remove(u)
                except:
                    pass
                r = r.emoji
                alfred = choice(self.choices)
                if r == self.exit:
                    embed = ef.cembed(
                        title="Bye",
                        description="Ig I'll see you later",
                        color=self.CLIENT.color(inter.guild),
                        thumbnail=self.CLIENT.user.avatar.url,
                    )
                    embed.add_field(name="You", value=s[user], inline=True)
                    embed.add_field(
                        name="Alfred", value=s[self.CLIENT.user], inline=True
                    )
                    await message.edit(embed=embed)
                    return
                if r in self.choices:
                    if r == alfred:
                        await message.edit(
                            embed=ef.cembed(
                                title="Draw",
                                description=f"You both put {r}",
                                color=self.CLIENT.color(inter.guild),
                                thumbnail=self.CLIENT.user.avatar.url,
                                footer="Try again",
                            )
                        )
                    elif r in self.victor and self.victor[r] == alfred:
                        embed = ef.cembed(
                            title="You won",
                            description=f"You put {r}, I put {alfred}",
                            color=self.CLIENT.color(inter.guild),
                            thumbnail=ef.safe_pfp(user),
                        )
                        s[user] += 1
                        embed.add_field(name="You", value=s[user], inline=True)
                        embed.add_field(
                            name="Alfred", value=s[self.CLIENT.user], inline=True
                        )
                        await message.edit(embed=embed)
                    else:
                        embed = ef.cembed(
                            title="You lost",
                            description=f"You put {r}, I put {alfred}",
                            color=self.CLIENT.color(inter.guild),
                            thumbnail=ef.safe_pfp(user),
                        )
                        s[self.CLIENT.user] += 1
                        embed.add_field(name="You", value=s[user], inline=True)
                        embed.add_field(
                            name="Alfred", value=s[self.CLIENT.user], inline=True
                        )
                        await message.edit(embed=embed)
            except asyncio.TimeoutError:
                await message.clear_reactions()
                await message.edit(
                    embed=ef.cembed(
                        title="Timeout",
                        description="Sorry gtg, the reactions timed out",
                        color=nextcord.Color.red(),
                    )
                )

    @nextcord.slash_command(name="guess", description="guess the song game")
    async def guess(self, inter):
        await inter.response.defer()
        if not (voice := inter.user.voice):
            await inter.send("Join a vc and then try again")
            return
        songs = self.CLIENT.da[432801163126243328]
        if not inter.guild.voice_client:
            await voice.channel.connect()
        voice = inter.guild.voice_client
        voice.stop()
        song = choice(songs)
        info = self.player.info(song)
        voice.play(self.player.download(info))
        await inter.send("Guess this Song, you have 30 seconds to tell")
        try:
            message = await self.CLIENT.wait_for(
                "message",
                timeout=30,
                check=lambda m: m.author == inter.user and inter.channel == m.channel,
            )
            voice.stop()
            if len(message.content) < 3:
                await inter.send("Type more than 3 letters of the song")
                return
            if message.content.lower() in ["lyrics", "official", "video"]:
                await inter.send(
                    f"That's cheating, anyway that was {info.get('title')}"
                )
                return
            if message.content.lower() in info.get("title").lower():
                await inter.send(f"Correct that was {info.get('title')}")
            else:
                await inter.send(f"Incorrect, that was {info.get('title')}")
        except asyncio.TimeoutError:
            await inter.send(f"Time up, that was {info.get('title')}")


def setup(CLIENT, **i):
    CLIENT.add_cog(Games(CLIENT, **i))
