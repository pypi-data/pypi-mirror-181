import unittest

from kf_utils import __version__
from test.resources import test_messages


class TestVersionFile(unittest.TestCase):
    """
    Test __version__.py file
    """

    mandatory_attributes: list[str] = [
        '__title__',
        '__description__',
        '__url__',
        '__download_url__',
        '__version__',
        '__author__',
        '__license__',
    ]

    def test_version_contains_mandatory_attributes(self) -> None:
        """
        Checks that __version__ file contains all the mandatory
        attributes
        """
        for attribute in self.mandatory_attributes:
            version_attr = getattr(__version__, attribute, None)
            self.assertIsNotNone(
                version_attr,
                test_messages.IS_NONE.format(first=f'{attribute} attribute')
            )
