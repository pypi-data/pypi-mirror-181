"""
File:               timers.py
Description:        Helpers for custom timers
Created on:         16-Sep-2022 12:46:38
Original author:    SEMBU-Team NTTData
"""
import typing
import zoneinfo
from datetime import datetime, timedelta


def now() -> datetime:
    """
    Returns the current timestamp with timezone

    :return: Current timestamp with Spain timezone
    """
    spain_tz = zoneinfo.ZoneInfo("Europe/Madrid")
    return datetime.now().replace(tzinfo=spain_tz)


def str_to_datetime(string_datetime: str) -> datetime:
    """
    Given a string with a datetime in format YYYY-mm-dd HH:MM:SS.f+Z (2022-07-13 10:00:00.21324+00:02),
    covert this string in a datetime object

    :param string_datetime: string with a properly formatted datetime

    :return: datetime object
    """
    converted_datetime = datetime.strptime(string_datetime, '%Y-%m-%d %H:%M:%S.%f%z')
    return converted_datetime


class Timer:
    """
    Capturing and display timedelta.

    Attributes:
        n       datetime that represents the current instant
        d       None
        out     Output of the class
    """

    n: typing.Union[datetime, None]
    d: typing.Union[timedelta, None]

    def __init__(self):
        self.n = self.now()
        self.d = None
        self.out = self.console

    def now(self) -> datetime:
        """
        This moment.

        :return: the current instant as datetime
        """
        self.n = datetime.now()
        return self.n

    def trig(self):
        """
        Triggers now(), and returns self.

        :return: the self object with n attribute updated with the current datetime instant
        """
        self.n = datetime.now()
        return self

    def console(self) -> str:
        """
        Prints the delta.

        :return: the delta as string. Please refer to delta method documentation for more information
        """
        dels = self.deltas()
        print(dels)
        #print(self.deltas())
        return dels

    def delta(self, reset: bool = False) -> timedelta:
        """
        Difference between now and the last now.
        If reset True n is set to 0, thus being able to use consecutive deltas without having to re-now(). Example:
            t = Timer().now()
            print(t.deltas(True))
            print(t.deltas(True))
            ...

        :param reset: if it is True, n attribute is set to 0

        :return: difference between now and the last now as timedelta object
        """
        self.n = datetime.now() if reset else self.n
        return datetime.now() - self.n

    def deltas(self) -> str:
        """
        Returns the timedelta as a string. Please, refer to delta method documentation for more information.

        :return: the timedelta as string.
        """
        return str(self.delta())
