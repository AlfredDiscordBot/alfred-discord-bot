import asyncio
import utils.assets as assets
import nextcord
import utils.External_functions as ef
from threading import Thread
from nextcord.ext import commands
from subprocess import getoutput

# Use nextcord.slash_command()


def requirements():
    return ["DEV_CHANNEL"]


class Pylint(
    commands.Cog,
    description="This is where an important cog in alfred where you can test out Alfred's Code Scores",
):
    TRUSTED_SERVERS = [
        822445271019421746,
        942303350182006815,
        869237028028579860,
        912569937116147772,
        930002874522562580,
    ]
    PROCESS_SELECTION = ef.defa(
        choices=["lint", "flake8"], required=False, default="lint"
    )

    def __init__(self, CLIENT: commands.Bot, DEV_CHANNEL):
        self.CLIENT = CLIENT
        self.DEV_CHANNEL = DEV_CHANNEL
        self.sample_lint = LintAction(5160)
        self.lint_in_session = False

    @nextcord.slash_command(
        name="pylint",
        description="Check Pylint of a py file",
        guild_ids=TRUSTED_SERVERS,
    )
    async def lin(self, inter, file, type=PROCESS_SELECTION):
        if self.lint_in_session:
            await inter.send(
                embed=ef.cembed(
                    title="Busy",
                    description="A Lint is in session, please wait till the Lint scan is done",
                    color=self.CLIENT.color(inter.guild),
                )
            )
            return
        self.lint_in_session = True
        await inter.response.defer()
        await self.CLIENT.get_channel(self.DEV_CHANNEL).send(
            embed=ef.cembed(
                title="Executed Lint Commands",
                description=f"This was done in {inter.guild} by {inter.user.mention}",
                color=self.CLIENT.color(inter.guild),
                thumbnail=self.CLIENT.user.avatar,
                author=inter.user,
            )
        )
        session = LintAction(self.CLIENT.color(inter.guild))
        session.lint(file, type)
        while True:
            await asyncio.sleep(3)
            if session.output:
                break
        embeds = session.split_output()
        self.lint_in_session = False
        await assets.pa(inter, embeds)

    @lin.on_autocomplete("file")
    async def autocomplete_lin(self, inter, file):
        await inter.response.send_autocomplete(
            [i for i in self.sample_lint.locations if file in i][:25]
        )


class LintAction:
    """
    Carries out Lint in a safe non-interrupting env
    """

    def __init__(self, color):
        self.locations = getoutput("ls *.py cogs/*.py utils/*.py").split("\n") + ["*"]
        self.output = None
        self.color = color
        self.type = "lint"

    def lint(self, file, type="lint"):
        """
        Process Lint and Flake8
        """
        self.type = type
        if file == "*":
            file = "cogs/*.py *.py utils/*.py"
        elif not file in self.locations:
            self.output = "Not in Range of files"
            return self.output

        def linting(file):
            self.output = getoutput(f"pylint {file}").strip()
            print("Lint Completed for", file)
            return self.output

        def flake(file):
            self.output = getoutput(f"flake8 {file} --exit-zero").strip()
            print("Flake8 complete for", file)
            return self.output

        if type == "flake8":
            func = flake
        else:
            func = linting

        t = Thread(target=func, args=(file,))
        t.start()

    def split_output(self):
        """
        Divide the output into embeds
        """
        splits = self.output.split("\n")
        descriptions = [""]

        for line in splits:
            descriptions[-1] += line + "\n"
            if len(descriptions[-1].split("\n")) == 20:
                descriptions.append("")

        embeds = []
        count = 0
        for description in descriptions:
            count += 1
            field_text = "\n".join(
                [i for i in descriptions[-1].split("\n") if i.startswith("Your")]
            )
            if not field_text:
                field_text = f"{len(splits)} Lines"

            embeds.append(
                ef.cembed(
                    title="PyLint Completed",
                    description=f"```py\n{description}\n```",
                    color=self.color,
                    footer=f"Have Fun Coding | {count} of {len(descriptions)}",
                    fields=[{"name": "Rating", "value": field_text}],
                )
            )
        return embeds


def setup(CLIENT, **i):
    CLIENT.add_cog(Pylint(CLIENT, **i))
