"""
Methods related with files and directories management
"""

import base64
import json
import ntpath
import os
import pathlib
import shutil
import typing
from itertools import islice
from shutil import rmtree
from zipfile import ZipFile
from collections.abc import Iterator

import yaml
from file_read_backwards import FileReadBackwards
from pkg_resources import Distribution, WorkingSet, DistributionNotFound

from .data_types.uri import URL


def base64_(file_path: str) -> str:
    """
    Returns the content of a file as a Base64 string.

    :param file_path: path to the file

    :return: content of the file encoded as Base64 string
    """
    with open(file_path, "rb") as file_path:
        binary = base64.b64encode(file_path.read()).decode()
    return binary


def copy_file(source_file_path: str, target_file_path: str) -> None:
    """
    Copies source file to target file.

    :param source_file_path: file to be copied
    :param target_file_path: file that will be created containing the source file content
    """
    shutil.copy(source_file_path, target_file_path)


def count_occurrences_in_file(txt: str, file_path: str, case_sensitive: bool = True) -> int:
    """
    Returns the number of times that the text occurs in the file.

    :param txt: text to find in the file content
    :param file_path: path to the file
    :param case_sensitive: whether the search is case-sensitive.
        By default, it is set to True

    :return: the number of times that the text occurs in the file
    """
    content = get_file_content(file_path)
    content = content.lower() if not case_sensitive else content
    txt = txt.lower() if not case_sensitive else txt
    return content.count(txt)


def delete_line_number(file_path: str, line: int) -> None:
    """
    Removes a line from a file.

    :param file_path: file to edit
    :param line: number of the line to be removed
    """
    with open(file_path, "r+") as f:
        d = f.readlines()
        f.seek(0)
        for i in range(len(d)):
            if i != line:
                f.write(d[i])
        f.truncate()


def to_file(txt: str, path: str) -> None:
    """
    Writes a text into a file.

    :param txt: text to be written in the file
    :param path: path where the file will be created
    """
    with open(path, 'w+', encoding="utf-8") as file:
        if txt:
            file.write(txt)


def delete(txt: str, file_path: str) -> None:
    """
    Removes all occurrences of a text from inside a file.

    :param txt: text to be removed in the file
    :param file_path: path to the file
    """
    content = get_file_content(file_path)
    content = content.replace(txt, '')
    to_file(content, file_path)


def get_file_name_from_path(path: str) -> str:
    """
    Given a full file path name, returns just the filename.

    :param path: full file path name

    :return: filename extracted from the path
    """
    _head, _tail = ntpath.split(path)
    return _tail or ntpath.basename(_head)


def file_split_name_ext(file_name: str) -> (str, str):
    """
    Given a complete file path name, it separates the name from the extension.

    :param file_name: complete file path name

    :return: filename, extension
    """
    v = os.path.splitext(file_name)
    return v[0], v[1]


def get_file(path_filename: str) -> (str, str):
    """
    Given the full file path name, it returns the name and the extension of the file.

    :param path_filename: full file path name

    :return: name, extension
    """
    name, ext = file_split_name_ext(get_file_name_from_path(path_filename))
    ext = ext.replace('.', '')
    return name, ext


def get_file_content(path: str, encoding: str = 'utf-8', bytes_number: int = 0) -> typing.Union[str, None]:
    """
    Returns the content of a file as a string.

    :param path: the path filename;
    :param encoding: the encoding of the content if known, otherwise defaults to 'utf-8';
    :param bytes_number: the number of bytes to read; if '0' the entire file is read;

    :return: the file content as a string.
    """
    if not path_exists(path):
        raise FileNotFoundError

    file_size = pathlib.Path(path).stat().st_size
    offset = bytes_number if bytes_number != 0 and bytes_number < file_size else file_size

    try:
        with open(path, 'rb') as fin:
            return fin.read(offset).decode(encoding)
    except Exception:
        raise Exception


def get_file_extension(file_path: str) -> str:
    """
    Returns the file extension from a path.

    Example:
    get_file_extension("/home/test.txt") -> txt

    :param file_path: absolute or relative path of the file

    :return: string with the extension of the file
    """
    filename, file_extension = os.path.splitext(file_path)
    return file_extension


def remove_extension_from_file_path(file_path: str) -> str:
    """
    Given the complete file path, remove the file extension.

    :param file_path: path where the file is

    :return: the entire file path without extension of the file
    """
    resource_path, file_extension = os.path.splitext(file_path)
    return resource_path


