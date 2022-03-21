from External_functions import cembed, defa


y = """
'yml_embed #channel
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


mod="""
You can choose to disable some of the sensitive commands or moderate your server using this

`'ban @mention `  
You can ban someone using this command
`'kick @mention`  
You can kick someone using this command, the user can return if he has the invite
`'mute @mention`  
Mutes a person
`'suicide      `  
Toggle suicide observation 
`'respond      ` 
Toggle auto response when you start with the word 'Alfred'
`'change_nickname @mention New name` 
Change the nickname of the person, <alias: '*'>
"""

effec = f"""
\n'effects <effect> <member> if member is none the users pfp will be modified \n The list of effects is \n- cartoonify \n- watercolor \n- canny \n- pencil \n- econify \n- negative \n- pen \n- candy \n- composition \n- feathers \n- muse \n- mosaic \n- night \n- scream \n- wave \n- udnie 
"""

def effects_helper():
    return defa(
        choices = [
            'cartoonify',
            'watercolor',
            'canny',
            'pencil',
            'econify',
            'negative',
            'pen',
            'candy',
            'composition',
            'feathers',
            'muse',
            'mosaic',
            'night',
            'scream',
            'wave',
            'udnie'
        ],
        default = None
    )

def help_him(ctx, client, re):

    thumbnail = client.user.avatar.url

    Emoji_help = cembed(
        title="Emojis",
        description="You can now get emojis from Alfred's servers using 'e <emoji_name> which will use webhook, you need to enable that permission if you havent, also it may affect when external emojis is not enabled for everyone, please check these, and then come to the support server. Also use 'clear_webhooks if webhooks are jammed\n\n",
        color=re[8],
        thumbnail=thumbnail,
        picture="https://copyrightalliance.org/wp-content/uploads/2017/07/emojis-cropped.png",
    )

    instagram_help = cembed(
        title="Instagram",
        description="Yes, you heard that right, if you give instagram account as parameter, it'll give you the latest post from instagram\n\nEx: 'instagram econhacksbangalore",
        color=re[8],
        thumbnail=thumbnail,
        picture="https://akm-img-a-in.tosshub.com/indiatoday/images/story/202106/photo-1611262588024-d12430b989_1200x768.jpeg?cKq2xcBMBm5eaadsXhYdeAAaFJXk5745&size=770:433",
    )

    reddit_help = cembed(
        title="Reddit",
        description="Alfred has reddit now, you can use the / command or 'reddit <account_name>",
        color=re[8],
        thumbnail=thumbnail,
        picture="https://play-lh.googleusercontent.com/MDRjKWEIHO9cGiWt-tlvOGpAP3x14_89jwAT-nQTS6Fra-gxfakizwJ3NHBTClNGYK4",
    )

    wolfram_help = cembed(
        title="Wolfram",
        description="I've added a simple API of Wolfram in Alfred, you can use it through 'wolf <expression>",
        thumbnail=thumbnail,
        picture="https://venturebeat.com/wp-content/uploads/2019/09/wolfram-alpha.png?fit=400%2C200&strip=all",
        color=re[8],
    )

    code_help = cembed(
        title="Code",
        description="You can execute programs from various programming languages\n\nEx: 'code <language>\n```\n#code here\n```",
        color=re[8],
        thumbnail=thumbnail,
        picture="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ8aYSfIp22UXBEkRt6vXwy4dmfhH3Q1lr8ow&usqp=CAU",
    )
    
    prefix_help = cembed(
        title="Set_Prefix",
        description="You can change the prefix of the bot for the server using set_prefix command.\nYou can also remove it using remove_prefix\n**Warning**: Only an admin can change",
        color=re[8],
        thumbnail=thumbnail,
        picture="https://i.kym-cdn.com/entries/icons/original/000/036/173/cover2.jpg"
    )
    
    music_help = cembed(
        title="Music commands",
        description="""You can use the following commands for controlling music
