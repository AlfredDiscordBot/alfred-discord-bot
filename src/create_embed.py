import nextcord as discord
from requests.models import PreparedRequest
from requests.exceptions import MissingSchema
from compile import filter_graves
from yaml import safe_load
import External_functions as ef

SUPER_AUTHOR_ID = 432801163126243328  # Do Not CHange
help_for_m_setup="""
'm_setup
```yaml
title: Title Goes Here
description: a good description for your embed
thumbnail: https://images-ext-1.discordapp.net/external/L58PZxhXkdE1gqzb-1FhC3f0t9YglNqEfW-0OVb2ubY/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/811591623242154046/115f0ef23ff700ffc894e6bed949b5fe.png?width=676&height=676
image: https://images-ext-1.discordapp.net/external/L58PZxhXkdE1gqzb-1FhC3f0t9YglNqEfW-0OVb2ubY/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/811591623242154046/115f0ef23ff700ffc894e6bed949b5fe.png?width=676&height=676
footer: The footer goes here
author: True/False
```

**Here's some Tips when you write this**

>In description, if you do `[something](https://link.com)`, the word something becomes a hyperlink

>You can use symbols like `*~|>` just like you do in your regular chat

>>Enjoy and have fun, we will not restrict

"""

def preset_change(text, ctx, client):
    presets = {
        'server-icon' : f'"{ctx.guild.icon_url}"',
        'author-icon' : f'"{ctx.author.avatar.url}"',
        'bot-icon' : f'"{client.user.avatar.url}"'
    }
    for i in presets:
        text=text.replace(presets[i])
    return text

    

class EmbedInfo:
    def __init__(
        self,
        title: str = None,
        description: str = None,
        thumbnail: str = None,
        image: str = None,
        footer: str = None,
        color: tuple = (48, 213, 200),
    ):
        """
        Creates an embed info object, with the provided information.
        """
        self.title = title
        self.description = description
        self.footer = footer

        self.set_thumbnail(thumbnail)
        self.set_image(image)

        self.color = discord.Color.from_rgb(*color)

    def set_color(self, color: tuple) -> None:
        """
        Set's the color for the embed
        """
        self.color = discord.Color.from_rgb(*color)

    def set_thumbnail(self, url: str) -> None:
        """
        Set's the url for the thumbnail of the embed.
        """
        url = (url or " ").strip()
        self.thumbnail = url if validate_url(url) else None

    def set_image(self, url: str) -> None:
        """
        Set's the url for the image of the embed.
        """
        url = (url or " ").strip()
        self.image = url if validate_url(url) else None

    def set_color(self, color: tuple) -> None:
        """
        Set's the color of the embed.
        """
        self.color = discord.Color.from_rgb(*color)

    def __repr__(self):
        return f"<EmbedInfo {self.title or False}>"

    @property
    def attributes(self) -> dict:
        """
        Returns the attributes for creating the embed, the
        """
        attr = ["color", "title", "description", "thumbnail", "image", "footer"]
        info_dict = {}

        for a in attr:
            if value := getattr(self, a, None):
                info_dict[a] = value

        return info_dict

    @classmethod
    def from_md(cls, MD: str):
        """
        Creates EmbedInfo from a given MD string.
        """
        info = cls()
        # TODO: Improve the interface
        try:
            split = MD.split("\n\n")

            info.title = split[0]
            info.set_thumbnail(split[1])
            info.description = (
                split[1] if not getattr(info, "thumbnail", None) else split[2]
            )

            try:
                info.set_image(split[3])
            except:
                pass

            try:
                info.footer = split[3] if not getattr(info, "image", None) else split[4]
            except:
                pass

        except Exception as e:
            print(e)  # maybe make an error embed here...

        return info


def validate_url(url: str) -> bool:
    """
    Checks if the url is valid or not
    """
    prepared_request = PreparedRequest()
    try:
        prepared_request.prepare_url(url, None)
        return True
    except MissingSchema as e:
        return False


def get_color(color):
    """
    returns the value of color as discord.color or int
    """
    default_color = discord.Color.from_rgb(48, 213, 200)

    if color is None:
        return default_color
    elif type(color) is int:
        return color
    elif (type(color) is str) and (type(col := eval(color)) is tuple):
        return discord.Color.from_rgb(*col)

    return default_color


def set_url(set_func, url) -> None:
    """
    set's the url value in the given set function.
    """
    if type(url) is str:
        url = (url or " ").strip()
        if url_ := (url if validate_url(url) else None):
            set_func(url=url_)
    elif type(url) is dict:
        set_func(**url)

    return


