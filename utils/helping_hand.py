import nextcord

from nextcord.ext import commands
from .External_functions import cembed, defa, dict2fields
from .assets import *


effec = f"""
```yml
'effects <effect> <member> if member is none the users pfp will be modified 
The list of effects is 
- cartoonify 
- watercolor 
- canny 
- pencil 
- econify 
- negative 
- pen 
- candy 
- composition 
- feathers 
- muse 
- mosaic 
- night 
- scream 
- wave 
- udnie 
```
"""


def effects_helper():
    return defa(
        choices=[
            "cartoonify",
            "watercolor",
            "canny",
            "pencil",
            "econify",
            "negative",
            "pen",
            "candy",
            "composition",
            "feathers",
            "muse",
            "mosaic",
            "night",
            "scream",
            "wave",
            "udnie",
        ],
        required=True,
    )

neofetch = """
  *(&@&&%%##%%&%                                                .%&%###%%&&&%/, 
       ..,*/*/(%%                                              *%#(**/*,..      
          ..,*//(#%%.                /,*/,*.                /%%#(/*,..          
             ..,//**/#%%%&&%#(((((%&&&####%&&&#(((((#%&&%%#(***//,..            
               ......,,,**/(##%#**/((/#%%%//((/*/#%#(//**,,......               
                             ....,****/**/****,,....                            
                                 ....,*,.,,,....                                
                                     .......                                    
                                                                                
"""

SAMPLE_YAML = """
```yml
fields:
    topic1: "Type some stuff here"
    topic2: "Type some stuff here"
    topic3: "Type some stuff here"
```
"""

FIELDS_MESSAGE = {
    '__YML_EMBED IMPROVEMENTS__':'There are tons of updates to yml_embed\nFirstly, the `field` attribute accepts dictionary, if you didnt get it, you can do this now\n'+SAMPLE_YAML+"\nThis has issues too, such as you can't repeat a field head value",
    '__MSETUP IMPROVEMENTS__': 'Msetup now has a selection, as people are getting confused at first, decided to do that'
}


MESSAGE = lambda client: cembed(
    title="Message from the developers",
    description=f"Thank you for using {client.user.name}. {client.user.name} has given me new experiences and to here your opinion and suggestions, it's great and I love listening to the suggestions you give us\n\nWith 💖 -> Developer",
    color=client.re[8],
    footer={
        'text': 'This bot was made for:\n- Being Free and Open Source\n- Educational purpose',
        'icon_url': client.user.avatar
    },
    fields=FIELDS_MESSAGE,
    author=client.user and not print(client.user),
    thumbnail=client.user.avatar
)

def help_him(client: commands.Bot):
    return AutoHelpGen(client, user=client.get_user(client.owner_id), extra_embeds=[MESSAGE(client)]).embeds()

class AutoHelpGen:
    '''
    Must only be used after or on_ready
    Automatically Creates Embeds based on Cogs
    '''
    def __init__(self, CLIENT: commands.Bot, user: nextcord.Member = None, extra_embeds: List[nextcord.Embed] = []):
        self.CLIENT = CLIENT
        self.USER = user if user else CLIENT.user
        self.COLOR = CLIENT.re[8]
        self.IGNORE = [
            "DataCleanup",
            "Developer",
            "SeaAlfred"
        ]
        self.COGS = self.generate_cogs()
        self.EMBEDS = [
            self.first_page(),
            *extra_embeds,
            *self.generate_embeds_cog()
        ]

    def generate_cogs(self):
        cogs = []
        for i, j in self.CLIENT.cogs.items():
            if i not in self.IGNORE:
                cogs.append((i, j))
        return cogs

    def generate_embeds_cog(self):
        embeds = []
        for name, cog in self.COGS:
            embeds.append(
                ef.cembed(
                    title=name,
                    description=cog.description,
                    color=self.COLOR,
                    author=self.CLIENT.user,
                    thumbnail=self.CLIENT.user.avatar,
                    footer={
                        'text': 'This bot was made for:\n- Being Free and Open Source\n- Educational purpose',
                        'icon_url': self.CLIENT.user.avatar
                    },
                    fields={
                        'Slash Commands': self.fetch_application_commands(cog),
                        'Prefix Commands': self.fetch_prefix_commands(cog)
                    }
                )
            )
        return embeds

    def embeds(self):
        return self.EMBEDS

    def first_page(self):
        return cembed(
            title=self.CLIENT.user.name,
            author=self.CLIENT.user,
            thumbnail=self.CLIENT.user.avatar,
            footer="✅Verified by Discord"
        )
    
    def fetch_application_commands(self, cog):
        application_commands = []
        for i in cog.application_commands:
            main = f"/{i.name} "
            application_commands.append(main)
        return "```diff\n+ "+"\n+ ".join(application_commands)+"\n```"

    def fetch_prefix_commands(self, cog):
        prefix_commands = []
        for i in cog.get_commands():
            prefix_commands.append(
                f"\'{i.name} {i.signature} -> {i.description}"
            )
        return "```diff\n+ "+"\n+ ".join(prefix_commands)+"\n```"
