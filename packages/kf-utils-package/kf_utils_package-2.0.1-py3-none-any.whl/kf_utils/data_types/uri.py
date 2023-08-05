"""
File:               uri.py
Description:        Core classes URL and URI
Created on:         04-june-2022 11:25:00
Author:             SEMBU Team - NTTData Barcelona
"""
import re
import typing

import urllib3 as ul
import validators

KNOWLEDGE_FACTORY_NAMESPACE = 'http://data.knowledgefactory.com/rsql/vars'


class ArgumentException(Exception):
    """
    Invalid argument received.
    """
    def __init__(self):
        self.msg = "Invalid argument."


class URISyntaxError(Exception):
    """
    Thrown if the URI passed to a VarUri does not comply with the expected syntax.
    """
    def __init__(self, msg: str = None):
        raise SyntaxError(msg if msg else None)


class URI:
    """
    URI data type. Accepts the following protocols:

        - file:../dir/dir/file.ext
        - http://example.org
        - ftp://repo.example.org/dir
        - ftps://repo.example.org/dir
        - mailto:username@server.org
        - urn:zone:domain:host:etc

    Attributes:
        host        URI's host part (e.g.: 'example.org')
        uri_str     URI stored as plain string
        protocol    URI's protocol (e.g.: 'file:', 'http:', 'ftp:')
    """
    host: typing.Union[str, None]
    uri_str: typing.Union[str, None]
    protocol: typing.Union[str, None]

    def __init__(self, uri: str = None):
        if uri is None:
            return
        self.validate(uri)
        self.uri_str = uri
        self.get_protocol()
        self.get_host()

    @staticmethod
    def validate(uri: str) -> None:
        """
        Checks whether the uri has a valid URI syntax, including the protocol "file:"

        :param uri: uri to validate

        :raise ArgumentException: if uri has not a valid format
        """
        p = '^file:'
        f = re.match(p, uri)
        val = validators.url(uri)
        if not val and f is None:
            error = ArgumentException()
            error.msg = f"The argument {uri} is not a valid URL."
            raise error

    def get_protocol(self) -> typing.Union[str, None]:
        """
        Returns the protocol of the URL (http:, ftp:, ftps:, file:). No need to verify if url is None,
        since this is taken care of at construction time.

        :return: the protocol of the url
        """
        try:
            i = self.uri_str.index(':')
            self.protocol = self.uri_str[:i + 1] if bool(i) else None
        except ValueError:
            self.protocol = None
        return self.protocol

    def get_host(self) -> typing.Union[str, None]:
        """
        Returns the host of the URI (example.org). No need to verify if url is None,
        since this is taken care of at construction time.

        :return: the host of the URI
        """
        self.host = ul.get_host(self.uri_str)
        self.host = self.host[1] if self.host and bool(self.host) and len(self.host) > 1 else None
        return self.host

    def __call__(self, uri: str = None):
        self.__init__(uri)


class URL(URI):
    """
    Specialisation of URI class, for back-wards compatibility with previous NTT-DGI developments.
    """
    def __init__(self, url: str):
        super(URL, self).__init__(url)
