import unittest

from test.resources.test_messages import IMPORT_IS_NONE


class TestUnittest(unittest.TestCase):
    """
    Test kf_utils and dependent packages imports
    """

    def test_import_kf_utils(self) -> None:
        """
        GIVEN a kf_utils package
        WHEN it's imported
        THEN no error is raised
        AND all the modules can be accessed directly
        """
        import kf_utils

        self.assertIsNotNone(kf_utils, IMPORT_IS_NONE.format(package='kf_utils'))

        char_codec = kf_utils.char_codec
        dicts = kf_utils.dicts
        extractors = kf_utils.extractors
        files = kf_utils.files
        graphs = kf_utils.graphs
        hashers = kf_utils.hashers
        lang = kf_utils.lang
        lists = kf_utils.lists
        replacers = kf_utils.replacers
        strings = kf_utils.strings
        timers = kf_utils.timers

        self.assertIsNotNone(char_codec, IMPORT_IS_NONE.format(package='char_codec'))
        self.assertIsNotNone(dicts, IMPORT_IS_NONE.format(package='dicts'))
        self.assertIsNotNone(extractors, IMPORT_IS_NONE.format(package='extractors'))
        self.assertIsNotNone(files, IMPORT_IS_NONE.format(package='files'))
        self.assertIsNotNone(graphs, IMPORT_IS_NONE.format(package='graphs'))
        self.assertIsNotNone(hashers, IMPORT_IS_NONE.format(package='hashers'))
        self.assertIsNotNone(lang, IMPORT_IS_NONE.format(package='lang'))
        self.assertIsNotNone(lists, IMPORT_IS_NONE.format(package='lists'))
        self.assertIsNotNone(replacers, IMPORT_IS_NONE.format(package='replacers'))
        self.assertIsNotNone(strings, IMPORT_IS_NONE.format(package='strings'))
        self.assertIsNotNone(timers, IMPORT_IS_NONE.format(package='timers'))

    def test_import_data_types(self) -> None:
        """
        GIVEN a data_types package
        WHEN it's imported
        THEN no error is raised
        AND all the modules can be accessed directly
        """
        from kf_utils import data_types

        self.assertIsNotNone(data_types, IMPORT_IS_NONE.format(package='data_types'))

        uri = data_types.uri

        self.assertIsNotNone(uri, IMPORT_IS_NONE.format(package='uri'))
