from typing import List, Union
from nextcord.ui import Button, button
from nextcord import Interaction
from nextcord.ext import commands
import nextcord
from . import External_functions as ef

color = nextcord.ButtonStyle.gray
BLUE_LINE = "https://www.wrberadio.com/home/attachment/blue-line-png-1"


class Confirm(nextcord.ui.View):
    def __init__(self, CLIENT: commands.Bot, re={8: 5160}):
        super().__init__()
        self.CLIENT = CLIENT
        self.value = None
        self.color = re[8]

    @button(label="Confirm", style=nextcord.ButtonStyle.green)
    async def confirm(self, button: Button, interaction: Interaction):
        await interaction.response.edit_message(
            embed=ef.cembed(
                title="Done",
                description="Confirming",
                color=self.color,
            )
        )
        self.value = True
        self.stop()
        return self.value

    @button(label="Cancel", style=color)
    async def cancel(self, button: Button, interaction: Interaction):
        await interaction.response.edit_message(
            embed=ef.cembed(
                title="Done",
                description="Cancelling",
                color=self.color,
            )
        )
        self.value = False
        self.stop()
        return self.value


async def confirm_button(ctx, message, CLIENT, re={8: 5160}):
    view = Confirm(CLIENT, re)
    await ctx.send(
        embed=ef.cembed(title="Confirmation", description=message, color=re[8]),
        view=view,
    )
    a = await view.wait()
    return a


class SelectionPages(nextcord.ui.Select):
    def __init__(
        self, CTX, EMBEDS: list, RESTRICTED: bool, page_change=None, *args, **kwargs
    ):
        self.CTX = CTX
        self.EMBEDS = EMBEDS[:25]
        self.RESTRICTED = RESTRICTED
        self.func = page_change
        options: list = []
        self.op: dict = {}
        for i in self.EMBEDS:
            if isinstance(i.title, str):
                self.op[i.title] = i
                options.append(
                    nextcord.SelectOption(
                        label=i.title, emoji="📜", description="Go to this page"
                    )
                )
            else:
                options.append(
                    nextcord.SelectOption(
                        label="Page Title Unavailable",
                        emoji="📜",
                        description="Go to this page",
                    )
                )
        super().__init__(
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: Interaction):
        user = getattr(self.CTX, "author", getattr(self.CTX, "user", None))
        if interaction.user.id == user.id:
            await interaction.edit(embed=self.op[self.values[0]])
            self.func(list(self.op.keys()).index(self.values[0]))


class Pages(nextcord.ui.View):
    def __init__(self, ctx, embeds, restricted=False, start_from=0, t="b"):
        super().__init__(timeout=None)
        if t in ["sb", "s"]:
            self.add_item(SelectionPages(ctx, embeds, restricted, self.page_change))
        if t in ["sb", "b"]:
            self.left, self.right = (
                Button(emoji="◀️", style=color),
                Button(emoji="▶️", style=color),
            )
            self.left.callback = self.previous
            self.right.callback = self.next
            self.add_item(self.left)
            self.add_item(self.right)
        self.embeds = embeds
        self.ctx = ctx
        self.restricted = restricted
        self.current_embed = embeds[start_from]
        self.page = start_from
        self.user = getattr(ctx, "user", getattr(ctx, "author", None))

    def page_change(self, page):
        self.page = page

    async def previous(self, inter):
        print(inter.data)
        if self.restricted:
            if not self.user == inter.user:
                return
        if self.page > 0:
            self.page -= 1
        await inter.response.edit_message(embed=self.embeds[self.page])

    async def next(self, inter):
        if self.restricted:
            if not self.user == inter.user:
                return

        if self.page < len(self.embeds) - 1:
            self.page += 1
        await inter.response.edit_message(embed=self.embeds[self.page])


async def pa(
    ctx: Union[commands.context.Context, Interaction],
    embeds,
    restricted=False,
    start_from=0,
    delete_after: int = None,
    t: str = "b",
):
    if len(embeds) > 1:
        return await ctx.send(
            embed=embeds[start_from],
            view=Pages(ctx, embeds, restricted, start_from, t),
            delete_after=delete_after,
        )
    else:
        return await ctx.send(embed=embeds[0], delete_after=delete_after)


