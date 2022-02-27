import nextcord as discord
import External_functions as ef

def error(message):
    return ef.cembed(
        color=discord.Color.from_rgb(255,0,0).value,
        thumbnail="https://github.com/yashppawar/alfred-discord-bot/blob/replit/error.png?raw=true",
        description=str(message)
    )


def requirements():
    return "re"


def main(client, re):
    pass
