import os
import sys

import discord
from discord.ext import commands

from External_functions import cembed, devop_mtext
from main_program import get_dev_users, set_dev_users, re, temp_dev, load_from_file, dev_channel, save_to_file, \
    location_of_file


class Sudo(commands.cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def remove_dev(self, ctx, member: discord.Member):
        print(member)
        dev_users = get_dev_users()
        if str(ctx.author.id) == "432801163126243328":
            dev_users.remove(str(member.id))
            set_dev_users(dev_users)
            await ctx.send(member.mention + " is no longer a dev")
        else:
            await ctx.send(
                embed=discord.Embed(
                    title="Permission Denied",
                    description="Dude! You are not Alvin",
                    color=discord.Color(value=re[8]),
                )
            )

    @commands.command()
    async def add_dev(self, ctx, member: discord.Member):
        print(member)
        dev_users = get_dev_users()
        print("Add dev", str(ctx.author))
        if str(ctx.author.id) in dev_users:
            set_dev_users(dev_users + [str(member.id)])
            await ctx.send(member.mention + " is a dev now")
        else:
            await ctx.send(
                embed=discord.Embed(
                    title="Permission Denied",
                    description="Dude! you are not a dev",
                    color=discord.Color(value=re[8]),
                )
            )

    @commands.command(aliases=["script"])
    async def add_access_to_script(self, ctx, member: discord.Member, ti="5"):
        dev_users = get_dev_users()
        if str(ctx.author.id) in dev_users:
            mess = await ctx.send(
                embed=discord.Embed(
                    title="Done",
                    desription=f"{ctx.author.mention} gave script access to {member.mention}\nTimeRemaining: {int(ti) * 60}s",
                    color=discord.Color(value=re[8]),
                )
            )
            temp_dev[member.id] = [int(ti) * 60, mess]
        else:
            await ctx.send(
                embed=discord.Embed(
                    title="Access Denied",
                    description="Only Developers can give temporary access",
                    color=discord.Color.from_rgb(250, 30, 0),
                )
            )

    @commands.command(aliases=["remscript"])
    async def remove_access_to_script(self, ctx, member: discord.Member):
        if str(ctx.author.id) in get_dev_users():
            await ctx.send(
                embed=discord.Embed(
                    title="Removed Access",
                    description=str(ctx.author.mention)
                                + " removed access from "
                                + str(member.mention),
                    color=discord.Color(value=re[8]),
                )
            )
            temp_dev.pop(member.id)
        else:
            await ctx.send(
                embed=discord.Embed(
                    title="Access Denied",
                    description="Only Developers can remove temporary access",
                    color=discord.Color.from_rgb(250, 30, 0),
                )
            )

    @commands.command()
    async def dev_op(self, ctx):
        if str(ctx.author.id) in get_dev_users():
            print("devop", str(ctx.author))
            channel = self.bot.get_channel(dev_channel)
            await devop_mtext(self.bot, channel, re[8])
        else:
            await ctx.send(embed=cembed(title="Permission Denied",
                                        description="You cannot use the devop function, only a developer can",
                                        color=re[8]))

    @commands.command()
    async def reset_from_backup(self, ctx):
        print("reset_from_backup", str(ctx.author))
        dev_users = get_dev_users()
        channel = self.bot.get_channel(dev_channel)
        if str(ctx.author.id) in dev_users:
            try:
                load_from_file()
                await ctx.send(
                    embed=discord.Embed(
                        title="Done",
                        description="Reset from backup: done",
                        color=discord.Color(value=re[8]),
                    )
                )
                await channel.send(
                    embed=discord.Embed(
                        title="Done",
                        description="Reset from backup: done\nBy: " + str(ctx.author),
                        color=discord.Color(value=re[8]),
                    )
                )
            except Exception as e:
                await channel.send(
                    embed=discord.Embed(
                        title="Reset_from_backup failed",
                        description=str(e),
                        color=discord.Color(value=re[8]),
                    )
                )
        else:
            await ctx.send(
                embed=cembed(title="Permission Denied", description="Only developers can access this function",
                             color=re[8],
                             thumbnail=self.bot.user.avatar_url_as(format="png")))

            await channel.send(
                embed=cembed(
                    description=f"{ctx.author.name} from {ctx.guild.name} tried to use reset_from_backup command",
                    color=re[8]))

    @commands.command()
    async def docs(self, ctx, name):
        try:
            if name.find("(") == -1:
                await ctx.send(
                    embed=discord.Embed(
                        title="Docs",
                        description=str(eval(name + ".__doc__")),
                        color=discord.Color(value=re[8]),
                    )
                )
            else:
                await ctx.send(
                    embed=discord.Embed(
                        title="Permissions Denied",
                        description="Functions are not allowed. Try without the brackets to get the information",
                        color=discord.Color(value=re[8]),
                    )
                )
        except Exception as e:
            await ctx.send(
                embed=discord.Embed(
                    title="Error", description=str(e), color=discord.Color(value=re[8])
                )
            )

    @commands.command(aliases=["!"])
    async def restart_program(self, ctx, text):
        try:
            voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
            voice.stop()
            await voice.disconnect()
        except:
            pass
        save_to_file()
        print("Restart")
        os.chdir(location_of_file)
        os.system("nohup python main.py &")
        await ctx.send(
            embed=cembed(
                title="Restarted",
                description="The program finished restarting",
                color=re[8],
                thumbnail=self.bot.user.avatar_url_as(format="png"),
            )
        )
        sys.exit()
