"""
embed.py
Clases and functions 

Author: Yash Pawar
Originally Written: 06 October 2021
Last Edited: 06 October 2021
"""

from typing import Optional
from dataclasses import dataclass 
from .utils import insensitive_dict

@dataclass(init=True, repr=True)
class Field:
    name: str
    value: str
    inplace: Optional[bool] = True

    @classmethod
    def from_dict(cls, field: dict):
        try:
            field = insensitive_dict(field)
            cls(
                name = field['name'],
                value = field['value'],
                inline = field.get('inline', True)
            )

        except KeyError:
            raise ValueError("Missing name or value for field")
