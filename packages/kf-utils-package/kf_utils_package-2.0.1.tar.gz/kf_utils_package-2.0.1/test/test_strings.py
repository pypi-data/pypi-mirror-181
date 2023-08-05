import unittest
import typing
import os
import re

from kf_utils import strings, files
from test.resources import test_messages


class TestStrings(unittest.TestCase):
    '''
    Test strings scripts and methods
    '''

    indices_method = 'strings.indices'
    is_get_list_method = 'strings.is_get_list'
    json_str_to_dict_method = 'strings.json_str_to_dict'
    mask_quoted_method = 'strings.mask_quoted'
    unmask_quoted_method = 'strings.unmask_quoted'
    nnl_method = 'strings.nnl'
    remove_comments_method = 'strings.remove_comments'
    slash_method = 'strings.slash'
    tokenize_method = 'strings.tokenize'
    unaccent_method = 'strings.unaccent'
    url_tail_method = 'strings.url_tail'
    url_head_method = 'strings.url_head'
    regex_method = 'strings.regex'

    pwd = os.path.abspath(os.path.dirname(__file__))
    commented_text_path: str = os.path.join(pwd, 'commented_text.txt')

    if pwd.endswith('test'):
        resources_path = os.path.join(
            pwd,
            'resources'
        )
    else:
        resources_path = os.path.join(
            pwd,
            'test'
            'resources'
        )

    def setUp(self) -> None:
        self.test_text: str = """Thís "is" a string test text tò test "strings" <mèthóds>"""
        self.list: typing.Union[list, str] = ["this", "is", "a", "list"]
        self.list_like: typing.Union[list, str] = """[1+2, "hello world", [2]+[3], True+False]"""
        self.list_like_dict: typing.Union[list, str] = """[x, y, x + y]"""
        self.dict = {"x": 5, "y":2}
        self.valid_json: str = """{"id": "04","name": "sunil", "department": "HR"}"""
        self.not_valid_json = {"hello"}
        self.text_newlines: str ="""This\ntext\nhas\nmany\nnew\nlines"""
        self.commented_text = os.path.join(self.resources_path, 'commented_text.txt')
        self.file_path = self.commented_text
        self.file_path_slashed = os.path.join(self.file_path, '')
        self.url = 'https://en.wikipedia.org/wiki/URL'


    #1. Test strings.indices
    def test_indices_not_valid_param(self) -> None:
        """
        GIVEN a not valid string param \n
        WHEN strings.indices method is called \n
        THEN a TypeError exception is raised
        """
        not_valid_param = 54
        self.assertRaises(TypeError, strings.indices, self.test_text, not_valid_param)

    def test_indices_return_type(self) -> None:
        """
        GIVEN a valid string param \n
        WHEN strings.indices method is called \n
        THEN strings.indices return type is not None\n
        AND strings.indices returned value is of type list[int]
        """

        self.assertIsNotNone(
            strings.indices(self.test_text, "i"),
            test_messages.METHOD_RETURNS_NONE.format(method=self.indices_method)
        )

        self.assertIsNotNone(
            strings.indices(self.test_text, "z"),
            test_messages.METHOD_RETURNS_NONE.format(method=self.indices_method)
        )

        self.assertIsInstance(
            strings.indices(self.test_text, "i"),
            list,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(method=self.indices_method,
                                                              value='list[int]')
        )


    def test_indices_correct_value(self) -> None:
        """
        GIVEN a valid string param \n
        WHEN strings.is_get_list method is called \n
        THEN strings.is_get_list determines if a text is a valid Python's list\n
        """
        self.assertEqual(
            strings.indices(self.test_text, "z"),
            [],
            test_messages.IS_NOT_EQUAL.format(first=strings.indices(self.test_text, "z"), second=[])
        )

        self.assertEqual(
            strings.indices(self.test_text, "i"),
            [6, 15, 41],
            test_messages.IS_NOT_EQUAL.format(first=strings.indices(self.test_text, "i"), second=[2, 5, 13, 38])
        )

        self.assertEqual(
            strings.indices(self.test_text, "test"),
            [19, 32],
            test_messages.IS_NOT_EQUAL.format(first=strings.indices(self.test_text, "test"), second=[17, 30])
        )

        self.assertEqual(
            strings.indices(self.test_text, "text"),
            [24],
            test_messages.IS_NOT_EQUAL.format(first=strings.indices(self.test_text, "text"), second=[22])
        )

        self.assertEqual(
            strings.indices(self.test_text, "test text"),
            [19],
            test_messages.IS_NOT_EQUAL.format(first=strings.indices(self.test_text, "test text"), second=[17])
        )

        self.assertEqual(
            strings.indices(self.test_text, "TEXT", True),
            [],
            test_messages.IS_NOT_EQUAL.format(first=strings.indices(self.test_text, "test text"), second=[])
        )

        self.assertEqual(
            strings.indices(self.test_text, "TEXT", False),
            [24],
            test_messages.IS_NOT_EQUAL.format(first=strings.indices(self.test_text, "test text"), second=[22])
        )

    # 2. Test strings.is_get_list
    def test_is_get_list_not_valid_param(self) -> None:
        """
        GIVEN a not valid list param \n
        WHEN strings.is_get_list method is called \n
        THEN a TypeError exception is raised
        """
        not_valid_param = 50
        self.assertRaises(AttributeError, strings.is_get_list, not_valid_param)

    def test_is_get_list_return_type(self) -> None:
        """
        GIVEN a valid list param \n
        WHEN strings.is_get_list method is called \n
        THEN strings.is_get_list return type is not None\n
        AND strings-is_get_list returned value is of type list
        """

        self.assertIsNotNone(
            strings.is_get_list(self.list),
            test_messages.METHOD_RETURNS_NONE.format(method=self.is_get_list_method)
        )

        self.assertIsInstance(
            strings.is_get_list(self.list),
            list,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(method=self.is_get_list_method, value='list')
        )

        self.assertIsNotNone(
            strings.is_get_list(self.list_like),
            test_messages.METHOD_RETURNS_NONE.format(method=self.is_get_list_method)
        )

        self.assertIsInstance(
            strings.is_get_list(self.list_like),
            list,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(method=self.is_get_list_method, value='list')
        )



    def test_is_get_list_correct_value(self) -> None:
        """
        GIVEN a valid list param \n
        WHEN strings.is_get_list method is called \n
        THEN strings.is_get_list determines if a text is a valid Python's list\n
        """

        self.assertEqual(
            strings.is_get_list(self.list),
            ["this", "is", "a", "list"],
            test_messages.IS_NOT_EQUAL.format(first=strings.indices(self.test_text, "test text"), second=[22])
        )

        self.assertEqual(
            strings.is_get_list(self.list_like),
            [3, "hello world", [2, 3], 1],
            test_messages.IS_NOT_EQUAL.format(first=strings.indices(self.test_text, "test text"), second=[22])
        )

        self.assertEqual(
            strings.is_get_list(self.list_like_dict, self.dict),
            [5, 2, 7],
            test_messages.IS_NOT_EQUAL.format(first=strings.indices(self.test_text, "test text"), second=[22])
        )


    #3. Test strings.json_str_to_dict
    def test_json_str_to_dict_not_valid_param(self) -> None:
        """
        GIVEN a not valid json-style string param \n
        WHEN strings.json_str_to_dict method is called \n
        THEN an Exception is raised
        """
        not_valid_param = self.not_valid_json
        self.assertRaises(Exception, strings.json_str_to_dict, not_valid_param)

    def test_json_str_to_dict_return_type(self) -> None:
        """
        GIVEN a valid json-style string param \n
        WHEN strings.json_str_to_dict method is called \n
        THEN strings.json_str_to_dict return type is not None\n
        AND strings.json_str_to_dict returned value is of type dict
        """

        self.assertIsNotNone(
            strings.json_str_to_dict(self.valid_json),
            test_messages.METHOD_RETURNS_NONE.format(method=self.json_str_to_dict_method)
        )

        self.assertIsInstance(
            strings.json_str_to_dict(self.valid_json),
            dict,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(method=self.is_get_list_method, value='list')
        )


    def test_json_str_to_dict_correct_value(self) -> None:
        """
        GIVEN a valid json-style string param \n
        WHEN strings.is_get_list method is called \n
        THEN strings.is_get_list transforms json's content into a Python's dictionary\n
        """
        dict = {
                "id": "04",
                "name": "sunil",
                "department": "HR"
               }
        self.assertEqual(
            strings.json_str_to_dict(self.valid_json),
            dict,
            test_messages.IS_NOT_EQUAL.format(first=strings.json_str_to_dict(self.valid_json), second=dict)
        )


    #4. Test strings.mask_quoted and test.unmask_quoted
    def test_mask_quoted_not_valid_param(self) -> None:
        """
        GIVEN a not valid string param \n
        WHEN strings.mask_quoted method is called \n
        THEN an AttributeError exception is raised
        """
        not_valid_param = self.not_valid_json
        self.assertRaises(Exception, strings.mask_quoted, not_valid_param)

    def test_mask_quoted_return_type(self) -> None:
        """
        GIVEN a valid string param \n
        WHEN strings.mask_quoted method is called \n
        THEN strings.mask_quoted return type is not None\n
        AND strings.mask_quoted returned value is of type (str, list)
        """

        self.assertIsNotNone(
            strings.mask_quoted(self.valid_json),
            test_messages.METHOD_RETURNS_NONE.format(method=self.mask_quoted_method)
        )

        self.assertIsInstance(
            strings.mask_quoted(self.valid_json),
            tuple,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(method=self.mask_quoted_method, value='tuple')
        )

        self.assertIsInstance(
            strings.mask_quoted(self.valid_json)[0],
            str,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(method=self.mask_quoted_method, value='str')
        )

        self.assertIsInstance(
            strings.mask_quoted(self.valid_json)[1],
            list,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(method=self.mask_quoted_method, value='list')
        )



    def test_mask_quoted_correct_value(self) -> None:
        """
        GIVEN a quoted text as string \n
        WHEN strings.mask_quoted method is called \n
        THEN strings.mask_quoted extracts quoted substring from the quoted, and returns the masked text and a
            list of tuples with the pairs [(original substring, masked substring), ...] text\n
        AMD strings.unmask_quoted replaces previously masked substrings into their original forms
        """

        masked_text, tuples = strings.mask_quoted(self.test_text)
        unmasked_text = strings.unmask_quoted(masked_text, tuples)

        self.assertEqual(
            unmasked_text,
            self.test_text,
            test_messages.IS_NOT_EQUAL.format(first=strings.unmask_quoted(masked_text, tuples), second=self.test_text)
        )

    #5. Test strings.nnl
    def test_nll_return_type(self) -> None:
        """
        GIVEN a valid string param \n
        WHEN strings.nll method is called \n
        THEN strings.nll return type is not None\n
        AND strings.nll returned value is of type str
        """

        self.assertIsNotNone(
            strings.nnl(self.text_newlines),
            test_messages.METHOD_RETURNS_NONE.format(method=self.nnl_method)
        )

        self.assertIsInstance(
            strings.nnl(self.text_newlines),
            str,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(method=self.nnl_method, value='str')
        )


    def test_nll_correct_value(self) -> None:
        """
        GIVEN a valid string param \n
        WHEN strings.nnl method is called \n
        THEN strings.nnl replaces all new lined '\n' with ' '\n
        """
        text_no_new_lines = """This text has many new lines"""
        self.assertEqual(
            strings.nnl(self.text_newlines),
            text_no_new_lines,
            test_messages.IS_NOT_EQUAL.format(first=strings.nnl(self.text_newlines), second=text_no_new_lines)
        )

    #6. Test strings.remove_comments
    def test_remove_comments_return_type(self) -> None:
        """
        GIVEN a valid string param \n
        WHEN strings.remove_comments method is called \n
        THEN strings.remove_comments return type is not None\n
        AND strings.remove_comments returned value is of type str
        """

        self.assertIsNotNone(
            strings.remove_comments(self.text_newlines),
            test_messages.METHOD_RETURNS_NONE.format(method=self.remove_comments_method)
        )

        self.assertIsInstance(
            strings.remove_comments(self.text_newlines),
            str,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(method=self.remove_comments_method, value='str')
        )

    def test_remove_comments_correct_value(self) -> None:
        """
        GIVEN a valid text string param \n
        WHEN strings.remove_comments method is called \n
        THEN strings.remove_comments removes all comments in the given text\n
        """
        uncommented_text: str = '''ThisisnotacommentLastline'''
        commented_text: str = files.get_file_content(self.commented_text)
        self.assertIsNotNone(
            strings.remove_comments(commented_text),
            test_messages.METHOD_RETURNS_NONE.format(method=self.remove_comments_method)
        )

        self.assertIsInstance(
            strings.remove_comments(commented_text),
            str,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(method=self.remove_comments_method, value='str')
        )

        result = re.sub('\W+', '', strings.remove_comments(commented_text))
        self.assertEqual(
            result,
            uncommented_text,
            test_messages.IS_NOT_EQUAL.format(first=strings.remove_comments(self.commented_text), second=uncommented_text)
        )



    #7. Test strings.slash
    def test_slash_return_type(self) -> None:
        """
        GIVEN a valid file path param \n
        WHEN strings.slash method is called \n
        THEN strings.slash return type is not None\n
        AND strings.slash returned value is of type str
        """

        self.assertIsNotNone(
            strings.slash(self.file_path),
            test_messages.METHOD_RETURNS_NONE.format(method=self.slash_method)
        )

        self.assertIsInstance(
            strings.slash(self.file_path),
            str,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(method=self.slash_method, value='str')
        )

    def test_slash_correct_value(self) -> None:
        """
        GIVEN a valid file path param \n
        WHEN strings.slash method is called \n
        THEN strings.slash adds the trailing slash if it's not already there\n
        """
        self.assertIn(
            strings.slash(self.file_path)[-1],
            ["\\", "/"]
        )

        self.assertEqual(
            strings.slash(self.file_path_slashed),
            self.file_path_slashed,
            test_messages.IS_NOT_EQUAL.format(first=strings.nnl(self.text_newlines),
                                              second=self.file_path_slashed)
        )

        self.assertIn(
            strings.slash(self.file_path_slashed)[-1],
            ["\\", "/"]
        )


    #8. Test strings.tokenize
    def test_tokenize_return_type(self) -> None:
        """
        GIVEN a valid string text param\n
        WHEN strings.tokenize method is called \n
        THEN strings.tokenize return type is not None\n
        AND strings.tokenize returned value is of type list
        """

        self.assertIsNotNone(
            strings.tokenize(self.test_text),
            test_messages.METHOD_RETURNS_NONE.format(method=self.tokenize_method)
        )

        self.assertIsInstance(
            strings.tokenize(self.test_text),
            list,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(method=self.tokenize_method, value='list')
        )

    def test_tokenize_correct_value(self) -> None:
        """
        GIVEN a valid string text param \n
        WHEN strings.tokenize method is called \n
        THEN strings.tokenize tokenizes the text as expetected\n
        """

        self.assertEqual(
            strings.tokenize(self.file_path),
            [self.commented_text],
            test_messages.IS_NOT_EQUAL.format(first=strings.tokenize(self.text_newlines), second=[self.commented_text])
        )

        self.assertEqual(
            strings.tokenize(self.file_path_slashed),
            [self.file_path_slashed],
            test_messages.IS_NOT_EQUAL.format(first=strings.tokenize(self.text_newlines),
                                              second=self.file_path_slashed)
        )


    # 9. Test strings.unaccent
    def test_unaccent_return_type(self) -> None:
        """
        GIVEN a valid string text param\n
        WHEN strings.unaccent method is called \n
        THEN strings.unaccent return type is not None\n
        AND strings.unaccent returned value is of type str
        """

        self.assertIsNotNone(
            strings.unaccent(self.test_text),
            test_messages.METHOD_RETURNS_NONE.format(method=self.unaccent_method)
        )

        self.assertIsInstance(
            strings.unaccent(self.test_text),
            str,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(method=self.unaccent_method, value='str')
        )


    def test_unaccent_correct_value(self) -> None:
        """
        GIVEN a valid string text param \n
        WHEN strings.unnacent method is called \n
        THEN strings.unnacent remvoes diacritics and character symbols from the given text \n
        """
        self.assertEqual(
            strings.unaccent(self.test_text),
            """This "is" a string test text to test "strings" <methods>""",
            test_messages.IS_NOT_EQUAL.format(first=strings.unaccent(self.test_text), second="""This "is" a string test text to test "strings" <methods>""")
        )

    # 10. Test strings.url_tail
    def test_url_tail_return_type(self) -> None:
        """
        GIVEN a valid url as a str param\n
        WHEN strings.url_tail method is called \n
        THEN strings.url_tail return type is not None\n
        AND strings.url_tail returned value is of type str
        """

        self.assertIsNotNone(
            strings.url_tail(self.url),
            test_messages.METHOD_RETURNS_NONE.format(method=self.url_tail_method)
        )

        self.assertIsInstance(
            strings.url_tail(self.url),
            str,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(method=self.url_tail_method, value='str')
        )


    def test_url_tail_correct_value(self) -> None:
        """
        GIVEN a valid string text param \n
        WHEN strings.url_tail method is called \n
        THEN strings.url_tail returns the element id of the given url\n
        """
        self.assertEqual(
            strings.url_tail(self.url),
            'URL',
            test_messages.IS_NOT_EQUAL.format(first=strings.url_tail(self.url),
                                              second='URL')
        )



    # 11. Test strings.url_head
    def test_url_head_return_type(self) -> None:
        """
        GIVEN a valid url as a str param\n
        WHEN strings.url_head method is called \n
        THEN strings.url_head return type is not None\n
        AND strings.url_head returned value is of type str
        """

        self.assertIsNotNone(
            strings.url_head(self.url),
            test_messages.METHOD_RETURNS_NONE.format(method=self.url_head_method)
        )

        self.assertIsInstance(
            strings.url_head(self.url),
            str,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(method=self.url_head_method, value='str')
        )


    def test_url_head_correct_value(self) -> None:
        """
        GIVEN a valid string text param \n
        WHEN strings.url_head method is called \n
        THEN strings.url_head returns the element head of the given url\n
        """

        self.assertEqual(
            strings.url_head(self.url),
            'https://en.wikipedia.org/wiki',
            test_messages.IS_NOT_EQUAL.format(first=strings.url_head(self.url),
                                              second='https://en.wikipedia.org/wiki')
        )


    # 12. Test strings.regex
    def test_regex_return_type(self) -> None:
        """
        GIVEN a valid url as a str param\n
        WHEN strings.regex method is called \n
        THEN strings.regex return type is not None\n
        AND strings.regex returned value is of type str
        """
        regex_condition = rf'<(.*?)>'
        self.assertIsNotNone(
            strings.regex(self.test_text, regex_condition),
            test_messages.METHOD_RETURNS_NONE.format(method=self.regex_method)
        )

        self.assertIsInstance(
            strings.regex(self.test_text, regex_condition),
            str,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(method=self.regex_method, value='str')
        )


    def test_regex_correct_value(self) -> None:
        """
        GIVEN a valid string text param \n
        WHEN strings.regex method is called \n
        THEN strings.regex returns the element head of the given url\n
        """

        regex_condition = rf'<(.*?)>'
        self.assertEqual(
            strings.regex(self.test_text, regex_condition),
            'mèthóds',
            test_messages.IS_NOT_EQUAL.format(first=strings.regex(self.test_text, regex_condition),
                                              second='mèthóds')
        )
