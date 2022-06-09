
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


def setup(client,**i):
    client.add_cog(Pokemon(client,**i))
