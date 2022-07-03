import asyncio
import assets
import nextcord
import External_functions as ef
from threading import Thread
from nextcord.ext import commands
from subprocess import getoutput

#Use nextcord.slash_command()

def requirements():
    return []

class Pylint(commands.Cog):
    def __init__(self, client):
        self.client = client  
        self.sample_lint = LintAction(self.client.re[8])
        self.lint_in_session = False
        
    @nextcord.slash_command(name="pylint", description="Check Pylint of a py file", guild_ids = [822445271019421746])
    async def lin(self, inter, file):
        if self.lint_in_session:
            await inter.send(
                embed=ef.cembed(
                    title="Busy",
                    description="A Lint is in session, please wait till the Lint scan is done",
                    color=self.client.re[8]
                )
            )
            return
        self.lint_in_session = True
        await inter.response.defer()
        session = LintAction(self.client.re[8])
        session.lint(file)
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
    '''
    Carries out Lint in a safe non-interrupting env
    '''
    def __init__(self, color):
        self.locations = getoutput(
            "ls *.py cogs/*.py src/*py utils/*.py"
        ).split("\n") + ['*']
        self.output = None
        self.color = color
        

    def lint(self, file):
        '''
        Process Lint
        '''
        if file == "*":
            file = "cogs/*.py src/*.py *.py utils/*.py"
        elif not file in self.locations:
            self.output = "Not in Range of files"
            return self.output

        def start_process(file):
            self.output = getoutput(f"pylint {file}").strip()
            print("Lint Completed for", file)
            return self.output

        t = Thread(target=start_process, args = (file,))
        t.start()

    def split_output(self):
        splits = self.output.split("\n")
        descriptions = ['']
        
        for line in splits:
            descriptions[-1]+=line+"\n"
            if len(descriptions[-1].split("\n")) == 30:
                descriptions.append('')

        embeds = []
        count = 0
        for description in descriptions:
            count+=1
            field_text = "\n".join([
                i for i in descriptions[-1].split("\n") if i.startswith("Your")
            ])
            if not field_text:
                field_text = "Should mostly be an error"
                
            embeds.append(
                ef.cembed(
                    title = "PyLint Completed",
                    description = f"```py\n{description}\n```",
                    color = self.color,
                    footer = f"Have Fun Coding | {count} of {len(descriptions)}",
                    fields = [
                        {
                            'name': 'Rating',
                            'value': field_text
                        }
                    ]
                )
            )
        return embeds
                        
        


def setup(client,**i):
    client.add_cog(Pylint(client,**i))
