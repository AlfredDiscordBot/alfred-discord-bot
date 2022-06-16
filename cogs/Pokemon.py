
import nextcord
import assets
import time
import traceback
import helping_hand
import assets
import random
import External_functions as ef
import helping_hand
from nextcord.ext import commands, tasks

#Use nextcord.slash_command()

def requirements():
    return []

class Pokemon(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.p = ef.Pokemon()

    @nextcord.slash_command(
        name="pokemon",
        description="Get details about a pokemon -> Beta"
    )
    async def poke(self, inter: nextcord.Interaction, pokemon: str):
        await inter.response.defer()
        embed = await self.p.get_stats(pokemon, True, self.client.re[8])
        await inter.send(
            embed=embed
        )

    @poke.on_autocomplete("pokemon")
    async def search_autocomplete(self, inter: nextcord.Interaction, pokemon: str):
        await inter.response.send_autocomplete(self.p.search(pokemon))

    


def setup(client,**i):
    client.add_cog(Pokemon(client,**i))