class Emotes:
    def __init__(self, CLIENT):
        self.CLIENT = CLIENT
        self.animated_wrong = CLIENT.get_emoji(935914136620134410)
        self.red_arrow = CLIENT.get_emoji(945741947220402176)
        self.animated_correct = CLIENT.get_emoji(958424323415212102)
        self.join_vc = CLIENT.get_emoji(852810663603994624)
        self.check = CLIENT.get_emoji(967279216343277579)
        self.loading = CLIENT.get_emoji(948396323843997776)
        self.upvote = CLIENT.get_emoji(945509681256865845)
        self.boost = CLIENT.get_emoji(975323250546597888)
        self.yikes = CLIENT.get_emoji(852810342991527946)

    def get_emoji(self, e):
        return getattr(self, e, None)


Alfred_Mehspace = """```yml
author:
  icon_url: https://cdn.discordapp.com/avatars/432801163126243328/a_d58b7cca15fbd376f4779b5873a97c6a.gif?size=1024
  name: Dark-Knight
color: <bot-color>
description: "Hi, I'm a very simple free and open source bot. Check through `/help`\
  \ for more information, I would love to see  you work with me. You can check out\
  \ my github repository, all the links will given later on. I have quite tons of\
  \ features, and my main purpose is to give you a smile \U0001F604. Do it now \U0001F604\
  ...... just a bit more wide \U0001F604.... good. I will list out some of my features\
  \ below"
fields:
- inline: false
  name: __FEATURES__
  value: "\u27E7\u27EB I'm free and open to use, you can even see my source by typing\
    \ `'src`\n\n\u27E7\u27EB `Trustable` \u2192 Totally trustable, if you have a query\
    \ about how something works, you can look into the source code or ask us, we even\
    \ have our Privacy Policy\n\n\u27E7\u27EB `Secure` \u2192 All of the features are\
    \ double checked\n\n\u27E7\u27EB `FunAPI` \u2192 Alfred has some fun stuff that\
    \ you can play with, check it out, dont miss it\n\n\u27E7\u27EB `Speed` \u2192 I\
    \ try to keep myself as fast as possible, well `it comes to us all`\n\n\u27E7\u27EB\
    \ `Support`  \u2192 You can walk into Wayne Enterprises and ask the mods or my\
    \ boss for help\n\n\u27E7\u27EB `FOSS` \u2192 Not gonna brag, but Stallman likes\
    \ me"
- inline: false
  name: __SETTING YOUR MEHSPACE__
  value: First up you gotta use the `msetup` command, or if you're a coder and if
    you know `yaml syntax` you can use it that way using `'yml_embed mehspace`. If
    you want to learn how renders and all the key and value structure, you can do
    it by replying to a message with an embed and typing `'embedinfo`. If you're using
    `msetup` it is quite self explanatory, type title or description, and then you
    type the text, I will delete that message and guide you through it
footer:
  icon_url: <server-icon>
  text: Join the Support Server for more info and if you want to contribute, head
    over to alfred's official website
image: https://github.com/AlfredDiscordBot/alfred-discord-bot/blob/default/Bat.jpg?raw=True
title: Hi I'm Alfred
button:
  -  label: "Invite Alfred"
     emoji: "<:Alfredmax:969783243048116234>"
     url: "https://discord.com/oauth2/authorize?client_id=811591623242154046&permissions=8&scope=bot%20applications.commands"
  -  label: "Support Server"
     emoji: "<a:wayne:993742860568506408>"    
     url: "https://discord.com/invite/XESZGvjDaT"
```
"""

# https://top.gg/bot/811591623242154046/vote
# https://discordbotlist.com/bots/811591623242154046/upvote
# https://botsfordiscord.com/bot/811591623242154046/vote
# https://bots.discordlabs.org/bot/811591623242154046

