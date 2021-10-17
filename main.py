"""
Alfred Discord Bot

rewrite

Author: Yash Pawar
Originally Written: 06 October 2021
Last Edited: 06 October 2021
"""

import discord
import os
from src.error_logger import ErrorLogger
from discord.ext import commands

DEV_CHANNEL = int(os.getenv("dev"))
INTENTS = discord.Intents.default()
CLIENT = commands.Bot(
    command_prefix=["dev'"],
    intents=INTENTS,
    case_sensitive=True,
)

channel: discord.channel.TextChannel = None
logger = ErrorLogger(channel)

@CLIENT.event
async def on_ready():
    global channel, logger
    channel = CLIENT.get_channel(DEV_CHANNEL)
    await channel.send("works?")
    logger.set_channel(channel)
    print(channel)

@CLIENT.command()
@logger.track_command
async def errur(ctx):
    raise NotImplemented("haha well it is implemented!")

@CLIENT.command()
@logger.track_command
async def errurr(ctx, *, text):
    raise TypeError("haha well " + text)

@CLIENT.command()
@logger.track_command
async def errur2(ctx, text_channel, *, text):
    raise TypeError("haha well " + str(text_channel) + text)

@CLIENT.command(aliases=["m"])
@logger.track_command
async def python_shell(ctx, *, text):
    print("Python Shell", text, str(ctx.author))
    try:
        text = text.replace("```py", "")
        text = text.replace("```", "")
        a = eval(text)
        print(text)
        em = discord.Embed(
            title=text,
            description=text + "=" + str(a)
        )
        em.set_thumbnail(
            url="https://engineering.fb.com/wp-content/uploads/2016/05/2000px-Python-logo-notext.svg_.png"
        )
        await ctx.send(embed=em)
    except Exception as e:
        await ctx.send(
            embed=discord.Embed(
                title="Error_message",
                description=str(e)
            )
        )


CLIENT.run(os.getenv("token"))
