"""
Language functools.
"""


def alpha2(lang: str) -> str:
    """
    Returns the alpha-2 version of an expanded idb lang, like from 'en-US' into 'en'

    :param lang: idb version of the lang

    :return: alpha-2 version of the lang
    """
    return None if not lang else lang[:2]