def embed_from_dict(info: dict, ctx_author=None) -> discord.Embed:
    """
    Generates an embed from given dict
    """
    info = {k.lower(): v for k, v in info.items()}  # make it case insensitive

    info["color"] = get_color(info.get("color", None))
    # print(info)

    embed = discord.Embed(**info)

    if image := info.get("image", None):
        set_url(embed.set_image, image)
    if thumbnail := info.get("thumbnail", None):
        set_url(embed.set_thumbnail, thumbnail)
    if footer := info.get("footer", None):
        embed.set_footer(text=footer)
    if author := info.get("author", None):
      if isinstance(author, bool):
        if author == True:
            embed.set_author(name=ctx_author.name, icon_url=ctx_author.avatar_url)
        elif type(author) == str and validate_url(author):
            embed.set_author(icon_url=author)
        elif type(author) == str:
            embed.set_author(name=author)
        else:
            embed.set_author(**author)
      else:
        embed.set_author(name=author.get("name", ""), url=author.get("url", ""), icon_url=author.get("icon_url", ""))

    if fields := info.get("fields", None):
        for field in fields:
            field = {k.lower(): v for k, v in field.items()}  # make it case insensitive
            embed.add_field(**field)

    return embed


def embed_from_yaml(yaml: str, ctx_author):
    info = safe_load(yaml)
    print(
        f"Creating Emebed for: '{ctx_author.name}' aka '{ctx_author.nick}' in '{ctx_author.guild}'"
    )
    return embed_from_dict(info, ctx_author)


def requirements() -> str:

    """
    Returns the requirements of the main function.
    """
    return ["re","mspace"]


def embed_from_info(info: EmbedInfo) -> discord.Embed:
    """
    returns a complete embed using the given EmbedInfo object
    """
    properties = info.attributes
    embed = discord.Embed(**properties)

    if "thumbnail" in properties:
        embed.set_thumbnail(url=info.thumbnail)
    if "image" in properties:
        embed.set_image(url=info.image)
    if "footer" in properties:
        embed.set_footer(text=info.footer)

    return embed


