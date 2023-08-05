"""
Class CarCodec. A helper to code and decode characters or strings of characters.

Main Use Cases: parsers, compiler, and text analysers in general that need to find patterns and replace portions
of text that match the patterns with another text or symbol.
"""
import re
import typing

from . import extractors, hashers, replacers


class CharCodec:
    """
    String coder and decoder.

    Attributes:
        code        The code taking the place of the substring to be replaced.
        to_replace  The substring that is being replaced.
        text        The text containing the substring to be replaced.
        exclude     A text NOT to replace if found inside the substring being replaced.
    """
    code: typing.Union[str, None]
    to_replace: typing.Union[str, None]
    text: typing.Union[str, None]
    exclude: typing.Union[str, None]

    def __init__(self, text: str = None, to_replace: str = None, code: str = None, exclude: str = None):
        self.text = text
        self.code = code
        self.to_replace = to_replace
        self.exclude = exclude

    @staticmethod
    def extract_bracketed(text: str, left: str, right: str) -> typing.Union[list, None]:
        """
        Extracts string between left and right delimiters.

        :param text: string to be analysed
        :param left: left delimiter
        :param right: right delimiter

        :return: extracted parts listed as strings
        """
        return extractors.extract_between_delimiters(text, left, right)

    @staticmethod
    def extract_quoted(text: str, exclude: str = None) -> typing.Union[list, None]:
        """
        Extracts text between double or single quotes unless it equals the 'exclude' text.

        :param text: string to be analysed
        :param exclude: text to exclude. By default, it is set to None

        :return: extracted parts listed as strings
        """
        exclude = '' if not exclude else exclude
        rex = r"['\"](.*?)['\"]"
        ret = re.findall(rex, text)
        ret = [ret for ret in ret if ret != exclude]
        return ret

    @staticmethod
    def __code_escaped_quotes__(text: str) -> (str, bool):
        """
        Returns a coded version of possible escaped "\'" inside the text and True|False if found|not found.
        The found|not found will be used to decode or not decode.

        :param text: text to be analysed

        :return: coded version of possible escaped "\'" inside the text and True|False if found|not found
        """
        if "\'" not in text:
            return text, False
        return text.replace("\'", hashers.hash("\'")), True

    @staticmethod
    def __decode_escaped_quotes__(text: str) -> str:
        """
        Returns a decoded version of possible escaped "\'" inside the text

        :param text: text to be analysed

        :return: decoded version of possible escaped "\'" inside the text
        """
        return text.replace(hashers.hash("\'"), "\'")

    def quoted(self) -> typing.Union[str, None]:
        """
        Replaces a substring inside a double or single quoted text with the code.

        :return: the text with the replaced substring
        """
        new_text = f"""{self.text}"""
        '''
        If the text contains escaped quotes, we replace them
        '''
        new_text, escaped_quotes = self.__code_escaped_quotes__(new_text)
        extracted = self.extract_quoted(new_text, exclude=self.exclude)
        for txt in extracted:
            ext_rep = txt.replace(self.to_replace, self.code) if txt != self.exclude else txt
            new_text = new_text.replace(txt, ext_rep) if ext_rep != self.exclude else new_text
        new_text = self.__decode_escaped_quotes__(new_text) if escaped_quotes else new_text
        return new_text

    def angled(self, exclude: str = None) -> typing.Union[str, None]:
        """
        Replaces everything between <>, uses a special pattern that avoids problems with statements containing
        operators like < and >.

        :param exclude: text to be excluded. By default, it is set to None

        :return: the text with angled chars replaced
        """
        return replacers.replace_angled(self.text, to_replace=self.to_replace, replacer=self.code, exclude=exclude)

    def bracketed(self, left: str, right: str, exclude: str = None) -> typing.Union[str, None]:
        """
        Replaces a substring inside parenthesis, square brackets, curly brackets, angles or disparate delimiters
        with the code.

        :param left: left delimiter
        :param right: right delimiter
        :param exclude: text to exclude. By default, it is set to None

        :return: the text with bracketed chars replaced
        """
        return replacers.replace_delimited(delimited_txt=self.text,
                                           left=left,
                                           right=right,
                                           to_replace=self.to_replace,
                                           replacer=self.code,
                                           exclude=exclude)

    def pointers(self) -> typing.Union[str, None]:
        """
        Replaces pointers to functions (e.g., the dot in "class.function_name(*args, **kwargs))" with the code.

        :return: function with pointers replaced
        """
        keywords = re.findall(r".\w+\s*\(", self.text)
        keywords = [k.lstrip(self.to_replace) for k in keywords]
        new_text = self.text
        for keyword in keywords:
            new_text = new_text.replace(f'{self.to_replace}{keyword}', self.code + keyword)
        return new_text

    def properties(self) -> typing.Union[str, None]:
        """
        Replaces invocation to method or class properties.

        Example:

                md5 = self.io().hash

            returns

                md5 = self.io()<code>hash

        :return: method or class properties with invocation replaced
        """
        new_text = self.text
        rex = fr'\).\w+'
        keywords = re.findall(rex, self.text)
        keywords = [k[2:] for k in keywords if bool(keywords)]
        for keyword in keywords:
            new_text = new_text.replace(f').{keyword}', f'){self.code}{keyword}')
        return new_text

    def sequence(self) -> typing.Union[str, None]:
        """
        Replaces each inner 'x' char with the code in a sequence of words separated with 'x'. E.g., with '.' as the
        separator and <code> representing whatever code you choose, e.g. <__DOT__>

                Given: sequence("com.nttdata.dgi.crud.Compiler.")
                Returns: "com<__DOT__>nttdata<__DOT__>dgi<__DOT__>crud<__DOT__>Compiler."

        Notice that the tokenizer is able to remove comments, which in this case is highly convenient.
        REMINDER: remove_comments defaults to True, thus this argument here is superfluous, but we keep it
        for the sake of clarity and documentation.

        :return: the new modified text
        """
        new_text = self.text
        rex = r'(?<=\.)\w+(?=\.)'
        keywords = set(re.findall(rex, self.text))
        for keyword in keywords:
            new_text = new_text.replace(f'{self.to_replace}{keyword}', f'{self.code}{keyword}')
            new_text = new_text.replace(f'{keyword}{self.to_replace}', f'{keyword}{self.code}')
        return new_text

    def __call__(self, text: str = None, to_replace: str = None, code: str = None, exclude: str = None):
        self.text = text if text else self.text
        self.to_replace = to_replace if to_replace else self.to_replace
        self.code = code if code else self.code
        self.exclude = exclude if exclude else self.exclude
        return self
