import nextcord
import traceback
import asyncio
import utils.External_functions as ef
import utils.assets as assets
from nextcord.ext import commands
from yaml import safe_load, safe_dump
from utils.callbacks import get_callback_functions
from typing import Union

from requests.models import PreparedRequest
from requests.exceptions import MissingSchema

# Use nextcord.slash_command()
# Coded by Yash P Pawar


def requirements():
    return []


def filter_graves(text):
    final = ""
    for i in text.split("\n"):
        if not i.startswith("```"):
            final += i + "\n"
    return final


def get_color(color):
    """
    returns the value of color as nextcord.color or int
    """
    default_color = nextcord.Color.from_rgb(48, 213, 200)

    if color is None:
        return default_color
    if type(color) is int:
        return color
    if col := map(int, ef.delete_all(color, "()").split(",")):
        return nextcord.Color.from_rgb(*col)

    return default_color


def converter(a: dict):
    if a.get("thumbnail"):
        a["thumbnail"] = a["thumbnail"]["url"]
    del a["type"]
    if a.get("footer"):
        if a["footer"].get("proxy_icon_url"):
            del a["footer"]["proxy_icon_url"]
        if list(a["footer"].keys()) == ["text"]:
            a["footer"] = a["footer"]["text"]
    if a.get("image"):
        a["image"] = a["image"]["url"]
    if a.get("color"):
        a["color"] = str(nextcord.Color(a["color"]).to_rgb())
    if a.get("author") and a["author"].get("proxy_icon_url"):
        del a["author"]["proxy_icon_url"]
    return a


def preset_change(di, ctx, CLIENT):
    user = getattr(ctx, "author", getattr(ctx, "user", None))
    presets = {
        "<server-icon>": getattr(ctx.guild.icon, "url", None),
        "<author-icon>": ef.safe_pfp(user),
        "<author-color>": str(user.color.to_rgb()),
        "<bot-icon>": CLIENT.user.avatar.url,
        "<bot-color>": str(nextcord.Color(CLIENT.color(ctx.guild)).to_rgb()),
        "<server-author>": {
            "name": ctx.guild.name if ctx.guild else "Unavailable",
            "icon_url": ef.safe_pfp(ctx.guild),
        },
    }
    if isinstance(di, str):
        di = {"description": di, "color": "<bot-color>"}

    if isinstance(di.get("author"), str):
        if di["author"].lower() in presets:
            di["author"] = presets[di["author"].lower()]
        else:
            di["author"] = {"name": di["author"]}
    elif isinstance(di.get("author"), dict):
        for i in di["author"]:
            if i == "icon_url":
                if di["author"]["icon_url"] in presets:
                    di["author"]["icon_url"] = presets[di["author"]["icon_url"]]

    elif isinstance(di.get("author"), bool):
        if di.get("author"):
            di["author"] = {"name": user.name, "icon_url": user.avatar}

    for i in di:
        if i in ["color", "thumbnail", "image", "picture"]:
            if di[i] in presets:
                di[i] = presets[di[i]]
        if i == "footer":
            if isinstance(di[i], dict):
                if di[i].get("icon_url") and di[i].get("icon_url") in presets:
                    di[i]["icon_url"] = presets[di[i]["icon_url"]]
    return di


def validate_url(url: str) -> bool:
    """
    Checks if the url is valid or not
    """
    prepared_request = PreparedRequest()
    try:
        prepared_request.prepare_url(url, None)
        return True
    except MissingSchema:
        return False


def embed_from_dict(info: dict, ctx, CLIENT) -> nextcord.Embed:
    """
    Generates an embed from given dict
    """
    if info == {}:
        info = {
            "description": "Nothing to Embed",
            "color": str(nextcord.Color(CLIENT.color(ctx.guild)).to_rgb()),
        }
    info = preset_change(info, ctx, CLIENT)
    info = {k.lower(): v for k, v in info.items()}  # make it case insensitive
    if isinstance(info.get("color"), str) and (
        info.get("color").startswith("0x") or info.get("color").startswith("#")
    ):
        info["color"] = str(ef.extract_color(info["color"].replace("#", "0x")))
    try:
        info["color"] = get_color(info.get("color", None))
    except Exception:
        info["color"] = nextcord.Color.default()
    if info["color"]:
        if isinstance(info["color"], int):
            info["color"] = nextcord.Color(info["color"])
        info["color"] = info["color"].value

    return ef.cembed(**info)


