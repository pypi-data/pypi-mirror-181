"""
functools for the manipulation of strings.
"""
import json
import os
import re
import typing

import unidecode

from . import hashers, extractors, replacers, files


def indices(txt: str, key: str, case_sensitive: bool = True) -> list[int]:
    """
    Searches a string (the key) in a text and returns a list with all the positions where the key occurs.

    :param txt: text where to search
    :param key: substrings to search inside the text
    :param case_sensitive: whether the search is case-sensitive. By default, it is set to True

    :return: list with all the positions where the key occurs in the given text
    """
    key = key.lower() if not case_sensitive else key
    txt = txt.lower() if not case_sensitive else txt
    return [i.start() for i in re.finditer(key, txt)]


def is_get_list(o: typing.Union[list, str], dic: dict = None) -> typing.Union[list, None]:
    """
    Determines whether a text is a valid Python's list.
    NOTE: 'is_get_' methods have a twofold mission:
        1. they check that a condition is met, and
        2. if the condition is met then return a value.

    In this case, the condition to be met is that the text is a
    valid Python list expressed as a text. The value returned is
    the Python's list.

    :param o: list or list-style string
    :param dic: a dictionary with all the variables needed for the Python interpreter to execute the code; if not
        provided, the presumption is that the statement to be executed is a primitive of the type x = 1 + 2, b = True,
        h = "Hello World", or similar. By default, it is set to None.

    :return: list with the o param content
    """
    if isinstance(o, list):
        return o
    elif isinstance(o, str):
        try:
            dic = dict() if dic is None else dic
            line = f'l_ = {o.strip()}'
            exec(line, dic)
            ret = dic.get('l_')
            dic.pop('l_')
            return ret if isinstance(ret, list) else None
        except Exception as ex:
            raise ex
    else:
        raise AttributeError

def json_str_to_dict(json_line: str) -> dict:
    """
    Used to read JSON objects expressed as texts and transform them into Python's dictionaries.
    One usage of this method is to read JSONL files and process the contents, e.g. to store these
    contents into NO-SQL databased, such as in an Elasticsearch index as Elastic documents.

    :param json_line: json-style string

    :return: Python's dictionary with the json content
    """

    try:
        return json.loads(json_line)
    except Exception as ex:
        raise Exception("FAILED: An exception was cast while trying to cast a JSON str line into a Python dict. "
                        f"The original exception thrown by the json library follows: {ex}")


def mask_quoted(quoted_txt: str) -> (str, list[tuple[str, str]]):
    """
    Extracts quoted substrings from a quoted text, masks (i.e., codes) the substrings and returns
    the masked text and a list of tuples with the pairs [(original substring, masked substring), ...]

    :param quoted_txt: text that contains quoted substrings

    :return: masked text and a list of tuples with the pairs [(original substring, masked substring), ...]
    """
    tuples = [(f'"{sbs}"', f'"{hashers.scrc(sbs)}"') for sbs in extractors.extract_double_quoted(quoted_txt)]
    tuples += [(f"'{sbs}'", f"'{hashers.scrc(sbs)}'") for sbs in extractors.extract_single_quoted(quoted_txt)]
    masked_txt = replacers.replace_substrings(quoted_txt, tuples) if bool(tuples) else quoted_txt
    return masked_txt, tuples


def unmask_quoted(masked_txt: str, tuples: list[tuple[str, str]]) -> str:
    """
    For a given text, and a list of pairs (substring, crc(substring)), replaces previously masked substrings
    into their original forms.

    :param masked_txt: masked text returned by mask_quoted method.
        Please refer to mask_quoted method documentation.
    :param tuples: list of tuples with the pairs [(original substring, masked substring), ...]

    :return: original text with its previously masked substrings replaced into their original forms
    """
    return replacers.replace_substrings(masked_txt, [(t[1], t[0]) for t in tuples])


def nnl(text: str) -> str:
    """
    Replaces all new lined '\n' with ' '

    :param text: text with new lines

    :return: text without new lines
    """
    return text.replace("\n", " ")


