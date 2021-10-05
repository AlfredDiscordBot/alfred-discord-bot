import discord


def error(message):
    embed = discord.Embed(
        color=discord.Color.from_rgb(),
        thumbnail="https://github.com/yashppawar/alfred-discord-bot/blob/replit/error.png?raw=true",
        message=str(message),
    )


def requirements():
    return ""


def main(client):
    pass
