import os
import re
import shutil
import sys
import unittest
from collections.abc import Iterator
from json import loads, JSONDecodeError, load

from kf_utils import files
from test.resources import test_messages


class TestFiles(unittest.TestCase):
    """
    Test files scripts and methods
    """

    make_dirs_method: str = 'files.make_dirs'
    get_extension_from_file_name_method: str = 'files.get_extension_from_file_name'
    get_file_method: str = 'files.get_file'
    get_directory_and_file_name_and_extension_from_path_method: str = 'files' \
                                                                      '.get_directory_and_file_' \
                                                                      'name_and_extension_from_path'
    get_file_content_method: str = 'files.get_file_content'
    from_json_method: str = 'files.from_json'
    to_json_method: str = 'files.to_json'
    exist_method: str = 'files.exist'
    drop_file_method: str = 'files.drop_file'
    base64_method: str = 'files.base64_'
    copy_file_method: str = 'files.copy_file'
    count_occurrences_in_file_method: str = 'files.count_occurrences_in_file'
    delete_line_number_method: str = 'files.delete_line_number'
    to_file_method: str = 'files.to_file'
    delete_method: str = 'files.delete'
    get_file_name_from_path_method: str = 'files.get_file_name_from_path'
    file_split_name_ext_method: str = 'files.file_split_name_ext'
    get_file_extension_method: str = 'files.get_file_extension'
    remove_extension_from_file_path_method: str = 'files.remove_extension_from_file_path'
    get_file_name_method: str = 'files.get_file_name'
    get_file_root_path_method: str = 'files.get_file_root_path'
    drop_dir_method: str = 'files.drop_dir'
    from_yaml_method: str = 'files.from_yaml'
    path_exists_method: str = 'files.path_exists'
    grep_method: str = 'files.grep'
    head_method: str = 'files.head'
    tail_method: str = 'files.tail'
    import_library_method: str = 'files.import_library'
    remove_file_protocol_method: str = 'files.remove_file_protocol'
    to_file_line_method: str = 'files.to_file_line'
    xst_file_method: str = 'files.xst_file'
    extract_files_from_zip_folder_method: str = 'files.extract_files_from_zip_folder'
    get_file_name_length_method: str = 'files.get_file_name_length'
    get_file_size_method: str = 'files.get_file_size'

    pwd = os.path.abspath(os.path.dirname(__file__))

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

    plain_text_file_path: str = os.path.join(resources_path, 'plain_text_file.txt')
    json_file_path: str = os.path.join(resources_path, 'json_file.json')
    test_files_folder: str = os.path.join(pwd, 'test_files_folder')
    delete_folder: str = os.path.join(pwd, 'delete_folder')
    folder_to_zip: str = os.path.join(resources_path, 'folder_to_zip')
    zip_folder: str = os.path.join(resources_path, 'zip_folder.zip')
    folder_to_zip_backup: str = os.path.join(resources_path, 'folder_to_zip_backup')

    def setUp(self) -> None:
        with open(self.plain_text_file_path, mode='r', encoding='utf-8') as f:
            self.plain_text_file_content: str = f.read()
        with open(self.json_file_path, mode='r', encoding='utf-8') as f:
            self.json_file_content: str = f.read()

        try:
            if os.path.exists(self.test_files_folder):
                shutil.rmtree(self.test_files_folder)
            os.makedirs(self.test_files_folder, exist_ok=True)
        except OSError as ex:
            print('Error creating test_files folder', ex.strerror)

    def tearDown(self) -> None:
        try:
            shutil.rmtree(self.test_files_folder)
        except OSError as ex:
            print('Error removing test_files folder', ex.strerror)

    # 1. Test files.make_dirs
    def test_make_dirs_creates_directories(self) -> None:
        """
        GIVEN a valid complete path to a file \n
        WHEN the method is executed \n
        THEN the directories preceding the name of the file have been created \n
        """
        # The full path will be: {pwd}/test_files_folder/make_dirs_parent/make_dirs_child/test.txt
        parent_directory: str = os.path.join(self.test_files_folder, 'make_dirs_parent')
        child_directory: str = os.path.join(parent_directory, 'make_dirs_child')
        file_path: str = os.path.join(child_directory, 'test.txt')

        files.make_dirs(file_path)

        parent_directory_exists: bool = os.path.exists(parent_directory)
        child_directory_exists: bool = os.path.exists(child_directory)

        self.assertTrue(parent_directory_exists, 'The parent directory has not been created')
        self.assertTrue(child_directory_exists, 'The child directory has not been created')

    # 2. Test files.get_extension_from_file_name
    def test_get_extension_from_file_name_using_file(self) -> None:
        """
        GIVEN a file \n
        WHEN the method is executed \n
        THEN the file name is returned \n
        AND the file extension is returned \n
        """
        file_name: str = 'test.txt'

        result: tuple[str, str] = files.get_extension_from_file_name(file_name)

        self.assertIsNotNone(
            result,
            test_messages.IS_NONE.format(first=f'{self.get_extension_from_file_name_method} returns a None value')
        )
        self.assertIsInstance(
            result,
            tuple,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(
                method=self.get_extension_from_file_name_method,
                value='tuple[str, str]'
            )
        )

        returned_file_name: str = result[0]
        returned_file_extension: str = result[1]

        self.assertIsInstance(returned_file_name, str)
        self.assertIsInstance(returned_file_extension, str)
        self.assertEqual(
            returned_file_name,
            'test',
            test_messages.IS_NOT_EQUAL.format(
                first=f'{self.get_extension_from_file_name_method} file name ({returned_file_name})',
                second='test'
            )
        )
        self.assertEqual(
            returned_file_extension,
            'txt',
            test_messages.IS_NOT_EQUAL.format(
                first=f'{self.get_extension_from_file_name_method} file extension ({returned_file_extension})',
                second='txt'
            )
        )

    def test_get_extension_from_file_name_using_folder(self) -> None:
        """
        GIVEN a folder \n
        WHEN the method is executed \n
        THEN the folder name is returned \n
        AND the folder extension is returned empty \n
        """
        folder_name: str = self.test_files_folder

        result: tuple[str, str] = files.get_extension_from_file_name(folder_name)

        self.assertIsNotNone(
            result,
            test_messages.IS_NONE.format(first=f'{self.get_extension_from_file_name_method} returns a None value')
        )
        self.assertIsInstance(
            result,
            tuple,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(
                method=self.get_extension_from_file_name_method,
                value='tuple[str, str]'
            )
        )

        returned_folder_name: str = result[0]
        returned_folder_extension: str = result[1]

        self.assertIsInstance(returned_folder_name, str)
        self.assertIsInstance(returned_folder_extension, str)
        self.assertEqual(
            returned_folder_name,
            folder_name,
            test_messages.IS_NOT_EQUAL.format(
                first=f'{self.get_extension_from_file_name_method} file name ({returned_folder_name})',
                second=folder_name
            )
        )
        self.assertEqual(
            returned_folder_extension,
            '',
            test_messages.IS_NOT_EQUAL.format(
                first=f'{self.get_extension_from_file_name_method} file extension ({returned_folder_extension})',
                second=''
            )
        )

    def test_get_file_using_file(self) -> None:
        """
        GIVEN a path to a file \n
        WHEN the method is executed \n
        THEN the file name is returned \n
        AND the file extension is returned \n
        """
        file_path: str = os.path.join(self.test_files_folder, 'test.txt')

        result: tuple[str, str] = files.get_file(file_path)

        self.assertIsNotNone(
            result,
            test_messages.IS_NONE.format(first=f'{self.get_extension_from_file_name_method} returns a None value')
        )
        self.assertIsInstance(
            result,
            tuple,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(
                method=self.get_extension_from_file_name_method,
                value='tuple[str, str]'
            )
        )

        returned_file_name: str = result[0]
        returned_file_extension: str = result[1]

        self.assertIsInstance(returned_file_name, str)
        self.assertIsInstance(returned_file_extension, str)
        self.assertEqual(
            returned_file_name,
            'test',
            test_messages.IS_NOT_EQUAL.format(
                first=f'{self.get_extension_from_file_name_method} file name ({returned_file_name})',
                second='test'
            )
        )
        self.assertEqual(
            returned_file_extension,
            'txt',
            test_messages.IS_NOT_EQUAL.format(
                first=f'{self.get_extension_from_file_name_method} file extension ({returned_file_extension})',
                second='txt'
            )
        )

    def test_get_file_using_folder(self) -> None:
        """
        GIVEN a path to a folder \n
        WHEN the method is executed \n
        THEN the folder name is returned \n
        AND the folder extension is returned empty \n
        """
        folder_name: str = 'test'
        folder_path: str = os.path.join(self.test_files_folder, folder_name)

        result: tuple[str, str] = files.get_file(folder_path)

        self.assertIsNotNone(
            result,
            test_messages.IS_NONE.format(first=f'{self.get_extension_from_file_name_method} returns a None value')
        )
        self.assertIsInstance(
            result,
            tuple,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(
                method=self.get_extension_from_file_name_method,
                value='tuple[str, str]'
            )
        )

        returned_folder_name: str = result[0]
        returned_folder_extension: str = result[1]

        self.assertIsInstance(returned_folder_name, str)
        self.assertIsInstance(returned_folder_extension, str)
        self.assertEqual(
            returned_folder_name,
            folder_name,
            test_messages.IS_NOT_EQUAL.format(
                first=f'{self.get_extension_from_file_name_method} file name ({returned_folder_name})',
                second=folder_name
            )
        )
        self.assertEqual(
            returned_folder_extension,
            '',
            test_messages.IS_NOT_EQUAL.format(
                first=f'{self.get_extension_from_file_name_method} file extension ({returned_folder_extension})',
                second=''
            )
        )

    # 3. Test files.get_directory_and_file_name_and_extension_from_path
    def test_get_directory_and_file_name_and_extension_from_path_using_file(self) -> None:
        """
        GIVEN a path to a file \n
        WHEN the method is executed \n
        THEN the full path to the file is returned \n
        AND the file name is returned \n
        AND the file extension is returned \n
        """
        file_name: str = 'test.txt'
        file_path: str = os.path.join(self.test_files_folder, file_name)

        result: tuple[str, str, str] = files.get_directory_and_file_name_and_extension_from_path(file_path)

        self.assertIsNotNone(
            result,
            test_messages.IS_NONE.format(first=f'{self.get_extension_from_file_name_method} returns a None value')
        )
        self.assertIsInstance(
            result,
            tuple,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(
                method=self.get_extension_from_file_name_method,
                value='tuple[str, str, str]'
            )
        )

        returned_folder: str = result[0]
        returned_file_name: str = result[1]
        returned_file_extension: str = result[2]

        self.assertIsInstance(returned_folder, str)
        self.assertIsInstance(returned_file_name, str)
        self.assertIsInstance(returned_file_extension, str)
        self.assertEqual(
            returned_folder,
            self.test_files_folder,
            test_messages.IS_NOT_EQUAL.format(
                first=f'{self.get_extension_from_file_name_method} full path ({returned_folder})',
                second=self.test_files_folder
            )
        )
        self.assertEqual(
            returned_file_name,
            'test',
            test_messages.IS_NOT_EQUAL.format(
                first=f'{self.get_extension_from_file_name_method} file name ({returned_file_name})',
                second='test'
            )
        )
        self.assertEqual(
            returned_file_extension,
            'txt',
            test_messages.IS_NOT_EQUAL.format(
                first=f'{self.get_extension_from_file_name_method} file extension ({returned_file_extension})',
                second='txt'
            )
        )

    def test_get_directory_and_file_name_and_extension_from_path_using_folder(self) -> None:
        """
        GIVEN a path to a folder \n
        WHEN the method is executed \n
        THEN the full path to the folder is returned \n
        AND the folder name is returned \n
        AND the folder extension is returned empty \n
        """
        folder_name: str = 'testing'
        file_path: str = os.path.join(self.test_files_folder, folder_name)

        result: tuple[str, str, str] = files.get_directory_and_file_name_and_extension_from_path(file_path)

        self.assertIsNotNone(
            result,
            test_messages.METHOD_RETURNS_NONE.format(method=self.get_extension_from_file_name_method)
        )
        self.assertIsInstance(
            result,
            tuple,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(
                method=self.get_extension_from_file_name_method,
                value='tuple[str, str, str]'
            )
        )

        returned_folder: str = result[0]
        returned_file_name: str = result[1]
        returned_file_extension: str = result[2]

        self.assertIsInstance(returned_folder, str)
        self.assertIsInstance(returned_file_name, str)
        self.assertIsInstance(returned_file_extension, str)
        self.assertEqual(
            returned_folder,
            self.test_files_folder,
            test_messages.IS_NOT_EQUAL.format(
                first=f'{self.get_extension_from_file_name_method} full path ({returned_folder})',
                second=self.test_files_folder
            )
        )
        self.assertEqual(
            returned_file_name,
            folder_name,
            test_messages.IS_NOT_EQUAL.format(
                first=f'{self.get_extension_from_file_name_method} file name ({returned_file_name})',
                second=folder_name
            )
        )
        self.assertEqual(
            returned_file_extension,
            '',
            test_messages.IS_NOT_EQUAL.format(
                first=f'{self.get_extension_from_file_name_method} file extension ({returned_file_extension})',
                second=''
            )
        )

    # 4. Test files.get_file_content
    def test_get_file_content_valid_file(self) -> None:
        """
        GIVEN a path to an existing file \n
        WHEN the method is executed \n
        THEN the file content is correctly returned \n
        """
        file_content: str = files.get_file_content(self.plain_text_file_path)

        self.assertIsNotNone(
            file_content,
            test_messages.METHOD_RETURNS_NONE.format(method=self.get_file_content_method)
        )
        self.assertIsInstance(
            file_content,
            str,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(
                method=self.get_file_content_method,
                value='str'
            )
        )

        self.assertEqual(
            file_content.strip(),
            self.plain_text_file_content.strip(),
            test_messages.IS_NOT_EQUAL.format(
                first=f'Returned file content ({file_content})',
                second=self.plain_text_file_content
            )
        )

    def test_get_file_content_not_valid_file(self) -> None:
        """
        GIVEN a path to a not existing file \n
        WHEN the method is executed \n
        THEN it raises a FileNotFoundError exception \n
        """
        not_valid_file_path = 'this file does not exist'

        self.assertRaises(FileNotFoundError, files.get_file_content, not_valid_file_path)

    # 5. Test files.from_json
    def test_from_json_valid_json(self) -> None:
        """
        GIVEN a path to an existing and valid json file \n
        WHEN the method is executed \n
        THEN the json file content is correctly extracted \n
        AND the json file content is correctly parsed to a Python dict \n
        """
        imported_json: dict = files.from_json(self.json_file_path)
        json_file_content: dict = loads(self.json_file_content)

        self.assertIsNotNone(
            imported_json,
            test_messages.METHOD_RETURNS_NONE.format(method=self.from_json_method)
        )
        self.assertIsInstance(
            imported_json,
            dict,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(
                method=self.from_json_method,
                value='dict'
            )
        )
        self.assertEqual(
            imported_json,
            json_file_content,
            test_messages.IS_NOT_EQUAL.format(
                first=f'Returned json content ({imported_json})',
                second=json_file_content
            )
        )

    def test_from_json_not_valid_json(self) -> None:
        """
        GIVEN a path to an exiting but not valid json file \n
        WHEN the method is executed \n
        THEN it raises a JSONDecodeError exception \n
        """
        self.assertRaises(JSONDecodeError, files.from_json, self.plain_text_file_path)

    def test_from_json_not_valid_file(self) -> None:
        """
        GIVEN a path to a not exiting file \n
        WHEN the method is executed \n
        THEN it raises a FileNotFoundError exception \n
        """
        not_valid_file_path = 'this file does not exist'

        self.assertRaises(FileNotFoundError, files.from_json, not_valid_file_path)

    # 6. Test files.to_json
    def test_to_json(self) -> None:
        """
        GIVEN a path to a file \n
        AND a valid Python dict \n
        WHEN the method is executed using the path and
        the dict as a params \n
        THEN a file is created \n
        AND it contains the Python dict \n
        """
        data: dict = {
            "employee": {
                "name": "John",
                "age": 30,
                "city": "New York"
            }
        }
        file_path: str = os.path.join(self.test_files_folder, 'to_json_data.json')

        files.to_json(data, file_path)

        exist: bool = os.path.exists(file_path)
        self.assertTrue(exist)

        with open(file_path, mode='r', encoding='utf-8') as f:
            json_file_data: dict = load(f)

        self.assertEqual(
            json_file_data,
            data,
            test_messages.IS_NOT_EQUAL.format(
                first=f'Stored file content ({json_file_data})',
                second=data
            )
        )

    # 7. Test files.exist
    def test_exist_true(self) -> None:
        """
        GIVEN a path to an existing file \n
        WHEN the method is executed \n
        THEN it returns True \n
        """
        file_path: str = os.path.join(self.test_files_folder, 'exist_file.txt')

        with open(file_path, mode='w', encoding='utf-8') as f:
            f.write('This file exists!')

        exist: bool = files.exist(file_path)

        self.assertIsNotNone(
            exist,
            test_messages.METHOD_RETURNS_NONE.format(method=self.exist_method)
        )
        self.assertIsInstance(
            exist,
            bool,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(
                method=self.exist_method,
                value='bool'
            )
        )
        self.assertTrue(
            exist,
            'The file exists and it returns False'
        )

    def test_exist_false(self) -> None:
        """
        GIVEN a path to a not existing file \n
        WHEN the method is executed \n
        THEN it returns False \n
        """
        file_path: str = os.path.join(self.test_files_folder, 'this_file_does_not_exist.txt')

        exist: bool = files.exist(file_path)

        self.assertIsNotNone(
            exist,
            test_messages.METHOD_RETURNS_NONE.format(method=self.exist_method)
        )
        self.assertIsInstance(
            exist,
            bool,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(
                method=self.exist_method,
                value='bool'
            )
        )
        self.assertFalse(
            exist,
            'The file does not exist and it returns True'
        )

    def test_exist_null_param(self) -> None:
        """
        GIVEN a param that contains None value \n
        WHEN the method is executed \n
        THEN it returns False \n
        """
        exist: bool = files.exist('')

        self.assertIsNotNone(
            exist,
            test_messages.METHOD_RETURNS_NONE.format(method=self.exist_method)
        )
        self.assertIsInstance(
            exist,
            bool,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(
                method=self.exist_method,
                value='bool'
            )
        )
        self.assertFalse(
            exist,
            'The file does not exist and it returns True'
        )

    # 8. Test files.drop_file
    def test_drop_file_exist(self) -> None:
        """
        GIVEN a path to an existing file \n
        WHEN the method is executed \n
        THEN the file is removed \n
        """
        file_path: str = os.path.join(self.test_files_folder, 'drop_file.txt')

        with open(file_path, mode='w', encoding='utf-8') as f:
            f.write('This file exists!')

        files.drop_file(file_path)

        exist = os.path.exists(file_path)

        self.assertFalse(
            exist,
            'The file has not been removed'
        )

    def test_drop_file_not_exist(self) -> None:
        """
        GIVEN a path to a not existing file \n
        WHEN the method is executed \n
        THEN the file is not removed \n
        AND there are no exceptions \n
        """
        file_path: str = os.path.join(self.test_files_folder, 'drop_file_this_file_does_not_exist.txt')
        expected_output: str = f"File path: '{file_path}' does not exist, so it could not be deleted."

        files.drop_file(file_path)

        exist = os.path.exists(file_path)

        self.assertFalse(
            exist,
            expected_output
        )

    # 9. Test files.base64_
    def test_base64_(self) -> None:
        with open(self.plain_text_file_path, mode='w', encoding='utf-8') as f:
            f.write('This is a test file')

        file_content_base64 = 'VGhpcyBpcyBhIHRlc3QgZmlsZQ=='

        self.assertIsNotNone(
            files.base64_(self.plain_text_file_path),
            test_messages.METHOD_RETURNS_NONE.format(method=self.base64_method)
        )

        self.assertIsInstance(
            files.base64_(self.plain_text_file_path),
            str,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(method=self.base64_method, value='str')
        )

        self.assertEqual(
            files.base64_(self.plain_text_file_path),
            file_content_base64,
            test_messages.IS_NOT_EQUAL.format(first=files.base64_(self.plain_text_file_path),
                                              second=file_content_base64)
        )

    # 10. Test files.copy_file
    def test_copy_file(self) -> None:
        source_file_path: str = os.path.join(self.test_files_folder, 'source_test_file.txt')
        with open(source_file_path, mode='w', encoding='utf-8') as f:
            f.write('This is a test file')
        target_file_path: str = os.path.join(self.test_files_folder, 'target_test_file.txt')
        with open(source_file_path, mode='w', encoding='utf-8') as f:
            f.write('')

        self.assertRaises(Exception,files.copy_file, 'not_valid_param', 'not_valid_param')

        self.assertIsNone(
            files.copy_file(source_file_path, target_file_path)
        )

        files.copy_file(source_file_path, target_file_path)
        self.assertEqual(
            files.get_file_content(source_file_path),
            files.get_file_content(target_file_path),
            test_messages.IS_NOT_EQUAL.format(first=files.get_file_content(source_file_path),
                                              second=files.get_file_content(target_file_path))
        )

        files.copy_file(source_file_path, target_file_path)
        with open(source_file_path, mode='w', encoding='utf-8') as f:
            f.write('Now the file content is different')
        self.assertNotEqual(
            files.get_file_content(source_file_path),
            files.get_file_content(target_file_path),
            test_messages.IS_EQUAL.format(first=files.get_file_content(source_file_path),
                                          second=files.get_file_content(target_file_path))
        )

    # 11. Test files.count_occurrences_in_file
    def test_count_occurrences_in_file(self) -> None:
        with open(self.plain_text_file_path, mode='w', encoding='utf-8') as f:
            f.write('There are 5 occurrences of the word are are are are')

        self.assertIsNotNone(
            files.count_occurrences_in_file('are', self.plain_text_file_path),
            test_messages.METHOD_RETURNS_NONE.format(method=self.count_occurrences_in_file_method)
        )

        self.assertIsInstance(
            files.count_occurrences_in_file('are', self.plain_text_file_path),
            int,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(method=self.count_occurrences_in_file_method, value='int')
        )

        self.assertEqual(
            files.count_occurrences_in_file('are', self.plain_text_file_path),
            5,
            test_messages.IS_NOT_EQUAL.format(first=files.count_occurrences_in_file('are', self.plain_text_file_path),
                                              second=5)
        )

    # 12. Test files.delete_line_number
    def test_delete_line_number(self) -> None:
        file_path: str = os.path.join(self.test_files_folder, 'test_file.txt')
        with open(file_path, mode='w', encoding='utf-8') as f:
            f.write('First line\nSecond line\nThird line')

        self.assertIsNone(
            files.delete_line_number(file_path, 0),
            test_messages.METHOD_RETURNS_NONE.format(method=self.delete_line_number_method)
        )

        # Rewrite the text in the file as it is modified when calling 'delete_line_number()'
        with open(file_path, mode='w', encoding='utf-8') as f:
            f.write('First line\nSecond line\nThird line')

        # Test that the method deletes the first line correctly
        with open(file_path, "r") as f:
            original_lines = f.readlines()
        files.delete_line_number(file_path, 0)
        with open(file_path, "r") as f:
            new_lines = f.readlines()

        self.assertEqual(
            new_lines,
            original_lines[1:],
            test_messages.IS_NOT_EQUAL.format(first=str(new_lines),
                                              second=str(original_lines[1:]))
        )

        # Test that the method deletes the second line correctly
        with open(file_path, mode='w', encoding='utf-8') as f:
            f.write('First line\nSecond line\nThird line')

        with open(file_path, "r") as f:
            original_lines = f.readlines()
        files.delete_line_number(file_path, 1)
        with open(file_path, "r") as f:
            new_lines = f.readlines()

        self.assertEqual(
            new_lines,
            [original_lines[0], original_lines[2]],
            test_messages.IS_NOT_EQUAL.format(first=str(new_lines),
                                              second=str([original_lines[0], original_lines[2]]))
        )

        # Test that the method deletes the last line correctly
        with open(file_path, mode='w', encoding='utf-8') as f:
            f.write('First line\nSecond line\nThird line')

        with open(file_path, "r") as f:
            original_lines = f.readlines()
        files.delete_line_number(file_path, 2)
        with open(file_path, "r") as f:
            new_lines = f.readlines()

        self.assertEqual(
            new_lines,
            original_lines[:2],
            test_messages.IS_NOT_EQUAL.format(first=str(new_lines),
                                              second=str(original_lines[:2]))
        )

    # 12. Test files.to_file
    def test_to_file(self) -> None:
        text: str = 'This text is to be copied into a file'
        file_path: str = os.path.join(self.test_files_folder, 'test_file.txt')
        with open(file_path, mode='w', encoding='utf-8') as f:
            f.write('Dummy text that will be overwritten')

        self.assertIsNone(
            files.to_file(text, file_path),
            test_messages.METHOD_RETURNS_NONE.format(method=self.to_file_method)
        )

        recovered_text: str = files.get_file_content(file_path)
        self.assertEqual(
            recovered_text,
            text,
            test_messages.IS_NOT_EQUAL.format(first=recovered_text,
                                              second=text)
        )

    # 12. Test files.delete
    def test_delete(self) -> None:
        with open(self.plain_text_file_path, mode='w', encoding='utf-8') as f:
            f.write('There are 5 ocurrences of the word are are are are')

        self.assertIsNone(
            files.delete('are', self.plain_text_file_path),
            test_messages.METHOD_RETURNS_NONE.format(method=self.delete_method)
        )

        deleted_text = 'There  5 ocurrences of the word    '
        self.assertEqual(
            files.get_file_content(self.plain_text_file_path),
            deleted_text,  # Observe that the remaining text is not padded
            test_messages.IS_NOT_EQUAL.format(first=files.get_file_content(self.plain_text_file_path),
                                              second=deleted_text)
        )

    # 13. Test files.get_file_name_from_path
    def test_get_file_name_from_path(self) -> None:
        self.assertIsNotNone(
            files.get_file_name_from_path(self.plain_text_file_path),
            test_messages.METHOD_RETURNS_NONE.format(method=self.get_file_name_from_path_method)
        )

        self.assertIsInstance(
            files.get_file_name_from_path(self.plain_text_file_path),
            str,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(method=self.get_file_name_from_path_method, value='str')
        )

        self.assertEqual(
            files.get_file_name_from_path(self.plain_text_file_path),
            'plain_text_file.txt',
            test_messages.IS_NOT_EQUAL.format(first=files.get_file_name_from_path(self.plain_text_file_path),
                                              second='plain_text_file.txt')
        )

    # 14. Test files.file_split_name_ext
    def test_file_split_name_ext(self) -> None:
        self.assertIsNotNone(
            files.file_split_name_ext(self.plain_text_file_path),
            test_messages.METHOD_RETURNS_NONE.format(method=self.file_split_name_ext_method)
        )

        self.assertIsInstance(
            files.file_split_name_ext(self.plain_text_file_path),
            tuple,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(method=self.file_split_name_ext_method,
                                                              value='(str, str)')
        )
        self.assertIsInstance(
            files.file_split_name_ext(self.plain_text_file_path)[0],
            str,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(method=self.file_split_name_ext_method, value='str')
        )

        self.assertIsInstance(
            files.file_split_name_ext(self.plain_text_file_path)[1],
            str,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(method=self.file_split_name_ext_method, value='str')
        )

        self.assertEqual(
            files.file_split_name_ext(self.plain_text_file_path),
            (self.plain_text_file_path[:-4], '.txt'),
            test_messages.IS_NOT_EQUAL.format(first=files.file_split_name_ext(self.plain_text_file_path),
                                              second=('.\\resources\\plain_text_file', 'txt'))
        )

    # 15. Test files.get_file_extension
    def test_get_file_extension(self) -> None:
        self.assertIsNotNone(
            files.get_file_extension(self.plain_text_file_path),
            test_messages.METHOD_RETURNS_NONE.format(method=self.get_file_extension_method)
        )

        self.assertIsInstance(
            files.get_file_extension(self.plain_text_file_path),
            str,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(method=self.get_file_extension_method, value='str')
        )

        self.assertEqual(
            files.get_file_extension(self.plain_text_file_path),
            '.txt',
            test_messages.IS_NOT_EQUAL.format(first=files.get_file_extension(self.plain_text_file_path),
                                              second='plain_text_file.txt')
        )

    # 16. Test files.get_file_extension
    def test_remove_extension_from_file_path(self) -> None:
        self.assertIsNotNone(
            files.remove_extension_from_file_path(self.plain_text_file_path),
            test_messages.METHOD_RETURNS_NONE.format(method=self.remove_extension_from_file_path_method)
        )

        self.assertIsInstance(
            files.remove_extension_from_file_path(self.plain_text_file_path),
            str,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(method=self.remove_extension_from_file_path_method,
                                                              value='str')
        )

        self.assertEqual(
            files.remove_extension_from_file_path(self.plain_text_file_path),
            self.plain_text_file_path[:-4],
            test_messages.IS_NOT_EQUAL.format(first=self.plain_text_file_path[:-4],
                                              second=files.remove_extension_from_file_path(self.plain_text_file_path))
        )

    # 17. Test files.get_file_extension
    def test_get_file_name(self) -> None:
        self.assertIsNotNone(
            files.get_file_name(self.plain_text_file_path),
            test_messages.METHOD_RETURNS_NONE.format(method=self.get_file_name_method)
        )

        self.assertIsInstance(
            files.get_file_name(self.plain_text_file_path),
            str,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(method=self.get_file_name_method, value='str')
        )

        self.assertEqual(
            files.get_file_name(self.plain_text_file_path),
            'plain_text_file.txt',
            test_messages.IS_NOT_EQUAL.format(first=files.get_file_name(self.plain_text_file_path),
                                              second='plain_text_file.txt')
        )

    # 18. Test files.get_file_extension
    def test_get_file_root_path(self) -> None:
        self.assertIsNotNone(
            files.get_file_root_path(self.plain_text_file_path),
            test_messages.METHOD_RETURNS_NONE.format(method=self.get_file_root_path_method)
        )

        self.assertIsInstance(
            files.get_file_root_path(self.plain_text_file_path),
            str,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(method=self.get_file_root_path_method, value='str')
        )

        self.assertEqual(
            files.get_file_root_path(self.plain_text_file_path),
            self.plain_text_file_path[:-20],
            test_messages.IS_NOT_EQUAL.format(first=files.get_file_root_path(self.plain_text_file_path),
                                              second=self.plain_text_file_path[:-20])
        )

    # 19. Test files.drop_dir
    def test_drop_dir(self) -> None:
        os.makedirs(self.delete_folder, exist_ok=True)

        # Check the directory exists
        self.assertTrue(
            os.path.isdir(self.delete_folder),
        )

        # Execute the method, checking there ir no return value
        self.assertIsNone(
            files.drop_dir(self.delete_folder),
            test_messages.METHOD_RETURNS_NONE.format(method=self.drop_dir_method)
        )

        # Check the directory does not exist anymore
        self.assertFalse(
            os.path.isdir(self.delete_folder),
        )

    # 20. Test files.from_yaml
    def test_from_yaml(self) -> None:
        yaml_file_path: str = os.path.join(self.resources_path, 'yaml_example_file.yaml')
        yaml_dict: dict = {'doe': 'a deer, a female deer',
                           'ray': 'a drop of golden sun',
                           'pi': 3.14159,
                           'xmas': True,
                           'french-hens': 3,
                           'calling-birds': ['huey', 'dewey', 'louie', 'fred']
                           }

        self.assertIsNotNone(
            files.from_yaml(yaml_file_path),
            test_messages.METHOD_RETURNS_NONE.format(method=self.from_yaml_method)
        )

        self.assertIsInstance(
            files.from_yaml(yaml_file_path),
            dict,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(method=self.from_yaml_method, value='dict')
        )

        self.assertEqual(
            files.from_yaml(yaml_file_path),
            yaml_dict,
            test_messages.IS_NOT_EQUAL.format(first=files.from_yaml(yaml_file_path),
                                              second=yaml_file_path[:-20])
        )

    # 21. Test files.path_exists
    def test_path_exists(self) -> None:
        existing_path: str = self.plain_text_file_path
        non_existing_path: str = os.path.abspath('non_existing_file.txt')

        self.assertIsNotNone(
            files.path_exists(existing_path),
            test_messages.METHOD_RETURNS_NONE.format(method=self.path_exists_method)
        )

        self.assertIsNotNone(
            files.path_exists(non_existing_path),
            test_messages.METHOD_RETURNS_NONE.format(method=self.path_exists_method)
        )

        self.assertIsInstance(
            files.path_exists(existing_path),
            bool,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(method=self.path_exists_method, value='bool')
        )

        self.assertIsInstance(
            files.path_exists(non_existing_path),
            bool,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(method=self.path_exists_method, value='bool')
        )

        self.assertEqual(
            files.path_exists(existing_path),
            True,
            test_messages.IS_NOT_EQUAL.format(first=files.path_exists(existing_path),
                                              second=True)
        )

        self.assertEqual(
            files.path_exists(non_existing_path),
            False,
            test_messages.IS_NOT_EQUAL.format(first=files.path_exists(non_existing_path),
                                              second=True)
        )

    # 22. Test files.grep
    def test_grep(self) -> None:
        with open(self.plain_text_file_path, mode='w', encoding='utf-8') as f:
            f.write('Here there is the word text\nIn this one not\nNeither in this one\nIn the last one there is text')

        self.assertIsNotNone(
            files.grep(self.plain_text_file_path, 'text'),
            test_messages.METHOD_RETURNS_NONE.format(method=self.grep_method)
        )

        self.assertIsNotNone(
            files.grep(self.plain_text_file_path, 'text', False),
            test_messages.METHOD_RETURNS_NONE.format(method=self.grep_method)
        )

        self.assertIsInstance(
            files.grep(self.plain_text_file_path, 'text'),
            Iterator,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(method=self.grep_method, value='list')
        )

        self.assertEqual(
            list(files.grep(self.plain_text_file_path, 'text')),
            ['Here there is the word text\n', 'In the last one there is text'],
            test_messages.IS_NOT_EQUAL.format(first=list(files.grep(self.plain_text_file_path, 'text')),
                                              second=['Here there is the word text\n', 'In the last one there is text'])
        )

    # 23. Test files.head
    def test_head(self) -> None:
        with open(self.plain_text_file_path, mode='w', encoding='utf-8') as f:
            f.write('Here there is the word text\nIn this one not\nNeither in this one\nIn the last one there is text')

        self.assertIsNotNone(
            files.head(self.plain_text_file_path, 2),
            test_messages.METHOD_RETURNS_NONE.format(method=self.head_method)
        )

        self.assertIsNotNone(
            files.head(self.plain_text_file_path, 2, 'utf-8', False),
            test_messages.METHOD_RETURNS_NONE.format(method=self.head_method)
        )

        self.assertIsInstance(
            files.head(self.plain_text_file_path, 2),
            Iterator,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(method=self.head_method, value='str')
        )

        self.assertEqual(
            list(files.head(self.plain_text_file_path, 2)),
            ['Here there is the word text\n', 'In this one not\n'],
            test_messages.IS_NOT_EQUAL.format(first=files.head(self.plain_text_file_path, 2),
                                              second=['Here there is the word text\n', 'In this one not\n'])
        )

    # 24. Test files.tail
    def test_tail(self) -> None:
        with open(self.plain_text_file_path, mode='w', encoding='utf-8') as f:
            f.write('Here there is the word text\nIn this one not\nNeither in this one\nIn the last one there is text')

        self.assertIsNotNone(
            files.tail(self.plain_text_file_path, 2),
            test_messages.METHOD_RETURNS_NONE.format(method=self.tail_method)
        )

        self.assertIsNotNone(
            files.tail(self.plain_text_file_path, 2, 'utf-8', False),
            test_messages.METHOD_RETURNS_NONE.format(method=self.tail_method)
        )

        self.assertIsInstance(
            files.tail(self.plain_text_file_path, 2),
            Iterator,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(method=self.tail_method, value='str')
        )

        result = list(files.tail(self.plain_text_file_path, 2))
        result[0] = result[0].strip()
        result[1] = result[1].strip()

        self.assertEqual(
            result,
            ['Neither in this one', 'In the last one there is text'],
            test_messages.IS_NOT_EQUAL.format(first=result,
                                              second=['Neither in this one', 'In the last one there is text'])
        )

    # 25. Test files.import_library
    def test_import_library(self) -> None:
        library = 'csv'
        files.import_library(library)
        is_imported: bool = library in sys.modules

        self.assertTrue(
            is_imported
        )

    # 26. Test files.remove_file_protocol
    def test_remove_file_protocol(self) -> None:
        url: str = 'file:///home/paula/.bashrc'
        file_1 = 'file://test'
        file_2 = 'file:test'

        self.assertIsNotNone(
            files.remove_file_protocol(url),
            test_messages.METHOD_RETURNS_NONE.format(method=self.remove_file_protocol_method)
        )

        self.assertIsNotNone(
            files.remove_file_protocol(file_1),
            test_messages.METHOD_RETURNS_NONE.format(method=self.remove_file_protocol_method)
        )

        self.assertIsNotNone(
            files.remove_file_protocol(file_2),
            test_messages.METHOD_RETURNS_NONE.format(method=self.remove_file_protocol_method)
        )
        self.assertIsInstance(
            files.remove_file_protocol(url),
            str,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(method=self.remove_file_protocol_method, value='str')
        )

        self.assertEqual(
            files.remove_file_protocol(url),
            '/home/paula/.bashrc',
            test_messages.IS_NOT_EQUAL.format(first=files.remove_file_protocol(url),
                                              second='/home/paula/.bashrc')
        )

    # 27. Test files.to_file_line
    def test_to_file_line(self) -> None:
        with open(self.plain_text_file_path, mode='w', encoding='utf-8') as f:
            f.write(
                'Here there is the word text\nIn this one not\nNeither in this one\nIn the last one there is text\n')

        text = 'Line to add \n'
        self.assertIsNone(
            files.to_file_line(text, self.plain_text_file_path, 3),
            test_messages.METHOD_RETURNS_NONE.format(method=self.to_file_method)
        )
        result_text: str = 'Here there is the word text\nIn this one not\nNeither in this one\nLine to add\nIn the ' \
                           'last one there is text\n '

        result = files.get_file_content(self.plain_text_file_path)
        result = re.sub('\W+', '', result)
        result_text = re.sub('\W+', '', result_text)

        self.assertEqual(
            result,
            result_text,
            test_messages.IS_NOT_EQUAL.format(first=result,
                                              second=result_text)
        )

        self.assertRaises(IndexError, files.to_file_line, text, self.plain_text_file_path, -5)

    # 28. Test files.xst_file
    def test_xst_file(self) -> None:
        file_path: str = self.plain_text_file_path
        dir_path: str = self.test_files_folder

        self.assertTrue(
            files.xst_file(file_path)
        )

        self.assertTrue(
            files.xst_file(dir_path)
        )

    # 29. Test files.extract_files_from_zip_folder
    def test_extract_files_from_zip_folder(self) -> None:
        shutil.make_archive(os.path.join(self.resources_path, 'zip_folder'), 'zip', self.folder_to_zip)
        extracted_files_paths = files.extract_files_from_zip_folder(self.zip_folder, self.folder_to_zip_backup)

        self.assertIsNotNone(
            extracted_files_paths,
            test_messages.METHOD_RETURNS_NONE.format(method=self.extract_files_from_zip_folder_method)
        )

        self.assertIsInstance(
            extracted_files_paths,
            list,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(method=self.extract_files_from_zip_folder_method,
                                                              value='list')
        )

        files_set = set()
        files_set.add(files.get_file_content(extracted_files_paths[0]))
        files_set.add(files.get_file_content(extracted_files_paths[1]))

        self.assertEqual(
            files_set,
            {'zip_folder_file_1 content', 'zip_folder_file_2 content'},
            test_messages.IS_NOT_EQUAL.format(first=files_set,
                                              second={'zip_folder_file_1 content', 'zip_folder_file_2 content'})
        )

        files.drop_file(extracted_files_paths[0])
        files.drop_file(extracted_files_paths[1])
        files.drop_dir(self.folder_to_zip_backup)

    # 30. Test files.get_file_name_length
    def test_get_file_name_length(self) -> None:
        file_name: str = os.path.join(self.resources_path, 'test.txt')

        self.assertIsNotNone(
            files.get_file_name_length(file_name),
            test_messages.METHOD_RETURNS_NONE.format(method=self.get_file_name_length_method)
        )

        self.assertIsInstance(
            files.get_file_name_length(file_name),
            int,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(method=self.get_file_name_length_method, value='int')
        )

        self.assertEqual(
            files.get_file_name_length(file_name),
            4,
            test_messages.IS_NOT_EQUAL.format(first=files.get_file_name_length(file_name),
                                              second=4)
        )

    # 31. Test files.get_file_size
    def test_get_file_size(self) -> None:
        self.assertIsNotNone(
            files.get_file_size(self.plain_text_file_path),
            test_messages.METHOD_RETURNS_NONE.format(method=self.get_file_size_method)
        )

        self.assertIsInstance(
            files.get_file_size(self.plain_text_file_path),
            int,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(method=self.get_file_size_method, value='int')
        )

        with open(self.plain_text_file_path, mode='w', encoding='utf-8') as f:
            f.write('The content is 33 characters long')

        self.assertEqual(
            files.get_file_size(self.plain_text_file_path),
            33,
            test_messages.IS_NOT_EQUAL.format(first=files.get_file_size(self.plain_text_file_path),
                                              second=33)
        )
