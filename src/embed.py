"""
embed.py
Clases and functions 

Author: Yash Pawar
Originally Written: 06 October 2021
Last Edited: 06 October 2021
"""

from typing import Optional 
from typing import Union
from .utils import insensitive_dict, is_valid_url

DEFAULT_COLOR = (48, 213, 200)

class EmbedInfo: 
    def __init__(
        self, 
        title: str = None,
        description: str = None,
        url: str = None,
        thumbnail: str = None,
        image: str = None,
        footer: str = None,
        author: Union[str, dict] = None,
        color: Union[tuple, int] = DEFAULT_COLOR,
        fields: list = None,
    ):
        self.embed_dict = {"base":{}}

        self.set_title(title)
        self.set_description(description)
        self.set_url(url)
        self.set_thumbnail(thumbnail)
        self.set_image(image)
        self.set_footer(footer)
        self.set_author(author)
        self.set_color(color)
        self.set_fields(fields)

    def set_title(self, title: str = None) -> None:
        """
        Set the title of the Embed
        :param title: string title of the embed
        """
        self.embed_dict["base"]["title"] = title

    def set_description(self, description: str = None) -> None: 
        """
        Set the Description of the Embed
        :param description: string description of the embed
        """
        self.embed_dict["base"]["description"] = description

    def set_footer(self, footer: str = None) -> None: 
        """
        Set the Footer of the Embed
        :param footer: string footer of the embed
        """
        self.embed_dict['footer'] = footer

    def set_url(self, url: str = None) -> None:
        """
        Set URL for the Embed, if url is valid
        :param url: string URL of the embed
        """
        url = (url or " ").strip()
        if is_valid_url(url):
            self.embed_dict["base"]["url"] = url
        else:
            raise ValueError("URL for embed URL is not valid.")

    # TODO: add svg support to images
    def set_thumbnail(self, thumbnail_url: str = None) -> None:
        """
        Set Thumbnail for the embed
        :param thumbnail_url: url for thumbnail
        """
        url = (thumbnail_url or " ").strip()
        if is_valid_url(url):
            self.embed_dict['thumbnail'] = url
        else:
            raise ValueError("URL for embed thumbnail is not valid.")
    
    def set_image(self, image_url: str = None) -> None:
        """
        Set image for the embed
        :param thumbnail_url: url for thumbnail
        """
        url = (image_url or " ").strip()
        if is_valid_url(url):
            self.embed_dict['image'] = url
        else:
            raise ValueError("URL for embed image is not valid.")

    def set_color(self, color: Union[tuple, int] = DEFAULT_COLOR) -> None:
        """
        Set Color for the embed
        :param color: tuple of rgb values or int 
        """
        if type(color) == tuple:
            color = int(f"{color[0]:02x}:{color[1]:02x}:{color[2]:02x}", 16)
        
        self.embed_dict["base"]["color"] = color
    
    #TODO: functionlaity for author = True
    def set_author(self, author):
        """
        Set author for the embed.
        :param author: name or name and url for avatar
        """
        if type(author) == str:
            self.embed_dict["author"] = {"name": author}
        else:
            self.embed_dict["author"] = {"name": author["name"], "icon_url": author["icon_url"]} # TODO: add aliases for icon_url

    def set_fields(self, fields: list = []) -> None:
        """
        Set fields for the embed
        :param fields: list of the fields the embed should have
        """
        self.embed_dict["fields"] = [self._set_field(field) for field in fields]

    def _set_field(self, field: dict) -> dict:
        """
        Return dict of a field
        """
        try:
            return { 
                "name": field["name"],
                "value": field["value"],
                "inline": field.get("inline", True)
            } 
        except KeyError:
            raise ValueError("Missing Name or Value for field")

    def __dict__(self) -> dict:
        """
        Convert the class to dictionary
        """
        return self.embed_dict
