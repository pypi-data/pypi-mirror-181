import unittest
import zoneinfo
from datetime import datetime, timedelta
from time import sleep

from kf_utils import timers
from test.resources import test_messages


class TestTimers(unittest.TestCase):
    """
    Test timers module
    """

    now_method: str = 'timers.now'
    str_to_datetime_method: str = 'timers.str_to_datetime'

    timezone: str = 'Europe/Madrid'
    valid_str_datetime: str = '2022-07-13 10:00:00.21324+00:02'
    timer: timers.Timer

    def setUp(self) -> None:
        self.timer = timers.Timer()

    # 1. Test timers.now method
    def test_now_return_type(self) -> None:
        """
        GIVEN timers.now call \n
        WHEN timers.now method is called \n
        THEN timers.now returned value is not None \n
        AND detes.now returned value type is datetime
        """
        now = timers.now()

        self.assertIsNotNone(
            now,
            test_messages.METHOD_RETURNS_NONE.format(method=self.now_method)
        )
        self.assertIsInstance(
            now,
            datetime,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(method=self.now_method, value='datetime')
        )

    def test_now_timezone(self) -> None:
        """
        GIVEN timers.now call \n
        WHEN timers.now method is called \n
        THEN timers.now timezone value is not None \n
        AND detes.now timezone value type is Europe/Madrid
        """
        self.test_now_return_type()

        timezone = timers.now().tzinfo
        spain_tz = zoneinfo.ZoneInfo(self.timezone)

        self.assertIsNotNone(
            timezone,
            test_messages.METHOD_RETURNS_NONE.format(method=f'{self.now_method} tzinfo')
        )
        self.assertEqual(
            timezone,
            spain_tz,
            test_messages.IS_NOT_EQUAL.format(first=f'{self.now_method} timezone', second=f'{self.timezone} timezone')
        )

    # 2. Test timers.str_to_datetime method
    def test_str_to_datetime_return_type(self) -> None:
        """
        GIVEN a valid str datetime param \n
        WHEN timers.str_to_datetime method is called \n
        THEN timers.str_to_datetime returned value is not None \n
        AND detes.str_to_datetime returned value type is datetime
        """
        date = timers.str_to_datetime(self.valid_str_datetime)

        self.assertIsNotNone(
            date,
            test_messages.METHOD_RETURNS_NONE.format(method=self.str_to_datetime_method)
        )
        self.assertIsInstance(
            date,
            datetime,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(method=self.str_to_datetime_method, value='datetime')
        )

    def test_str_to_datetime_bad_param(self) -> None:
        """
        GIVEN a not valid str datetime param \n
        WHEN timers.str_to_datetime method is called \n
        THEN timers.str_to_datetime raises a ValueError exception
        """
        not_valid_str_datetime = '2022-07-13 10:00:00.21324'

        self.assertRaises(ValueError, timers.str_to_datetime, not_valid_str_datetime)

    # 3. Test timers.Timer class
    def test_timer_is_build(self) -> None:
        """
        GIVEN no parameters \n
        WHEN Timer's constructor is called \n
        THEN a Timer object is built
        """
        self.assertIsNotNone(self.timer, test_messages.IS_NONE.format(first='Timer class'))

    def test_timer_now(self) -> None:
        """
        GIVEN a Timer object \n
        WHEN now() is called \n
        THEN the actual datetime is returned \n
        AND the actual datetime is saved in the 'n' attribute of the class
        """
        timer_old_now: datetime = self.timer.n
        sleep(0.0000001)
        now: datetime = self.timer.now()
        timer_new_now: datetime = self.timer.n

        self.assertIsInstance(timer_old_now, datetime)
        self.assertIsInstance(now, datetime)
        self.assertIsInstance(timer_new_now, datetime)

        self.assertNotEqual(timer_old_now, timer_new_now)
        self.assertEqual(now, timer_new_now)

    def test_timer_trig(self) -> None:
        """
        GIVEN a Timer object \n
        WHEN trig() is called \n
        THEN a Timer object is returned \n
        AND now() is also executed \n
        AND 'n' attribute is updated
        """
        timer_old_now: datetime = self.timer.n
        sleep(0.0000001)
        trig_result: timers.Timer = self.timer.trig()
        timer_new_now: datetime = self.timer.n
        trig_timer_new_now: datetime = trig_result.n

        self.assertIsInstance(timer_old_now, datetime)
        self.assertIsInstance(timer_new_now, datetime)
        self.assertIsInstance(trig_timer_new_now, datetime)
        self.assertIsInstance(trig_result, timers.Timer)

        self.assertEqual(self.timer, trig_result)
        self.assertNotEqual(timer_old_now, timer_new_now)
        self.assertEqual(timer_new_now, trig_timer_new_now)

    def test_timer_delta_reset_now(self) -> None:
        """
        GIVEN a Timer object \n
        WHEN delta() is called \n
        THEN if reset = False, 'n' attribute is not reset \n
        AND if reset = TRue, 'n' attribute is reset
        """
        timer_first_now: datetime = self.timer.n
        sleep(0.0000001)
        self.timer.delta()
        timer_second_now: datetime = self.timer.n
        sleep(0.0000001)
        self.timer.delta(True)
        timer_third_now: datetime = self.timer.n

        self.assertEqual(timer_first_now, timer_second_now)
        self.assertNotEqual(timer_first_now, timer_third_now)

    def test_timer_delta(self) -> None:
        """
        GIVEN a Timer object \n
        WHEN delta() is called \n
        THEN difference between now and last now is well calculated
        """
        delta: timedelta = self.timer.delta()

        self.assertIsNotNone(delta)
        self.assertIsInstance(delta, timedelta)

    def test_timer_console(self) -> None:
        """
        GIVEN a Timer object \n
        WHEN console() is called \n
        THEN deltas() is executed and returned
        """
        console_deltas: str = self.timer.console()

        self.assertIsNotNone(console_deltas)
        self.assertIsInstance(console_deltas, str)

    def test_timer_deltas(self) -> None:
        """
        GIVEN a Timer object \n
        WHEN deltas() is called \n
        THEN delta() as string is returned
        """
        deltas: str = self.timer.deltas()

        self.assertIsNotNone(deltas)
        self.assertIsInstance(deltas, str)
