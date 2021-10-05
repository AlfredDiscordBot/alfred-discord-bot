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

    return [Emoji_help, instagram_help, reddit_help, wolfram_help, code_help]
