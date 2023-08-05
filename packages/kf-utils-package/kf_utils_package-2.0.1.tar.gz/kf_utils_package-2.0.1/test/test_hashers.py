import hashlib
import os
import unittest

from kf_utils import hashers
from test.resources import test_messages


class TestHashers(unittest.TestCase):
    """
    Test hashers scripts and methods
    """

    hash_method: str = 'hashers.hash'
    hashbin_method: str = 'hashers.hashbin'
    crc_method: str = 'hashers.crc'
    scrc_method: str = 'hashers.scrc'
    md5_method: str = 'hashers.md5'
    md5int_method: str = 'hashers.md5int'
    uuids_method: str = 'hashers.uuids'

    pwd = os.path.abspath(os.path.dirname(__file__))

    if pwd.endswith('test'):
        plain_text_file_path = os.path.join(
            pwd,
            'resources',
            'plain_text_file.txt'
        )
    else:
        plain_text_file_path = os.path.join(
            pwd,
            'test'
            'resources',
            'plain_text_file.txt'
        )

    with open(plain_text_file_path, 'rb', buffering=0) as f:
        plain_text_file_content = f.read().decode()

    def setUp(self) -> None:
        self.plain_text_file_content_hashed_md5 = hashlib.md5(
            bytearray(self.plain_text_file_content.encode('utf-8'))).hexdigest()

        self.plain_text_file_content_hashed_sha1 = hashlib.sha1(
            bytearray(self.plain_text_file_content.encode('utf-8'))).hexdigest()

        self.plain_text_file_content_hashed_sha256 = hashlib.sha256(
            bytearray(self.plain_text_file_content.encode('utf-8'))).hexdigest()

        self.test_text: str = 'This is a test text for hashing'
        self.test_text_crc: int = 3080635617
        self.test_text_scrc: str = '3080635617'
        self.test_text_md5: str = 'aabf71857499877f1c0c775630e39614'
        self.test_text_md5int: int = 226962790469132544160521203571155506708

    # 1. Test hashers.hashbin method with md5
    def test_hashbin_not_valid_file(self) -> None:
        """
        GIVEN a file path that does not exist \n
        WHEN hashers.hashbin method is called \n
        THEN an FileNotFoundError exception is raised \n
        """
        not_valid_file_path = 'this file does not exist'

        self.assertRaises(FileNotFoundError, hashers.hashbin, not_valid_file_path)

    def test_hashbin_equals_calculated_md5_hash(self) -> None:
        """
        GIVEN a file path that exists \n
        WHEN hashers.hashbin method is called with md5\n
        THEN the returned value is not None \n
        AND the returned value type is str \n
        AND the returned hash equals to the calculated one
        """
        file_hash = hashers.hashbin(self.plain_text_file_path, hashers.HashAlgorithm.md5)

        self.assertIsNotNone(
            file_hash,
            test_messages.METHOD_RETURNS_NONE.format(method=self.hashbin_method)
        )
        self.assertIsInstance(
            file_hash,
            str,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(
                method=self.hashbin_method,
                value='str'
            )
        )
        self.assertEqual(
            file_hash,
            self.plain_text_file_content_hashed_md5
        )

    # 2. Test hashers.hashbin method with sha1
    def test_hashbin_equals_calculated_sha1_hash(self) -> None:
        """
        GIVEN a file path that exists \n
        WHEN hashers.hashbin method is called with sha1\n
        THEN the returned value is not None \n
        AND the returned value type is str \n
        AND the returned hash equals to the calculated one
        """
        file_hash = hashers.hashbin(self.plain_text_file_path, hashers.HashAlgorithm.sha1)

        self.assertIsNotNone(
            file_hash,
            test_messages.METHOD_RETURNS_NONE.format(method=self.hashbin_method)
        )
        self.assertIsInstance(
            file_hash,
            str,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(
                method=self.hashbin_method,
                value='str'
            )
        )
        self.assertEqual(
            file_hash,
            self.plain_text_file_content_hashed_sha1
        )

    # 3. Test hashers.hashbin method with sha256
    def test_hashbin_equals_calculated_sha256_hash(self) -> None:
        """
        GIVEN a file path that exists \n
        WHEN hashers.hashbin method is called with sha256\n
        THEN the returned value is not None \n
        AND the returned value type is str \n
        AND the returned hash equals to the calculated one
        """
        file_hash = hashers.hashbin(self.plain_text_file_path, hashers.HashAlgorithm.sha256)

        self.assertIsNotNone(
            file_hash,
            test_messages.METHOD_RETURNS_NONE.format(method=self.hashbin_method)
        )
        self.assertIsInstance(
            file_hash,
            str,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(
                method=self.hashbin_method,
                value='str'
            )
        )
        self.assertEqual(
            file_hash,
            self.plain_text_file_content_hashed_sha256
        )


    # 4. Test hashers.hash method with md5
    def test_hash_equals_calculated_md5_hash(self) -> None:
        """
        GIVEN a file content as str \n
        WHEN hashers.hash method is called with md5\n
        THEN the returned value is not None \n
        AND the returned value type is str \n
        AND the returned hash equals to the calculated one
        """
        file_hash = hashers.hash(self.plain_text_file_content, hashers.HashAlgorithm.md5)

        self.assertIsNotNone(
            file_hash,
            test_messages.METHOD_RETURNS_NONE.format(method=self.hash_method)
        )
        self.assertIsInstance(
            file_hash,
            str,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(
                method=self.hash_method,
                value='str'
            )
        )
        self.assertEqual(
            file_hash,
            self.plain_text_file_content_hashed_md5
        )

    # 5. Test hashers.hash method with sha1
    def test_hash_equals_calculated_sha1_hash(self) -> None:
        """
        GIVEN a file content as str \n
        WHEN hashers.hash method is called with sha1\n
        THEN the returned value is not None \n
        AND the returned value type is str \n
        AND the returned hash equals to the calculated one
        """
        file_hash = hashers.hash(self.plain_text_file_content, hashers.HashAlgorithm.sha1)

        self.assertIsNotNone(
            file_hash,
            test_messages.METHOD_RETURNS_NONE.format(method=self.hash_method)
        )
        self.assertIsInstance(
            file_hash,
            str,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(
                method=self.hash_method,
                value='str'
            )
        )
        self.assertEqual(
            file_hash,
            self.plain_text_file_content_hashed_sha1
        )

    # 6. Test hashers.hash method with sha256
    def test_hash_equals_calculated_sha256_hash(self) -> None:
        """
        GIVEN a file content as str \n
        WHEN hashers.hash method is called with sha256\n
        THEN the returned value is not None \n
        AND the returned value type is str \n
        AND the returned hash equals to the calculated one
        """
        file_hash = hashers.hash(self.plain_text_file_content, hashers.HashAlgorithm.sha256)

        self.assertIsNotNone(
            file_hash,
            test_messages.METHOD_RETURNS_NONE.format(method=self.hash_method)
        )
        self.assertIsInstance(
            file_hash,
            str,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(
                method=self.hash_method,
                value='str'
            )
        )
        self.assertEqual(
            file_hash,
            self.plain_text_file_content_hashed_sha256
        )


    #7. Test hashers.crc method
    def test_crc_correct_value(self) -> None:
        crc_value = hashers.crc(self.test_text)
        self.assertIsNotNone(
            crc_value,
            test_messages.METHOD_RETURNS_NONE.format(method=self.crc_method)
        )
        self.assertIsInstance(
            crc_value,
            int,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(
                method=self.crc_method,
                value='int'
            )
        )
        self.assertEqual(
            crc_value,
            self.test_text_crc
        )


    #8. Test hashers.scrc method
    def test_scrc_correct_value(self) -> None:
        scrc_value = hashers.scrc(self.test_text)
        self.assertIsNotNone(
            scrc_value,
            test_messages.METHOD_RETURNS_NONE.format(method=self.scrc_method)
        )
        self.assertIsInstance(
            scrc_value,
            str,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(
                method=self.scrc_method,
                value='str'
            )
        )
        self.assertEqual(
            scrc_value,
            self.test_text_scrc
        )


    #9. Test hashers.md5 method
    def test_md5_correct_value(self) -> None:
        md5_value = hashers.md5(self.test_text)
        self.assertIsNotNone(
            md5_value,
            test_messages.METHOD_RETURNS_NONE.format(method=self.md5_method)
        )
        self.assertIsInstance(
            md5_value,
            str,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(
                method=self.md5_method,
                value='str'
            )
        )
        self.assertEqual(
            md5_value,
            self.test_text_md5
        )


    #10. Test hashers.uuids method
    def test_uuids_correct_value(self) -> None:
        uuids_value = hashers.uuids()
        self.assertIsNotNone(
            uuids_value,
            test_messages.METHOD_RETURNS_NONE.format(method=self.uuids_method)
        )
        self.assertIsInstance(
            uuids_value,
            str,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(
                method=self.uuids_method,
                value='str'
            )
        )
        self.assertNotEqual(
            uuids_value,
            hashers.uuids() #Check that the method returns different values on each call
        )

    #11. Test hashers.md5int method
    def test_md5int_correct_value(self) -> None:
        md5int_value = hashers.md5int(self.test_text)
        self.assertIsNotNone(
            md5int_value,
            test_messages.METHOD_RETURNS_NONE.format(method=self.md5int_method)
        )
        self.assertIsInstance(
            md5int_value,
            int,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(
                method=self.uuids_method,
                value='str'
            )
        )
        self.assertEqual(
            md5int_value,
            self.test_text_md5int
        )