# https://top.gg/servers/822445271019421746/vote
VOTE_MESSAGE = """
Thank you for voting and supporting us for the past year, We've listened to your suggestions, your needs and this helped us tune Alfred into a perfect bot ||Although I've seen some bugs around, fixing that ⚒️||. 
We've uploaded Alfred's source code to [github](https://github.com/alvinbengeorge/alfred-discord-bot) for openness.
You can find our bot in some of the Discord Bot Listing Sites
"""
VOTE_FIELD_HOLDER = {
    "Top.gg Alfred": "You can click this [link](https://top.gg/bot/811591623242154046/vote) to go to Alfred's Top.gg Page",
    "Discord Bot List": "You can click this [link](https://discordbotlist.com/bots/811591623242154046/upvote) to go to Alfred's Discord Bot List Page",
    "Bots For Discord": "Click this [link](https://botsfordiscord.com/bot/811591623242154046/vote) to go to Alfred's Bots For Discord Page",
    "DiscordBotLabs Page": "Go to this [link](https://bots.discordlabs.org/bot/811591623242154046) to vote for Alfred in DBL",
    "Wayne Enterprise Top.gg": "Vote for Alfred's Support Server in Top.gg using this [link](https://top.gg/servers/822445271019421746/vote)",
}
VOTE_FIELDS = [
    {"name": i, "value": VOTE_FIELD_HOLDER[i], "inline": False}
    for i in VOTE_FIELD_HOLDER
]
vote_embed = lambda CLIENT: ef.cembed(
    title="Thanks for all your support 💖",
    description=VOTE_MESSAGE,
    color=CLIENT.re[8],
    author=CLIENT.user,
    fields=VOTE_FIELDS,
    thumbnail=CLIENT.user.avatar,
    image="https://previews.123rf.com/images/enterline/enterline1806/enterline180601886/103633300-the-word-vote-concept-written-in-colorful-abstract-typography-vector-eps-10-available-.jpg",
    footer={
        "text": "Have a great day",
        "icon_url": "https://st.depositphotos.com/1048238/2045/i/600/depositphotos_20457989-stock-photo-have-fun-concept.jpg",
    },
)


class JSONViewer(nextcord.ui.View):
    def __init__(self, di, main: Union[Interaction, commands.context.Context]):
        super().__init__()
        self.USER = getattr(main, "author", getattr(main, "user", None))
        self.di = di
        self.current_location = []
        self.CLIENT = getattr(main, "client", getattr(main, "bot", None))
        self.currently_selected = list(self.di)[0] if len(self.di) else None

    def smart_get(self, a, location):
        if isinstance(a, list) and isinstance(location, int):
            return a[location]
        if isinstance(a, list):
            return a[a.index(location)]
        return a.get(location, [])

    def temp_handler(self, temp):
        temp = temp if isinstance(temp, list) else list(temp.keys())
        s, e = (
            temp.index(self.currently_selected) - 5,
            temp.index(self.currently_selected) + 5,
        )
        if e > len(temp):
            e = len(temp)
        if s < 0:
            s = 0
        return temp[s:e]

    def display(self) -> nextcord.Embed:
        if not self.di:
            return ef.cembed(
                title="Empty",
                description="This location is empty",
                color=self.CLIENT.re[8],
                author=self.CLIENT.user,
            )

        temp = self.di.copy()
        for i in self.current_location:
            temp = self.smart_get(temp, i)

        if not temp:
            return ef.cembed(
                title="Empty",
                description="This location is empty",
                color=self.CLIENT.re[8],
                author=self.CLIENT.user,
            )

        if not isinstance(temp, (list, dict)):
            temp = [temp]

        temp = self.temp_handler(temp)

        description = ""
        for i in temp:
            if i == self.currently_selected:
                description += f"**{str(i)[:50]}**\n"
            else:
                description += str(i)[:50] + "\n"

        return ef.cembed(
            title=f"JSONViewer",
            description=f"{description}\n\n{'/'.join([str(i)[:30] for i in self.current_location])}",
            color=self.CLIENT.re[8],
            author=self.CLIENT.user,
        )

    @button(emoji="◀️", style=color)
    async def back(self, button, inter):
        if self.current_location:
            self.currently_selected = self.current_location.pop()
        await inter.edit(embed=self.display())

    @button(emoji="▶️", style=color)
    async def forward(self, button, inter):
        if self.currently_selected:
            self.current_location.append(self.currently_selected)
            temp = self.di.copy()
            for i in self.current_location:
                temp = self.smart_get(temp, i)
            if not isinstance(temp, (list, dict)):
                temp = [temp]
            if isinstance(temp, dict):
                self.currently_selected = list(temp)[0]
            else:
                self.currently_selected = temp[0]
        await inter.edit(embed=self.display())

    @button(emoji="🔼", style=color)
    async def up(self, button, inter):
        temp = self.di.copy()
        for i in self.current_location:
            temp = self.smart_get(temp, i)

        if not isinstance(temp, (list, dict)):
            temp = [temp]

        t = list(temp)
        if self.currently_selected in t:
            index = t.index(self.currently_selected)
            if index > 0:
                self.currently_selected = t[index - 1]

        await inter.edit(embed=self.display())

    @button(emoji="🔽", style=color)
    async def down(self, button, inter):
        temp = self.di.copy()
        for i in self.current_location:
            temp = self.smart_get(temp, i)

        if not isinstance(temp, (list, dict)):
            temp = [temp]

        t = list(temp)
        if self.currently_selected in t:
            index = t.index(self.currently_selected)
            if index < len(t) - 1:
                self.currently_selected = t[index + 1]

        await inter.edit(embed=self.display())


