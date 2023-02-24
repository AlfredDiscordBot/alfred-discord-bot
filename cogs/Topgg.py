import os
import utils.External_functions as ef
from nextcord.ext import commands, tasks

# Use nextcord.slash_command()


class TopGG_BASE:
    def __init__(self, token: str):
        self.TOKEN = token
        self.HEADER = {"Authorization": token}
        self.BASE_URL = "https://top.gg/api/"

    def url(self, loc: str):
        return self.BASE_URL + loc

    async def search_bots(self, bot_id: int):
        return await ef.get_async(
            self.url(f"/bot/{bot_id}"), headers=self.HEADER, kind="json"
        )

    async def post_stats(self, client: commands.Bot):
        await client.wait_until_ready()
        await ef.post_async(
            self.url(f"bots/811591623242154046/stats"),
            header=self.HEADER,
            json={"server_count": len(client.guilds)},
        )


def requirements():
    return []


class Topgg(commands.Cog):
    def __init__(self, CLIENT: commands.Bot):
        self.CLIENT = CLIENT
        self.topgg = TopGG_BASE(os.getenv("topgg"))
        if os.getenv("REPL_OWNER"):
            self.loop.start()

    @tasks.loop(minutes=30)
    async def loop(self):
        try:
            await self.CLIENT.wait_until_ready()
            await self.topgg.post_stats(self.CLIENT)
        except:
            print("TopGG not updated")


def setup(client, **i):
    client.add_cog(Topgg(client, **i))
