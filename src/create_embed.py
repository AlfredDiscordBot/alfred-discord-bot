import discord
from requests.models import PreparedRequest
from requests.exceptions import MissingSchema


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

    def set_color(self, color:tuple) -> None:
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
            info.description = split[1] if not getattr(info, 'thumbnail', None) else split[2]

            try:
                info.set_image(split[3])
            except:
                pass

            try:
                info.footer = split[3] if not getattr(info, 'image', None) else split[4]
            except:
                pass

        except Exception as e:
            print(e) # maybe make an error embed here...

        return info


def requirements() -> str:
    """
    Returns the requirements of the main function.
    """
    return ["re"]


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


def embed_from_info(info: EmbedInfo) -> discord.Embed:
    """
    returns a complete embed using the given EmbedInfo object
    """
    properties = info.attributes
    embed = discord.Embed(**properties)

    if 'thumbnail' in properties: embed.set_thumbnail(url = info.thumbnail)
    if 'image' in properties: embed.set_image(url = info.image)
    if 'footer' in properties: embed.set_footer(text = info.footer)

    return embed


def main(client, re):
    embeds = {}

    def quick_embed(description:str) -> discord.Embed:
        return discord.Embed(
            description = description,
            color = discord.Color(value=re[8]),
        )

    @client.command(aliases=["init_embed", "embed_init"])
    async def create_embed_init(ctx):
        re[0] += 1
        if (
            ctx.author.guild_permissions.manage_messages
            or ctx.author.id == 432801163126243328
        ):
            # embeds.pop(ctx.guild.id)
            embeds[ctx.guild.id] = EmbedInfo()

            await ctx.send(
                embed=quick_embed("Embed initialization complete")  # add embeds[ctx.guild.id] in description for debugging
            )

    @client.command(aliases=['emd'])
    async def embed_it(ctx, *, string:str):
        """
        Uses the new custom class and makes embed out of it, does the same thing as `embed_it()`
        """
        if (
            ctx.author.guild_permissions.manage_messages 
            or ctx.author.id == 432801163126243328
        ):
            try:
                re[0] += 1
                embeds[ctx.guild.id] = EmbedInfo.from_md(string)

                await ctx.send(embed=quick_embed("Done"))
            except Exception as e:
                await ctx.send(str(e))

    @client.command(aliases=["color_for_embed"])
    async def set_color(ctx, color:tuple):
        if (
            ctx.author.guild_permissions.manage_messages
            or ctx.author.id == 432801163126243328
        ):
            try:
                c = eval(color)
                re[0] += 1
                if ctx.guild.id not in embeds: create_embed_init(ctx)

                embeds[ctx.guild.id].set_color(*c)

                await ctx.send(embed=quick_embed("Color Set to " + str(c)))
            except Exception as e:
                await ctx.send(str(e))

    @client.command(aliases=["title"])
    async def set_title(ctx, *, title:str):
        if (
            ctx.author.guild_permissions.manage_messages
            or ctx.author.id == 432801163126243328
        ):
            if ctx.guild.id not in embeds: create_embed_init(ctx)
            embeds[ctx.guild.id].title = title
            re[0] += 1
            await ctx.send(embed=quick_embed("Title Set to " + title))

    @client.command(aliases=["description"])
    async def set_description(ctx, *, description:str):
        if (
            ctx.author.guild_permissions.manage_messages
            or ctx.author.id == 432801163126243328
        ):
            if ctx.guild.id not in embeds: create_embed_init(ctx)
            embeds[ctx.guild.id].description = description
            re[0] += 1
            await ctx.send(
                embed=quick_embed("Description Set to " + (description if len(description) < 21 else (description[:20] + '...')))
                ) 

    @client.command(aliases=["footer"])
    async def set_footer(ctx, *, footer:str):
        if (
            ctx.author.guild_permissions.manage_messages
            or ctx.author.id == 432801163126243328
        ):
            if ctx.guild.id not in embeds: create_embed_init(ctx)
            embeds[ctx.guild.id].footer = footer
            await ctx.send(embed=quick_embed("Footer Set to " + footer))

    @client.command(aliases=["thumbnail"])
    async def set_thumbnail(ctx, url:str):
        if (
            ctx.author.guild_permissions.manage_messages
            or ctx.author.id == 432801163126243328
        ):
            if ctx.guild.id not in embeds: create_embed_init(ctx)
            embeds[ctx.guild.id].set_thumbnail(url)
            await ctx.send(embed=quick_embed("Thumbnail Set"))
    
    @client.command(aliases=["image"])
    async def set_image(ctx, url:str):
        if (
            ctx.author.guild_permissions.manage_messages
            or ctx.author.id == 432801163126243328
        ):
            if ctx.guild.id not in embeds: create_embed_init(ctx)
            embeds[ctx.guild.id].set_image(url)
            await ctx.send(embed=quick_embed("Image Set"))

    @client.command(aliases=["send"])
    async def send_embed(ctx, channel: discord.TextChannel):
        if (
            ctx.author.guild_permissions.manage_messages
            or ctx.author.id == 432801163126243328
        ):
            if client.get_channel(channel.id) != None:
                send_channel = client.get_channel(channel.id)
                embed = discord.Embed()
                embed.set_author(
                    name=ctx.author.name,
                    icon_url=ctx.author.avatar_url_as(format="png"),
                )
                if ctx.guild.id in embeds and embeds.get(ctx.guild.id, None).attributes.get('description', False):
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