`Pause, Resume` does.... well pause and resume
`Play` command to play a song in your queue through index no. or you can put a song after that to play it instantly
`Queue` command to add a song to the queue
`Remove` command to remove a song from the queue
        """,
        thumbnail=thumbnail,
        color=re[8],
        picture="https://i.pinimg.com/originals/f1/90/97/f19097b29a4b606f8a91252fab526c6f.jpg",
        footer="Here's a little tip, when the bot says that this content is meant for only adults, search for the lyrics version of the song"
    )
    youtube_help = cembed(
        title="Youtube Subscribe to a channel",
        description="You can now add or make Alfred send you updates in the channel\n\nUse 'subscribe #channel https://www.youtube.com/c/LinusTechTips/videos to subscribe ",
        thumbnail=thumbnail,
        color=re[8],
        picture="https://play-lh.googleusercontent.com/vA4tG0v4aasE7oIvRIvTkOYTwom07DfqHdUPr6k7jmrDwy_qA_SonqZkw6KX0OXKAdk"
    )
    yaml_help = cembed(
        title="Yaml Embed tutorial",
        description=f"You can use this to create embed, I can show you an example\n\n{y}",
        color=re[8],
        thumbnail=thumbnail,
        picture="https://media.discordapp.net/attachments/877393101562445834/926120618603196416/unknown.png?width=391&height=436"
    )
    mod_help = cembed(
        title="Moderation commands",
        description=mod,
        color=re[8],
        thumbnail=thumbnail,
        picture="https://i.ytimg.com/vi/aN6Ywnwsahk/maxresdefault.jpg"
    )
    github_help = cembed(
        title="Source Code for Alfred",
        description="Here you go, click this link and it'll redirect you to the github page\n[Github page](https://github.com/alvinbengeorge/alfred-discord-bot)\n\nClick this link to invite the bot \n[Invite Link](https://discord.com/oauth2/authorize?client_id=811591623242154046&permissions=8&scope=bot%20applications.commands)",
        color=re[8],
        thumbnail="https://github.githubassets.com/images/modules/open_graph/github-octocat.png",
        picture=thumbnail,
    )
    first_page = cembed(
        title="Help",
        description="Hi I am Alfred. I was made by [Alvin](https://github.com/alvinbengeorge/).\nPrefix for this bot is '\n\nIf you have any complaints or issues with Alfred, please give us a feedback using the command `'feedback`",
        thumbnail="https://static.wikia.nocookie.net/newdcmovieuniverse/images/4/47/Pennyalf.PNG/revision/latest?cb=20190207195903",
        picture=thumbnail,
        color=re[8],
    )
    message_developer = cembed(
        title = "Message from the developers",
        description = "Hey guys, just wanted to say something about the bot, We just moved from discord.py to Nextcord, please check if there are some issues with the commands. You can report to us using the `'feedback` command, it's going to be fun.\n\nFor yml_embed, we kept little bit of Presets like\n```\n<server-icon>\n<author-icon>\n<bot-icon>\n<bot-color>\n```\n\nWe're moving to Slash command step by step, so keep watching that, it's going to be fun, and Thank you for choosing Alfred, I hope to see your irl, Good Bye, Check through this page btw to see more updates.",
        color=re[8],
        thumbnail=thumbnail,
        picture="https://www.whitesourcesoftware.com/wp-content/media/2021/05/aHViPTcyNTE0JmNtZD1pdGVtZWRpdG9yaW1hZ2UmZmlsZW5hbWU9aXRlbWVkaXRvcmltYWdlXzVlMjA1MWQxOWY2NTUuanBnJnZlcnNpb249MDAwMCZzaWc9NGJhMDhmZWU5ZDQ4ZGVjNjcwNzFlNmFhMDg3NzliNzA3D.jpeg"
    )
    effects_help = cembed(
        title="Effects",
        description="This command will apply effects to your Profile Picture, Use it by `'effects <effect name> @mention`"+effec,
        color=re[8],
        thumbnail=thumbnail,
        image="https://github.com/alvinbengeorge/alfred-discord-bot/blob/main/Krypton.png?raw=true"
    )
        

    return [first_page, github_help, message_developer, effects_help, music_help, mod_help, yaml_help, reddit_help, wolfram_help, code_help, Emoji_help, prefix_help, youtube_help, instagram_help]

neofetch="""
  *(&@&&%%##%%&%                                                .%&%###%%&&&%/, 
       ..,*/*/(%%                                              *%#(**/*,..      
          ..,*//(#%%.                /,*/,*.                /%%#(/*,..          
             ..,//**/#%%%&&%#(((((%&&&####%&&&#(((((#%&&%%#(***//,..            
               ......,,,**/(##%#**/((/#%%%//((/*/#%#(//**,,......               
                             ....,****/**/****,,....                            
                                 ....,*,.,,,....                                
                                     .......                                    
                                                                                
"""