def main(client, re, mspace):
    embeds = {}

    def quick_embed(description: str) -> discord.Embed:
        return discord.Embed(
            description=description,
            color=discord.Color(value=re[8]),
        )

    @client.command(aliases=["init_embed", "embed_init"])
    async def create_embed_init(ctx):
        re[0] += 1
        if (
            ctx.author.guild_permissions.manage_messages
            or ctx.author.id == SUPER_AUTHOR_ID
        ):
            # embeds.pop(ctx.guild.id)
            embeds[ctx.guild.id] = EmbedInfo()

            await ctx.send(
                embed=quick_embed(
                    "Embed initialization complete"
                )  # add embeds[ctx.guild.id] in description for debugging
            )

    @client.command(aliases=["yml_embed"])
    async def embed_using_yaml(
        ctx, channel: discord.TextChannel = None, *, yaml: str = None
    ):
        """
        Create an embed from given yaml string and send it in the provided channel.
        """
        yaml = preset_change(yaml, ctx, client)
        if (
            ctx.author.guild_permissions.manage_messages
            or ctx.author.id == SUPER_AUTHOR_ID or ctx.author.permissions_in(channel).send_messages
        ):
            if not channel:
                channel = ctx.channel  # set default channel to current

            if (send_channel := client.get_channel(channel.id)) != None:
                embed = (
                    embed_from_yaml(filter_graves(yaml), ctx.author)
                    if yaml
                    else quick_embed("Nothing to embed")
                )
                await send_channel.send(embed=embed)
            else:
                await ctx.send(
                    embed=discord.Embed(
                        title="Oops",
                        description="This channel does not exist. Please check again",
                        color=discord.Color(value=re[8]),
                    )
                )
    @client.command()
    async def myspace(ctx, member :discord.Member = None):
        if not member:
            if ctx.author.id in mspace: 
                await embed_using_yaml(ctx, channel = ctx.channel, yaml = mspace[ctx.author.id])
                return
            
            else:
                await ctx.send(
                    embed = ef.cembed(
                        title="Oops",
                        description="You haven't set MySpace yet, use the command m_setup to set up your myspace. It follows a similar pattern to yml_embed, Instructions for yml_embed is in help\n\n"+help_for_m_setup,
                        color=re[8],
                        thumbnail=client.user.avatar.url
                    
                    )
                )
            return
        if member.id in mspace:
            await embed_using_yaml(ctx,channel=ctx.channel,yaml=mspace[member.id])
            return
        

        await ctx.send(
            embed=ef.cembed(
                title="Oops",
                description="This user has not set their MySpace yet",
                color=re[8],
                thumbnail=client.user.avatar.url
            )
        )
    @client.command()
    async def m_setup(ctx, *, yml):
        try:
            await embed_using_yaml(ctx,channel = ctx.channel, yaml = yml)
            #ctx, client, message, color=61620,usr=None
            confirm = await ef.wait_for_confirm(ctx,client,"Do you want to use this as your profile?",color=re[8],usr=ctx.author)
            if confirm: mspace[ctx.author.id]=yml
        except Exception as e:
            await ctx.send(
                embed=ef.cembed(
                    title="Error",
                    description=str(e),
                    color=re[8],
                    thumbnail=client.user.avatar.url
                )
            )
        
        

    @client.command(aliases=["emd"])
    async def embed_it(ctx, *, string: str):
        """
        Uses the new custom class and makes embed out of it, does the same thing as `embed_it()`
        """
        if (
            ctx.author.guild_permissions.manage_messages
            or ctx.author.id == SUPER_AUTHOR_ID
        ):
            try:
                re[0] += 1
                embeds[ctx.guild.id] = EmbedInfo.from_md(string)

                await ctx.send(embed=quick_embed("Done"))
            except Exception as e:
                await ctx.send(str(e))

    @client.command(aliases=["color_for_embed"])
    async def set_color(ctx, color):
        if (
            ctx.author.guild_permissions.manage_messages
            or ctx.author.id == SUPER_AUTHOR_ID
        ):
            try:
                c = [int(i) for i in color.replace(")", "").replace("(", "").split(",")]
                re[0] += 1
                if ctx.guild.id not in embeds:
                    create_embed_init(ctx)
                print(c, type(c))
                embeds[ctx.guild.id].set_color(*c)
                await ctx.send(embed=quick_embed("Color Set to " + str(c)))
            except Exception as e:
                await ctx.send(str(e))

    @client.command(aliases=["title"])
    async def set_title(ctx, *, title: str):
        if (
            ctx.author.guild_permissions.manage_messages
            or ctx.author.id == SUPER_AUTHOR_ID
        ):
            if not embeds.get(ctx.guild.id, False):
                embeds[ctx.guild.id] = EmbedInfo()

            embeds[ctx.guild.id].title = title
            re[0] += 1
            await ctx.send(embed=quick_embed("Title Set to " + title))

    @client.command(aliases=["description"])
    async def set_description(ctx, *, description: str):
        if (
            ctx.author.guild_permissions.manage_messages
            or ctx.author.id == SUPER_AUTHOR_ID
        ):
            if not embeds.get(ctx.guild.id, False):
                embeds[ctx.guild.id] = EmbedInfo()

            embeds[ctx.guild.id].description = description
            re[0] += 1
            await ctx.send(
                embed=quick_embed(
                    "Description Set to "
                    + (
                        description
                        if len(description) < 21
                        else (description[:20] + "...")
                    )
                )
            )

    @client.command(aliases=["footer"])
    async def set_footer(ctx, *, footer: str):
        if (
            ctx.author.guild_permissions.manage_messages
            or ctx.author.id == SUPER_AUTHOR_ID
        ):
            if not embeds.get(ctx.guild.id, False):
                embeds[ctx.guild.id] = EmbedInfo()

            embeds[ctx.guild.id].footer = footer
            await ctx.send(embed=quick_embed("Footer Set to " + footer))

    @client.command(aliases=["thumbnail"])
    async def set_thumbnail(ctx, url: str):
        if (
            ctx.author.guild_permissions.manage_messages
            or ctx.author.id == SUPER_AUTHOR_ID
        ):
            if not embeds.get(ctx.guild.id, False):
                embeds[ctx.guild.id] = EmbedInfo()

            embeds[ctx.guild.id].set_thumbnail(url)
            await ctx.send(embed=quick_embed("Thumbnail Set"))

    @client.command(aliases=["image"])
    async def set_image(ctx, url: str):
        if (
            ctx.author.guild_permissions.manage_messages
            or ctx.author.id == SUPER_AUTHOR_ID
        ):
            if not embeds.get(ctx.guild.id, False):
                embeds[ctx.guild.id] = EmbedInfo()

            embeds[ctx.guild.id].set_image(url)
            await ctx.send(embed=quick_embed("Image Set"))

    @client.command(aliases=["send"])
    async def send_embed(ctx, channel: discord.TextChannel):
        if (
            ctx.author.guild_permissions.manage_messages
            or ctx.author.id == SUPER_AUTHOR_ID
        ):
            if client.get_channel(channel.id) != None:
                send_channel = client.get_channel(channel.id)
                embed = discord.Embed()
                embed.set_author(
                    name=ctx.author.name,
                    icon_url=ctx.author.avatar.url,
                )
                if ctx.guild.id in embeds and embeds.get(
                    ctx.guild.id, None
                ).attributes.get("description", False):
                    try:
                        embed = embed_from_info(embeds[ctx.guild.id])
                    except Exception as e:
                        await ctx.send(str(e))

                await send_channel.send(embed=embed)
            else:
                await ctx.send(
                    embed=discord.Embed(
                        title="Oops",
                        description="This channel does not exist. Please check again",
                        color=discord.Color(value=re[8]),
                    )
                )