async def test_JSON(ctx, url):
    user = getattr(ctx, "author", getattr(ctx, "user", None))
    client = getattr(ctx, "bot", getattr(ctx, "client", None))
    color = ctx.client.re[8] if isinstance(ctx, Interaction) else ctx.bot.re[8]
    if ef.validate_url(url):
        try:
            json = await ef.get_async(url, kind="json")
        except:
            await ctx.send(
                embed=ef.cembed(
                    title="Got an Unexpected error",
                    description=f"```py\n{ef.traceback.format_exc()}\n```",
                    color=color,
                    author=user,
                    thumbnail=client.user.avatar,
                )
            )
        await ctx.send(
            embed=ef.cembed(
                title="JSONViewer",
                description="Here's the beginning of test_JSON\nHave fun",
                color=color,
                author=user,
                thumbnail=client.user.avatar,
            ),
            view=JSONViewer(json, ctx),
        )
    else:
        await ctx.send(
            embed=ef.cembed(
                title="Invalid",
                description="Invalid URL, please type in proper URL to fetch from",
                color=color,
                author=user,
            )
        )


class Role(nextcord.ui.Select):
    def __init__(self, roles: List[nextcord.Role]):
        self.roles = roles
        options = [
            nextcord.SelectOption(label=i.name, emoji="▶️", value=i.id) for i in roles
        ]
        super().__init__(
            placeholder="Select your Role",
            min_values=0,
            max_values=len(tuple(self.roles)),
            options=options,
            custom_id="alfred_role_application",
        )

    async def callback(self, interaction: Interaction):
        await interaction.response.defer()
        roles = [interaction.guild.get_role(int(i)) for i in self.values]
        has, has_not = [], []
        for i in roles:
            if i in interaction.user.roles:
                has.append(i)
            else:
                has_not.append(i)
        await interaction.user.remove_roles(*has, reason="Selection Role")
        await interaction.user.add_roles(*has_not, reason="Selection Roles")
        content = ef.dict2str(
            {
                "Added": "".join([i.mention for i in has_not]),
                "Removed": "".join([i.mention for i in has]),
            }
        )
        await interaction.send(content=content, ephemeral=True)


class RoleView(nextcord.ui.View):
    def __init__(self, roles):
        super().__init__(timeout=None)
        self.roles = roles
        self.add_item(Role(self.roles))


class Msetup_DropDownSelect(nextcord.ui.Select):
    def __init__(self, func, user: nextcord.Member):
        self.user = user
        self.func = func
        options = [
            nextcord.SelectOption(label=i.upper(), emoji="⏺️", description=f"Set {i}")
            for i in ef.m_options
        ]
        super().__init__(
            placeholder="Select Embed Feature",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: Interaction):
        if interaction.user.id != self.user.id:
            await interaction.response.send_message("Not your Embed 🔪", ephemeral=True)
            return
        await self.func(self.values[0], interaction)


class Msetup_DropDownView(nextcord.ui.View):
    def __init__(self, func, user, *more_items):
        super().__init__(timeout=600)
        self.add_item(Msetup_DropDownSelect(func=func, user=user))
        for i in more_items:
            self.add_item(i)


class DEVOPVIEW(nextcord.ui.View):
    def __init__(self, client: ef.commands.Bot, functions):
        self.functions = functions
        self.client = client
        super().__init__(timeout=None)
        invite_link = "https://discord.com/oauth2/authorize?client_id=811591623242154046&permissions=8&scope=bot%20applications.commands"
        stats, save, ex, invite, report = (
            Button(style=color, label="Stats", emoji="⭕"),
            Button(style=color, label="Save", emoji="💾"),
            Button(style=color, label="Exit", emoji="❌"),
            Button(style=color, label="Invite", emoji="🔗", url=invite_link),
            Button(style=color, label="Report", emoji="📜"),
        )
        stats.callback = functions["stats"]
        save.callback = functions["save"]
        ex.callback = functions["exit"]
        report.callback = functions["report"]
        for i in (stats, save, ex, invite, report):
            self.add_item(i)
