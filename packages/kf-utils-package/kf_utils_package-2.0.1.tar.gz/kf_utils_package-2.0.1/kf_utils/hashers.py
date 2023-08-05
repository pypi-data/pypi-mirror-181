"""
File:               hashers.py
Description:        Helpers for custom hashing
Created on:         19-feb-2022 12:46:38
Original author:    SEMBU-Team NTTData
"""
import enum
import hashlib
import uuid
import zlib


class HashAlgorithm(enum.IntEnum):
    """
    Hashing methods.
    """
    md5 = 1
    sha1 = 2
    sha256 = 3


def crc(value) -> int:
    """
    Returns the CRC of a text as an int. Uses zlib.

    :param value: the value to hash

    :return: the CRC of the text as int
    """
    return zlib.crc32(str(value).encode()) & 0xffffffff  # Must use "& 0xffffffff" as per docs.


def scrc(value) -> str:
    """
    Returns the CRC of a text as a string. Uses zlib.

    :param value: the text to hash

    :return: the CRC of the text as string
    """
    return str(zlib.crc32(str(value).encode()) & 0xffffffff)  # Must use "& 0xffffffff" as per docs.


def hash(file_content: str, algorithm: HashAlgorithm = HashAlgorithm.md5) -> str:
    """
    Returns the hash of a file content.

    :param file_content: the str with the file content
    :param algorithm: the type of hash

    :return: the hash of a file content as string
    """
    if algorithm == HashAlgorithm.md5:
        return hashlib.md5(file_content.encode()).hexdigest()
    elif algorithm == HashAlgorithm.sha1:
        return hashlib.sha1(file_content.encode()).hexdigest()
    elif algorithm == HashAlgorithm.sha256:
        return hashlib.sha256(file_content.encode()).hexdigest()


def md5(text) -> str:
    """
    Returns the MD5 hash as a string.

    :param text: text to hash

    :return: MD5 of the text as string
    """
    return hash(str(text))


def hashbin(file: str, algorithm_type: HashAlgorithm = HashAlgorithm.md5) -> str:
    """
    Returns the hash of a binary file content.

    :param file: path to the file
    :param algorithm_type: algorithm to use to hash the file content.
        By default, is set to md5

    :return: the file content hashed using a specific algorithm as string

    :raise NotImplemented: if the algorithm type is not implemented
    """
    buffer_size = 65536  # lets read stuff in 64kb chunks!

    if algorithm_type == HashAlgorithm.md5:
        algorithm = hashlib.md5()
    elif algorithm_type == HashAlgorithm.sha1:
        algorithm = hashlib.sha1()
    elif algorithm_type == HashAlgorithm.sha256:
        algorithm = hashlib.sha256()

    with open(file, 'rb') as handle:
        while True:
            data = handle.read(buffer_size)
            if not data:
                break
            algorithm.update(data)

    return algorithm.hexdigest()


def md5int(text) -> int:
    """
    Returns the MD5 hash as an int.

    :param text: text to hash

    :return: MD5 hash as integer
    """
    return int(hash(text), 16)


def uuids() -> str:
    """
    Returns a standard 4-UUID as a string.

    :return: standard 4-UUID as a string
    """
    return str(uuid.uuid4())