def get_extension_from_file_name(file_path: str) -> tuple[str, str]:
    """
    Given the complete file path, remove the entire file path and preserve the extension.

    :param file_path: path where the file is

    :return: the name and extension of the file
    """
    name, extension = os.path.splitext(file_path)
    return name, extension[1:]


def get_directory_and_file_name_and_extension_from_path(path: str) -> tuple[str, str, str]:
    """
    Given the complete file path, remove the entire file path and preserve the file name.

    :param path: path where the file is

    :return: directory of the file, file name and extension.
    """
    head, tail = ntpath.split(path)
    file_name, extension = get_extension_from_file_name(tail)
    return head, file_name, extension


def get_file_name(file_path: str) -> str:
    """
    Extract the file name and extension from a path.

    Example:
    get_file_name("/home/test.txt") -> test.txt

    :param file_path: absolute or relative path of the file

    :return: file 'name.extension'
    """
    return os.path.basename(file_path)


def get_file_root_path(file_path: str) -> str:
    """
    Given the complete file path, remove the file name from the path.

    :param file_path: path where the file is

    :return: path to the directory in which a file is located without the file name
    """
    folder_path, resource = ntpath.split(file_path)

    return folder_path


def to_json(dict_data: dict, path: str) -> None:
    """
    Save a dictionary to a JSON file.

    :param dict_data: dictionary to save to json file
    :param path: absolute or relative path where the json will be saved
    """
    with open(path, "w") as json_file:
        json.dump(dict_data, json_file, indent=4)


def exist(file_path: str) -> bool:
    """
    Check if the file exists.

    :param file_path: absolute or relative path of the file

    :return: boolean indicating if the file exists.
    """
    if file_path:
        return os.path.exists(file_path)
    else:
        return False


def drop_dir(dir_path: str) -> None:
    """
    Recursively removes a directory tree from the file system.

    :param dir_path: path to the directory
    """
    if os.path.isdir(dir_path):
        shutil.rmtree(dir_path)


def drop_file(file_path: str) -> None:
    """
    Removes a file from the file system.

    :param file_path: absolute or relative path of the file
    """
    if os.path.isfile(file_path):
        os.remove(file_path)


def from_json(file_path: str) -> dict:
    """
    Returns the Python dictionary out of a JSON file.

    :param file_path: absolute or relative path of the json file to load

    :return: file content as a Python dict
    """
    with open(file_path, 'r', encoding="utf-8") as fp:
        return json.load(fp)


def from_yaml(file_path: str) -> dict:
    """
    Returns the Python dictionary out of a YAML file.

    :param file_path: absolute or relative path of the YAML file to load

    :return: file content as a Python dict
    """
    with open(file_path, 'r', encoding="utf-8") as f:
        content_dict = yaml.safe_load(f)
    return content_dict


def path_exists(path: str) -> bool:
    """
    Checks whether a file or directory exists or not.

    :param path: the path to the dir or file

    :return: the result of the checking
    """
    return os.path.isdir(path) or os.path.isfile(path)

def grep(file: str, text: str, case_sensitive: bool = True) -> Iterator[str]:
    """
    Extracts the lines of a file where a text occurs.

    :param file: the file containing the text to grep;
    :param text: the string to find in the file content;
    :param case_sensitive: if False, the comparison is insensitive to the letter casing.

    :return: extracted lines listed as strings
    """
    f = open(file, 'r')
    for line in f:
        if not case_sensitive and text.lower() in line.lower():
            yield line
        elif text in line:
            yield line
    f.close()


def head(file_path: str, lines: int, encoding: str = 'utf-8', forwards: bool = True) -> Iterator[str]:
    """
    Returns the first n lines of a text file. If the number of lines is negative or the forwards flag
    is set to False, the lines are reversed.

    :param file_path: path to the file containing the text
    :param lines: number of lines to be returned
    :param encoding: the encoding of the content if known, otherwise defaults to 'utf-8'
    :param forwards: whether the lines should be reversed. By default, it is set to True

    :return: the extracted lines from the file content
    """
    forwards = forwards if forwards and lines > 0 else False
    lines = abs(lines)
    with open(file_path, encoding=encoding) as f:
        v = list(islice(f, lines))
    if not forwards:
        v.reverse()
    for line in v:
        yield line


def tail(file_path: str, lines: int = 10, encoding: str = 'utf-8', forwards: bool = True) -> Iterator[str]:
    """
    Returns the last n lines of a text file. If the number of lines is negative or the forwards flag
    is set to False, the lines are reversed.

    :param file_path: path to the file containing the text
    :param lines: number of lines to be returned
    :param encoding: the encoding of the content if known, otherwise defaults to 'utf-8'
    :param forwards: whether the lines should be reversed. By default, it is set to True

    :return: the extracted lines from the file content
    """
    v = []
    forwards = True if forwards is True and lines > 0 else False
    lines = abs(lines)
    with FileReadBackwards(file_path, encoding=encoding) as frb:
        while True:
            line = frb.readline()
            v.append(line)
            if not line or len(v) == lines:
                break
    if forwards:
        v.reverse()

    for line in v:
        yield line.rstrip('\n')


