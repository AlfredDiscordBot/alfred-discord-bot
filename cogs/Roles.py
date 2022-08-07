import nextcord
import utils.assets as assets
import utils.External_functions as ef
from nextcord.ext import commands
from typing import List

# Use nextcord.slash_command()


def requirements():
    return []


class Roles(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.CLIENT: commands.Bot = client

    @commands.Cog.listener()
    async def on_ready(self):
        while not all([self.CLIENT.get_guild(i) for i in self.CLIENT.config["roles"]]):
            for i in self.CLIENT.config["roles"]:
                if not self.CLIENT.get_guild(i):
                    del self.CLIENT.config["roles"][i]
                    break

        for guild, role_list in self.CLIENT.config["roles"].items():
            for roles in role_list:
                roles = map(self.CLIENT.get_guild(guild).get_role, roles)
                self.CLIENT.add_view(setup_view(roles))


def setup_view(roles: List[nextcord.Role]):
    return assets.RoleView(roles)


def setup(CLIENT, **i):
    CLIENT.add_cog(Roles(CLIENT, **i))
