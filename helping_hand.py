from External_functions import cembed


def help_him(ctx, client, re):

    thumbnail = client.user.avatar_url_as(format="png")

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
        picture="https://techcrunch.com/wp-content/uploads/2015/04/codecode.jpg",
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
Pause, Resume
Play command to play a song in your queue through index no. or you can put a song after that to play it instantly
Queue command to add a song to the queue
Remove command to remove a song from the queue

~~*Spotify not supported yet :frowning:*~~
        """,
        thumbnail=thumbnail,
        color=re[8],
        picture="https://i.pinimg.com/originals/f1/90/97/f19097b29a4b606f8a91252fab526c6f.jpg"
    )
    youtube_help = cembed(
        title="Youtube Subscribe to a channel",
        description="You can now add or make Alfred send you updates in the channel\n\nUse 'subscribe #channel https://www.youtube.com/c/LinusTechTips/videos to subscribe ",
        thumbnail=thumbnail,
        color=re[8],
        picture="https://play-lh.googleusercontent.com/vA4tG0v4aasE7oIvRIvTkOYTwom07DfqHdUPr6k7jmrDwy_qA_SonqZkw6KX0OXKAdk"
    )
        

    return [Emoji_help, music_help, instagram_help, reddit_help, wolfram_help, code_help, prefix_help, youtube_help]
