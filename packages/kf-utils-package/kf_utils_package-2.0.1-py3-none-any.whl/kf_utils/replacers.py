"""
File:               replacers.py
Description:        Helpers for advanced string replacement
Created on:         16-sep-2022 12:46:38
Original author:    SEMBU-Team NTTData
"""
import operator
import re
import typing
from functools import reduce

from . import extractors as extractor, hashers as hashing


def replace_chars(txt: str, trans: dict) -> str:
    """
    Returns a str where mapped {'char': 'replacer', ...} are replaced.

    :param txt: text where to replace specific chars
    :param trans: dict that maps specific characters and its replacer. E.g.: {'char': 'replacer', ...}

    :return: replaced text as string
    """
    return txt.translate(str.maketrans(trans))


def replace_substrings(txt: str, tuple_list: list[tuple[str, str]]) -> str:
    """
    Replaces multiples substrings in a text with the pairs (source_substring, target_substring). Example:
        Given the text "The quick brown fox jumps over the lazy dog"
        And the list of pairs "[("brown", "red"), ("lazy", "quick")]"
        Returns "The quick red fox jumps over the quick dog"

    :param txt: text where to replace specific substrings
    :param tuple_list: list of pairs (source_substring, target_substring)

    :return: replaced text as string
    """
    return reduce(lambda a, kv: a.replace(*kv), tuple_list, txt)


def replace_match_boundaries(to_replace: str,
                             tuples: list[tuple[str, str]],
                             escape_chars: dict = None,
                             mask_quoted: bool = False) -> typing.Union[str, None]:
    """
    Replaces a word in a string but not other words containing that word.

    Example:
    Given the string 's':

        s = "allowedX and allowed and allowedXX"
        replace_match_boundaries(s, [('allowed', 'ALLOWED')])

    the returned value will be:

        "allowedX and ALLOWED and allowedXX"

    :param to_replace: text with substrings to be replaced
    :param tuples: a list of tuples containing the substring to match and the replacer substring
    :param escape_chars: a list of tuples containing special chars that need to be coded before the replacement
    :param mask_quoted: if False, quoted substrings inside the to_replace will not be masked. Masking is used to
            avoid unwanted boundaries inside the to_replace string.

    :return: replaced text as string
    """
    '''
    Default escape_chars if none provided.
    '''
    bnd = '():.<>' if escape_chars is None else escape_chars
    escape_chars = reduce(operator.or_, [{c: hashing.scrc(c)} for c in bnd]) if not escape_chars else escape_chars

    txt = to_replace
    ctl = None
    '''
    Incoming text containing special re symbols like <, >, ., *, [, ], ?, etc. need to be masked 
    (coded, i.e. replaced) a priori. At the end of the replacement operations, these chars are
    unmasked. An example of this need is when working with a string containing 
    any URI (e.g., <http://example.org>).
    '''
    if escape_chars is not None and bool(escape_chars):
        change = str.maketrans(escape_chars)    # maps codes in dict to unicode key
        tuples = [(i.translate(change), j.translate(change)) for i, j in tuples]    # replaces chars.
        ctl = list(escape_chars.items())
        txt = reduce(lambda a, kv: a.replace(*kv), ctl, txt)
    '''
    Example of something that would not work if not masked_quoted set to True: '"comma, comma", "comma, comma, comma"'.
    '''
    qt = None
    if mask_quoted and bool(qt := extractor.extract_double_quoted(txt) + extractor.extract_single_quoted(txt)):
        qtt = [f'\"{q}\"' for q in qt]
        qtt2 = [(q, f'\"_{hashing.scrc(q)}_\"') for q in qtt]
        txt = [txt := [txt.replace(c, f'\"_{hashing.scrc(c)}_\"')][0] for c in qtt][-1]
        tuples = [(qtt2[i][1], tuples[i][1]) for i in range(len(tuples))] if len(qtt2) == len(tuples) else None

    if tuples is None:
        return to_replace

    tl = []  # tuple list

    for tup in tuples:
        m = re.finditer(rf'\b{tup[0]}\b', txt)
        tl += [(tup[0], tup[1], p.start(), p.end()) for p in m]

    '''
    At this point, we have a list of tuples with all the data about elements that are to be replaced; e.g.:
        [('txt 1', 'TXT 1', 7, 12), ('txt 2', 'TXT 2', 0, 4)]

    NOTICE THAT, in the example, the first tuple's substring ('txt 1') occurs after the second tuple's 
    substring in the original text. We need to sort the list so we have first in the list the tuples 
    that occur first; otherwise the recalculation of the positions will fail when subtracting lengths to start 
    position 0 (which will produce a negative value).     
    '''
    tl = sorted(tl, key=lambda _x_: _x_[2])
    '''
    Per each tuple in the list, execute the replacement and recalculate the positions iteratively.
    '''
    for i in range(len(tl)):
        t = tl[i]  # tuple
        txt = txt[:t[2]] + t[1] + txt[t[3]:]  # new text
        '''
        The txt length has change, hence the positions in the tuple list have to be recalculated
        '''
        rl = len(t[1])  # length of the replacer
        pl = len(t[0])  # length of the to_be_replaced
        sl = rl - pl
        tl = [(a, b, c + sl, d + sl) for a, b, c, d in tl]

    if escape_chars:
        inv_ctl = [(c[1], c[0]) for c in ctl]
        txt = reduce(lambda a, kv: a.replace(*kv), inv_ctl, txt)
    '''
    If mask_quoted, the replaced value in tuples has not quote, we have to add them.
    '''
    if bool(qt) and mask_quoted:
        txt = replace_substrings(txt, tuples)
        tr = [(t[1], f'\"{t[1]}\"') for t in tuples]
        txt = replace_substrings(txt, tr)

    return txt


