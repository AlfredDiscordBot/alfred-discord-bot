import nextcord
from nextcord import Interaction, SlashOption
import External_functions as ef

color = nextcord.ButtonStyle.blurple

class Confirm(nextcord.ui.View):
    def __init__(self, re = {8: 5160}):
        super().__init__()
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

async def confirm_button(ctx, message, client, re={8: 5160}):
    view = Confirm(re)
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
        
    @nextcord.ui.button(label="<",style=color)
    async def previous(self, button, inter):
        if self.restricted:
            if not self.user == inter.user:
                return
        if self.page > 0:
            self.page-=1
        await inter.response.edit_message(embed=self.embeds[self.page])

    @nextcord.ui.button(label=">",style=color)
    async def next(self, button, inter):
        if self.restricted:
            if not self.user == inter.user:
                return
                
        if self.page < len(self.embeds)-1:
            self.page+=1
        await inter.response.edit_message(embed=self.embeds[self.page])

async def pa(ctx, embeds, restricted = False, start_from = 0):
    if len(embeds)>1:
        await ctx.send(
            embed = embeds[start_from],
            view = Pages(ctx, embeds, restricted, start_from)
        )
    else:
        await ctx.send(embed=embeds[0])

class Emotes:
    def __init__(self, client):
        self.client = client
        self.animated_wrong = client.get_emoji(958424684540612688)
        self.red_arrow = client.get_emoji(945741947220402176)
        self.animated_correct = client.get_emoji(958424323415212102)
        self.join_vc = client.get_emoji(852810663603994624)
        self.check = client.get_emoji(967279216343277579)
        self.loading = client.get_emoji(948396323843997776)
        self.upvote = client.get_emoji(945509681256865845)
        self.boost = client.get_emoji(975323250546597888)
        self.yikes = client.get_emoji(852810342991527946)


class DictionaryViewer(nextcord.ui.View):
    def __init__(self, di, col):
        self.di = di
        self.path = "/"
        self.currently_selected = 0
        self.col = col
        self.cr = []

    def embed_maker(self):
        path = self.path.split("/")[1:]
        if not path:
            return ef.cembed(
                description="This attribute is empty"
            )
        self.cr = list(self.current_data_locator(path, self.di.copy()))
        title = path[-1] if path[-1] else "Home"
        cc = self.currently_selected-10
        description = "" if cc < 10 else " |->...\n"
        for i in range(cc-10 if cc-10>=0 else 0, cc+10):
            if i<len(self.cr) and i>0:
                if cc == i:
                    description+=f"\n |-> *{self.cr[i]}*"
                    continue
                description+=f"\n |-> {self.cr[i]}"
        description+="\n |-> ..." if len(self.cr)-cc>10 else ""
        return ef.cembed(
            title=title,
            description=description,
            color=self.col,
            footer="This feature is still in it's beta stage"
        )      
        

    def current_data_locator(self, path, di):        
        if len(path) !=0:
            a = path.pop(0)
            if isinstance(di, list):                
                return self.current_data_locator(path,di[int(a)])
            elif isinstance(di, dict):
                if a in di:
                    return self.current_data_locator(path,di[a])
                else:
                    return self.current_data_locator(path,di[int(a)])
        return di
        
        