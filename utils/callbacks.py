# To use this extra functionality, you need to contribute to alfred
# Basic way to add functions is by creating a function starting with the name `callback_ID`
# These are async functions, and all these callback functions will accept `nextcord.Interaction`
# There will be no global defining, and we will check this file in PR, and we will only accept Pull Request to `development` branch
# Have fun, and this is only contributor function
# To the person who is contributing, only that person's ID is allowed and no other changes
# Inside the function, `docstring` must be provided as the button name

import sys
import nextcord

from nextcord.ui import Button, button, View
from .External_functions import cembed, get_all_slash_commands
from .assets import pa


def functions(*args, **kwargs):
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
    Profile
    """

    await get_all_slash_commands(inter.client)["code"].children["github"].children[
        "user"
    ].callback(inter.client.cogs["Code"], inter, "alvinbengeorge")
