import nextcord
import utils.assets as assets
import os
import utils.External_functions as ef
from nextcord.ext import commands
from asyncio import sleep

# Use nextcord.slash_command()


def requirements():
    return ["WOLFRAM"]


models = ["BlenderBot", "DialoGPT", "Wolfram Scientific", "PopCat"]


class ChatBot(
    commands.Cog,
    description=f"ChatBot features, Contains Four Models: {', '.join(models)}. They are amazing and unique\nCheck out each Model",
):
    def __init__(self, CLIENT: commands.Bot, WOLFRAM):
        self.CLIENT = CLIENT
        self.WOLFRAM = WOLFRAM
        self.models = models
        self.past_response = {}
        self.generated = {}
        self.auth = os.getenv("transformers_auth")
        self.headers = {"Authorization": f"Bearer {self.auth}"}

    def moderate_variables(self, guild_id, input_text, output):
        if len(self.past_response[guild_id]) >= 50:
            self.past_response[guild_id].pop(0)
            self.generated[guild_id].pop(0)
        self.past_response[guild_id].append(input_text)
        self.generated[guild_id].append(output)

    @commands.Cog.listener()
    async def on_message(self, message):
        conditions = [
            message.clean_content.lower().startswith("alfred "),
            message.guild and message.guild.id not in self.CLIENT.config["respond"],
            not message.author.bot,
        ]
        if all(conditions):
            if not self.CLIENT.is_ready():
                return
            print(message.content, message.guild)
            if message.guild.id not in self.generated:
                self.generated[message.guild.id] = []

            if message.guild.id not in self.past_response:
                self.past_response[message.guild.id] = []

            input_text = message.clean_content[6:]

            if self.CLIENT.re[10].get(message.guild.id, 4) == 3:
                a = await ef.wolf_spoken(self.WOLFRAM, input_text)

            if self.CLIENT.re[10].get(message.guild.id, 4) in (1, 2):
                BASE_URL = "https://api-inference.huggingface.co/models"
                API_URL = f"{BASE_URL}/facebook/blenderbot-400M-distill"
                payload = {
                    "inputs": {
                        "past_user_inputs": self.past_response[message.guild.id],
                        "generated_responses": self.generated[message.guild.id],
                        "text": input_text,
                    },
                    "parameters": {"repetition_penalty": 1.33},
                }

                if self.CLIENT.re[10].get(message.guild.id, 4) == 2:
                    API_URL = f"{BASE_URL}/microsoft/DialoGPT-large"
                    payload = {"inputs": input_text}
                output, type = await ef.post_async(
                    API_URL, header=self.headers, json=payload
                )
                print(output)
                a = output["generated_text"]
                self.moderate_variables(message.guild.id, input_text, a)
            if self.CLIENT.re[10].get(message.guild.id, 4) == 4:
                a = await ef.get_async(
                    f"https://api.popcat.xyz/chatbot?msg={ef.convert_to_url(input_text)}&owner=Batman&botname=Alfred",
                    kind="json",
                )
                a = a["response"]

            await message.reply(a)

    @commands.command()
    @commands.check(ef.check_command)
    async def gen(self, ctx, *, text):
        self.CLIENT.re[0] += 1
        API_URL2 = "https://api-inference.huggingface.co/models/EleutherAI/gpt-neo-2.7B"
        header2 = {"Authorization": f"Bearer {os.environ['transformers_auth']}"}
        payload2 = {
            "inputs": text,
            "parameters": {"max_new_tokens": 100, "return_full_text": True},
        }

        output, type = await ef.post_async(API_URL2, header2, payload2)
        print(output)
        o = output[0]["generated_text"]

        await ctx.reply(
            embed=ef.cembed(
                title="Generated text",
                description=o,
                color=self.CLIENT.color(ctx.guild),
                thumbnail=self.CLIENT.user.avatar.url,
            )
        )

    @nextcord.slash_command(
        name="talktomyhand", description="Bots Talking to themselves"
    )
    async def talk(self, inter, start: str = "Hello there"):
        texts = [f"User-> {start}"]
        embed = ef.cembed(
            title="Talk To My hand",
            author=inter.user,
            description="\n".join(texts),
            color=inter.client.color(inter.guild),
            thumbnail=inter.client.user.avatar.url,
        )
        await inter.send(embed=embed)
        past_response = [start]
        message = await inter.original_message()
        for _ in range(10):
            await sleep(2)
            a = await ef.get_async(
                f"https://api.popcat.xyz/chatbot?msg={ef.convert_to_url(past_response[-1])}&owner=Batman&botname=Alfred",
                kind="json",
            )
            texts.append(f"Bot -> {a['response']}")
            past_response.append(a["response"])
            embed.description = "\n".join(texts)
            await message.edit(embed=embed)

    @nextcord.slash_command("model")
    async def changeM(self, inter, model=ef.defa(choices=models)):
        if not model:
            mod = models[self.CLIENT.re[10].get(inter.guild.id, 1) - 1]
            await inter.send(
                embed=ef.cembed(
                    description=f"Current model is {mod}",
                    color=self.CLIENT.color(inter.guild),
                )
            )
            return
        if not inter.user.guild_permissions.manage_guild:
            d = assets.Emotes(self.CLIENT).animated_wrong
            await inter.send(
                ephemeral=True,
                embed=ef.cembed(
                    title="Permissions Denied",
                    description=f"{d} You cannot change the model of this server, you need Manage server permissions",
                    color=self.CLIENT.color(inter.guild),
                    thumbnail=self.CLIENT.user.avatar.url,
                ),
            )
            return
        self.CLIENT.re[10][inter.guild.id] = self.models.index(model) + 1
        message = f"Switched to {model}"
        await inter.send(
            embed=ef.cembed(
                title="Done",
                description=message,
                color=self.CLIENT.color(inter.guild),
                thumbnail=self.CLIENT.user.avatar.url,
            )
        )


def setup(CLIENT, **i):
    CLIENT.add_cog(ChatBot(CLIENT, **i))
