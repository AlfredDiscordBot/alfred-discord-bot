import nextcord
from nextcord import Interaction, SlashOption
import External_functions as ef

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
        
    @nextcord.ui.button(label="Confirm",style=nextcord.ButtonStyle.red)
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
    await view.wait()
    if view.value is None:
        print('Timed out...')
    elif view.value:
        await ctx.message.edit(
            embed=ef.cembed(
                description="Confirmed",
                color=re[8]                
            )
        )
    else:
        print('Cancelled...')


class Emotes:
    def __init__(self, client):
        self.client = client
        self.animated_wrong = client.get_emoji(958424684540612688)
        self.red_arrow = client.get_emoji(945741947220402176)
        self.animated_correct = client.get_emoji(958424323415212102)
        self.join_vc = client.get_emoji(852810663603994624)
        self.check = client.get_emoji(957688162610729070)
        self.loading = client.get_emoji(948396323843997776)
        self.upvote = client.get_emoji(945509681256865845)
        
    