import unittest

from kf_utils import extractors
from test.resources import test_messages


class TestExtractors(unittest.TestCase):
    '''
    Test extractors scripts and methods
    '''

    test_text: str = " This <is a test> text (for) the extractors file. <Please> (ignore) <this> (text) "
    test_text_delimiters: str = " This text is #delimited by two characters* "
    test_text_delimiters_2: str = " This #text* is delimited #twice* "
    test_text_delimiters_3: str = " Text delimited _by the same character_ "
    test_text_double_quoted: str = """ This text contains a "reference" """
    test_text_double_quoted_2: str = """ This text contains a "reference" in "two" places"""
    test_text_single_quoted: str = """ This text contains a 'reference' """
    test_text_single_quoted_2: str = """ This text contains a 'reference' in 'two' places"""
    test_text_exclude_single: str = """ The program should 'exclude' this"""
    test_text_exclude_single_2: str = """ The 'program' 'should' 'exclude' this"""
    test_text_exclude_double: str = """ The program should "exclude" this"""
    test_text_exclude_double_2: str = """ The "program" "should" "exclude" this"""
    test_text_quoted: str = """ This contains both 'single' and "double" quotes """
    test_text_quoted_2: str = """ Text 'single' a "double" b 'exclude' c "exclude" """
    problematic_text: str = "<> this text should be ignored <>"

    extract_angled_method: str = 'extractors.extract_angled'
    extract_between_parenthesis_method: str = 'extractors.extract_between_parenthesis'
    extract_between_delimiters_method: str = 'extractors.extract_between_delimiters'
    extract_quoted_method: str = 'extractors.extract_quoted'
    extract_double_quoted_method: str = 'extractors.extract_double_quoted'
    extract_single_quoted_method: str = 'extractors.extract_single_quoted'

    # 1. Test extractors.extract_angled
    def test_extract_angled_not_valid_param(self) -> None:
        """
        GIVEN a not valid param \n
        WHEN extractors.extract_angled method is called \n
        THEN a TypeError exception is raised
        """
        not_valid_param = ['this is not a valid string param']

        self.assertRaises(TypeError, extractors.extract_angled, not_valid_param)

    def test_extract_angled_return_type(self) -> None:
        """
        GIVEN a valid str param \n
        WHEN extractors.extract_angled method is called \n
        THEN extractors.extract_angled returned value is not None \n
        AND extractors.extract_angled returned value type is list
        """

        extracted_text = extractors.extract_angled(self.test_text)

        self.assertIsNotNone(
            extracted_text,
            test_messages.METHOD_RETURNS_NONE.format(method=self.extract_angled_method)
        )
        self.assertIsInstance(
            extracted_text,
            list,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(method=self.extract_angled_method, value='list')
        )

    def test_extract_angled_return_correct_value(self) -> None:
        """
        GIVEN a valid str param \n
        WHEN extractors.extract_angled method is called \n
        THEN extractors.extract_angled extracts text between < and > correctly\n
        """
        extracted_text = extractors.extract_angled(self.test_text)
        problematic_text = extractors.extract_angled(self.problematic_text)

        self.assertEqual(
            extracted_text,
            ['is a test', 'Please', 'this'],
            test_messages.IS_NOT_EQUAL.format(first="Extracted text", second="expected extracted text")
        )
        self.assertEqual(
            problematic_text,
            ['', ''],
            test_messages.IS_NOT_EQUAL.format(first="Extracted text", second="expected extracted text")
        )

    # 2. Test extractors.extract_between_parenthesis
    def test_extract_between_parenthesis_not_valid_param(self) -> None:
        """
        GIVEN a not valid str param \n
        WHEN extractors.extract_between_parenthesis method is called \n
        THEN an TypeError exception is raised
        """
        not_valid_param = ['this is not a valid string param']

        self.assertRaises(TypeError, extractors.extract_between_parenthesis, not_valid_param)

    def test_extract_between_parenthesis_return_type(self) -> None:
        """
        GIVEN a valid str param \n
        WHEN extractors.extract_between_parenthesis method is called \n
        THEN extractors.extract_between_parenthesis returned value is not None \n
        AND extractors.extract_between_parenthesis returned value type is list
        """

        extracted_parenthesis_text = extractors.extract_between_parenthesis(self.test_text)

        self.assertIsNotNone(
            extracted_parenthesis_text,
            test_messages.METHOD_RETURNS_NONE.format(method=self.extract_between_parenthesis_method)
        )
        self.assertIsInstance(
            extracted_parenthesis_text,
            list,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(method=self.extract_between_parenthesis_method, value='list')
        )

    def test_extract_between_parenthesis_return_correct_value(self) -> None:
        """
        GIVEN a valid str param \n
        WHEN extractors.extract_between_parenthesis method is called \n
        THEN extractors.extract_between_parenthesis extracts text between ( and ) correctly\n
        """
        extracted_text = extractors.extract_between_parenthesis(self.test_text)

        self.assertEqual(
            extracted_text,
            ['for', 'ignore', 'text'],
            test_messages.IS_NOT_EQUAL.format(first="Extracted text", second="expected extracted text")
        )

    # 3. Test extractors.extract_between_delimiters
    def test_extract_between_delimiters_not_valid_param(self) -> None:
        """
        GIVEN a not valid str param \n
        WHEN extractors.extract_between_delimiters method is called \n
        THEN a TypeError exception is raised
        """
        not_valid_param = ['this is not a valid string param']

        self.assertRaises(TypeError, extractors.extract_between_delimiters, not_valid_param)

    def test_extract_between_delimiters_return_type(self) -> None:
        """
        GIVEN a valid str param \n
        WHEN extractors.extract_between_delimiters method is called \n
        THEN extractors.extract_between_delimiters returned value is not None \n
        AND extractors.extract_between_delimiters returned value type is list
        """

        extracted_text = extractors.extract_between_delimiters(self.test_text, '<', '>')

        self.assertIsNotNone(
            extracted_text,
            test_messages.METHOD_RETURNS_NONE.format(method=self.extract_between_delimiters_method)
        )
        self.assertIsInstance(
            extracted_text,
            list,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(method=self.extract_between_delimiters_method, value='list')
        )

    def test_extract_between_delimiters_return_correct_value(self) -> None:
        """
        GIVEN a valid str param \n
        WHEN extractors.extract_between_delimiters method is called \n
        THEN extractors.extract_between_delimiters extracts text between given delimiters correctly\n
        """
        extracted_text = extractors.extract_between_delimiters(self.test_text_delimiters, '#', '*')
        extracted_text_2 = extractors.extract_between_delimiters(self.test_text_delimiters_2, '#', '*')
        extracted_text_3 = extractors.extract_between_delimiters(self.test_text_delimiters_3, '_', '_')

        self.assertEqual(
            extracted_text,
            ['delimited by two characters'],
            test_messages.IS_NOT_EQUAL.format(first="Extracted text", second="expected extracted text")
        )

        self.assertEqual(
            extracted_text_2,
            ['text', 'twice'],
            test_messages.IS_NOT_EQUAL.format(first="Extracted text", second="expected extracted text")
        )

        self.assertEqual(
            extracted_text_3,
            ['by the same character'],
            test_messages.IS_NOT_EQUAL.format(first="Extracted text", second="expected extracted text")
        )


    # 4. Test extractors.extract_quoted
    def test_extract_quoted_valid_param(self) -> None:
        """
        GIVEN a not valid str param \n
        WHEN extractors.extract_quoted method is called \n
        THEN a TypeError exception is raised
        """
        not_valid_param = ['this is not a valid string param']

        self.assertRaises(TypeError, extractors.extract_quoted, not_valid_param)

    def test_extract_quoted_return_type(self) -> None:
        """
        GIVEN a valid str param \n
        WHEN extractors.extract_quoted method is called \n
        THEN extractors.extract_quoted returned value is not None \n
        AND extractors.extract_quoted returned value type is list
        """

        extracted_text = extractors.extract_quoted(self.test_text)

        self.assertIsNotNone(
            extracted_text,
            test_messages.METHOD_RETURNS_NONE.format(method=self.extract_quoted_method)
        )
        self.assertIsInstance(
            extracted_text,
            list,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(method=self.extract_quoted_method, value='list')
        )

    def test_extract_quoted_return_correct_value(self) -> None:
        """
        GIVEN a valid str param \n
        WHEN extractors.extract_quoted method is called \n
        THEN extractors.extract_quoted extracts quoted text correctly\n
        """
        extracted_text = extractors.extract_quoted(self.test_text_quoted, "exclude")
        extracted_text_2 = extractors.extract_quoted(self.test_text_quoted_2, "exclude")

        self.assertEqual(
            extracted_text,
            ["double", 'single'],
            test_messages.IS_NOT_EQUAL.format(first="Extracted text", second="expected extracted text")
        )

        self.assertEqual(
            extracted_text_2,
            ["double", 'single'],
            test_messages.IS_NOT_EQUAL.format(first="Extracted text", second="expected extracted text")
        )

    # 5. Test extractors.extract_double_quoted
    def test_extract_double_quoted_not_valid_param(self) -> None:
        """
        GIVEN a not valid str param \n
        WHEN extractors.extract_double_quoted method is called \n
        THEN a TypeError exception is raised
        """
        not_valid_param = ['this is not a valid string param']

        self.assertRaises(TypeError, extractors.extract_double_quoted, not_valid_param)

    def test_extract_double_quoted_return_type(self) -> None:
        """
        GIVEN a valid str param \n
        WHEN extractors.extract_double_quoted method is called \n
        THEN extractors.extract_double_quoted returned value is not None \n
        AND extractors.extract_double_quoted returned value type is list
        """

        extracted_text = extractors.extract_double_quoted(self.test_text)

        self.assertIsNotNone(
            extracted_text,
            test_messages.METHOD_RETURNS_NONE.format(method=self.extract_double_quoted_method)
        )
        self.assertIsInstance(
            extracted_text,
            list,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(method=self.extract_double_quoted_method, value='list')
        )

    def test_extract_double_quoted_return_correct_value(self) -> None:
        """
        GIVEN a valid str param \n
        WHEN extractors.extract_angled method is called \n
        THEN extractors.extract_angled extracts text between double quotes correctly\n
        """
        extracted_text = extractors.extract_double_quoted(self.test_text_double_quoted)
        extracted_text_2 = extractors.extract_double_quoted(self.test_text_double_quoted_2)
        extracted_text_3 = extractors.extract_double_quoted(self.test_text_exclude_double, "exclude")
        extracted_text_4 = extractors.extract_double_quoted(self.test_text_exclude_double_2, "exclude")

        self.assertEqual(
            extracted_text,
            ['reference'],
            test_messages.IS_NOT_EQUAL.format(first="Extracted text", second="expected extracted text")
        )

        self.assertEqual(
            extracted_text_2,
            ['reference', 'two'],
            test_messages.IS_NOT_EQUAL.format(first="Extracted text", second="expected extracted text")
        )

        self.assertEqual(
            extracted_text_3,
            [],
            test_messages.IS_NOT_EQUAL.format(first="Extracted text", second="expected extracted text")
        )

        self.assertEqual(
            extracted_text_4,
            ['program', 'should'],
            test_messages.IS_NOT_EQUAL.format(first="Extracted text", second="expected extracted text")
        )

    # 6. Test extractors.extract_single_quoted
    def test_extract_single_quoted_not_valid_param(self) -> None:
        """
        GIVEN a not valid str param \n
        WHEN extractors.extract_single_quoted method is called \n
        THEN a TypeError exception is raised
        """
        not_valid_param = ['this is not a valid string param']

        self.assertRaises(TypeError, extractors.extract_single_quoted, not_valid_param)

    def test_extract_single_quoted_return_type(self) -> None:
        """
        GIVEN a valid str param \n
        WHEN extractors.extract_single_quoted method is called \n
        THEN extractors.extract_single_quoted returned value is not None \n
        AND extractors.extract_single_quoted returned value type is list
        """

        extracted_text = extractors.extract_single_quoted(self.test_text)

        self.assertIsNotNone(
            extracted_text,
            test_messages.METHOD_RETURNS_NONE.format(method=self.extract_single_quoted_method)
        )
        self.assertIsInstance(
            extracted_text,
            list,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(method=self.extract_single_quoted_method, value='list')
        )

    def test_extract_single_quoted_return_correct_value(self) -> None:
        """
        GIVEN a valid str param \n
        WHEN extractors.extract_single_quoted method is called \n
        THEN extractors.extract_single_quoted extracts text between single quotes correctly\n
        """
        extracted_text = extractors.extract_single_quoted(self.test_text_single_quoted)
        extracted_text_2 = extractors.extract_single_quoted(self.test_text_single_quoted_2)
        extracted_text_3 = extractors.extract_single_quoted(self.test_text_exclude_single, "exclude")
        extracted_text_4 = extractors.extract_single_quoted(self.test_text_exclude_single_2, "exclude")

        self.assertEqual(
            extracted_text,
            ['reference'],
            test_messages.IS_NOT_EQUAL.format(first="Extracted text", second="expected extracted text")
        )

        self.assertEqual(
            extracted_text_2,
            ['reference', 'two'],
            test_messages.IS_NOT_EQUAL.format(first="Extracted text", second="expected extracted text")
        )

        self.assertEqual(
            extracted_text_3,
            [],
            test_messages.IS_NOT_EQUAL.format(first="Extracted text", second="expected extracted text")
        )

        self.assertEqual(
            extracted_text_4,
            ['program', 'should'],
            test_messages.IS_NOT_EQUAL.format(first="Extracted text", second="expected extracted text")
        )

