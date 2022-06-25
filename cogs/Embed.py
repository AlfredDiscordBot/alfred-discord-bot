import nextcord
import assets
import time
import traceback
import helping_hand
import assets
import random
import External_functions as ef
import helping_hand
from nextcord.ext import commands, tasks
from yaml import safe_load, safe_dump
from typing import Union

from requests.models import PreparedRequest
from requests.exceptions import MissingSchema

#Use nextcord.slash_command()

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
    elif type(color) is int:
        return color
    elif (type(color) is str) and (type(col := tuple([int(i) for i in color.replace("(","").replace(")","").split(",")])) is tuple):
        return nextcord.Color.from_rgb(*col)

    return default_color

    
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

def embed_from_dict(info: dict, ctx, client) -> nextcord.Embed:
    """
    Generates an embed from given dict
    """
    info = preset_change(info, ctx, client, re = client.re)
    ctx_author = getattr(ctx, 'author', getattr(ctx,'user',None))
    info = {k.lower(): v for k, v in info.items()}  # make it case insensitive
    info["color"] = get_color(info.get("color", None))
    if info['color']: info['color']=info['color'].value     
    embed = ef.cembed(**info)
    return embed

def yaml_to_dict(yaml):
    try:
        return safe_load(yaml)
    except:
        return {
            'title': 'Embed',
            'description':yaml,
            'color':'<bot-color>'
        }


class Embed(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def yml_embed1(self, ctx, channel: Union[nextcord.TextChannel, str, nextcord.threads.Thread], *, yaml):
        embed = embed_from_dict(
            yaml_to_dict(filter_graves(yaml)),
            ctx, self.client
        )
        if isinstance(channel, (nextcord.TextChannel, nextcord.threads.Thread)):
            await channel.send(embed=embed)
        elif validate_url(channel):
            data = embed.to_dict()
            await post_async(channel, json={'embeds':[data]})

    
            
    


def setup(client,**i):
    client.add_cog(Embed(client,**i))
