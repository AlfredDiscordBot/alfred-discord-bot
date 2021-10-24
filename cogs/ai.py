import os
import random

import aiohttp
import discord
from discord.ext import commands

from External_functions import genpost, cembed
from main_program import re, censor, prefix_dict, save_to_file, dev_channel, get_dev_users, req


class AI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.past_response = []
        self.generate = []

    async def transformer(api, header, json):
        async with aiohttp.ClientSession() as session:
            async with session.post(api, headers=header, json=json) as resp:
                return await resp.json()

    @commands.command()
    async def changeM(ctx, *, num):
        if str(ctx.author.id) in get_dev_users():
            num = int(num)

            if num == 1:
                re[10] = 1
                await ctx.send(
                    embed=discord.Embed(
                        title="Model change",
                        description="Changed to blenderbot",
                        color=discord.Color(value=re[8]),
                    )
                )
            elif num == 2:
                re[10] = 2
                await ctx.send(
                    embed=discord.Embed(
                        title="Model change",
                        description="Changed to dialo-gpt",
                        color=discord.Color(value=re[8]),
                    )
                )
            else:

                await ctx.send(
                    embed=discord.Embed(
                        title="Model change",
                        description="Bruh thats not a valid option",
                        color=discord.Color(value=re[8]),
                    )
                )

        else:
            await ctx.send(
                embed=discord.Embed(
                    title="Model change",
                    description="F off thout isn't un dev user",
                    color=discord.Color(value=re[8]),
                )
            )

    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message):
        auth = os.getenv("transformers_auth")

        headeras = {"Authorization": f"Bearer {auth}"}
        if re[10] == 1:
            api_url = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
        else:
            api_url = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-large"

        try:
            for word in censor:
                if word in msg.content.lower() and msg.guild.id in [
                    822445271019421746,
                    841026124174983188,
                    853670839891394591,
                ]:
                    await msg.delete()
            if msg.guild.id in [822445271019421746]:
                if "?" in msg.content.lower() and re[4] == 1:
                    await msg.channel.send("thog dont caare")
                elif "why do chips".strip() in msg.content.lower():
                    await msg.channel.send(
                        "https://pics.me.me/thumb_why-do-chips-get-stale-gross-i-just-eat-a-49666262.png"
                    )
                else:
                    if re[4] == 1:
                        for i in ["what", "how", "when", "why", "who", "where"]:
                            if i in msg.content.lower():
                                await msg.channel.send("thog dont caare")
                                break

            if msg.content.lower().startswith("alfred"):

                input_text = msg.content.lower().replace("alfred", "")
                payload = {
                    "inputs": {
                        "past_user_inputs": self.past_respose,
                        "generated_responses": self.generated,
                        "text": input_text,
                    },
                    "parameters": {"repetition_penalty": 1.33},
                }

                output = await self.transformer(api_url, header=headeras, json=payload)

                if len(self.past_respose) < 50:
                    self.past_respose.append(input_text)
                    self.generated.append(output["generated_text"])
                else:
                    self.past_respose.pop(0)
                    self.generated.pop(0)
                    self.past_respose.append(input_text)
                    self.generated.append(output["generated_text"])

                print(output)
                await msg.reply(output["generated_text"])

            if f"<@!{self.bot.user.id}>" in msg.content:
                prefi = prefix_dict.get(msg.guild.id, "'")
                embed = discord.Embed(
                    title="Hi!! I am Alfred.",
                    description=f"""Prefix is {prefi}\nFor more help, type {prefi}help""",
                    color=discord.Color(value=re[8]),
                )
                embed.set_image(
                    url=random.choice(
                        [
                            "https://giffiles.alphacoders.com/205/205331.gif",
                            "https://c.tenor.com/PQu-tE-5HxwAAAAd/michael-caine-the-dark-knight.gif",
                        ]
                    )
                )

                await msg.channel.send(embed=embed)
            if msg.content.startswith(prefix_dict.get(msg.guild.id, "'")) == 0:
                save_to_file("recover")
            await self.bot.process_commands(msg)
        except Exception as e:
            channel = self.bot.get_channel(dev_channel)
            await channel.send(
                embed=discord.Embed(
                    title="Error", description=str(e), color=discord.Color(value=re[8])
                )
            )

    @commands.command()
    async def gen(self, ctx, *, text):
        req()
        api_url2 = "https://api-inference.huggingface.co/models/EleutherAI/gpt-neo-2.7B"
        header2 = {"Authorization": f"Bearer {os.environ['transformers_auth']}"}
        payload2 = {
            "inputs": text,
            "parameters": {"max_new_tokens": 250, "return_full_text": True},
        }

        output = await genpost(api_url2, header2, payload2)
        await ctx.reply(
            embed=cembed(
                title="Generated text", description=output[0]["generated_text"], color=re[8]
            )
        )


def setup(client):
    client.add_cog(Fun(client))
