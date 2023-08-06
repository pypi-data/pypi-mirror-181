import unittest
from unittest.mock import call, Mock

from freezegun import freeze_time

from tepet import PerfTimer
from tepet.timer import Timer


class PerfTimerTest(unittest.TestCase):
    def setUp(self):
        self.printer_mock = Mock()

    def assertCallsPrinterCorrectly(self):
        calls = [
            call('1970 Jan 01 00:00:00 +0000 ==== started'),
            call('1970 Jan 01 00:00:00 +0000 ==== elapsed 0.00000 seconds')]
        self.printer_mock.assert_has_calls(calls)
        self.assertEqual(self.printer_mock.call_count, 2)

    def test_timer_works_as_a_contextmanager(self):
        with freeze_time("1970-01-01"):
            with PerfTimer(printer=self.printer_mock):
                pass # noqa
        self.assertCallsPrinterCorrectly()

    def test_timer_works_as_a_decorator(self):
        @PerfTimer(printer=self.printer_mock)
        def workload():
            # noqa
            pass

        with freeze_time("1970-01-01"):
            workload()
        self.assertCallsPrinterCorrectly()


class TimerTest(unittest.TestCase):
    def setUp(self):
        self.printer_mock = Mock()

    def assertHasCorrectCallCount(self):
        self.assertEqual(self.printer_mock.call_count, 1)

    def test_timer_works_as_a_contextmanager(self):
        with freeze_time("1970-01-01"):
            with Timer(self.printer_mock):
                pass # noqa
        self.assertHasCorrectCallCount()

    def test_timer_works_as_a_decorator(self):
        @Timer(self.printer_mock)
        def workload():
            # noqa
            pass

        with freeze_time("1970-01-01"):
            workload()
        self.assertHasCorrectCallCount()