def yaml_to_dict(yaml):
    try:
        a = safe_load(yaml)
        return a
    except:
        return yaml


class MSetup:
    def __init__(
        self,
        ctx: Union[commands.context.Context, nextcord.Interaction],
        CLIENT: commands.Bot,
    ):
        self.ctx = ctx
        self.USER = getattr(ctx, "author", getattr(ctx, "user", None))
        self.CLIENT = CLIENT
        self.END = False
        self.di: dict = {}
        self.EDIT_MESSAGE = None
        self.INSTRUCTION = None
        self.OPTIONS = ef.m_options
        self.SETUP_VALUE = None
        self.presets = [
            "<server-icon>",
            "<author-icon>",
            "<bot-color>",
            "<bot-icon>",
            "<author-color>",
            "<server-author>",
        ]

    def set_preset(self):
        self.di = preset_change(self.di, self.ctx, self.CLIENT)

    async def send_instructions(self):
        description = "Welcome to Msetup, you can select from these options down below\n```diff\nSETUP VALUES:\n"
        for i in self.OPTIONS:
            if i in self.di:
                description += "\n- "
            else:
                description += "\n+ "
            description += i
        description += "\n```\n\nSeperate Fields heading and body with >, and adding new field with two extra lines\n`Heading> Body here`\n\nSeperate footer text and icon_url with |>\n`Footer text|> <server-icon>`\n\n```\nYour First time? Start off with typing 'title', you will see the embed changing in the bottom, follow accordingly\n```\nColor input is only in (R, G, B) for now, will bring more options soon"
        embed = ef.cembed(
            title="MehSetup Instructions",
            description=description,
            color=self.CLIENT.color(self.ctx.guild),
            thumbnail=self.CLIENT.user.avatar.url,
            footer="Have Fun",
            fields=[
                {
                    "name": "Send It",
                    "value": ef.line_strip(
                        """To send it somewhere, type 
                    `send <#channel|webhook_url>`"""
                    ),
                    "inline": False,
                },
                {
                    "name": "Set As Mehspace",
                    "value": "To set it as your mehspace, type `done`",
                    "inline": False,
                },
                {
                    "name": "Cancel",
                    "value": "To cancel it type `cancel`",
                    "inline": False,
                },
                {
                    "name": "Import",
                    "value": "To import from your old mehspace, just type `import`\nIf you want to import from an embed, reply to a message and type import",
                    "inline": False,
                },
                {
                    "name": "Instructions",
                    "value": ef.dict2str(
                        {
                            "Fields": "\nHeading and the value should be seperated by `|>` for inline\nPutting `-|>` makes it not inline\n",
                            "Button": "\nLink buttons are available for public use, live buttons can only be used by developers"
                            + "To use link button, the syntax is simple\n`emoji url label`\nFor Example:`🎥 https://www.youtube.com Youtube`\n"
                            + "The Emoji, URL and the Label(in this case `Youtube`) must be seperated with space\n",
                            "Presets": "\nWe have a couple of presets, some are limited to certain features only\n"
                            + ef.list2str([f"`{i}`" for i in self.presets]),
                        }
                    ),
                },
            ],
        )
        if self.INSTRUCTION:
            await self.INSTRUCTION.edit(embed=embed)
        else:
            self.INSTRUCTION = await self.ctx.send(embed=embed)
        if not self.EDIT_MESSAGE:
            user = getattr(self.ctx, "user", getattr(self.ctx, "author", None))
            view = assets.Msetup_DropDownView(self.change_setup, user)
            embed = embed_from_dict(self.di, self.ctx, self.CLIENT)
            if isinstance(embed, tuple):
                embed, view_ = embed
                for i in view_.children:
                    view.add_item(i)
            self.EDIT_MESSAGE = await self.ctx.send(
                embed=embed,
                view=view,
            )
        else:
            embed = embed_from_dict(self.di, self.ctx, self.CLIENT)
            user = getattr(self.ctx, "user", getattr(self.ctx, "author", None))
            view = assets.Msetup_DropDownView(self.change_setup, user)
            if isinstance(embed, tuple):
                embed, view_ = embed
                for i in view_.children:
                    view.add_item(i)
            await self.EDIT_MESSAGE.edit(embed=embed, view=view)

    async def change_setup(self, MODE: str, inter: nextcord.Interaction) -> str:
        if self.END:
            await inter.response.send_message(
                content="🔚This Msetup Session Ended, please use `import` and reply to this embed by creating a new `/msetup`",
                ephemeral=True,
            )
            return
        self.SETUP_VALUE = MODE.lower()
        await inter.edit(
            embed=ef.cembed(
                title=f"Editing {MODE}",
                description=f"Currently editing {MODE}, please follow the syntax from the instruction page",
                color=self.CLIENT.color(inter.guild),
                thumbnail=self.CLIENT.user.avatar.url,
            )
        )
        return MODE

    def to_yaml(self):
        """
        converts to yaml
        """
        self.set_preset()
        return "```yml\n" + safe_dump(self.di) + "\n```"

    async def imp(self, msg: nextcord.Message):
        """
        import from a message
        """
        buttons = []
        for j in msg.components:
            for i in j.children:
                print(getattr(i, "url", False))
                if url := getattr(i, "url", False):
                    buttons.append(
                        {
                            "url": url,
                            "label": getattr(i, "label", nextcord.utils.MISSING),
                            "emoji": str(getattr(i, "emoji", None)),
                        }
                    )
        if len(msg.embeds) == 0:
            await self.ctx.send("I see no embed in that message", delete_after=5)
            return
        self.di = converter(msg.embeds[0].to_dict())
        self.di["button"] = buttons[:5]
        return self.to_yaml()

    def footer(self, text):
        """
        processes Footer to text to str or dict
        """
        footer = text.split("|>")

        if len(footer) > 1 and not (
            validate_url(footer[1]) or footer[1] in self.presets
        ):
            return text

        elif len(footer) > 1:
            return {"text": footer[0].strip(), "icon_url": footer[1].strip()}

        else:
            return text

    def fields(self, text):
        """
        processes field text to list of dicts
        """
        f = [i.split("|>") for i in text.split("\n\n\n")]
        all_fields = []
        for i in f:
            if len(i) != 2:
                all_fields.append({"name": "Heading", "value": ">".join(i)})
            else:
                fi = {"name": i[0], "value": i[1]}
                if fi["name"].endswith("-"):
                    fi["name"] = fi["name"][:-1]
                    fi["inline"] = False
                all_fields.append(fi)
        return all_fields

    def author(self, text=None):
        return (
            {"name": self.USER.name, "icon_url": ef.safe_pfp(self.USER)}
            if text.lower() == "true"
            else text
        )

    def process_button(self, text: str = None):
        lines = [i for i in text.split("\n") if i.strip()]
        buttons = []
        for i in lines:
            sp = [j for j in i.split(" ") if j.strip()]
            e, url, label = *sp[:2], " ".join(sp[2:])
            if not validate_url(url):
                continue
            buttons.append({"emoji": e, "url": url, "label": label})
        return buttons

    async def process_message(self, msg):
        """
        Send the message here and the class will automatically do it's work :)
        Should only be passed after `send_instructions |coro|`
        """
        text = msg.content
        if not any(map(text.startswith, ["send", "done", "cancel"])):
            await msg.delete()

        if text in self.OPTIONS:
            self.SETUP_VALUE = text.lower()
            await self.EDIT_MESSAGE.edit(
                embed=ef.cembed(
                    title=f"Editing {text}",
                    description=f"Currently editing {text}, please follow the syntax from the instruction page",
                    color=self.CLIENT.color(msg.guild),
                    thumbnail=self.CLIENT.user.avatar.url,
                )
            )

            self.set_preset()
            return self.to_yaml()

        if text.lower().startswith("import"):
            if msg.reference:
                impor = await self.ctx.channel.fetch_message(msg.reference.message_id)
                await self.imp(impor)
            elif validate_url((url := text.lower()[6:].strip())):
                channel_id, message_id = int(url.split("/")[-2]), int(
                    url.split("/")[-1]
                )
                channel = self.CLIENT.get_channel(channel_id)
                if not channel:
                    await self.ctx.send("I can't see that channel", delete_after=5)
                    return
                message = await channel.fetch_message(message_id)
                if not message.embeds:
                    await self.ctx.send(
                        "There are no embeds in this message", delete_after=5
                    )
                    return
                self.di = converter(message.embeds[0].to_dict())
            elif msg.author.id in self.CLIENT.mspace:
                self.di = safe_load(filter_graves(self.CLIENT.mspace[msg.author.id]))

            else:
                await self.ctx.send(
                    "You have no mehspace, if you want to import from a message, reply to the message",
                    delete_after=5,
                )

        elif any(map(text.lower().startswith, ["send", "done", "cancel"])):
            return self.to_yaml()

        elif self.SETUP_VALUE:
            if text == "-" and self.di.get(self.SETUP_VALUE):
                del self.di[self.SETUP_VALUE]
                await self.send_instructions()
                return
            output = text
            if self.SETUP_VALUE == "footer":
                output = self.footer(text)
            if self.SETUP_VALUE == "fields":
                output = self.fields(text)
            if self.SETUP_VALUE == "author":
                output = self.author(text)
            if self.SETUP_VALUE == "button":
                output = self.process_button(text)
            if self.SETUP_VALUE == "image":
                if (not validate_url(text)) and (not text.lower() in self.presets):
                    await self.ctx.send(
                        "Please enter a valid URL or one of the presets", delete_after=5
                    )
                    return
            self.di[self.SETUP_VALUE] = output
            self.set_preset()

        else:
            await self.ctx.send(
                "Please type a setup value from the instructions", delete_after=5
            )
            self.set_preset()
        await self.send_instructions()
        return self.to_yaml()