def remove_comments(txt: str, include_double_slash: bool = True) -> str:
    """
    Removes C-like /*...*/ block and // or # line comments.

    :param txt: the string containing comments;
    :param include_double_slash: if True, line comments starting with '//' will be removed.
        Defaults to False, because strings containing 'http://whatever.org' would be
        reduced to 'http:'.

    :return: text without comments
    """
    def __blot_out_non_new_lines__(_str_in_) -> str:
        """
        Return a string containing only the newline chars contained in strIn

        :param _str_in_: string where to find newline chars

        :return: string containing only the newline chars contained in strIn
        """
        return "" + ("\n" * _str_in_.count('\n'))

    def replacer(match: re.Match) -> str:
        """
        Replaces matches

        :param match: re.Match object

        :return: text with replaced substrings using match object
        """
        s = match.group(0)
        '''
        Matched string is //...EOL or # ... EOL or /*...*/  ==> Blot out all non-newline chars
        '''
        if s.startswith('/') or s.startswith('#'):
            return __blot_out_non_new_lines__(s)
        else:  # Matched string is '...' or "..."  ==> Keep unchanged
            return s

    doubled_slash_included = r'#.*?$|//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"'
    doubled_slash_excluded = r'#.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"'
    pattern = re.compile(doubled_slash_included if include_double_slash else doubled_slash_excluded,
                         re.DOTALL | re.MULTILINE)
    return re.sub(pattern, replacer, txt)


def slash(path: str) -> str:
    """
    Will add the trailing slash if it's not already there.

    :param path: path file name

    :return: slashed path file name
    """
    return os.path.join(path, '')


def tokenize(txt: str, punctuation_tokens: str = None) -> list[str]:
    """
    Very elementary tokenizer totally oriented to parse Query strings. It implements at least some interesting
    features:

    1. It is able to remove C-like comments (both block and line comments);
    2. The list of punctuation signs can be customised, so one can decide what signs to isolate as tokens; and
    3. It is fast and language-independent.

    :param txt: the string to be tokenized;
    :param punctuation_tokens: a string with punctuation signs to be split. If None, a default list is provided;

    :return: the list of tokens.
    """
    p = "{}()[]'\"`+|#" if punctuation_tokens is None else punctuation_tokens
    '''
    Add extra spaces to separate punctuation preceded or followed with other characters. These 
    spaces are removed when removing comments.
    '''
    new_txt = ''
    for c in txt:
        new_txt += c if c not in p else ' ' + c + ' '
    tokens = (' '.join(new_txt.strip().split())).split()
    return tokens


def unaccent(text: str) -> str:
    """
    Removes the diacritics and character symbols of a text.

    :param text: text with diacritics and character symbols

    :return: text without diacritics and character symbols
    """
    return unidecode.unidecode(text)


def url_tail(url: str, sep: str = '/') -> str:
    """
    Returns the element id of an url. If instead of sep being '/' it is a different one, this function can be used
    for many other purposes, e.g. getting the last element after '#}' in '{blahblahblah.blablhablah#}type', which
    would return 'type' if sep = '#}'.

    :param url: url where to find the id
    :param sep: url delimiter. By default, it is set to '/'

    :return: element id of the url as string
    """
    return url.rsplit(sep, 1)[1]


def url_head(url: str, sep: str = '/') -> str:
    """
    See url_tail. Same comments.

    Returns the element head of an url. If instead of sep being '/' it is a different one, this function can be used
    for many other purposes, e.g. getting the last element after '#}' in '{blahblahblah.blablhablah#}type', which
    would return '{blahblahblah.blablhablah' if sep = '#}'.

    :param url: url where to extract the head
    :param sep: url delimiter. By default, it is set to '/'

    :return: head of the url as string
    """
    return url.rsplit(sep, 1)[0] if url else ''


def regex(content: str, regex_condition: str) -> typing.Union[str, None]:
    """
    Returns the result of the search regex

    :param content: text where to search
    :param regex_condition: regex expression to search in the text

    :return: first match in the text content as string
    """
    match = re.search(regex_condition, content)

    if not match:
        return None

    first_match = match.group(1)
    return first_match if first_match is not None and len(first_match) > 0 else None
