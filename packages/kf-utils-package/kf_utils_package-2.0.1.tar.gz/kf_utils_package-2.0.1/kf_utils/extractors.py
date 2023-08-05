"""
File:               extractors.py
Description:        Helpers for advance extraction of substrings.
Created on:         16-Sept-2022 12:46:38
Original author:    SEMBU-Team NTTData
"""
import re


def extract_angled(txt: str) -> list:
    """
    Extracts text between < and >.

    Copes with the situation:
        var_name = 1 > 2 .

    :param txt: txt to be analysed

    :return: extracted parts listed
    """
    rex = rf'<(.*?)>'  # This works well with <>
    ret = re.findall(rex, txt)
    return ret


def extract_between_parenthesis(txt: str) -> list:
    """
    Extracts text between '(' and ')'

    :param txt: text to be analysed

    :return: extracted parts listed
    """
    return extract_between_delimiters(txt, '(', ')')


def extract_between_delimiters(txt: str, left: str, right: str) -> list:
    """
    Extracts text between any left char and right car.

    BEWARE THAT the last right char is included and needs to be removed

    :param txt: text to be analysed
    :param left: left delimiter
    :param right: right delimiter

    :return: extracted parts listed
    """
    rex = rf'\{left}(.*?)\{right}'
    ret = re.findall(rex, txt)
    ret = [r.strip(right) for r in ret]
    return ret


def extract_quoted(quoted_txt: str, exclude: str = None) -> list:
    """
    Extracts text between double or single quotes unless it equals the 'exclude' text.

    :param quoted_txt: quoted text to be analysed
    :param exclude: text to exclude. By default, it is set to None

    :return: extracted parts listed
    """
    exclude = '' if not exclude else exclude

    ret_1 = extract_double_quoted(quoted_txt, exclude)
    ret_2 = extract_single_quoted(quoted_txt, exclude)
    return ret_1 + ret_2


def extract_double_quoted(quoted_txt: str, exclude: str = None) -> list:
    """
    Extracts text between double quotes unless it equals the 'exclude' text.

    :param quoted_txt: double-quoted text to be analysed
    :param exclude: text to exclude. By default, it is set to None

    :return: extracted parts listed
    """
    exclude = '' if not exclude else exclude
    rex = r"\"(.*?)\""
    ret = re.findall(rex, quoted_txt)
    ret = [ret for ret in ret if ret != exclude]
    return ret


def extract_single_quoted(quoted_txt: str, exclude: str = None) -> list:
    """
    Extracts text between single quotes unless it equals the 'exclude' text.

    :param quoted_txt: single-quoted text to be analysed
    :param exclude: text to exclude. By default, it is set to None

    :return: extracted parts listed
    """
    exclude = '' if not exclude else exclude
    rex = r"\'(.*?)\'"
    ret = re.findall(rex, quoted_txt)
    ret = [ret for ret in ret if ret != exclude]
    return ret
