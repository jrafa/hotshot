# -*- coding: utf-8 -*-
"""
This module contains tests for hotshot, shot.
"""

import unittest
from datetime import date
from hotshot import convert_to_date, FORMAT_CALENDAR, FORMAT_DATETIME, check_date


class HotshotsTest(unittest.TestCase):
    """
    Class with tests module hotshot and shot
    """

    def test_convert_date(self):
        """
        Method checks convert string to date. Test with correct data.
        :return:
        """
        self.assertEqual(convert_to_date('2015-11-03 13:21:02.071381',
                                         FORMAT_DATETIME), date(2015, 11, 3))
        self.assertEqual(convert_to_date('03.11.2015', FORMAT_CALENDAR), date(2015, 11, 3))

    def test_convert_date_error(self):
        """
        Method checks convert string to date. Test with wrong data.
        :return:
        """
        try:
            convert_to_date('N/A', FORMAT_CALENDAR)
        except ValueError as error:
            self.assertEqual(type(error), ValueError)

    def test_hotshot_check_date(self):
        """
        Check if the date is between range of dates. Test with correct data.
        :return:
        """
        date_first = check_date('2015-11-03 13:21:02.071381', '03.11.2015', '20.11.2015')
        date_second = check_date('2015-11-03 13:21:02.071381', '01.11.2015', '02.11.2015')

        self.assertTrue(date_first)
        self.assertFalse(date_second)

    def test_hotshot_check_date_error(self):
        """
        Check if the date is between range of dates. Test with wrong data.
        :return:
        """
        try:
            check_date('N/A', 'N/A', '20.11.2015')
        except ValueError as error:
            self.assertEqual(type(error), ValueError)


if __name__ == "__main__":
    unittest.main()