def replace_quoted(quoted_txt: str, to_replace: str, replacer: str, exclude: str = None) -> str:
    """
    Replaces a portion of text (the 'to_replace') enclosed with double or single quotes (the text_to_replace) with
    an alternative text, unless it equals the 'exclude' text.

    See the Compiler class within the Persistor package to see an example of how this is used to code and
    decode dots (.) occurring between quotes. Examples:

    Example:
    txt = ''' a text with "double quoted dots ." and a p.function('.') call'''

        replace_quoted(txt, '.', self.hash('.'), '.')

    would return:

        ''' a text with "double quoted dots 5058f1af8388633f609cadb75a75dc9d" and a p.function('.') call'''

    Where all quoted text has been replaced with the dot hash, except in p.function('.'), since:
        1. the dot between p and function is not double or single quoted
        2. the argument of the function contains the string to exclude.

    :param quoted_txt: the text containing quoted words and possibly unquoted words;
    :param to_replace: the text inside the quotes to be replaced;
    :param replacer: the text used to swap the to_replace var with;
    :param exclude: do not apply the replacement if the quoted text contains this text;

    :return: replaced text as string
    """
    rep = f"""{quoted_txt}"""
    extracted = extractor.extract_quoted(rep, exclude=exclude)
    for txt in extracted:
        ext_rep = txt.replace(to_replace, replacer) if txt != exclude else txt
        rep = str.replace(rep, txt, ext_rep) if ext_rep != exclude else rep
    return rep


def un_pad_fixed_locations(txt: str, locations: list[tuple]) -> str:
    """
    Given a text padded with padding_char, and a list with (substring, start, end),
    it replaces the portions that had been padded with the original text.

    :param txt: the text containing the substrings that are to be replaced with the masker
    :param locations: the list of tuples containing the (masked_substrings, start, end)

    :return: replaced text as string
    """

    for loc in locations:
        start = loc[1]
        end = loc[2]
        txt = txt[start + 1:] + loc[0] + txt[end:]
    return txt


def replace(original_txt: str, to_replace: str, replacer: str, listed_terms: list[str], exclude: str) -> str:
    """
    Replaces a text with the items in a list, except if the item is to be excluded.

    :param original_txt: the text original text to be analysed;
    :param to_replace: the text to be replaced;
    :param replacer: the text used to swap the to_replace var with;
    :param listed_terms: list of terms to replace;
    :param exclude: do not apply the replacement if the substring contains this text;

    :return: replaced text as string
    """
    rep = f"""{original_txt}"""
    for txt in listed_terms:
        ext_rep = txt.replace(to_replace, replacer) if exclude not in txt else txt
        rep = str.replace(rep, txt, ext_rep) if exclude not in ext_rep else rep
    return rep


def replace_angled(angled_txt: str,
                   to_replace: str,
                   replacer: str,
                   exclude: str = None) -> str:
    """
    Treats differently the <> than when using replace_between_delimiters. Copes with the case
    where the line contains just one angle, like in exec statements with <, >, <=, and >= operators.

    :param angled_txt: the text containing angled words and possibly non-angled words;
    :param to_replace: the text inside the angled to be replaced;
    :param replacer: the text used to swap the to_replace var with;
    :param exclude: do not apply the replacement if the angled text contains this text;

    :return: replaced text as string
    """
    rep = f"""{angled_txt}"""
    extracted = extractor.extract_angled(angled_txt)
    return replace(original_txt=rep,
                   to_replace=to_replace,
                   replacer=replacer,
                   listed_terms=extracted,
                   exclude=exclude)


def replace_delimited(delimited_txt: str,
                      left: str,
                      right: str,
                      to_replace: str,
                      replacer: str,
                      exclude: str = None) -> str:
    """
    Ibidem to replace quoted, but with different delimiters to the left and right sides.
    Replaces a portion of text (the 'to_replace') enclosed with specific delimiters (the text_to_replace) with
    an alternative text, unless it equals the 'exclude' text.

    :param delimited_txt: the text containing delimited words and possibly non-delimited words;
    :param left: left delimiter;
    :param right: right delimiter;
    :param to_replace: the text inside the delimiters to be replaced;
    :param replacer: the text used to swap the to_replace var with;
    :param exclude: do not apply the replacement if the delimited text contains this text;

    :return: replaced text as string
    """
    rep = f"""{delimited_txt}"""
    extracted = extractor.extract_between_delimiters(delimited_txt, left, right)
    return replace(original_txt=rep, to_replace=to_replace, replacer=replacer, listed_terms=extracted, exclude=exclude)