def import_library(package: str) -> typing.Union[Distribution, None]:
    """
    Imports a library dynamically if installed.

    Use Case: control the installation of different libraries based on the Operating System, the version of the
    library, the dynamical installation of one library or another (e.g., install NLTK or spaCy?), etc.

    See the DGI/SEMBU 'FilePersistor.select()' method for a Use Case where the content of the file is returned as a
    spaCy Doc if spaCy is installed or as a string if not installed.

    CAUTION: Make sure the library iadn is installed.

    :param package: package to be installed

    :return: the import statement as a Distribution object
    """
    working_set = WorkingSet()
    # Detecting if the module is installed
    try:
        dist = [library for library in working_set.require(package)]
        dist = dist[0] if dist and len(dist) > 0 else None
        dist = __import__(dist.key) if dist else None
        return dist
    except DistributionNotFound:
        return None


def make_dirs(file_path: str) -> None:
    """
    Given the complete path to a file, creates the directories preceding the name of the file.

    :param file_path: a relative or absolute path or path file name
    """
    dir_, file_ = ntpath.split(file_path)
    os.makedirs(dir_, exist_ok=True)


def remove_file_protocol(url: typing.Union[str, URL, None]) -> str:
    """
    Removes file: and file:// from a url string, like in 'file:../test/files/eDeclaration.xsd' or
    'file:///home/paula/.bashrc'.

    :param url: url to be modified

    :return: url without 'file://' protocol
    """
    '''
    Early return
    '''
    protocol: str = 'file://'
    protocol_no_slash: str = protocol[:-2]

    if url and type(url) is URL:
        url = url.uri_str

    if not url:
        return url

    if protocol in url[: len(protocol)]:
        return url[len(protocol):]
    elif protocol_no_slash in url[: len(protocol)]:
        return url[len(protocol_no_slash):]
    return url


def to_file_line(txt: str, file_path: str, index: int) -> None:
    """
    Inserts a line in a file containing multiple lines.

    :param txt: text to add in the file
    :param file_path: path to the file
    :param index: number of the line where the text will be inserted
    """
    with open(file_path, "r") as f:
        contents = f.readlines()

    if index < 0 or index > len(contents):
        raise IndexError

    contents.insert(index, txt)

    with open(file_path, "w") as f:
        contents = "".join(contents)
        f.write(contents)


def xst_file(path: str) -> bool:
    """
    Checks whether a file or directory exists or not.

    :param path: the path to the dir or file

    :return: the result of the checking
    """
    return os.path.isdir(path) or os.path.isfile(path)


def extract_files_from_zip_folder(save_file_path: str, temporal_folder: str) -> list[str]:
    """
    Given the complete zip file path, unzip the documents zipped.

    :param save_file_path: path where the zip file is
    :param temporal_folder: path where the zip object will be
        temporally extracted

    :return: list with the path to each unzipped file
    """
    folder_path = get_file_root_path(save_file_path)
    extraction_path = temporal_folder
    make_dirs(extraction_path)
    path_list = []
    with ZipFile(save_file_path, 'r') as zip_object:
        zip_object.extractall(extraction_path)
        zip_files = zip_object.namelist()
        for file in zip_files:
            file_name = get_file_name_from_path(file)
            source_path = os.path.join(extraction_path, file)
            target_path = os.path.join(folder_path, file_name)
            os.rename(source_path, target_path)
            path_list.append(target_path)
    ZipFile.close(zip_object)
    os.remove(save_file_path)
    rmtree(extraction_path, ignore_errors=True)
    return path_list


def get_file_name_length(file_path: str) -> int:
    """
    Return the length of the file name.

    Example:
    get_file_name_length("/home/test.txt") -> 4

    :param file_path: absolute or relative path of the file

    :return: int with the length of the file name
    """
    file_name_extension = get_file_name(file_path)
    file_name = file_name_extension.split(".")[0]
    return len(file_name)


def get_file_size(file_path: str) -> int:
    """
    Return the file size.

    Example:
    get_file_size("/home/test.txt") -> 10769322

    :param file_path: absolute or relative path of the file

    :return: bytes value of the file size
    """
    return os.path.getsize(file_path)
