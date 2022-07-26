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
        self.client: commands.Bot = client

    @commands.Cog.listener()
    async def on_ready(self):
        while not all([self.client.get_guild(i) for i in self.client.config["roles"]]):
            for i in self.client.config["roles"]:
                if not self.client.get_guild(i):
                    del self.client.config["roles"][i]
                    break

        for guild, role_list in self.client.config["roles"].items():
            for roles in role_list:
                roles = map(self.client.get_guild(guild).get_role, roles)
                self.client.add_view(setup_view(roles))


def setup_view(roles: List[nextcord.Role]):
    return assets.RoleView(roles)


def setup(client, **i):
    client.add_cog(Roles(client, **i))
