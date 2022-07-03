import nextcord
import traceback
import asyncio
import External_functions as ef
from nextcord.ext import commands
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
    elif col := map(int, ef.delete_all(color,"()").split(",")):
        return nextcord.Color.from_rgb(*col)

    return default_color

def converter(a):
    if a.get('thumbnail'):
        a['thumbnail'] = a['thumbnail']['url']
    del a['type']
    if a.get('footer'):        
        if a['footer'].get('proxy_icon_url'):
            del a['footer']['proxy_icon_url']
        if list(a['footer'].keys()) == ['text']:
            a['footer'] = a['footer']['text']
    if a.get('image'):
        a['image']=a['image']['url']
    if a.get('color'):
        a['color']=str(nextcord.Color(a['color']).to_rgb())
    if a.get('author'):
        if a['author'].get('proxy_icon_url'):
            del a['author']['proxy_icon_url']
    return a 
    
def preset_change(di, ctx, client):
    user = getattr(ctx, 'author', getattr(ctx,'user',None))
    presets = {
        '<server-icon>' : getattr(ctx.guild.icon, 'url', None),
        '<author-icon>' : ef.safe_pfp(user),
        '<author-color>': str(user.color.to_rgb()),
        '<bot-icon>' : client.user.avatar.url,
        '<bot-color>' : str(nextcord.Color(client.re[8]).to_rgb())
    }
    if isinstance(di, str):
        di = {
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
    except MissingSchema:
        return False

def embed_from_dict(info: dict, ctx, client) -> nextcord.Embed:
    """
    Generates an embed from given dict
    """
    if info == {}: info = {
        'description': 'Nothing to Embed',
        'color': str(nextcord.Color(client.re[8]).to_rgb())
    }
    info = preset_change(info, ctx, client)
    ctx_author = getattr(ctx, 'author', getattr(ctx,'user',None))
    info = {k.lower(): v for k, v in info.items()}  # make it case insensitive
    info["color"] = get_color(info.get("color", None))
    if info['color']: info['color']=info['color'].value         
    return ef.cembed(**info)

def yaml_to_dict(yaml):
    try:
        a = safe_load(yaml)
        return a
    except:
        return yaml

class MSetup:
    def __init__(self, ctx, client):
        self.ctx = ctx
        self.client = client
        self.di = {}
        self.EDIT_MESSAGE = None
        self.INSTRUCTION = None
        self.OPTIONS = ef.m_options
        self.SETUP_VALUE = None
        self.presets = [
            '<server-icon>',
            '<author-icon>',
            '<bot-color>',
            '<bot-icon>',
            '<author-color>'
        ]

    def set_preset(self):
        self.di = preset_change(self.di, self.ctx, self.client)

    async def send_instructions(self):
        description="Welcome to Msetup, you can select from these options down below\n```diff\nSETUP VALUES:\n"
        for i in self.OPTIONS:
            if i in self.di:
                description+="\n- "
            else:
                description+="\n+ "
            description+=i
        description+="\n```\n\nSeperate Fields heading and body with >, and adding new field with two extra lines\n`Heading> Body here`\n\nSeperate footer text and icon_url with |>\n`Footer text|> <server-icon>`\n\n```\nYour First time? Start off with typing 'title', you will see the embed changing in the bottom, follow accordingly\n```\nColor input is only in (R, G, B) for now, will bring more options soon"
        embed=ef.cembed(
            title="MehSetup Instructions",
            description=description,
            color=self.client.re[8],
            thumbnail=self.client.user.avatar.url,
            footer="Have Fun"
        )
        if self.INSTRUCTION:
            await self.INSTRUCTION.edit(
                embed=embed
            )
        else:
            self.INSTRUCTION = await self.ctx.send(
                embed=embed
            )
        if not self.EDIT_MESSAGE:
            self.EDIT_MESSAGE = await self.ctx.send(
                embed=embed_from_dict(self.di, self.ctx, self.client)
            )
        else:
            await self.EDIT_MESSAGE.edit(
                embed=embed_from_dict(self.di, self.ctx, self.client)
            )
        
    def to_yaml(self):
        '''
        converts to yaml
        '''
        self.set_preset()
        return "```yml\n"+safe_dump(self.di)+"\n```"

    async def imp(self, msg):
        '''
        import from a message
        '''
        if len(msg.embeds) == 0:
            await self.ctx.send("I see no embed in that message", delete_after = 5)
            return
        self.di = converter(msg.embeds[0].to_dict())     
        return self.to_yaml()
        

    def footer(self, text):
        '''
        processes Footer to text to str or dict
        '''
        footer = text.split("|>")
        
        if len(footer) > 1 and not (validate_url(footer[1]) or footer[1] in self.presets):
            return text
            
        elif len(footer) > 1:
            return {
                'text': footer[0].strip(),
                'icon_url': footer[1].strip()
            }
            
        else:
            return text

    def fields(self, text):
        '''
        processes field text to list of dicts
        '''
        f = [i.split(">") for i in text.split("\n\n")]
        all_fields = []
        for i in f:
            if len(i) != 2:
                all_fields.append(
                    {
                        'name': 'Heading',
                        'value': '>'.join(i)
                    }
                )
            else:
                fi = {
                    'name': i[0],
                    'value': i[1]
                }
                if fi['name'].endswith("-"):
                    fi['name'] = fi['name'][:-1]
                    fi['inline'] = False
                all_fields.append(fi)
        return all_fields

    def author(self, text):
        return {
            'name': self.ctx.author.name,
            'icon_url': ef.safe_pfp(self.ctx.author)
        }

    async def process_message(self, msg):
        '''
        Send the message here and the class will automatically do it's work :)
        Should only be passes after `send_instructions |coro|`
        '''
        text = msg.content
        if not any(map(text.startswith, ['send','done','cancel'])):
            await msg.delete()
        
        if text in self.OPTIONS:
            self.SETUP_VALUE = text.lower()
            await self.EDIT_MESSAGE.edit(
                embed=ef.cembed(
                    title=f"Editing {text}",
                    description=f"Currently editing {text}, please follow the syntax from the instruction page",
                    color=self.client.re[8],
                    thumbnail=self.client.user.avatar.url                    
                )
            )
            
            self.set_preset()
            return self.to_yaml()

        if text.lower() == "import":
            if msg.reference:
                impor = await self.ctx.channel.fetch_message(
                    msg.reference.message_id
                )
                await self.imp(impor)
            elif msg.author.id in self.client.mspace:
                self.di = safe_load(filter_graves(self.client.mspace[msg.author.id]))
                
            else:
                await self.ctx.send(
                    "You have no mehspace, if you want to import from a message, reply to the message",
                    delete_after = 5
                )
                
        elif any(map(text.startswith, ['send','done','cancel'])):
            return self.to_yaml()
            
        elif self.SETUP_VALUE:   
            if text == "-" and self.di.get(self.SETUP_VALUE):
                del self.di[self.SETUP_VALUE]
                await self.send_instructions()
                return
            output = text
            print(self.SETUP_VALUE)
            if self.SETUP_VALUE == "footer":
                output = self.footer(text)
            if self.SETUP_VALUE == "fields":
                output = self.fields(text)
            if self.SETUP_VALUE == "author":
                output = self.author(text)
            self.di[self.SETUP_VALUE] = output
            self.set_preset()                            
        
            
        else:
            await self.ctx.send("Please type a setup value from the instructions", delete_after = 5)
            self.set_preset()
        await self.send_instructions()
        return self.to_yaml()
        
        
        


class Embed(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.old_messages = {}

    @commands.command()
    async def msetup1(self, ctx):
        session = MSetup(ctx, self.client)
        await session.send_instructions()
        scd = [
            'send',
            'cancel',
            'done'
        ]
        
        while True:
            try:
                message = await self.client.wait_for(
                    "message",
                    check = lambda m: all([
                        m.author == ctx.author,
                        m.channel == ctx.channel
                    ])
                )
                await session.process_message(message)
                
                if any(map(message.content.lower().startswith, scd)):
                    embed = embed_from_dict(session.di, ctx, self.client)
                    text = message.content
                    
                    if text.lower() == "done":
                        confirm = await ef.wait_for_confirm(ctx, self.client, "Do you want to set this as your mehspace?", color=self.client.re[8])
                        
                        if confirm:
                            self.client.mspace[ctx.author.id] = session.to_yaml()
                            await ctx.send("Done")
                            break
                            
                        await ctx.send("Continue, mehspace is not set")
                        continue

                            
                    if text.lower() == "cancel":
                        await ctx.send("Cancelled")
                        return

                    if text.lower().startswith("send"):
                        if validate_url(text[5:]):
                            print("URL detected")
                            await ef.post_async(text[5:], json={'embeds':[embed.to_dict()]})
                            await ctx.send("Done")
                            continue
                        if self.client.get_channel(int(text[7:-1])):
                            channel = self.client.get_channel(int(text[7:-1]))
                            print(channel)
                            if channel.permissions_for(ctx.author).send_messages:
                                if channel.permissions_for(ctx.guild.me).send_messages:
                                    await channel.send(
                                        embed=embed
                                    )
                                else:
                                    await ctx.send("Bot doesnt have enough permissions", delete_after = 5)
                                    continue
                            else:
                                await ctx.send("You dont have permission to send messages there")       
                        
                        
            except asyncio.TimeoutError:
                await ctx.send(
                    embed=ef.cembed(
                        title="Sorry",
                        description="Timed out, Discord will kill me if i wait longer",
                        color=self.client.re[8],
                        thumbnail=self.client.user.avatar.url
                    )
                )    
                break
            except:
                print(traceback.format_exc())

    @commands.command()
    @commands.check(ef.check_command)
    async def yml_embed(self, ctx, channel: Union[nextcord.TextChannel, str, nextcord.threads.Thread], *, yaml = None):
        embed = embed_from_dict(
            yaml_to_dict(filter_graves(yaml)),
            ctx, self.client
        )
        if isinstance(channel, (nextcord.TextChannel, nextcord.threads.Thread)):
            await channel.send(embed=embed)
        elif validate_url(channel):
            data = embed.to_dict()
            await ef.post_async(channel, json={'embeds':[data]})
        elif channel.lower() == "mehspace":
            if yaml:
                await ctx.send(embed=embed)
                confirm = await ef.wait_for_confirm(ctx, self.client, "Do you want to use this as your profile?", color=self.client.re[8], usr=ctx.author)
                if confirm:
                    self.client.mspace[ctx.author.id]  = yaml
            else:
                await ctx.send(
                    embed = embed_from_dict(
                        yaml_to_dict(filter_graves(yaml)),
                        ctx, self.client
                    )
                )
        else:
            await ctx.send("Invalid channel or URL form")

    @nextcord.user_command(name="mehspace")
    async def meh(self, inter, member):
        if member.id not in self.client.mspace:
            await inter.send("The user has not set mehspace", ephemeral = True)
            return
        yaml = filter_graves(self.client.mspace[member.id])
        di = yaml_to_dict(yaml)
        embed=embed_from_dict(
            di,
            inter, self.client
        )
        await inter.send(embed=embed)

    @nextcord.slash_command(name="mehspace",description="Show Mehspace of someone")
    async def mehspace(self, inter, user: nextcord.User = None):
        if not user: user = inter.user
        if user.id not in self.client.mspace:
            await inter.response.send_message(
                embed=ef.cembed(
                    title="Unavailable",
                    description="This user has not set mehspace",
                    color=self.client.re[8],
                    thumbnail="https://www.cambridge.org/elt/blog/wp-content/uploads/2019/07/Sad-Face-Emoji-480x480.png.webp"
                )
            )
            return
        await inter.response.send_message(
            embed=embed_from_dict(
                yaml_to_dict(
                    filter_graves(self.client.mspace[user.id])
                ),
                inter, self.client
            )
        )

    @nextcord.slash_command(name="embed",description="Create your embed using this")
    async def em(self, inter, description, title = None, color = "(1,1,1)", thumbnail = None, image = None, footer = None, author:nextcord.Member = None):
        await inter.response.defer()       
        try:
            d = {
                'description' : description,
                'color': color,
            }
            if author:
                d['author'] = {
                    'name' : author.name,
                    'icon_url' : ef.safe_pfp(author)
                }
            if image:
                d['image'] = image
            if thumbnail:
                d['thumbnail'] = thumbnail
            if footer:
                d['footer'] = footer
            if title:
                d['title'] = title
    
            embed = embed_from_dict(d, inter, self.client)
            await inter.send(embed=embed)
        except:
            print(traceback.format_exc())
            await inter.send(
                embed=ef.cembed(
                    title="Oops",
                    description="Something is wrong",
                    color=self.client.re[8]
                )
            )

    @nextcord.message_command(name="embedinfo")
    async def embedinfo(self, inter, message):
        if len(message.embeds) == 0:
            await inter.send("I see no embed here",  ephemeral = True)
            return

        e = message.embeds[0].to_dict()
        
        await inter.send(
            embed=ef.cembed(
                title="EmbedInfo",
                description=f"```yml\n{safe_dump(converter(e))}\n```",
                color=self.client.re[8],
                thumbnail=self.client.user.avatar.url
            ),
            ephemeral = True
        )
        
    @commands.command(name="embedinfo")
    async def embedi(self, ctx):
        if not ctx.message.reference:
            await ctx.send("Reply to a message")
            return
        message = await ctx.channel.fetch_message(
            ctx.message.reference.message_id
        )
        if len(message.embeds) == 0:
            await ctx.send("I see no embed here")
            return

        e = message.embeds[0].to_dict()

        await ctx.send(
            embed=ef.cembed(
                title="EmbedInfo",
                description=f"```yml\n{safe_dump(converter(e))}\n```",
                color=self.client.re[8],
                thumbnail = self.client.user.avatar.url
            )
        )
    


def setup(client,**i):
    client.add_cog(Embed(client,**i))
