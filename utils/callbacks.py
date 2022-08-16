# To use this extra functionality, you need to contribute to alfred
# Basic way to add functions is by creating a function starting with the name `callback_ID`
# These are async functions, and all these callback functions will accept `nextcord.Interaction`
# There will be no global defining, and we will check this file in PR, and we will only accept Pull Request to `development` branch
# Have fun, and this is only contributor function
# To the person who is contributing, only that person's ID is allowed and no other changes
# Inside the function, `docstring` must be provided as the button name

import sys
import nextcord

from .External_functions import get_all_slash_commands, wait_for_confirm
from .assets import pa


def get_callback_functions(*args, **kwargs):
    here = sys.modules[__name__]
    return {
        int(i.replace("callback_", "")): (
            getattr(here, i),
            getattr(here, i).__doc__.strip(),
        )
        for i in dir(here)
        if i.startswith("callback_")
    }


async def callback_432801163126243328(inter: nextcord.Interaction):
    """
    Github Profile
    """
    print(inter.user)
    await get_all_slash_commands(inter.client)["code"].children["github"].children[
        "user"
    ].callback(inter.client.cogs["Code"], inter, "alvinbengeorge")


async def callback_811591623242154046(inter: nextcord.Interaction):
    """
    Msetup
    """
    await get_all_slash_commands(inter.client)["msetup"].callback(
        inter.client.cogs["Embed"], inter
    )


async def callback_848551732048035860(inter: nextcord.Interaction):
    """
    Msetup
    """
    await callback_811591623242154046(inter)
