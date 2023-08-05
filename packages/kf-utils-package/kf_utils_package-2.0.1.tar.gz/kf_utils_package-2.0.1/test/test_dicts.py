import unittest

from kf_utils import dicts
from test.resources import test_messages


class TestDicts(unittest.TestCase):
    """
    Test dicts scripts and methods
    """

    clean_dict_method = 'dicts.clean_dict'

    test_dict: dict = {
        "str_value": 'value',
        "int_value": 1,
        "bool_value": True,
        "none_value": None
    }
    test_dict_keys: list[str] = list(test_dict.keys())

    # 1. Test dicts.clean_dict method
    def test_clean_dict_not_valid_param(self) -> None:
        """
        GIVEN a not valid dict param \n
        WHEN dicts.clean_dict method is called \n
        THEN an AttributeError exception is raised
        """
        not_valid_param = 'I''m a string, not a dict'

        self.assertRaises(AttributeError, dicts.clean_dict, not_valid_param)

    def test_clean_dict_return_type(self) -> None:
        """
        GIVEN a valid dict param \n
        WHEN dicts.clean_dict method is called \n
        THEN dicts.clean_dict returned value is not None \n
        AND dicts.clean_dict returned value type is dict
        """
        clean_dict = dicts.clean_dict(self.test_dict)

        self.assertIsNotNone(
            clean_dict,
            test_messages.METHOD_RETURNS_NONE.format(method=self.clean_dict_method)
        )
        self.assertIsInstance(
            clean_dict,
            dict,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(method=self.clean_dict_method, value='dict')
        )

    def test_clean_dict_remove_null_values(self) -> None:
        """
        GIVEN a valid dict param \n
        AND contains null value \n
        WHEN dicts.clean_dict method is called \n
        THEN dicts.clean_dict returned dict values does not contain null values \n
        AND dicts.clean_dict returned dict keys are not equal to origin dict keys
        """
        self.test_clean_dict_return_type()

        clean_dict = dicts.clean_dict(self.test_dict)
        clean_dict_keys = list(clean_dict.keys())
        clean_dict_values = list(clean_dict.values())

        self.assertNotIn(
            None,
            clean_dict_values,
            test_messages.METHOD_RETURNED_OBJECT_CONTAINS_VALUE.format(
                method=self.clean_dict_method,
                returns='dict',
                value='None'
            )
        )
        self.assertNotEqual(
            self.test_dict_keys,
            clean_dict_keys,
            test_messages.IS_EQUAL.format(
                first='Origin dict',
                second='dicts.clean_dict returned dict'
            )
        )
