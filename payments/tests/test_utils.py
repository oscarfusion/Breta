import pytz
from django.utils import timezone
from django.test import TestCase

from .. import utils


class UtilsTestCase(TestCase):
    def test_display_at_date_thursday(self):
        date = timezone.datetime(year=2015, month=1, day=1)
        new_date = utils.transaction_display_at(date)
        self.assertEqual(new_date.year, 2015)
        self.assertEqual(new_date.day, 7)
        self.assertEqual(new_date.month, 1)

    def test_display_at_date_sunday(self):
        date = timezone.datetime(year=2015, month=1, day=4, hour=8)
        new_date = utils.transaction_display_at(date)
        self.assertEqual(new_date.year, 2015)
        self.assertEqual(new_date.day, 7)
        self.assertEqual(new_date.month, 1)

    def test_display_at_date_sunday_after_nine_utc(self):
        tz = pytz.timezone("UTC")
        date = timezone.datetime(year=2015, month=1, day=4, hour=10)
        date = tz.localize(date)
        new_date = utils.transaction_display_at(date)
        self.assertEqual(new_date.year, 2015)
        self.assertEqual(new_date.day, 7)
        self.assertEqual(new_date.month, 1)

    def test_display_at_date_sunday_after_nine_eastern(self):
        tz = pytz.timezone("UTC")
        date = timezone.datetime(year=2015, month=1, day=4, hour=15)
        date = tz.localize(date)
        new_date = utils.transaction_display_at(date)
        self.assertEqual(new_date.year, 2015)
        self.assertEqual(new_date.day, 14)
        self.assertEqual(new_date.month, 1)

    def test_display_at_date_monday(self):
        tz = pytz.timezone("UTC")
        date = timezone.datetime(year=2015, month=1, day=5)
        date = tz.localize(date)
        new_date = utils.transaction_display_at(date)
        self.assertEqual(new_date.year, 2015)
        self.assertEqual(new_date.day, 14)
        self.assertEqual(new_date.month, 1)
