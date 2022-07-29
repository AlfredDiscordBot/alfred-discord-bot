import nextcord
import utils.External_functions as ef
from nextcord.ext import commands

# Use nextcord.slash_command()


def requirements():
    return []


class DataCleanup(commands.Cog):
    def __init__(self, CLIENT: commands.Bot):
        self.CLIENT = CLIENT

    @commands.Cog.listener()
    async def on_ready(self):
        print("DELETING MISC DATA")
        self.config()
        self.queue_song()

    def queue_song(self):
        count = 0
        while True:
            for i in self.CLIENT.queue_song:
                if not self.CLIENT.get_guild(i):
                    count += 1
                    del self.CLIENT.queue_song[i]
                    break
            else:
                break
        print("QUEUE_SONG ->", count)

    def config(self):
        count = 0
        while True:
            for i in self.CLIENT.config["snipe"]:
                if not self.CLIENT.get_guild(i):
                    count += 1
                    self.CLIENT.config["snipe"].remove(i)
                    break
            else:
                break
        print("CONFIG SNIPE ->", count)

        count = 0
        while True:
            for i in self.CLIENT.config["respond"]:
                if not self.CLIENT.get_guild(i):
                    count += 1
                    self.CLIENT.config["respond"].remove(i)
                    break
            else:
                break
        print("CONFIG RESPOND ->", count)

        count = 0
        while True:
            for i, j in self.CLIENT.config["youtube"].items():
                if (not self.CLIENT.get_channel(i)) or j == set():
                    count += 1
                    del self.CLIENT.config["youtube"][i]
                    break
            else:
                break
        print("CONFIG YOUTUBE ->", count)

        count = 0
        while True:
            for i, j in self.CLIENT.config["welcome"].items():
                if not (
                    self.CLIENT.get_guild(i) and self.CLIENT.get_channel(j["channel"])
                ):
                    count += 1
                    del self.CLIENT.config["welcome"][i]
                    break
            else:
                break
        print("CONFIG WELCOME ->", count)

        count = 0
        while True:
            for i, j in self.CLIENT.config["security"].items():
                if not all([self.CLIENT.get_guild(i), self.CLIENT.get_channel(j)]):
                    count += 1
                    del self.CLIENT.config["security"][i]
                    break
            else:
                break
        print("CONFIG SECURITY ->", count)


def setup(client, **i):
    client.add_cog(DataCleanup(client, **i))
