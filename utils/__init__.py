from . import (
    assets,
    External_functions,
    helping_hand,
    inshort,
    spotify_client,
    Storage_facility,
    Trend,
)

ef = External_functions


class DEVOP:
    EMBED = {
        "title": "DEVOP",
        "description": "Powerful Control for Alfred, you can use this to save and restart alfred",
        "fields": {
            "Instructions": "⭕ for `Stats`\n💾 for `Save`\n❌ for `Exit`\n🔗 for `Invite link`\n📜for `Report`"
        },
        "footer": {
            "text": "Only Developers can access this function\nHave a good day Master Wayne",
            "icon_url": "https://cdn.discordapp.com/avatars/811591623242154046/18736ae6885bad04990795dff7acf2ad.png?width=664&height=664",
        },
    }


async def send_devop(CLIENT: ef.commands.Bot, channel: int, functions: dict):
    embed = DEVOP.EMBED
    embed["color"], embed["author"], embed["thumbnail"] = (
        CLIENT.re[8],
        CLIENT.user,
        CLIENT.user.avatar,
    )
    channel = CLIENT.get_channel(channel)
    await channel.delete_messages(
        [i async for i in channel.history(limit=100) if not i.pinned][:100]
    )
    return await channel.send(
        embed=ef.cembed(**embed), view=assets.DEVOPVIEW(CLIENT, functions=functions)
    )
