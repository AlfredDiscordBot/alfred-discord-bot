import nextcord
from External_functions import cembed, defa, safe_pfp
from assets import *

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
```diff
+ In description, if you do `[something](https://link.com)`, the word something becomes a hyperlink

+ You can use symbols like `*~|>` just like you do in your regular chat

+ Color should be in (R, G, B) format only, if you type `red` or `blue` or a hexcode, it will give error

+ Do not worry when you get the error, you can edit the same message if you're using yml, look at the given error, especially the bottom part of it, it'll point you in the right direction

+ For yml_embed, give a space after colon, could solve error, we still recommend trying msetup if you don't need fields, and learn to type yaml from google
```

**If you find the above method confusing, use the regular msetup, although I must warn that there's no fields implemented, plus no modification in the author space**

Type `'msetup` and follow along the message, type one of the options given in the first embed, `-` to remove the value,

It'll delete the message, and edit the second embed, you can see the changes there, follow along with it

`The above mentioned tips will be applicable to this also`
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
`'response      ` 
Toggle auto response when you start with the word 'Alfred'
`'change_nickname @mention New name` 
Change the nickname of the person, <alias: '*'>
`'clear OK <number defaults to 10>`
Clear <number> messages from a channel or thread
Will ask permission if it's more than 15
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
        required = True
    )

message_from = r"""
**Increased stability and improvement**
Alfred is much faster than ever before, even with more command and slash commands. Effects and Blend(image commands) is much better to interact with using slash command. Text in voice channel works more or less, you cant delete messages, you cant create webhooks like `'e <emoji>` command

**Running latest Nextcord version**
Alfred gets updates a lot quicker, and compatibility

**Added a new feature called wordcloud**
Wordcloud basically collects the messages specified *we do not store it anywhere*, and creates a picture with the words in it. Larger font means more you say that word.

**New PopCat Model**
Added a new free model from PopCat Community, PopCat is an amazing community with multiple **free** APIs squeezed into one and has been helpful in Alfred's development
"""

def help_him(client, re):
    thumbnail = client.user.avatar.url

    Emoji_help = cembed(
        title="Emojis",
        description="You can now get emojis from Alfred's servers using 'e <emoji_name> which will use webhook, you need to enable that permission if you havent, also it may affect when external emojis is not enabled for everyone, please check these, and then come to the support server. Also use 'clear_webhooks if webhooks are jammed\n\n",
        color=re[8],
        thumbnail=thumbnail,
        picture="https://copyrightalliance.org/wp-content/uploads/2017/07/emojis-cropped.png",
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
        picture="https://c.tenor.com/oHyLJOAYQBsAAAAC/gotham-knights-dc.gif"
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
        picture="https://pbs.twimg.com/tweet_video_thumb/FNGjh0zXIAMRyxA?format=jpg&name=large",
    )
    first_page = cembed(
        title="Help",
        description="Hi I am Alfred. I was made by [Alvin](https://github.com/alvinbengeorge/).\nPrefix for this bot is '\n\nIf you have any complaints or issues with Alfred, please give us a feedback using the command `'feedback`\nVote for me in [top.gg](https://top.gg/bot/811591623242154046/vote). Thank you\n\n||Here's a lil tip from the developers which you probably wont find in any other bots, edit a command and it'll run again||",
        thumbnail="https://static.wikia.nocookie.net/newdcmovieuniverse/images/4/47/Pennyalf.PNG/revision/latest?cb=20190207195903",
        picture=thumbnail,
        color=re[8],
        footer="Have a great day | Best with slash command"
    )
    message_developer = cembed(
        title = "Message from the developers",
        description = message_from,
        color=re[8],
        thumbnail=thumbnail,
        picture = "https://raw.githubusercontent.com/nextcord/nextcord/master/assets/repo-banner.png",
        footer=f"Powered by Nextcord {nextcord.__version__}"
    )
    effects_help = cembed(
        title="Effects",
        description="This command will apply effects to your Profile Picture, Use it by `'effects <effect name> @mention`"+effec,
        color=re[8],
        thumbnail=thumbnail,
        image="https://raw.githubusercontent.com/alvinbengeorge/alfred-discord-bot/default/Krypton.png"
    )
    
    social_help=cembed(
        title="Socials",
        description="`'reddit <account>` for reddit posts\n`'instagram <account>` for 7 latest instagram postst\n`'quote` gives a random quote\n`'mehspace @mention` will give a person's mehspace\n`/subscribe` command for subscribing to a channel\n`/unsubscribe` command to unsubscribe from a channel\n\nIf you need to learn to setup mehspace, go to  the `Yaml help page`",
        color=re[8],
        image="https://media.smallbiztrends.com/2022/01/social-audio.png"
    )
    games_help = cembed(
        title="Games",
        description="This is a new feature in Alfred.\nAlfred currently has two new games\n```diff\n+ RockPaperScissor\n+ Guess\n```\n\nNote that `Guess` is not written in the regular prefix command anymore as we're shifting to slash commands",
        color=re[8],
        footer="More games coming soon",
        image="https://c.tenor.com/_yS6EXe8Tc0AAAAC/gotham-knights-dc.gif"
    )
        

    all_embeds = [first_page, github_help, message_developer, effects_help, music_help, games_help, mod_help, yaml_help, code_help, wolfram_help, Emoji_help, social_help]
    
    new_embeds = []
    for i in all_embeds:
        i.set_author(name = client.user.name, icon_url = client.user.avatar.url, url = "https://www.github.com/alvinbengeorge/alfred-discord-bot")
        new_embeds.append(i)
    return new_embeds

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
