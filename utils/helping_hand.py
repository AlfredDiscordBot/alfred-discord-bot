from typing import Union
import nextcord

from nextcord.ext import commands
from .External_functions import (
    cembed,
    defa,
    dict2str,
    line_strip,
    list2str,
    slash_and_sub,
)
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

FIELDS_MESSAGE = {
    "__DELETING MUSIC COG__": "As Youtube mentioned not to use their source for creating bots, even though it was totally legal if the service was free, `Discord` is cancelling verification for some bots which has this feature. Removing this is both a good news and a bad news\n\n```\n"
    + list2str(
        [
            "The Good News is that Alfred is compatible completely in railway, and many other hosting platforms, known and unknown\n",
            "The Bad News is that people love Alfred for it's Music and we're disappointing maybe 100s of people, and I'm truly sorry for this, It has to be done to maintain the verification status of Alfred",
        ]
    )
    + "\n```",
    "__LYRICS COMMAND__": "Lyrics command is going to be moved to `/api` subcommands instead of `/music lyrics` Because of the update above",
    "__NEW POLL GRAPH__": "There's a new poll graph designed by `yashppawar`, which is inspired from xkcd",
    "__SOURCE__": dict2str(
        {
            "Source Code   ": "[🔗](https://github.com/AlfredDiscordBot/alfred-discord-bot)",
            "Organisation  ": "[🔗](https://github.com/AlfredDiscordBot)",
            "Website       ": "[🔗](https://alfreddiscordbot.github.io/)",
            "Support Server": "[🔗](https://discord.gg/XESZGvjDaT)",
        }
    ),
}


MESSAGE = lambda client, guild: cembed(
    title="Message from the developers",
    description=f"Thank you for using {client.user.name}. {client.user.name} has given me new experiences and to here your opinion and suggestions, it's great and I love listening to the suggestions you give us\n\nWith 💖 -> Developer",
    color=client.color(guild),
    footer={
        "text": "This bot was made for:\n- Being Free and Open Source\n- Educational purpose",
        "icon_url": client.user.avatar,
    },
    fields=FIELDS_MESSAGE,
    author=client.user,
    thumbnail=client.user.avatar,
)


def help_him(
    client: commands.Bot,
    main: Union[nextcord.Interaction, commands.context.Context] = None,
    *args,
    **kwargs,
):
    return AutoHelpGen(
        client, main, extra_embeds=[MESSAGE(client, getattr(main, "guild", None))]
    ).embeds()


class AutoHelpGen:
    """
    Must only be used after or on_ready
    Automatically Creates Embeds based on Cogs
    """

    def __init__(
        self,
        CLIENT: commands.Bot,
        main: Union[nextcord.Interaction, commands.context.Context] = None,
        extra_embeds: List[nextcord.Embed] = [],
    ):
        self.CLIENT = CLIENT
        self.USER = (
            CLIENT.user
            if not main
            else getattr(main, "user", getattr(main, "author", None))
        )
        self.GUILD = getattr(main, "guild", None)
        self.COLOR = self.CLIENT.color(self.GUILD)
        self.IGNORE = ["DataCleanup", "Developer", "Sealfred", "Roles"]
        self.COGS = self.generate_cogs()
        self.EMBEDS = [self.first_page(), *extra_embeds, *self.generate_embeds_cog()]

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
                    author=self.USER,
                    thumbnail=self.CLIENT.user.avatar,
                    footer={
                        "text": "This bot was made for:\n- Being Free and Open Source\n- Educational purpose",
                        "icon_url": self.CLIENT.user.avatar,
                    },
                    fields={
                        "APPLICATION COMMANDS": self.fetch_application_commands(cog),
                        "PREFIX COMMANDS": self.fetch_prefix_commands(cog),
                    },
                )
            )
        return embeds

    def embeds(self):
        return self.EMBEDS

    def first_page(self):
        FEATURES = line_strip(
            """
        ```yml
        - EMBED
        - CODE
        - FUN
        - API
        ```
        """
        )
        return cembed(
            title=self.CLIENT.user.name,
            author=self.USER,
            thumbnail=self.CLIENT.user.avatar,
            footer={
                "text": "Verified By Discord",
                "icon_url": "https://emoji.discord.st/emojis/acf3edc7-d547-4be7-a006-51719c3b9080.png",
            },
            color=self.COLOR,
            image="https://github.com/AlfredDiscordBot/alfred-discord-bot/blob/default/Bat.jpg?raw=True",
            description=f"Default Prefix is `'`\n{self.CLIENT.user.name} is a free and open source software with MIT License published in Github, which is currently in {len(self.CLIENT.guilds)} servers",
            fields=[{"name": "__MAIN FEATURES__", "value": FEATURES}],
        )

    def fetch_application_commands(self, cog):
        application_commands = slash_and_sub(self.CLIENT, cog)
        return "```diff\n+ " + "\n+ ".join(application_commands) + "\n```"

    def fetch_prefix_commands(self, cog):
        prefix_commands = []
        prefix = self.CLIENT.prefix_dict.get(getattr(self.GUILD, "id", None), "'")
        for i in cog.get_commands():
            prefix_commands.append(
                f"{prefix}{i.name} {i.signature} {('-> '+i.description) if i.description else ''}"
            )
        return "```diff\n+ " + "\n+ ".join(prefix_commands) + "\n```"
