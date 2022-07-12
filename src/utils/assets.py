import nextcord
import External_functions as ef

color = nextcord.ButtonStyle.blurple


class Confirm(nextcord.ui.View):
    def __init__(self, client, re={8: 5160}):
        super().__init__()
        self.client = client
        self.value = None
        self.color = re[8]

    @nextcord.ui.button(label="Confirm", style=nextcord.ButtonStyle.green)
    async def confirm(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
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

    @nextcord.ui.button(label="Cancel", style=color)
    async def cancel(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
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


async def confirm_button(ctx, message, client, re={8: 5160}):
    view = Confirm(client, re)
    await ctx.send(
        embed=ef.cembed(title="Confirmation", description=message, color=re[8]),
        view=view,
    )
    a = await view.wait()
    return a


class Pages(nextcord.ui.View):
    def __init__(self, ctx, embeds, restricted=False, start_from=0):
        super().__init__()
        self.embeds = embeds
        self.ctx = ctx
        self.restricted = restricted
        self.current_embed = embeds[start_from]
        self.page = start_from
        self.user = getattr(ctx, "user", getattr(ctx, "author", None))

    @nextcord.ui.button(label="<", style=color)
    async def previous(self, button, inter):
        if self.restricted:
            if not self.user == inter.user:
                return
        if self.page > 0:
            self.page -= 1
        await inter.response.edit_message(embed=self.embeds[self.page])

    @nextcord.ui.button(label=">", style=color)
    async def next(self, button, inter):
        if self.restricted:
            if not self.user == inter.user:
                return

        if self.page < len(self.embeds) - 1:
            self.page += 1
        await inter.response.edit_message(embed=self.embeds[self.page])


async def pa(ctx, embeds, restricted=False, start_from=0):
    if len(embeds) > 1:
        await ctx.send(
            embed=embeds[start_from], view=Pages(ctx, embeds, restricted, start_from)
        )
    else:
        await ctx.send(embed=embeds[0])


class Emotes:
    def __init__(self, client):
        self.client = client
        self.animated_wrong = client.get_emoji(935914136620134410)
        self.red_arrow = client.get_emoji(945741947220402176)
        self.animated_correct = client.get_emoji(958424323415212102)
        self.join_vc = client.get_emoji(852810663603994624)
        self.check = client.get_emoji(967279216343277579)
        self.loading = client.get_emoji(948396323843997776)
        self.upvote = client.get_emoji(945509681256865845)
        self.boost = client.get_emoji(975323250546597888)
        self.yikes = client.get_emoji(852810342991527946)

    def get_emoji(self, e):
        return getattr(self, e)


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
vote_embed = lambda client: ef.cembed(
    title="Thanks for all your support 💖",
    description=VOTE_MESSAGE,
    color=client.re[8],
    author=client.user,
    fields=VOTE_FIELDS,
    thumbnail=client.user.avatar.url,
    image="https://previews.123rf.com/images/enterline/enterline1806/enterline180601886/103633300-the-word-vote-concept-written-in-colorful-abstract-typography-vector-eps-10-available-.jpg",
    footer={
        "text": "Have a great day",
        "icon_url": "https://st.depositphotos.com/1048238/2045/i/600/depositphotos_20457989-stock-photo-have-fun-concept.jpg",
    },
)
