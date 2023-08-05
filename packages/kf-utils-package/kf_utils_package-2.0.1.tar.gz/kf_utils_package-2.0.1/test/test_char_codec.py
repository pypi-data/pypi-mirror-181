import unittest

from kf_utils import char_codec, hashers
from test.resources import test_messages


class TestCharCodec(unittest.TestCase):
    '''
    Test CharCodec scripts and methods
    '''

    extract_bracketed_method = 'CharCodec.extract_bracketed'
    extract_quoted_method = 'CharCodec.extract_quoted'
    __code_escaped_quotes__method = 'CharCodec.__code_escaped_quotes__'
    __decode_escaped_quotes__method = 'CharCodec.__decode_escaped_quotes__'
    quoted_method = 'CharCodec.quoted'
    angled_method = 'CharCodec.angled'
    bracketed_method = 'CharCodec.bracketed'
    properties_method = 'CharCodec.properties'
    pointers_method = 'CharCodec.pointers'
    sequence_method = 'CharCodec.sequence'

    def setUp(self) -> None:
        self.test_text = '''This <is a> test "text" #for_ (char_codec.py) methods'''
        self.test_text_2 = '''This contains a \' character'''

    # 1. Test CharCodec.extract_bracketed
    def test_extract_bracketed_not_valid_param(self) -> None:
        """
        GIVEN a not valid string text and delimiters params \n
        WHEN CharCodec.extract_bracketed method is called \n
        THEN a TypeError exception is raised
        """
        not_valid_param = {"this is not a dict"}
        self.assertRaises(TypeError, char_codec.CharCodec.extract_bracketed, not_valid_param, '_', '_')

    def test_extract_bracketed_return_type(self) -> None:
        """
        GIVEN a valid string text and delimiters params \n
        WHEN CharCodec.extract_bracketed method is called \n
        THEN CharCodec.extract_bracketed return type is not None\n
        AND CharCodec.extract_bracketed returned value is of type list
        """

        self.assertIsNotNone(
            char_codec.CharCodec.extract_bracketed(self.test_text, '#', '_'),
            test_messages.METHOD_RETURNS_NONE.format(method=self.extract_bracketed_method)
        )

        self.assertIsNotNone(
            char_codec.CharCodec.extract_bracketed(self.test_text, '#', '#'),
            test_messages.METHOD_RETURNS_NONE.format(method=self.extract_bracketed_method)
        )

        self.assertIsInstance(
            char_codec.CharCodec.extract_bracketed(self.test_text, '#', '_'),
            list,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(method=self.extract_bracketed_method,
                                                              value='list')
        )

    def test_extract_bracketed_correct_value(self) -> None:
        """
        GIVEN a valid string text and delimiters params \n
        WHEN CharCodec.extract_bracketed method is called \n
        THEN CharCodec.extract_bracketed extract text between the given delimiters\n
        """

        extracted_text = ['for']
        self.assertEqual(
            char_codec.CharCodec.extract_bracketed(self.test_text, '#', '_'),
            extracted_text,
            test_messages.IS_NOT_EQUAL.format(first=char_codec.CharCodec.extract_bracketed(self.test_text, '#', '_'),
                                              second=extracted_text)
        )

        extracted_text = ['is a']
        self.assertEqual(
            char_codec.CharCodec.extract_bracketed(self.test_text, '<', '>'),
            extracted_text,
            test_messages.IS_NOT_EQUAL.format(first=char_codec.CharCodec.extract_bracketed(self.test_text, '<', '>'),
                                              second=extracted_text)
        )

        extracted_text = ['text']
        self.assertEqual(
            char_codec.CharCodec.extract_bracketed(self.test_text, '"', '"'),
            extracted_text,
            test_messages.IS_NOT_EQUAL.format(first=char_codec.CharCodec.extract_bracketed(self.test_text, '"', '"'),
                                              second=extracted_text)
        )

        extracted_text = ['char_codec.py']
        self.assertEqual(
            char_codec.CharCodec.extract_bracketed(self.test_text, '(', ')'),
            extracted_text,
            test_messages.IS_NOT_EQUAL.format(first=char_codec.CharCodec.extract_bracketed(self.test_text, '(', ')'),
                                              second=extracted_text)
        )

    # 2. Test CharCodec.extract_quoted
    def test_extract_quoted_not_valid_param(self) -> None:
        """
        GIVEN a not valid string text param \n
        WHEN CharCodec.extract_quoted method is called \n
        THEN a TypeError exception is raised
        """
        not_valid_param = 54
        self.assertRaises(TypeError, char_codec.CharCodec.extract_quoted, not_valid_param)

    def test_extract_quoted_return_type(self) -> None:
        """
        GIVEN a valid string text and delimiters params \n
        WHEN CharCodec.extract_quoted method is called \n
        THEN CharCodec.extract_quoted return type is not None\n
        AND CharCodec.extract_quoted returned value is of type list
        """

        self.assertIsNotNone(
            char_codec.CharCodec.extract_quoted(self.test_text),
            test_messages.METHOD_RETURNS_NONE.format(method=self.extract_quoted_method)
        )

        self.assertIsInstance(
            char_codec.CharCodec.extract_quoted(self.test_text),
            list,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(method=self.quoted_method,
                                                              value='list')
        )

    def test_extract_quoted_correct_value(self) -> None:
        """
        GIVEN a valid string text and delimiters params \n
        WHEN CharCodec.extract_quoted method is called \n
        THEN CharCodec.extract_quoted extract quoted text from the given text\n
        """

        extracted_text = ['text']
        self.assertEqual(
            char_codec.CharCodec.extract_quoted(self.test_text),
            extracted_text,
            test_messages.IS_NOT_EQUAL.format(first=char_codec.CharCodec.extract_quoted(self.test_text),
                                              second=extracted_text)
        )

    # 3. Test CharCodec.__code_escaped_quotes__
    def test__code_escaped_quotes__not_valid_param(self) -> None:
        """
        GIVEN a not valid string text param \n
        WHEN CharCodec.__code_escaped_quotes__ method is called \n
        THEN a TypeError exception is raised
        """
        not_valid_param = 54
        self.assertRaises(TypeError, char_codec.CharCodec.__code_escaped_quotes__, not_valid_param)

    def test__code_escaped_quotes__return_type(self) -> None:
        """
        GIVEN a valid string text and delimiters params \n
        WHEN CharCodec.__code_escaped_quotes__ method is called \n
        THEN CharCodec.__code_escaped_quotes__return type is not None\n
        AND CharCodec.__code_escaped_quotes__ returned value is of type list
        """

        self.assertIsNotNone(
            char_codec.CharCodec.__code_escaped_quotes__(self.test_text),
            test_messages.METHOD_RETURNS_NONE.format(method=self.__code_escaped_quotes__method)
        )

        self.assertIsInstance(
            char_codec.CharCodec.__code_escaped_quotes__(self.test_text),
            tuple,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(method=self.__code_escaped_quotes__method,
                                                              value='tuple')
        )

        self.assertIsInstance(
            char_codec.CharCodec.__code_escaped_quotes__(self.test_text)[0],
            str,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(method=self.__code_escaped_quotes__method,
                                                              value='tuple')
        )

        self.assertIsInstance(
            char_codec.CharCodec.__code_escaped_quotes__(self.test_text)[1],
            bool,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(method=self.__code_escaped_quotes__method,
                                                              value='tuple')
        )

    def test__code_escaped_quotes__correct_value(self) -> None:
        """
        GIVEN a valid string text and delimiters params \n
        WHEN CharCodec.__code_escaped_quotes__ method is called \n
        THEN CharCodec.__code_escaped_quotes__ replaces the characters in the text appearing in the dict\n
        """
        hash = hashers.hash("\'")
        coded_text = 'This contains a '+hash+' character'

        self.assertEqual(
            char_codec.CharCodec.__code_escaped_quotes__(self.test_text_2)[0],
            coded_text,
            test_messages.IS_NOT_EQUAL.format(first=char_codec.CharCodec.__code_escaped_quotes__(self.test_text_2)[0],
                                              second=coded_text)
        )

    # 4. Test CharCodec.__decode_escaped_quotes__
    def test__decode_escaped_quotes__(self) -> None:
        hash = hashers.hash("\'")
        coded_text = 'This contains a ' + hash + ' character'

        self.assertIsNotNone(
            char_codec.CharCodec.__decode_escaped_quotes__(coded_text),
            test_messages.METHOD_RETURNS_NONE.format(method=self.__decode_escaped_quotes__method)
        )

        self.assertIsInstance(
            char_codec.CharCodec.__decode_escaped_quotes__(coded_text),
            str,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(method=self.__decode_escaped_quotes__method,
                                                              value='tuple')
        )

        self.assertEqual(
            char_codec.CharCodec.__decode_escaped_quotes__(coded_text),
            self.test_text_2,
            test_messages.IS_NOT_EQUAL.format(first=char_codec.CharCodec.__decode_escaped_quotes__(coded_text),
                                              second=self.test_text_2)
        )


    # 5. Test CharCodec.quoted
    def test_quoted(self) -> None:
        text = '''This text will be "changed" now'''
        to_replace = 'changed'
        code = 'modified'
        exclude = 'exclude'
        codec = char_codec.CharCodec(text, to_replace, code, exclude)
        modified_text = '''This text will be "modified" now'''

        self.assertIsNotNone(
            codec.quoted(),
            test_messages.METHOD_RETURNS_NONE.format(method=self.quoted_method)
        )

        self.assertIsInstance(
            codec.quoted(),
            str,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(method=self.quoted_method,
                                                              value='str')
        )

        self.assertEqual(
            codec.quoted(),
            modified_text,
            test_messages.IS_NOT_EQUAL.format(first=codec.quoted(),
                                              second=modified_text)
        )


    # 6. Test CharCodec.angled
    def test_angled(self) -> None:
        text = '''This text will be <changed> now'''
        to_replace = 'changed'
        code = 'modified'
        exclude = 'exclude'
        codec = char_codec.CharCodec(text, to_replace, code, exclude)
        modified_text = '''This text will be <modified> now'''

        self.assertIsNotNone(
            codec.angled(exclude),
            test_messages.METHOD_RETURNS_NONE.format(method=self.angled_method)
        )

        self.assertIsInstance(
            codec.angled(exclude),
            str,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(method=self.angled_method,
                                                              value='str')
        )

        self.assertEqual(
            codec.angled(exclude),
            modified_text,
            test_messages.IS_NOT_EQUAL.format(first=codec.angled(exclude),
                                              second=modified_text)
        )


    # 7. Test CharCodec.bracketed
    def test_bracketed(self) -> None:
        text = '''This text will be (changed) now'''
        to_replace = 'changed'
        code = 'modified'
        exclude = 'exclude'
        codec = char_codec.CharCodec(text, to_replace, code, exclude)
        modified_text = '''This text will be (modified) now'''

        self.assertIsNotNone(
            codec.bracketed('(', ')', exclude),
            test_messages.METHOD_RETURNS_NONE.format(method=self.bracketed_method)
        )

        self.assertIsInstance(
            codec.bracketed('(', ')', exclude),
            str,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(method=self.bracketed_method,
                                                              value='str')
        )

        self.assertEqual(
            codec.bracketed('(', ')', exclude),
            modified_text,
            test_messages.IS_NOT_EQUAL.format(first=codec.bracketed('(', ')', exclude),
                                              second=modified_text)
        )


    # 8. Test CharCodec.pointers
    def test_pointers(self) -> None:
        text = "class.function_name(*args, **kwargs))"
        to_replace = '.'
        code = '#'
        exclude = 'exclude'
        codec = char_codec.CharCodec(text, to_replace, code, exclude)
        modified_text = "class#function_name(*args, **kwargs))"

        self.assertIsNotNone(
            codec.pointers(),
            test_messages.METHOD_RETURNS_NONE.format(method=self.pointers_method)
        )

        self.assertIsInstance(
            codec.pointers(),
            str,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(method=self.pointers_method,
                                                              value='str')
        )

        self.assertEqual(
            codec.pointers(),
            modified_text,
            test_messages.IS_NOT_EQUAL.format(first=codec.pointers(),
                                              second=modified_text)
        )


    # 9. Test CharCodec.properties
    def test_properties(self) -> None:
        text = '''md5 = self.io().hash'''
        to_replace = 'changed'
        code = 'modified'
        exclude = 'exclude'
        codec = char_codec.CharCodec(text, to_replace, code, exclude)
        modified_text = '''md5 = self.io()modifiedhash'''

        self.assertIsNotNone(
            codec.properties(),
            test_messages.METHOD_RETURNS_NONE.format(method=self.properties_method)
        )

        self.assertIsInstance(
            codec.properties(),
            str,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(method=self.properties_method,
                                                              value='str')
        )

        self.assertEqual(
            codec.properties(),
            modified_text,
            test_messages.IS_NOT_EQUAL.format(first=codec.properties(),
                                              second=modified_text)
        )


    # 10. Test CharCodec.sequence
    def test_sequence(self) -> None:
        text = "com.nttdata.dgi.crud.Compiler."
        to_replace = '.'
        code = '<__DOT__>'
        exclude = 'exclude'
        codec = char_codec.CharCodec(text, to_replace, code, exclude)
        modified_text = "com<__DOT__>nttdata<__DOT__>dgi<__DOT__>crud<__DOT__>Compiler<__DOT__>"

        self.assertIsNotNone(
            codec.sequence(),
            test_messages.METHOD_RETURNS_NONE.format(method=self.sequence_method)
        )

        self.assertIsInstance(
            codec.sequence(),
            str,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(method=self.sequence_method,
                                                              value='str')
        )

        self.assertEqual(
            codec.sequence(),
            modified_text,
            test_messages.IS_NOT_EQUAL.format(first=codec.sequence(),
                                              second=modified_text)
        )