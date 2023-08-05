"""
Manipulation of lists.
"""
import typing


def duplicated(elements: list) -> bool:
    """
    Returns True if an element of a list contains duplicated elements, or False otherwise.

    :param elements: list to be analysed

    :return: whether the list contains duplicate elements
    """
    return len(elements) > len(set(elements))


def index(list_: list, pattern: str, case_insensitive: bool = True) -> typing.Union[int, None]:
    """
    Returns the position of an string element in a list or None if not found.

    :param list_: the list to look up into;
    :param pattern: the string to find within the list;
    :param case_insensitive: if True the search does not care about the case of the pattern;

    :return: the position of the pattern, an integer, or None if not found.
    """
    try:
        s = f'v.upper() == "{pattern}".upper()' if case_insensitive else f'v == "{pattern}"'
        return next(i for i, v in enumerate(list_) if eval(s))
    except StopIteration:
        return None


def ordered_set(items: list) -> list:
    """
    Removes duplicate items from a list without altering the occurrence order. Faster than OrderedDict.

    :param items: list of items to order and remove duplicate

    :return: the given list without duplicate items
    """
    return list(dict.fromkeys(items))


def remove_duplicates(vector: list) -> list:
    """
    Removes duplicated elements from a list

    :param vector: list of items

    :return: list without duplicate items
    """
    return [i for n, i in enumerate(vector) if i not in vector[:n]]
