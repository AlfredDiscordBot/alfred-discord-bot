import nextcord as discord
import External_functions as ef

def error(message):
    return ef.cembed(
        title="Error",
        color=discord.Color.red(),
        thumbnail="https://github.com/yashppawar/alfred-discord-bot/blob/replit/error.png?raw=true",
        description=str(message),
        footer="The developers will work on this issue soon"
    )


def requirements():
    return ""


def main(client):
    pass