class Embed(
    commands.Cog,
    description="This is one of the best Set of Features in Alfred, Helps you create Embed and is one of the most widely used command",
):
    def __init__(self, CLIENT: commands.Bot):
        self.CLIENT = CLIENT
        self.old_messages = {}

    @commands.Cog.listener()
    async def on_ready(self):
        self.CLIENT.mspace[self.CLIENT.user.id] = assets.Alfred_Mehspace

    @nextcord.slash_command(name="msetup", description="Set your mehspace here")
    async def msetup_slash(self, inter: nextcord.Interaction):
        if not inter.channel.permissions_for(inter.user).send_messages:
            await inter.response.send_message(
                content="You dont have permission to speak here", ephemeral=True
            )
            return
        await self.msetup(inter)

    def special_callback(self, member_id, embed, view):
        if member_id not in get_callback_functions():
            return embed, view
        f = get_callback_functions().get(member_id)
        button = nextcord.ui.Button(label=f[1], emoji="▶️", style=assets.color)
        button.callback = f[0]
        if not isinstance(view, nextcord.ui.View):
            view = nextcord.ui.View(timeout=None)
        view.add_item(button)
        return embed, view

    @commands.command(aliases=["msetup1", "mehsetup"])
    async def msetup(self, ctx):
        session = MSetup(ctx, self.CLIENT)
        await session.send_instructions()
        scd = ["send", "cancel", "done"]
        user = getattr(ctx, "user", getattr(ctx, "author", None))

        while True:
            try:
                message = await self.CLIENT.wait_for(
                    "message",
                    check=lambda m: all([m.author == user, m.channel == ctx.channel]),
                )
                await session.process_message(message)

                if any(map(message.content.lower().startswith, scd)):
                    embed = embed_from_dict(session.di, ctx, self.CLIENT)
                    view: nextcord.ui.View = nextcord.utils.MISSING
                    if isinstance(embed, tuple):
                        embed, view = self.special_callback(user.id, *embed)
                    text = message.content

                    if text.lower() == "done":
                        confirm = await ef.wait_for_confirm(
                            ctx,
                            self.CLIENT,
                            "Do you want to set this as your mehspace?",
                            color=self.CLIENT.color(ctx.guild),
                        )

                        if confirm:
                            self.CLIENT.mspace[user.id] = session.to_yaml()
                            await ctx.send("Done")
                            break

                        await ctx.send("Continue, mehspace is not set")
                        continue

                    if text.lower() == "cancel":
                        await ctx.send("Cancelled")
                        break

                    if text.lower().startswith("send"):
                        if validate_url(text[5:]):
                            print("URL detected")
                            await ef.post_async(
                                text[5:], json={"embeds": [embed.to_dict()]}
                            )
                            await ctx.send("Done")
                            continue
                        if self.CLIENT.get_channel(int(text[7:-1])):
                            for i in getattr(view, "children", []):
                                if not getattr(i, "url", False):
                                    view.remove_item(i)
                                    break
                            channel = self.CLIENT.get_channel(int(text[7:-1]))
                            if channel.permissions_for(user).send_messages:
                                if channel.permissions_for(ctx.guild.me).send_messages:
                                    await channel.send(embed=embed, view=view)
                                else:
                                    await ctx.send(
                                        "Bot doesnt have enough permissions",
                                        delete_after=5,
                                    )
                                    continue
                            else:
                                await ctx.send(
                                    "You dont have permission to send messages there"
                                )

            except asyncio.TimeoutError:
                await ctx.send(
                    embed=ef.cembed(
                        title="Sorry",
                        description="Timed out, Discord will kill me if i wait longer",
                        color=self.CLIENT.color(ctx.guild),
                        thumbnail=self.CLIENT.user.avatar.url,
                    )
                )
                break
            except:
                print(traceback.format_exc())

        session.END = True

    @commands.command()
    @commands.check(ef.check_command)
    async def yml_embed(
        self,
        ctx,
        channel: Union[nextcord.TextChannel, str, nextcord.threads.Thread],
        *,
        yaml=None,
    ):
        try:
            embed = embed_from_dict(yaml_to_dict(filter_graves(yaml)), ctx, self.CLIENT)
            view = nextcord.utils.MISSING
            if isinstance(embed, tuple):
                embed, view = embed
            if isinstance(channel, (nextcord.TextChannel, nextcord.threads.Thread)):
                await channel.send(embed=embed, view=view)
            elif validate_url(channel):
                data = embed.to_dict()
                await ef.post_async(channel, json={"embeds": [data]})
            elif channel.lower() == "mehspace":
                if yaml:
                    embed, view = self.special_callback(ctx.author.id, embed, view)
                    await ctx.send(embed=embed, view=view)
                    confirm = await ef.wait_for_confirm(
                        ctx,
                        self.CLIENT,
                        "Do you want to use this as your profile?",
                        color=self.CLIENT.color(ctx.guild),
                        usr=ctx.author,
                    )
                    if confirm:
                        self.CLIENT.mspace[ctx.author.id] = yaml
                else:
                    embed = embed_from_dict(
                        yaml_to_dict(filter_graves(yaml)), ctx, self.CLIENT
                    )
                    view = nextcord.utils.MISSING
                    if isinstance(embed, tuple):
                        embed, view = self.special_callback(ctx.author.id, *embed)
                    await ctx.send(embed=embed, view=view)
            else:
                await ctx.send("Invalid channel or URL form")
        except:
            print(traceback.format_exc())

    @nextcord.user_command(name="mehspace")
    async def meh(self, inter, member):
        if member.id not in self.CLIENT.mspace:
            await inter.send("The user has not set mehspace", ephemeral=True)
            return
        yaml = filter_graves(self.CLIENT.mspace[member.id])
        di = yaml_to_dict(yaml)
        embed = embed_from_dict(di, inter, self.CLIENT)
        view = nextcord.utils.MISSING
        if isinstance(embed, tuple):
            embed, view = self.special_callback(member.id, *embed)
        await inter.send(embed=embed, view=view)

    @commands.command(name="mehspace", aliases=["meh", "myspace"])
    @commands.check(ef.check_command)
    async def mehspace_prefix_command(self, ctx, user: nextcord.Member = None):
        if not user:
            user = ctx.author
        if user.id not in self.CLIENT.mspace:
            await ctx.send(
                embed=ef.cembed(
                    title="Unavailable",
                    description="This user has not set mehspace",
                    color=self.CLIENT.color(ctx.guild),
                    author=user,
                    thumbnail="https://www.cambridge.org/elt/blog/wp-content/uploads/2019/07/Sad-Face-Emoji-480x480.png.webp",
                )
            )
            return
        embed = embed_from_dict(
            yaml_to_dict(filter_graves(self.CLIENT.mspace[user.id])),
            ctx,
            self.CLIENT,
        )
        view = nextcord.utils.MISSING
        if isinstance(embed, tuple):
            embed, view = self.special_callback(user.id, *embed)
        await ctx.send(embed=embed, view=view)

    @nextcord.slash_command(name="mehspace", description="Show Mehspace of someone")
    async def mehspace(self, inter: nextcord.Interaction, user: nextcord.User = None):
        if not user:
            user = inter.user
        if user.id not in self.CLIENT.mspace:
            await inter.response.send_message(
                embed=ef.cembed(
                    title="Unavailable",
                    description="This user has not set mehspace",
                    color=self.CLIENT.color(inter.guild),
                    thumbnail="https://www.cambridge.org/elt/blog/wp-content/uploads/2019/07/Sad-Face-Emoji-480x480.png.webp",
                    author=user,
                )
            )
            return
        embed = embed_from_dict(
            yaml_to_dict(filter_graves(self.CLIENT.mspace[user.id])),
            inter,
            self.CLIENT,
        )
        view = nextcord.utils.MISSING
        if isinstance(embed, tuple):
            embed, view = self.special_callback(user.id, *embed)
        await inter.response.send_message(embed=embed, view=view)

    @nextcord.slash_command(name="embed", description="Create your embed using this")
    async def em(
        self,
        inter,
        description,
        title=None,
        color="(1,1,1)",
        thumbnail=None,
        image=None,
        footer=None,
        author: nextcord.Member = None,
    ):
        await inter.response.defer()
        try:
            d = {
                "description": description,
                "color": color,
            }
            if author:
                d["author"] = {"name": author.name, "icon_url": ef.safe_pfp(author)}
            if image:
                d["image"] = image
            if thumbnail:
                d["thumbnail"] = thumbnail
            if footer:
                d["footer"] = footer
            if title:
                d["title"] = title

            embed = embed_from_dict(d, inter, self.CLIENT)
            await inter.send(embed=embed)
        except:
            print(traceback.format_exc())
            await inter.response.send_message(
                embed=ef.cembed(
                    title="Oops",
                    description="Something is wrong",
                    color=self.CLIENT.color(inter.guild),
                ),
                ephemeral=True,
            )

    @nextcord.message_command(name="embedinfo")
    async def embedinfo(self, inter, message):
        if len(message.embeds) == 0:
            await inter.send("I see no embed here", ephemeral=True)
            return

        e = message.embeds[0].to_dict()
        e["button"] = []
        for i in message.components:
            for j in i.children:
                if url := getattr(j, "url", False):
                    e["button"].append(
                        {
                            "url": url,
                            "label": getattr(j, "label", "Link"),
                            "emoji": str(getattr(j, "emoji")),
                        }
                    )

        await inter.send(
            embed=ef.cembed(
                title="EmbedInfo",
                description=f"```yml\n{safe_dump(converter(e))}\n```",
                color=self.CLIENT.color(inter.guild),
                thumbnail=self.CLIENT.user.avatar.url,
            ),
            ephemeral=True,
        )

    @commands.command(name="embedinfo")
    async def embedi(self, ctx):
        if not ctx.message.reference:
            await ctx.send("Reply to a message")
            return
        message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        if len(message.embeds) == 0:
            await ctx.send("I see no embed here")
            return

        e = message.embeds[0].to_dict()
        e["button"] = []
        for i in message.components:
            for j in i.children:
                if url := getattr(j, "url", False):
                    e["button"].append(
                        {
                            "url": url,
                            "label": getattr(j, "label", "Link"),
                            "emoji": str(getattr(j, "emoji")),
                        }
                    )

        await ctx.send(
            embed=ef.cembed(
                title="EmbedInfo",
                description=f"```yml\n{safe_dump(converter(e))}\n```",
                color=self.CLIENT.color(ctx.guild),
                thumbnail=self.CLIENT.user.avatar.url,
            )
        )

    @nextcord.message_command()
    async def view_raw(self, inter, message):
        a = message.content.replace("`", "\\`")
        await inter.response.send_message(f"```\n{a}\n```", ephemeral=True)

    @commands.command(name="view_raw", aliases=["vr"])
    async def raw(self, ctx):
        a = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        a = a.content.replace("`", "\\`")

        await ctx.send(f"```\n{a}```")


def setup(CLIENT, **i):
    CLIENT.add_cog(Embed(CLIENT, **i))
