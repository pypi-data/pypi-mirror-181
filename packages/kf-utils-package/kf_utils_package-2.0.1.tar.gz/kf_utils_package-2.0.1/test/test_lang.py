import unittest

from kf_utils import lang
from test.resources import test_messages


class TestLang(unittest.TestCase):
    '''
    Test lang scripts and methods
    '''

    alpha2_method = 'lang.alpha2'


    # 1. Test lang.alpha2 method
    def test_alpha2_correct_value(self) -> None:
        expanded_lang = 'en-US'
        short_lang = 'en'

        self.assertIsNotNone(
            lang.alpha2(expanded_lang),
            test_messages.METHOD_RETURNS_NONE.format(method=self.alpha2_method)
        )

        self.assertIsInstance(
            lang.alpha2(expanded_lang),
            str,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(method=self.alpha2_method, value='str')
        )

        self.assertEqual(
            lang.alpha2(expanded_lang),
            short_lang,
            test_messages.IS_NOT_EQUAL.format(first=lang.alpha2(expanded_lang), second={short_lang})
        )