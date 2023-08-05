import unittest

from kf_utils import replacers, extractors as extractor, hashers as hashing
from test.resources import test_messages


class TestReplacers(unittest.TestCase):
    '''
    Test replacers scripts and methods
    '''

    replace_chars_method = 'replacers.replace_chars'
    replace_substrings_method = 'replacers.replace_substrings'
    replace_match_boundaries_method = 'replacers.replace_match_boundaries'
    replace_quoted_method = 'replacers.replace_quoted'
    un_pad_fixed_locations_method = 'replacers.un_pad_fixed_locations'
    replace_method = 'replacers.replace'
    replace_angled_method = 'replacers.replace_angled'
    replace_delimited_method = 'replacers.replace_delimited'

    def setUp(self) -> None:
        self.test_text = "This is a test text for methods in replacers.py"
        self.test_text_2 = """allowedX and allowed and allowedXX "andy" """
        self.test_text_3 = ''' a text with "double quoted dots ." and a p.function('.') call'''
        self.test_text_4 = '''Use this test text for padding replacements'''
        self.test_text_5 = "This is a test text for methods in replacers.py for word exclude"
        self.test_text_angled = '''This text contains <angled text at the end>'''
        self.test_text_delimited = '''This text #contains two different_ delimiters'''


    #1. Test replacers.replace_chars
    def test_replace_chars_not_valid_param(self) -> None:
        """
        GIVEN a not valid string and dict param \n
        WHEN replacers.replace_chars method is called \n
        THEN a TypeError exception is raised
        """
        not_valid_param = {"this is not a dict"}
        self.assertRaises(TypeError, replacers.replace_chars, self.test_text, not_valid_param)

    def test_replace_chars_return_type(self) -> None:
        """
        GIVEN a valid string and dict param \n
        WHEN replacers.replace_chars method is called \n
        THEN replacers.replace_chars return type is not None\n
        AND replacers.replace_chars returned value is of type str
        """
        dict_1 = {"i": "o", "e": "z", ".":"#"}

        self.assertIsNotNone(
            replacers.replace_chars(self.test_text, dict_1),
            test_messages.METHOD_RETURNS_NONE.format(method=self.replace_chars_method)
        )

        self.assertIsInstance(
            replacers.replace_chars(self.test_text, dict_1),
            str,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(method=self.replace_chars_method,
                                                              value='str')
        )

    def test_replace_chars_correct_value(self) -> None:
        """
        GIVEN a valid string and dict param \n
        WHEN replacers.replace_chars method is called \n
        THEN replacers.replace_chars replaces the characters in the text appearing in the dict\n
        """
        dict_1 = {"i": "o", "e": "z", ".": "#"}
        dict_2 = {}
        dict_3 = {"w":"q"}

        replaced_text = "Thos os a tzst tzxt for mzthods on rzplaczrs#py"
        self.assertEqual(
            replacers.replace_chars(self.test_text, dict_1),
            replaced_text,
            test_messages.IS_NOT_EQUAL.format(first=replacers.replace_chars(self.test_text, dict_1), second=replaced_text)
        )

        self.assertEqual(
            replacers.replace_chars(self.test_text, dict_2),
            self.test_text,
            test_messages.IS_NOT_EQUAL.format(first=replacers.replace_chars(self.test_text, dict_2),
                                              second=self.test_text)
        )

        self.assertEqual(
            replacers.replace_chars(self.test_text, dict_3),
            self.test_text,
            test_messages.IS_NOT_EQUAL.format(first=replacers.replace_chars(self.test_text, dict_3),
                                              second=self.test_text)
        )


    #2. Test replacers.replace_substrings
    def test_replace_substrings_not_valid_param(self) -> None:
        """
        GIVEN a not valid string and list of pairs param \n
        WHEN replacers.replace_substrings method is called \n
        THEN a TypeError exception is raised
        """
        not_valid_param = {"this is not a dict"}
        self.assertRaises(TypeError, replacers.replace_substrings, self.test_text, not_valid_param)

    def test_replace_substrings_return_type(self) -> None:
        """
        GIVEN a valid string and list of pairs param \n
        WHEN replacers.replace_substrings method is called \n
        THEN replacers.replace_substrings return type is not None\n
        AND replacers.replace_substrings returned value is of type str
        """
        list_1 = [("text", "string")]

        self.assertIsNotNone(
            replacers.replace_substrings(self.test_text, list_1),
            test_messages.METHOD_RETURNS_NONE.format(method=self.replace_substrings_method)
        )

        self.assertIsInstance(
            replacers.replace_substrings(self.test_text, list_1),
            str,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(method=self.replace_substrings_method,
                                                              value='str')
        )

    def test_replace_substrings_correct_value(self) -> None:
        """
        GIVEN a valid string and list of pairs param \n
        WHEN replacers.replace_substrings method is called \n
        THEN replacers.replace_substrings replaces the pairs in the text\n
        """
        list_1 = [("text", "string")]
        list_2 = []
        list_3 = [("text", "string"), ("This", "The following")]

        replaced_text_1 = "This is a test string for methods in replacers.py"
        replaced_text_3 = "The following is a test string for methods in replacers.py"

        self.assertEqual(
            replacers.replace_substrings(self.test_text, list_1),
            replaced_text_1,
            test_messages.IS_NOT_EQUAL.format(first=replacers.replace_substrings(self.test_text, list_1),
                                              second=replaced_text_1)
        )

        self.assertEqual(
            replacers.replace_substrings(self.test_text, list_2),
            self.test_text,
            test_messages.IS_NOT_EQUAL.format(first=replacers.replace_substrings(self.test_text, list_2),
                                              second=self.test_text)
        )

        self.assertEqual(
            replacers.replace_substrings(self.test_text, list_3),
            replaced_text_3,
            test_messages.IS_NOT_EQUAL.format(first=replacers.replace_substrings(self.test_text, list_3),
                                              second=replaced_text_3)
        )


    #3. Test replacers.replace_match_boundaries
    def test_replace_match_boundaries_not_valid_param(self) -> None:
        """
        GIVEN a not valid string and list of pairs param \n
        WHEN replacers.replace_substrings method is called \n
        THEN a TypeError exception is raised
        """
        not_valid_param = 54 #This is not a valid list of tuples
        self.assertRaises(TypeError, replacers.replace_match_boundaries, self.test_text, not_valid_param)

    def test_replace_match_boundaries_return_type(self) -> None:
        """
        GIVEN a valid string and list of pairs param \n
        WHEN replacers.replace_match_boundaries method is called \n
        THEN replacers.replace_match_boundaries return type is not None\n
        AND replacers.replace_match_boundaries returned value is of type str
        """
        list_1 = [('allowed', 'ALLOWED')]

        self.assertIsNotNone(
            replacers.replace_match_boundaries(self.test_text_2, list_1),
            test_messages.METHOD_RETURNS_NONE.format(method=self.replace_match_boundaries_method)
        )

        self.assertIsInstance(
            replacers.replace_match_boundaries(self.test_text_2, list_1),
            str,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(method=self.replace_match_boundaries_method,
                                                              value='str')
        )

    def test_replace_match_boundaries_correct_value(self) -> None:
        """
        GIVEN a valid string and list of pairs param \n
        WHEN replacers.replace_substrings method is called \n
        THEN replacers.replace_substrings replaces a word in a string but not other words containing that word\n
        """
        list_1 = [('allowed', 'ALLOWED')]
        list_2 = [('allowed', 'ALLOWED'), ('and', 'HELLO')]
        list_3 = [('andy', 'ANDY')]

        replaced_text_1 = """allowedX and ALLOWED and allowedXX "andy" """
        replaced_text_2 = """allowedX HELLO ALLOWED HELLO allowedXX "andy" """
        replaced_text_3 = """allowedX and ALLOWED and allowedXX "ANDY" """

        self.assertEqual(
            replacers.replace_match_boundaries(self.test_text_2, list_1),
            replaced_text_1,
            test_messages.IS_NOT_EQUAL.format(first=replacers.replace_match_boundaries(self.test_text, list_1),
                                              second=replaced_text_1)
        )

        self.assertEqual(
            replacers.replace_match_boundaries(self.test_text_2, list_2),
            replaced_text_2,
            test_messages.IS_NOT_EQUAL.format(first=replacers.replace_match_boundaries(self.test_text, list_2),
                                              second=replaced_text_2)
        )

    #4. Test replacers.replace_quoted
    def test_replace_quoted_not_valid_param(self) -> None:
        """
        GIVEN three not valid str params \n
        WHEN replacers.replace_substrings method is called \n
        THEN a TypeError exception is raised
        """
        not_valid_param = {"this is not a string"}
        self.assertRaises(TypeError, replacers.replace_quoted, self.test_text_3, not_valid_param, '.')

    def test_replace_quoted_return_type(self) -> None:
        """
        GIVEN three valid string params \n
        WHEN replacers.replace_quoted method is called \n
        THEN replacers.replace_quoted return type is not None\n
        AND replacers.replace_quoted returned value is of type str
        """

        self.assertIsNotNone(
            replacers.replace_quoted(self.test_text_3, '.', hashing.hash('.'), '.'),
            test_messages.METHOD_RETURNS_NONE.format(method=self.replace_quoted_method)
        )

        self.assertIsInstance(
            replacers.replace_quoted(self.test_text_3, '.', hashing.hash('.'), '.'),
            str,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(method=self.replace_quoted_method,
                                                              value='str')
        )

    def test_replace_quoted_correct_value(self) -> None:
        """
        GIVEN three valid string params \n
        WHEN replacers.replace_quoted method is called \n
        THEN replacers.replace_quoted replaces a portion of text enclosed with double or single quotes
            with an alternative text, unless it equals the 'exclude' text.
        """
        replaced_text = ''' a text with "double quoted dots 5058f1af8388633f609cadb75a75dc9d" and a p.function('.') call'''

        self.assertEqual(
            replacers.replace_quoted(self.test_text_3, '.', hashing.hash('.'), '.'),
            replaced_text,
            test_messages.IS_NOT_EQUAL.format(first=replacers.replace_quoted(self.test_text_3, '.', hashing.hash('.'), '.'),
                                              second=replaced_text)
        )


    #5. Test replacers.un_pad_fixed_locations
    def test_un_pad_fixed_locations_not_valid_param(self) -> None:
        """
        GIVEN a not valid text and list of tuples params\n
        WHEN replacers.un_pad_fixed_locations method is called \n
        THEN a TypeError exception is raised
        """
        not_valid_param = {"this is not a list"}
        self.assertRaises(TypeError, replacers.un_pad_fixed_locations, self.test_text_4, not_valid_param)

    def test_un_pad_fixed_locations_return_type(self) -> None:
        """
        GIVEN a valid text and list of tuples params \n
        WHEN replacers.un_pad_fixed_locations method is called \n
        THEN replacers.un_pad_fixed_locations return type is not None\n
        AND replacers.un_pad_fixed_locations returned value is of type str
        """

        self.assertIsNotNone(
            replacers.un_pad_fixed_locations(self.test_text_4, [('hello', 5, 10)]),
            test_messages.METHOD_RETURNS_NONE.format(method=self.un_pad_fixed_locations_method)
        )

        self.assertIsInstance(
            replacers.un_pad_fixed_locations(self.test_text_4, [('hello', 5, 10)]),
            str,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(method=self.un_pad_fixed_locations_method,
                                                              value='str')
        )

    def test_un_pad_fixed_locations_correct_value(self) -> None:
        """
        GIVEN three valid string params \n
        WHEN replacers.replace_quoted method is called \n
        THEN replacers.replace_quoted replaces a portion of text enclosed with double or single quotes
            with an alternative text, unless it equals the 'exclude' text.
        """

        text = """\tTexto tabulado\nTexto sin tabular"""
        un_padded_text = """Texto tabulado\nTexto sin tabular"""

        locations = [('', 0, len(text))]
        self.assertEqual(
            replacers.un_pad_fixed_locations(text, locations),
            un_padded_text,
            test_messages.IS_NOT_EQUAL.format(
                first=replacers.un_pad_fixed_locations(text, locations),
                second=un_padded_text)
        )


    #6. Test replacers.replace
    def test_replace_not_valid_param(self) -> None:
        """
        GIVEN not valid string params or a not valid list param \n
        WHEN replacers.replace method is called \n
        THEN a TypeError exception is raised
        """
        not_valid_param = {"this is not a list"}
        self.assertRaises(TypeError, replacers.replace, self.test_text, ' ', ' ',not_valid_param)

    def test_replace_return_type(self) -> None:
        """
        GIVEN three valid string params and a valid list param\n
        WHEN replacers.replace method is called \n
        THEN replacers.replace return type is not None\n
        AND replacers.replace returned value is of type str
        """

        self.assertIsNotNone(
            replacers.replace(self.test_text, 'test', 'hello', ['test'], 'exclude'),
            test_messages.METHOD_RETURNS_NONE.format(method=self.replace_method)
        )

        self.assertIsInstance(
            replacers.replace(self.test_text, 'test', 'hello', ['test'], 'exclude'),
            str,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(method=self.replace_method,
                                                              value='str')
        )

    def test_replace_correct_value(self) -> None:
        """
        GIVEN three valid string params \n
        WHEN replacers.replace method is called \n
        THEN replacers.replace replaces a text with the items in a list, except if the item is to be excluded
        """

        replaced_text = 'This is a try text for methods in replacers.py for word exclude'
        self.assertEqual(
            replacers.replace(self.test_text_5, 'test', 'try', ['test'], 'exclude'),
            replaced_text,
            test_messages.IS_NOT_EQUAL.format(first=replacers.replace(self.test_text_5, 'test', 'try', ['test'], 'exclude'),
                                              second=replaced_text)
        )

        self.assertEqual(
            replacers.replace(self.test_text_5, 'test', 'try', ['replace'], 'exclude'),
            self.test_text_5,
            test_messages.IS_NOT_EQUAL.format(
                first=replacers.replace(self.test_text_5, 'test', 'try', ['replace'], 'exclude'),
                second=self.test_text_5)
        )

        replaced_text = 'This is a test text change methods in replacers.py for word exclude'
        self.assertEqual(
            replacers.replace(self.test_text_5, 'test', 'try', ['replace'], 'exclude'),
            self.test_text_5,
            test_messages.IS_NOT_EQUAL.format(
                first=replacers.replace(self.test_text_5, 'for', 'change', ['text for methods', 'replacers.py for word'], 'word'),
                second=replaced_text)
        )


    #7. Test replacers.replace_angled
    def test_replace_angled_not_valid_param(self) -> None:
        """
        GIVEN three not valid string params \n
        WHEN replacers.replace_angled method is called \n
        THEN a TypeError exception is raised
        """
        not_valid_param = {"this is not a string"}
        self.assertRaises(TypeError, replacers.replace_angled, not_valid_param, '', '')

    def test_replace_angled_return_type(self) -> None:
        """
        GIVEN three valid string params \n
        WHEN replacers.replace_angled method is called \n
        THEN replacers.replace_angled return type is not None\n
        AND replacers.replace_angled returned value is of type str
        """

        self.assertIsNotNone(
            replacers.replace_angled(self.test_text_angled, 'angled text', 'words', 'exclude'),
            test_messages.METHOD_RETURNS_NONE.format(method=self.replace_angled_method)
        )

        self.assertIsInstance(
            replacers.replace_angled(self.test_text_angled, 'angled text', 'words', 'exclude'),
            str,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(method=self.replace_angled_method,
                                                              value='str')
        )

    def test_replace_angled_correct_value(self) -> None:
        """
        GIVEN a valid string params \n
        WHEN replacers.replace_angled method is called \n
        THEN replacers.replace_angled replaces the angled text correctly\n
        """

        replaced_text_1 = '''This text contains <words>'''
        replaced_text_2 = '''This text contains <angled words at the end>'''
        self.test_text_angled = '''This text contains <angled text at the end>'''

        self.assertEqual(
            replacers.replace_angled(self.test_text_angled, 'angled text at the end', 'words', 'exclude'),
            replaced_text_1,
            test_messages.IS_NOT_EQUAL.format(first=replacers.replace_angled(self.test_text_angled, 'angled text', 'words', 'exclude'),
                                              second=replaced_text_1)
        )

        self.assertEqual(
            replacers.replace_angled(self.test_text_angled, 'text', 'words', 'exclude'),
            replaced_text_2,
            test_messages.IS_NOT_EQUAL.format(
                first=replacers.replace_angled(self.test_text_angled, 'text', 'words', 'exclude'),
                second=replaced_text_2)
        )

        self.assertEqual(
            replacers.replace_angled(self.test_text_angled, 'angled text at the end', 'words', 'angled text'),
            self.test_text_angled,
            test_messages.IS_NOT_EQUAL.format(
                first=replacers.replace_angled(self.test_text_angled, 'angled text at the end', 'words', 'at the end'),
                second=self.test_text_angled)
        )

        self.assertEqual(
            replacers.replace_angled(self.test_text_angled, 'exclude', 'words', 'angled text'),
            self.test_text_angled,
            test_messages.IS_NOT_EQUAL.format(
                first=replacers.replace_angled(self.test_text_angled, 'exclude', 'words', 'at the end'),
                second=self.test_text_angled)
        )


    #8. Test replacers.replace_delimited
    def test_replace_delimited_not_valid_param(self) -> None:
        """
        GIVEN five not valid string params \n
        WHEN replacers.replace_delimited method is called \n
        THEN a TypeError exception is raised
        """
        not_valid_param = {"this is not a string"}
        self.assertRaises(TypeError, replacers.replace_delimited, not_valid_param, '', '', '')

    def test_replace_delimited_return_type(self) -> None:
        """
        GIVEN five valid string params \n
        WHEN replacers.replace_delimited method is called \n
        THEN replacers.replace_delimited return type is not None\n
        AND replacers.replace_delimited returned value is of type str
        """
        self.assertIsNotNone(
            replacers.replace_delimited(self.test_text_delimited, '#', '_', 'two', 'words', 'exclude'),
            test_messages.METHOD_RETURNS_NONE.format(method=self.replace_delimited_method)
        )

        self.assertIsInstance(
            replacers.replace_delimited(self.test_text_delimited, '#', '_', 'two', 'words', 'exclude'),
            str,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(method=self.replace_delimited_method,
                                                              value='str')
        )

    def test_replace_delimited_correct_value(self) -> None:
        """
        GIVEN a valid string params \n
        WHEN replacers.replace_delimited method is called \n
        THEN replacers.replace_delimited replaces the text correctly between the given delimiters correctly\n
        """
        replaced_text_1 = '''This text #words_ delimiters'''
        replaced_text_2 = '''This text #contains words different_ delimiters'''

        self.assertEqual(
            replacers.replace_delimited(self.test_text_delimited, '#', '_', 'contains two different', 'words', 'exclude'),
            replaced_text_1,
            test_messages.IS_NOT_EQUAL.format(
                first=replacers.replace_delimited(self.test_text_delimited, '#', '_', 'contains two different', 'words', 'exclude'),
                second=replaced_text_1)
        )

        self.assertEqual(
            replacers.replace_delimited(self.test_text_delimited, '#', '_', 'two', 'words', 'exclude'),
            replaced_text_2,
            test_messages.IS_NOT_EQUAL.format(first=replacers.replace_delimited(self.test_text_delimited, '#', '_', 'two', 'words', 'exclude'),
                                              second=replaced_text_2)
        )