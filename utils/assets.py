from typing import List
import nextcord
from . import External_functions as ef

color = nextcord.ButtonStyle.blurple
BLUE_LINE = "https://www.wrberadio.com/home/attachment/blue-line-png-1"

class Confirm(nextcord.ui.View):
    def __init__(self, CLIENT, re = {8: 5160}):
        super().__init__()
        self.CLIENT = CLIENT
        self.value = None
        self.color = re[8]
        
    @nextcord.ui.button(label="Confirm",style=nextcord.ButtonStyle.green)
    async def confirm(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.edit_message(
            embed=ef.cembed(
                title="Done",
                description="Confirming",
                color = self.color,                
            )
        )
        self.value = True
        self.stop()
        return self.value
        
    @nextcord.ui.button(label="Cancel",style=color)
    async def cancel(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.edit_message(
            embed=ef.cembed(
                title="Done",
                description="Cancelling",
                color = self.color,                
            )
        )
        self.value = False
        self.stop()
        return self.value

async def confirm_button(ctx, message, CLIENT, re={8: 5160}):
    view = Confirm(CLIENT, re)
    await ctx.send(
        embed=ef.cembed(
            title="Confirmation",
            description=message,
            color=re[8]
        ),
        view=view
    )
    a = await view.wait()
    return a



class Pages(nextcord.ui.View):
    def __init__(self, ctx, embeds, restricted = False, start_from = 0):
        super().__init__()
        self.embeds = embeds
        self.ctx = ctx
        self.restricted = restricted
        self.current_embed = embeds[start_from]
        self.page = start_from
        self.user = getattr(ctx, 'user', getattr(ctx,'author',None))
        
    @nextcord.ui.button(style=color, emoji="◀️")
    async def previous(self, button, inter):
        if self.restricted:
            if not self.user == inter.user:
                return
        if self.page > 0:
            self.page-=1
        await inter.response.edit_message(embed=self.embeds[self.page])

    @nextcord.ui.button(style=color, emoji="▶️")
    async def next(self, button, inter):
        if self.restricted:
            if not self.user == inter.user:
                return
                
        if self.page < len(self.embeds)-1:
            self.page+=1
        await inter.response.edit_message(embed=self.embeds[self.page])

async def pa(ctx, embeds, restricted = False, start_from = 0, delete_after: int=None):
    if len(embeds)>1:
        await ctx.send(
            embed = embeds[start_from],
            view = Pages(ctx, embeds, restricted, start_from),
            delete_after=delete_after
        )
    else:
        await ctx.send(embed=embeds[0], delete_after=delete_after)

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



# https://top.gg/bot/811591623242154046/vote
# https://discordbotlist.com/bots/811591623242154046/upvote
# https://botsfordiscord.com/bot/811591623242154046/vote
# https://bots.discordlabs.org/bot/811591623242154046

# https://top.gg/servers/822445271019421746/vote
VOTE_MESSAGE = """
Thank you for voting and supporting us for the past year, We've listened to your suggestions, your needs and this helped us tune Alfred into a perfect bot ||Although I've seen some bugs around, fixing that <:Builder:991565723476447262>||. 
We've uploaded Alfred's source code to [github](https://github.com/alvinbengeorge/alfred-discord-bot) for openness.
You can find our bot in some of the Discord Bot Listing Sites
"""
VOTE_FIELD_HOLDER = {
    'Top.gg Alfred': "You can click this [link](https://top.gg/bot/811591623242154046/vote) to go to Alfred's Top.gg Page",
    'Discord Bot List': "You can click this [link](https://discordbotlist.com/bots/811591623242154046/upvote) to go to Alfred's Discord Bot List Page",
    'Bots For Discord': "Click this [link](https://botsfordiscord.com/bot/811591623242154046/vote) to go to Alfred's Bots For Discord Page",
    'DiscordBotLabs Page': "Go to this [link](https://bots.discordlabs.org/bot/811591623242154046) to vote for Alfred in DBL",
    'Wayne Enterprise Top.gg': "Vote for Alfred's Support Server in Top.gg using this [link](https://top.gg/servers/822445271019421746/vote)"
}
VOTE_FIELDS =[
    {'name': i, 'value': VOTE_FIELD_HOLDER[i], 'inline': False} for i in VOTE_FIELD_HOLDER
]
vote_embed = lambda CLIENT: ef.cembed(
    title = "Thanks for all your support 💖",
    description = VOTE_MESSAGE,
    color = CLIENT.re[8],
    author = CLIENT.user,
    fields = VOTE_FIELDS,
    thumbnail = CLIENT.user.avatar.url,
    image = "https://previews.123rf.com/images/enterline/enterline1806/enterline180601886/103633300-the-word-vote-concept-written-in-colorful-abstract-typography-vector-eps-10-available-.jpg",
    footer = {
        'text': 'Have a great day',
        'icon_url': 'https://st.depositphotos.com/1048238/2045/i/600/depositphotos_20457989-stock-photo-have-fun-concept.jpg'
    }
)

class JSONViewer(nextcord.ui.View):
    def __init__(self, di, CLIENT):
        super().__init__()
        self.di = di
        self.current_location = []
        self.CLIENT = CLIENT
        self.currently_selected = list(self.di)[0] if len(self.di) else None

    def smart_get(self, a, location):
        if isinstance(a, list) and isinstance(location, int):
            return a[location]
        if isinstance(a, list):
            return a[a.index(location)]
        return a.get(location, [])

    def temp_handler(self, temp):
        temp = temp if isinstance(temp, list) else list(temp.keys())
        s, e = temp.index(self.currently_selected)-5, temp.index(self.currently_selected)+5
        if e>len(temp):
            e = len(temp)
        if s<0:
            s = 0
        return temp[s:e]
            

    def display(self) -> nextcord.Embed:
        if not self.di:
            return ef.cembed(
                title="Empty",
                description="This location is empty",
                color=self.CLIENT.re[8],
                author=self.CLIENT.user
            )

        temp = self.di.copy()
        for i in self.current_location:
            temp = self.smart_get(temp, i)       

        if not temp:
            return ef.cembed(
                title="Empty",
                description="This location is empty",
                color=self.CLIENT.re[8],
                author=self.CLIENT.user
            )       

        if not isinstance(temp, (list, dict)):
            temp = [temp]

        temp = self.temp_handler(temp)

        description=""
        for i in temp:
            if i == self.currently_selected:
                description+=f"**{str(i)[:50]}**\n"
            else:
                description+=str(i)[:50]+"\n"

        return ef.cembed(
            title=f"JSONViewer",
            description=f"{description}\n\n{'/'.join([str(i)[:30] for i in self.current_location])}",
            color=self.CLIENT.re[8],
            author=self.CLIENT.user
        )


    @nextcord.ui.button(emoji="◀️", style=color)
    async def back(self, button, inter):
        if self.current_location:
            self.currently_selected = self.current_location.pop()
        await inter.edit(
            embed=self.display()
        )

    @nextcord.ui.button(emoji="▶️", style=color)
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
        await inter.edit(
            embed=self.display()
        )

    @nextcord.ui.button(emoji="🔼", style=color)
    async def up(self, button, inter):
        temp = self.di.copy()
        for i in self.current_location:
            temp = self.smart_get(temp, i)

        if not isinstance(temp, (list, dict)):
            temp = [temp]

        t = list(temp)
        if self.currently_selected in t:
            index = t.index(self.currently_selected)
            if index>0:
                self.currently_selected = t[index-1]

        await inter.edit(
            embed=self.display()
        )

    @nextcord.ui.button(emoji="🔽", style=color)
    async def down(self, button, inter):
        temp = self.di.copy()
        for i in self.current_location:
            temp = self.smart_get(temp, i)

        if not isinstance(temp, (list, dict)):
            temp = [temp]

        t = list(temp)
        if self.currently_selected in t:
            index = t.index(self.currently_selected)
            if index<len(t)-1:
                self.currently_selected = t[index+1]

        await inter.edit(
            embed=self.display()
        )

async def test_JSON(ctx, url):
    if ef.validate_url(url):
        try:
            json = await ef.get_async(url, kind="json")    
        except:
            await ctx.send(
                embed=ef.cembed(
                    title="Got an Unexpected error",
                    description=f"```py\n{ef.traceback.format_exc()}\n```",
                    color=ctx.bot.re[8],
                    author=ctx.author,
                    thumbnail=ctx.bot.user.avatar.url
                )
            )    
        await ctx.send(
            embed=ef.cembed(
                title="JSONViewer",
                description="Here's the beginning of test_JSON\nHave fun",
                color=ctx.bot.re[8]
            ),
            view=JSONViewer(json, ctx.bot)
        )
    else:
        await ctx.send(
            embed=ef.cembed(
                title="Invalid",
                description="Invalid URL, please type in proper URL to fetch from",
                color=ctx.bot.re[8],
                author=ctx.author
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
            min_values=1,
            max_values=1,
            options=options,
            custom_id="alfred_role_application"
        )

    async def callback(self, interaction: nextcord.Interaction):
        await interaction.response.defer()
        role = interaction.guild.get_role(int(self.values[0]))
        if role in interaction.user.roles:
            await interaction.user.remove_roles(
                role, 
                reason=f"Selection Role"
            )
            await interaction.send(
                content=f"Removed {role.mention}",
                ephemeral=True
            )
        else:
            await interaction.user.add_roles(role)
            await interaction.send(
                content=f"Added {role.mention}",
                ephemeral=True
            )

class RoleView(nextcord.ui.View):
    def __init__(self, roles):
        super().__init__(timeout=None)
        self.roles = roles
        self.add_item(Role(self.roles))