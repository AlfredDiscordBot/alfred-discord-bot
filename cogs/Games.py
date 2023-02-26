import nextcord
import requests
import utils.External_functions as ef
import emoji
import asyncio

from nextcord.ext import commands, tasks
from nextcord.ui import Button, button, Select, View
from random import choice, shuffle
from typing import List
from utils.assets import color

# Use nextcord.slash_command()


def requirements():
    return ["FFMPEG_OPTIONS"]


class HangMan:
    def __init__(self, difficultyLevel: int = 2):
        self.words = []
        self.dL = difficultyLevel
        self.load_words()
        self.word = choice(self.words)
        self.display = ["_" for _ in self.word]
        self.chances = 6

    def load_words(self):
        with open("words") as f:
            self.words = list(
                filter(
                    lambda a: all(
                        [
                            len(a) <= self.dL + 4,
                            len(a) >= self.dL - 4,
                            "x" not in a.lower(),
                        ]
                    ),
                    f.read().split("\n"),
                )
            )

    def click(self, letter: str):
        letter = letter.lower()
        for i in range(len(self.word)):
            if self.word[i] == letter:
                self.display[i] = letter
        if letter not in self.word:
            self.chances -= 1
            return False
        return True

    def is_over(self):
        return self.chances == 0 or "_" not in self.display

    def __str__(self):
        return "Hangman: `" + "".join(self.display) + "`"


class HangManButton(Button):
    def __init__(self, func, label: str = None, style=color):
        super().__init__(label=label, style=style)
        self.callback = self.buttonCallback
        self.func = func
        self.label = label

    async def buttonCallback(self, interaction):
        await self.func(interaction, self.label, self)


class HangManView(View):
    def __init__(self, CLIENT: commands.Bot):
        super().__init__()
        self.game = HangMan()
        self.CLIENT = CLIENT
        self.letters = [
            HangManButton(func=self.buttonCallback, label=letter, style=color)
            for letter in "ABCDEFGHIJKLMNOPQRSTUVWYZ"
        ]
        self.letters = [self.letters[i : i + 5] for i in range(0, len(self.letters), 5)]
        for i in range(len(self.letters)):
            for j in range(len(self.letters[i])):
                self.letters[i][j].row = i
                self.add_item(self.letters[i][j])

    async def buttonCallback(self, inter, label: str, button: Button):
        if self.game.is_over():
            await inter.edit(
                embed=ef.cembed(
                    title="Game Over",
                    description="You won!" if self.game.chances > 0 else "You lost!",
                    fields={
                        "The word was": self.game.word,
                    },
                    color=self.CLIENT.color(inter.guild),
                    thumbnail=self.CLIENT.user.avatar,
                ),
                view=None,
            )
            return
        output = self.game.click(label)
        if output:
            button.style = nextcord.ButtonStyle.green
        else:
            button.style = nextcord.ButtonStyle.red
        await inter.edit(
            embed=ef.cembed(
                title="Hangman",
                description=str(self.game),
                fields={
                    "Chances": self.game.chances,
                },
                color=self.CLIENT.color(inter.guild),
                thumbnail=self.CLIENT.user.avatar,
                author=inter.user,
            ),
            view=self,
        )


class OrderButton(Button):
    def __init__(self, label: str, callback_func):
        self.callable = callback_func
        super().__init__(style=color, row=0, label=label)

    async def callback(self, interaction: nextcord.Interaction):
        await self.callable(interaction, self.label)


class OrderView(View):
    def __init__(self, words: List[str], CLIENT: commands.Bot):
        super().__init__(timeout=None)
        self.words = words[:5]
        self.user_words = []
        self.display = self.words.copy()
        shuffle(self.display)
        self.CLIENT = CLIENT
        for word in self.display:
            self.add_item(OrderButton(word, self.called))

    async def edit_message(self, inter: nextcord.Interaction):
        await inter.edit(
            embed=ef.cembed(
                title="Put the words in order",
                fields={"Words": self.user_words},
                color=self.CLIENT.color(inter.guild),
                author=inter.user,
            )
        )

    async def called(self, interaction: nextcord.Interaction, label: str):
        if len(self.user_words) + 1 <= 5 and label not in self.user_words:
            self.user_words.append(label)
            await self.edit_message(interaction)

    @button(label="BackSpace", emoji="🔙", row=1)
    async def backspace(self, button: Button, inter: nextcord.Interaction):
        if self.user_words.pop() if len(self.user_words) > 0 else False:
            await self.edit_message(inter=inter)

    @button(label="Confirm", emoji="✅", row=1)
    async def confirm(self, button: Button, inter: nextcord.Interaction):
        if self.words == self.user_words:
            result = "Correct answer, good job"
        else:
            result = "Wrong answer, it's fine, try again"
        await inter.edit(
            embed=ef.cembed(
                title="Confirmed",
                fields={"Words": self.user_words, "Correct Order": self.words},
                footer={"text": result, "icon_url": self.CLIENT.user.avatar},
                color=self.CLIENT.color(inter.guild),
                author=inter.user,
            )
        )
        self.clear_items()
        self.stop()


class Games(commands.Cog, description="Very Simple Games"):
    def __init__(self, CLIENT: commands.Bot, FFMPEG_OPTIONS):
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
        with open("words") as f:
            self.words = f.read().split("\n")

    @nextcord.slash_command(name="game")
    async def game(self, inter):
        print(inter.user)

    @game.subcommand(name="rps", description="play some rock paper scissors against me")
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

    @game.subcommand(name="order", description="Follow the order of words")
    async def order(self, inter: nextcord.Interaction):
        shuffle(self.words)
        words = self.words[:5]
        message = await inter.response.send_message(
            embed=ef.cembed(
                title="Welcome to The game of `ORDER`",
                description="You should remember the order of the words correctly",
                color=self.CLIENT.color(inter.guild),
                author=inter.user,
                footer={
                    "text": "This message will be edited in 5 seconds",
                    "icon_url": self.CLIENT.user.avatar,
                },
                fields={"Remember these words": words},
                thumbnail=self.CLIENT.user.avatar,
            )
        )
        await asyncio.sleep(5)
        await message.edit(
            embed=ef.cembed(
                title="Put the words in order",
                fields={"Words": "Empty"},
                color=self.CLIENT.color(inter.guild),
                author=inter.user,
                thumbnail=self.CLIENT.user.avatar,
            ),
            view=OrderView(words=words, CLIENT=self.CLIENT),
        )

    @game.subcommand(name="hangman", description="Play some hangman")
    async def hangman(self, inter: nextcord.Interaction):
        await inter.response.defer()
        embed = ef.cembed(
            title="`Hangman`",
            description="You will be playing hangman against me, please try not to delay it as discord hates me for waiting",
            color=self.CLIENT.color(inter.guild),
            thumbnail=self.CLIENT.user.avatar,
            author=inter.user,
        )
        await inter.send(embed=embed, view=HangManView(CLIENT=self.CLIENT))


def setup(CLIENT, **i):
    CLIENT.add_cog(Games(CLIENT, **i))
