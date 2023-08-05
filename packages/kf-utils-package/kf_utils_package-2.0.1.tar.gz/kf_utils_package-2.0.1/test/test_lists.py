import unittest

from kf_utils import lists
from test.resources import test_messages


class TestLists(unittest.TestCase):
    """
    Test lists scripts and methods
    """

    duplicated_method = 'lists.duplicated'
    index_method = 'lists.index'
    ordered_set_method = 'lists.orderded_set'
    remove_duplicates_method = 'lists.remove_duplicates'

    def setUp(self) -> None:
        self.test_list_1 = []
        self.test_list_2 = ['repeat', 'repeat']
        self.test_list_3 = ['one', 'two', 'three']
        self.test_list_4 = ['a', 'a', 'd', 'd', 'c', 'c', 'a']
        self.test_list_5 = ['test', 'repetition', 'test']
        self.test_list_6 = ["sensitive"]
        self.test_list_7 = [4, 4, 0, 0, 2, 2]

    #1. Test lists.duplicated method
    def test_duplicated_not_valid_param(self) -> None:
        """
        GIVEN a not valid list param \n
        WHEN lists.duplicated method is called \n
        THEN a TypeError exception is raised
        """
        not_valid_param = 54
        self.assertRaises(TypeError, lists.duplicated, not_valid_param)

    def test_duplicated_return_type(self) -> None:
        """
        GIVEN a valid list param \n
        WHEN lists.duplicated method is called \n
        THEN lists.duplicated detects if there are duplicated values correctly\n
        """

        self.assertIsNotNone(
            lists.duplicated(self.test_list_1),
            test_messages.METHOD_RETURNS_NONE.format(method=self.duplicated_method)
        )
        self.assertIsNotNone(
            lists.duplicated(self.test_list_3),
            test_messages.METHOD_RETURNS_NONE.format(method=self.duplicated_method)
        )
        self.assertIsNotNone(
            lists.duplicated(self.test_list_5),
            test_messages.METHOD_RETURNS_NONE.format(method=self.duplicated_method)
        )
        self.assertIsInstance(
            lists.duplicated(self.test_list_1),
            bool,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(method=self.duplicated_method, value='list')
        )
        self.assertIsInstance(
            lists.duplicated(self.test_list_3),
            bool,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(method=self.duplicated_method, value='list')
        )
        self.assertIsInstance(
            lists.duplicated(self.test_list_5),
            bool,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(method=self.duplicated_method, value='list')
        )


    def test_duplicated_correct_value(self) -> None:
        """
        GIVEN a valid list param \n
        WHEN lists.duplicated method is called \n
        THEN lists.duplicated return value is the correct position of the pattern in the list or None if not found\n
        """
        self.assertEqual(
            lists.duplicated(self.test_list_1),
            False
        )
        self.assertEqual(
            lists.duplicated(self.test_list_2),
            True
        )
        self.assertEqual(
            lists.duplicated(self.test_list_3),
            False
        )
        self.assertEqual(
            lists.duplicated(self.test_list_4),
            True
        )
        self.assertEqual(
            lists.duplicated(self.test_list_5),
            True
        )
        self.assertEqual(
            lists.duplicated(self.test_list_6),
            False
        )


    # 2. Test lists.index method
    def test_index_not_valid_param(self) -> None:
        """
        GIVEN a not valid list param \n
        WHEN lists.index method is called \n
        THEN a TypeError exception is raised
        """
        not_valid_param = "This is not a list"
        self.assertRaises(TypeError, lists.index, not_valid_param)

    def test_index_return_type(self) -> None:
        """
        GIVEN a valid list param \n
        WHEN lists.index method is called \n
        THEN lists.index return is None or is of type bool\n
        """
        tested_list_1 = lists.index(self.test_list_1, 'hello')
        tested_list_3 = lists.index(self.test_list_3, 'two')
        tested_list_6 = lists.index(self.test_list_5, 'None')
        if tested_list_1 is not None:
            self.assertIsInstance(
                tested_list_1,
                bool,
                test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(method=self.index_method, value='bool or None')
            )
        if tested_list_1 is not None:
            self.assertIsInstance(
                tested_list_3,
                bool,
                test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(method=self.index_method, value='bool or None')
            )
        if tested_list_1 is not None:
            self.assertIsInstance(
                tested_list_6,
                bool,
                test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(method=self.index_method, value='bool or None')
            )

    def test_index_correct_value(self) -> None:
        """
        GIVEN a valid list param \n
        WHEN lists.index method is called \n
        THEN lists.index return value is the correct position of the pattern in the list or None if not found\n
        """

        self.assertEqual(
            lists.index(self.test_list_1, 'empty'),
            None
        )
        self.assertEqual(
            lists.index(self.test_list_2, 'repeat'),
            0
        )
        self.assertEqual(
            lists.index(self.test_list_3, 'four'),
            None
        )
        self.assertEqual(
            lists.index(self.test_list_4, 'd'),
            2
        )
        self.assertEqual(
            lists.index(self.test_list_5, 'test'),
            0
        )

        self.assertEqual(
            lists.index(self.test_list_6, 'Sensitive', True),
            0
        )

        self.assertEqual(
            lists.index(self.test_list_6, 'Sensitive', False),
            None
        )



    # 3. Test lists.ordered_set method
    def test_ordered_set_not_valid_param(self) -> None:
        """
        GIVEN a not valid list param \n
        WHEN lists.ordered_set method is called \n
        THEN a TypeError exception is raised
        """

        not_valid_param = 55
        self.assertRaises(TypeError, lists.ordered_set, not_valid_param)

    def test_ordered_set_return_type(self) -> None:
        """
        GIVEN a valid list param \n
        WHEN lists.ordered_set method is called \n
        THEN lists.ordered_set return value is not None\n
        AND lists.ordered_set return value is of type list
        """

        self.assertIsInstance(
            lists.ordered_set(self.test_list_1),
            list,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(method=self.ordered_set_method, value='list')
        )

        self.assertIsInstance(
            lists.ordered_set(self.test_list_3),
            list,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(method=self.ordered_set_method, value='list')
        )

        self.assertIsInstance(
            lists.ordered_set(self.test_list_6),
            list,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(method=self.ordered_set_method, value='list')
        )

    def test_ordered_set_correct_value(self) -> None:
        """
        GIVEN a valid list param \n
        WHEN lists.ordered_set method is called \n
        THEN lists.ordered_set returns the given list ordered and without duplicate items \n
        """
        self.assertEqual(
            lists.ordered_set(self.test_list_1),
            []
        )
        self.assertEqual(
            lists.ordered_set(self.test_list_2),
            ['repeat']
        )
        self.assertEqual(
            lists.ordered_set(self.test_list_3),
            ['one', 'two', 'three']
        )
        self.assertEqual(
            lists.ordered_set(self.test_list_4),
            ['a', 'd', 'c']
        )
        self.assertEqual(
            lists.ordered_set(self.test_list_5),
            ['test', 'repetition']
        )
        self.assertEqual(
            lists.ordered_set(self.test_list_7),
            [4, 0 ,2]
        )

    # 4. Test lists.remove_duplicates method
    def test_remove_duplicates_not_valid_param(self) -> None:
        """
        GIVEN a not valid list param \n
        WHEN lists.remove_duplicates method is called \n
        THEN a TypeError exception is raised
        """

        not_valid_param = 55
        self.assertRaises(TypeError, lists.remove_duplicates, not_valid_param)

    def test_remove_duplicates_return_type(self) -> None:
        """
        GIVEN a valid list param \n
        WHEN lists.remove_duplicates method is called \n
        THEN lists.remove_duplicates return value is not None\n
        AND lists.remove_duplicates return value is of type list
        """
        tested_list_1 = lists.remove_duplicates(self.test_list_1)
        tested_list_3 = lists.remove_duplicates(self.test_list_3)
        tested_list_6 = lists.remove_duplicates(self.test_list_5)

        self.assertIsInstance(
            tested_list_1,
            list,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(method=self.remove_duplicates_method, value='list')
        )

        self.assertIsInstance(
            tested_list_3,
            list,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(method=self.remove_duplicates_method, value='list')
        )

        self.assertIsInstance(
            tested_list_6,
            list,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(method=self.remove_duplicates_method, value='list')
        )

    def test_remove_duplicates_correct_value(self) -> None:
        """
        GIVEN a valid list param \n
        WHEN lists.remove_duplicates method is called \n
        THEN lists.remove_duplicatesreturns the given list ordered and without duplicate items \n
        """

        self.assertEqual(
            lists.remove_duplicates(self.test_list_1),
            []
        )
        self.assertEqual(
            lists.remove_duplicates(self.test_list_2),
            ['repeat']
        )
        self.assertEqual(
            lists.remove_duplicates(self.test_list_3),
            ['one', 'two', 'three']
        )
        self.assertEqual(
            lists.remove_duplicates(self.test_list_4),
            ['a', 'd', 'c']
        )
        self.assertEqual(
            lists.remove_duplicates(self.test_list_5),
            ['test', 'repetition']
        )
        self.assertEqual(
            lists.remove_duplicates(self.test_list_6),
            ['sensitive']
        )
        self.assertEqual(
            lists.remove_duplicates(self.test_list_7),
            [4, 0, 2]
        )