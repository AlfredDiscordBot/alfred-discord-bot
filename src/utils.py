"""
utils.py
this code has the utility functions to be used by other modules in src

Author: Yash Pawar
Originally Written: 06 October 2021
Last Edited: 06 October 2021
"""

def insensitive_dict(sensitive_dict: dict) -> dict:
    """
    Convert a case sensitive dictionary into a case insensitive dictionary.

    :param sensitive_dict: the dictionary which is to be make insensitive.
    """
    return { k.lower(): v for k, v in sensitive_dict.items() }
