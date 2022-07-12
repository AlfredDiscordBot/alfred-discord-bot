import nextcord
from nextcord.ext import commands
from requests.models import PreparedRequest
from requests.exceptions import MissingSchema
from yaml import safe_load
import utils.External_functions as ef


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

def preset_change(di, ctx, client, re = {8: 6619080}):
    user = getattr(ctx, 'author', getattr(ctx,'user',None))
    presets = {
        '<server-icon>' : getattr(ctx.guild.icon, 'url', None),
        '<author-icon>' : ef.safe_pfp(user),
        '<author-color>': str(user.color.to_rgb()),
        '<bot-icon>' : client.user.avatar.url,
        '<bot-color>' : str(nextcord.Color(re[8]).to_rgb())
    }
    if type(di) == str:
        di ={
            'description': di,
            'color': '<bot-color>'
        }
    if type(di.get('author')) == str:
        di['author'] = {
            'name' : di['author']
        }
    
    for i in di:
        if i in ['color','thumbnail','image','picture']:
            if di[i] in presets:
                di[i] = presets[di[i]]
        if i == "footer":
            if isinstance(di[i], dict):
                if di[i].get("icon_url") and di[i].get("icon_url") in presets:
                    di[i]['icon_url'] = presets[di[i]['icon_url']]
                    
                
    if  type(di.get('author')) == dict:
        for i in di['author']:
            if i == 'icon_url':
                if di['author']['icon_url'] in presets:
                    di['author']['icon_url'] = presets[di['author']['icon_url']]
    return di

    

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

        self.color = nextcord.Color.from_rgb(*color)

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
        self.color = nextcord.Color.from_rgb(*color)

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
    returns the value of color as nextcord.color or int
    """
    default_color = nextcord.Color.from_rgb(48, 213, 200)

    if color is None:
        return default_color
    elif type(color) is int:
        return color
    elif (type(color) is str) and (type(col := tuple([int(i) for i in color.replace("(","").replace(")","").split(",")])) is tuple):
        return nextcord.Color.from_rgb(*col)

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


def embed_from_dict(info: dict, ctx, client, re) -> nextcord.Embed:
    """
    Generates an embed from given dict
    """
    info = preset_change(info, ctx, client, re = re)
    ctx_author = getattr(ctx, 'author', getattr(ctx,'user',None))
    info = {k.lower(): v for k, v in info.items()}  # make it case insensitive
    info["color"] = get_color(info.get("color", None))
    if info['color']: info['color']=info['color'].value     
    embed = ef.cembed(**info)

    return embed


def embed_from_yaml(yaml: str, ctx, client, re):
    info = safe_load(yaml)
    ctx_author = getattr(ctx, 'author', getattr(ctx,'user',None))
    print(
        f"Creating Embed for: '{ctx_author.name}' aka '{ctx_author.nick}' in '{ctx_author.guild}'"
    )
    return embed_from_dict(info, ctx, client, re)


def requirements() -> str:

    """
    Returns the requirements of the main function.
    """
    return ["re","mspace","dev_channel"]


def embed_from_info(info: EmbedInfo) -> nextcord.Embed:
    """
    returns a complete embed using the given EmbedInfo object
    """
    properties = info.attributes
    embed = nextcord.Embed(**properties)

    if "thumbnail" in properties:
        embed.set_thumbnail(url=info.thumbnail)
    if "image" in properties:
        embed.set_image(url=info.image)
    if "footer" in properties:
        embed.set_footer(text=info.footer)

    return embed


def main(client, re, mspace, dev_channel):
    pass      
    
                    
