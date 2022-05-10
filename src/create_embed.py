import nextcord as discord
from nextcord.ext import commands
from requests.models import PreparedRequest
from requests.exceptions import MissingSchema
from compile import filter_graves
from yaml import safe_load, safe_dump
import traceback
import asyncio
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

def preset_change(di, ctx, client, re = {8: 6619080}):
    presets = {
        '<server-icon>' : getattr(ctx.guild.icon, 'url', None),
        '<author-icon>' : ef.safe_pfp(ctx.author),
        '<bot-icon>' : client.user.avatar.url,
        '<bot-color>' : str(discord.Color(re[8]).to_rgb())
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
    elif (type(color) is str) and (type(col := tuple([int(i) for i in color.replace("(","").replace(")","").split(",")])) is tuple):
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


def embed_from_dict(info: dict, ctx, client, re) -> discord.Embed:
    """
    Generates an embed from given dict
    """
    info = preset_change(info, ctx, client, re = re)
    ctx_author = getattr(ctx, 'author', getattr(ctx,'user',None))
    info = {k.lower(): v for k, v in info.items()}  # make it case insensitive

    info["color"] = get_color(info.get("color", None))
    if info['color']: info['color']=info['color'].value     
    embed = ef.cembed(**info)

    if image := info.get("image", None):
        set_url(embed.set_image, image)
    if thumbnail := info.get("thumbnail", None):
        set_url(embed.set_thumbnail, thumbnail)
    if footer := info.get("footer", None):
        embed.set_footer(text=footer)
    if author := info.get("author", None):
      if isinstance(author, bool):
        if author == True:
            embed.set_author(name=ctx_author.name, icon_url=ctx_author.avatar.url)
        elif type(author) == str and validate_url(author):
            embed.set_author(icon_url=author)
        elif type(author) == str:
            embed.set_author(name=author)
        else:
            embed.set_author(**author)
      else:
          print(author)
          embed.set_author(name=author.get("name", ""), url=author.get("url", ""), icon_url=author.get("icon_url", ""))

    if fields := info.get("fields", None):
        print(fields)
        for field in fields:
            field = {k.lower(): v for k, v in field.items()}  # make it case insensitive
            embed.add_field(**field)

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


def main(client, re, mspace, dev_channel):
    embeds = {}

    def quick_embed(description: str) -> discord.Embed:
        return discord.Embed(
            description=description,
            color=discord.Color(value=re[8]),
        )

    @client.command(aliases=["yml_embed"])
    @commands.check(ef.check_command)
    async def embed_using_yaml(
        ctx, channel: discord.TextChannel = None, *, yaml: str = None
    ):
        """
        Create an embed from given yaml string and send it in the provided channel.
        """        
        try:
            if (
                channel.permissions_for(ctx.author).send_messages
                or ctx.author.id == SUPER_AUTHOR_ID
            ):
                if not channel:
                    channel = ctx.channel  # set default channel to current

                if (send_channel := client.get_channel(channel.id)) != None:
                    embed = (
                        embed_from_yaml(filter_graves(yaml), ctx, client, re)
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
        except Exception as e:
            embed=ef.cembed(
                title="Error in yml embed",
                description=f"{traceback.format_exc()}",
                color=re[8],
                footer="Reporting this to the developer"
            )
            await ctx.send(
                embed=ef.cembed(
                    title="Error",
                    description=str(e),
                    footer="Reporting to developers",
                    color=re[8]
                )
            )
            await client.get_channel(dev_channel).send(
                embed=embed
            )
            return "Error"

    @client.command(aliases=['mehspace','mspace'])
    @commands.check(ef.check_command)
    async def myspace(ctx, member :discord.Member = None):
        if not member:
            if ctx.author.id in client.mspace: 
                await embed_using_yaml(ctx, channel = ctx.channel, yaml = client.mspace[ctx.author.id])
                return            
            else:
                await ctx.send(
                    embed = ef.cembed(
                        title="Oops",
                        description="You haven't set MehSpace yet, use the command m_setup to set up your Mehspace. It follows a similar pattern to yml_embed, Instructions for yml_embed is in help\n\n"+help_for_m_setup,
                        color=re[8],
                        thumbnail=client.user.avatar.url
                    
                    )
                )
            return
        if member.id in client.mspace:
            await embed_using_yaml(ctx,channel=ctx.channel,yaml=client.mspace[member.id])
            return
        

        await ctx.send(
            embed=ef.cembed(
                title="Oops",
                description="This user has not set their MehSpace yet",
                color=re[8],
                thumbnail=client.user.avatar.url
            )
        )

    def converter(a):
        if a.get('thumbnail'):
            a['thumbnail'] = a['thumbnail']['url']
        del a['type']
        if a.get('footer'):
            a['footer']=a['footer']['text']
        if a.get('image'):
            a['image']=a['image']['url']
        if a.get('color'):
            a['color']=str(discord.Color(a['color']).to_rgb())
        return a 

    @client.command(aliases = ['info'])
    @commands.check(ef.check_command)
    async def embedinfo(ctx):
        d = ctx.message.reference
        if not d:
            await ctx.send(
                embed=ef.cembed(
                    title="Hmm",
                    description="Reply to an embed message to continue",
                    color=re[8]
                )
            )
            return
        me = await client.get_channel(d.channel_id).fetch_message(d.message_id)
        if me.embeds == [] or not me.author.bot:
            await ctx.send(
                embed=ef.cembed(
                    title="Oops",
                    description="We found no embed in that message, check again and try",
                    color=re[8]
                )
            )
            return
        a = me.embeds[0].to_dict()
        a = converter(a)
        await ctx.send(
            embed=ef.cembed(
                title="Extracting Embed Information",
                description="```yml\n"+safe_dump(a)+"\n```",
                color=re[8],
                thumbnail=me.author.avatar.url
            )
        )
        

            
    @client.command(aliases = ['mehsetup','msetup'])
    @commands.check(ef.check_command)
    async def m_setup(ctx, *, yml = None):
        if yml:
            try:
                a = await embed_using_yaml(ctx,channel = ctx.channel, yaml = yml)
                #ctx, client, message, color=61620,usr=None
                confirm = await ef.wait_for_confirm(ctx,client,"Do you want to use this as your profile?",color=re[8],usr=ctx.author)
                if confirm and not a: client.mspace[ctx.author.id]=yml
            except Exception as e:
                await ctx.send(
                    embed=ef.cembed(
                        title="Error",
                        description=str(e),
                        color=re[8],
                        thumbnail=client.user.avatar.url
                    )
                )
        else:
            di = {}
            setup_value = None
            mai = await ctx.send(
                embed=ef.cembed(
                    description=f"Settings up MehSpace. You can choose from:\n"+'\n'.join(ef.m_options)+"\n\nType done or cancel to finish this\nsend #channel will send it to the channel\n\nType `-` to remove the setup value",
                    color=re[8],
                    footer=f"Follow this message along to setup | {ctx.author.name}"
                )
            )
            emb = await ctx.send(embed=ef.cembed(description='Empty Embed',color=re[8]))
            while True:
                try:                    
                    diff = ef.subtract_list(ef.m_options, list(di))
                    message = await client.wait_for("message", check = lambda m: m.author == ctx.author and m.channel == ctx.channel,timeout=720)                
                    msg = message.clean_content
                    if msg.startswith("send"):
                        channel_id = int(message.content.split()[1][2:-1])
                        channel = client.get_channel(channel_id)
                        if channel in ctx.guild.channels:     
                            if not channel.permissions_for(ctx.author).send_messages:
                                await ctx.send(
                                    embed=ef.cembed(
                                        title="Permissions Denied",
                                        description="You need to be able to send messages in that channel to send this embed",
                                        color=discord.Color.red(),
                                        thumbnail=client.user.avatar.url
                                    )
                                )
                                continue
                            await channel.send(
                                embed=embed_from_dict(di,ctx,client,re)
                            )
                        continue
                    if msg.lower() == "import":
                        if client.mspace.get(message.author.id):
                            di = safe_load('\n'.join([i for i in client.mspace[ctx.author.id].split("\n") if not i.startswith("```")]))
                            await emb.edit(
                                embed=embed_from_dict(di,ctx,client,re)
                            )
                        else:
                            await ctx.send("You do not have an existing mehspace")
                    elif msg.lower() in (ef.m_options+['done','cancel','send']):
                        if msg.lower() not in "cancel done send":
                            setup_value = msg
                            await emb.edit(
                                embed=ef.cembed(
                                    title="Setting up",
                                    description=f"Setting up {setup_value}" if setup_value!="send" else "mention the channel to send",
                                    color=re[8], thumbnail = client.user.avatar.url
                                )
                            )
                        elif msg.lower() == "cancel":
                            await ctx.send(
                                embed=ef.cembed(
                                    title="Cancelling",
                                    description="Deleting the embed formed till now",
                                    color=re[8]
                                )
                            )
                            break
                        else:                            
                            if di == {}:
                                await emb.edit(
                                    embed=ef.cembed(
                                        description=f"Your embed is empty\nYou can't save this\nSettings up MehSpace. You can choose from:\n"+'\n'.join(ef.m_options),
                                        color=re[8],
                                        footer=f"Follow this message along to setup | {ctx.author.name}"
                                    )
                                )
                            else:
                                confirm = await ef.wait_for_confirm(ctx,client,"Do you want to use this as your profile?",color=re[8],usr=ctx.author)
                                if confirm:
                                    s = "```yml\n"+safe_dump(di)+"\n```"
                                    client.mspace[ctx.author.id] = s
                                    te = await ctx.send("Finished Setting up mehspace")
                                    await asyncio.sleep(5)
                                    await te.delete()
                                    break
                                else:
                                    te = await ctx.reply("It's not saved but continue mehspace")
                                    await asyncio.sleep(5)
                                    await te.delete()
                                    
                    elif setup_value:       
                        
                        if msg == '-' and di.get(setup_value):
                            di.pop(setup_value)
                        elif msg.lower() == 'true' and setup_value.lower() == "author":
                            di[setup_value] ={
                                'name' : ctx.author.name,
                                'icon_url': ef.safe_pfp(ctx.author)
                            }
                        else:
                            di[setup_value] = msg

                        if di == {}:
                            di == {
                                'description': 'Empty Embed'
                            }
                        await emb.edit(
                            embed=embed_from_dict(di,ctx,client,re)
                        )                        
                    try:
                        await message.delete()  
                    except:
                        await mai.edit("Insufficient Permissions, you can continue, but the bot can't delete the message, which could potentially over crowd the chat, Keep an eye on the edits")
                except asyncio.TimeoutError:
                    await ctx.send(
                        embed=ef.cembed(
                            title="Timeout",
                            description="Sorry Discord will kill me if i wait longer",
                            color=client.re[8],
                            thumbnail=client.user.avatar.url
                        )
                    )
                    break
                except Exception as e:
                    causes = "\n\n`This can be caused because you gave author as something different(must only be True) or you didnt put the RGB values properly with commas. Must only be RGB`"
                    await ctx.send(
                        embed=__import__("error").error(str(e)+causes)
                    )
                    try:
                        di.pop(setup_value)
                    except:
                        pass
                    await client.get_channel(dev_channel).send(
                        embed=ef.cembed(
                            title="Error in mehsetup new",
                            description=str(traceback.format_exc()),
                            color=re[8],
                            footer=ctx.guild.name
                        )
                    )
                    
