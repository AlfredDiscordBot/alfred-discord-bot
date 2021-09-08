def requirements():
    return "re"


def main(client, re):
    import discord
    import re as regex

    URL_REGEX = regex.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', regex.IGNORECASE)

    title_of_embed = {}
    color_of_embed = {}
    thumbnail_of_embed = {}
    description_for_embed = {}
    footer_of_embed = {}
    image={}

     # add helper functions for embed megafunction
    def validate_url(url:str) -> bool:
        """
        Checks if the given url is valid or not.
        """
        return regex.match(URL_REGEX, url) is not None

    def split_md(md:str) -> dict:
        """
        splits the given markdown into a dictionary.
        """
        info = {
            "color": "(48,213,200)",
            "image": '',
            'title': '',
            "thumbnail": '',
            "description": '',
            "footer": ''
        }
        try:
            split = md.split("\n\n")

            info["title"] = split[0]

            info['thumbnail'] = split[1] if validate_url(split[1]) else ''

            info['description'] = split[1] if info['thumbnail'] == '' else split[2]

            try:
                info['image'] = split[3] if validate_url(split[1]) else ''
            except:
                pass

            try:
                info['footer'] = split[3] if info['image'] == '' else split[4]
            except:
                pass
        except Exception as e:
            print(e) # maybe make an error embed here...

        return info

    @client.command(aliases=["init_embed", "embed_init"])
    async def create_embed_init(ctx):
        re[0]+=1
        if (
            ctx.author.guild_permissions.manage_messages
            or ctx.author.id == 432801163126243328
        ):
            title_of_embed.pop(ctx.guild.id)
            color_of_embed.pop(ctx.guild.id)
            thumbnail_of_embed.pop(ctx.guild.id)
            description_for_embed.pop(ctx.guild.id)
            footer_of_embed.pop(ctx.guild.id)
            image.pop(ctx.guild.id)

    @client.command()
    async def embed_it(ctx,*,string):        
        info=split_md(string)
        req[0]+=1
        if info['title']!='':
           title_of_embed[ctx.guild.id]=info['title'] 
        if info['description']!='':
            description_for_embed[ctx.guild.id]=info['description']
        if info['thumbnail']!='':
            thumbnail_of_embed[ctx.guild.id]=info['thumbnail']
        if info['footer']!='':
            footer_of_embed[ctx.guild.id]=info['footer']
        if info['image']!='':
            image[ctx.guild.id]=info['image']
        c=eval(info['color'])
        print(c,type(c))
        color_of_embed[ctx.guild.id]=discord.Color.from_rgb(*c)
        await ctx.send(embed=discord.Embed(description="Done",color=discord.Color(value=re[8])))
        


    @client.command(aliases=["color_for_embed"])
    async def set_color(ctx, color):
        if (
            ctx.author.guild_permissions.manage_messages
            or ctx.author.id == 432801163126243328
        ):
            try:
                c = eval(color)
                req[0]+=1
                color_of_embed[ctx.guild.id] = discord.Color.from_rgb(*c)
                await ctx.send(
                    embed=discord.Embed(
                        description="Color Set", color=discord.Color(value=re[8])
                    )
                )
            except Exception as e:
                await ctx.send(str(e))

    @client.command(aliases=["title"])
    async def set_title(ctx, *, title):
        if (
            ctx.author.guild_permissions.manage_messages
            or ctx.author.id == 432801163126243328
        ):
            title_of_embed[ctx.guild.id] = title
            req[0]+=1
            await ctx.send(
                embed=discord.Embed(
                    description="Title Set", color=discord.Color(value=re[8])
                )
            )

    @client.command(aliases=["description"])
    async def set_description(ctx, *, description):
        if (
            ctx.author.guild_permissions.manage_messages
            or ctx.author.id == 432801163126243328
        ):
            description_for_embed[ctx.guild.id] = description
            req[0]+=1 
            await ctx.send(
                embed=discord.Embed(
                    description="Description Set", color=discord.Color(value=re[8])
                )
            )

    @client.command(aliases=["footer"])
    async def set_footer(ctx, *, footer):
        if (
            ctx.author.guild_permissions.manage_messages
            or ctx.author.id == 432801163126243328
        ):
            footer_of_embed[ctx.guild.id] = footer
            await ctx.send(
                embed=discord.Embed(
                    description="Footer Set", color=discord.Color(value=re[8])
                )
            )

    @client.command(aliases=["thumbnail"])
    async def set_thumbnail(ctx, url):
        if (
            ctx.author.guild_permissions.manage_messages
            or ctx.author.id == 432801163126243328
        ):
            thumbnail_of_embed[ctx.guild.id] = url
            await ctx.send(
                embed=discord.Embed(
                    description="Thumbnail Set", color=discord.Color(value=re[8])
                )
            )

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
                if ctx.guild.id in list(description_for_embed.keys()):
                    try:
                        embed = discord.Embed(
                            description=description_for_embed[ctx.guild.id]
                        )
                    except Exception as e:
                        await ctx.send(str(e))
                if ctx.guild.id in list(title_of_embed.keys()):
                    try:
                        embed.title = title_of_embed[ctx.guild.id]
                    except Exception as e:
                        await ctx.send(str(e))
                if ctx.guild.id in list(thumbnail_of_embed.keys()):
                    try:
                        embed.set_thumbnail(url=thumbnail_of_embed[ctx.guild.id])
                    except Exception as e:
                        await ctx.send(str(e))
                if ctx.guild.id in list(image.keys()):
                    try:
                        embed.set_image(url=image[ctx.guild.id])
                    except Exception as e:
                        await ctx.send(str(e))
                if ctx.guild.id in list(color_of_embed.keys()):
                    try:
                        embed.color = color_of_embed[ctx.guild.id]
                    except Exception as e:
                        await ctx.send(str(e))
                if ctx.guild.id in list(footer_of_embed.keys()):
                    try:
                        embed.set_footer(text=footer_of_embed[ctx.guild.id])
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
