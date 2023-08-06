import calendar
import unittest

from monthinfo import monthinfo


class TestMonthInfo(unittest.TestCase):

    def test_can_assign_month(self):
        month_info = monthinfo.CurrentMonth(month=11, year=2022, first_week_day=5)
        self.assertEqual(month_info.month, 11)

    def test_calendar(self):
        month_info = monthinfo.CurrentMonth(11, 2022, 5)
        self.assertEqual(month_info.calendar()[0][3], 1)

    def test_is_saturday(self):
        month_info = monthinfo.CurrentMonth(month=11, year=2022, first_week_day=5)
        self.assertTrue(month_info.is_saturday(5))
        self.assertFalse(month_info.is_saturday(6))

    def test_is_sunday(self):
        month_info = monthinfo.CurrentMonth(month=11, year=2022, first_week_day=5)
        self.assertTrue(month_info.is_sunday(6))
        self.assertFalse(month_info.is_sunday(5))

    def test_is_monday(self):
        month_info = monthinfo.CurrentMonth(month=11, year=2022, first_week_day=5)
        self.assertTrue(month_info.is_monday(7))

    def test_is_tuesday(self):
        month_info = monthinfo.CurrentMonth(month=11, year=2022, first_week_day=5)
        self.assertTrue(month_info.is_tuesday(1))

    def test_is_wednesday(self):
        month_info = monthinfo.CurrentMonth(month=11, year=2022, first_week_day=5)
        self.assertTrue(month_info.is_wednesday(2))

    def test_is_thursday(self):
        month_info = monthinfo.CurrentMonth(month=11, year=2022, first_week_day=5)
        self.assertTrue(month_info.is_thursday(3))

    def test_is_friday(self):
        month_info = monthinfo.CurrentMonth(month=11, year=2022, first_week_day=5)
        self.assertTrue(month_info.is_friday(4))

    def test_is_first_weekend(self):
        month_info = monthinfo.CurrentMonth(month=11, year=2022, first_week_day=5)
        self.assertTrue(month_info.is_first_weekend(5))
        self.assertTrue(month_info.is_first_weekend(6))
        self.assertFalse(month_info.is_first_weekend(12))
        self.assertFalse(month_info.is_first_weekend(13))

    def test_is_first_saturday(self):
        month_info = monthinfo.CurrentMonth(month=11, year=2022, first_week_day=5)
        self.assertTrue(month_info.is_first_saturday(5))

    def test_is_first_sunday(self):
        month_info = monthinfo.CurrentMonth(month=11, year=2022, first_week_day=5)
        self.assertTrue(month_info.is_first_sunday(6))

    def test_is_first_monday(self):
        month_info = monthinfo.CurrentMonth(month=11, year=2022, first_week_day=5)
        self.assertTrue(month_info.is_first_monday(7))

    def test_is_first_tuesday(self):
        month_info = monthinfo.CurrentMonth(month=11, year=2022, first_week_day=5)
        self.assertTrue(month_info.is_first_tuesday(1))

    def test_is_first_wednesday(self):
        month_info = monthinfo.CurrentMonth(month=11, year=2022, first_week_day=5)
        self.assertTrue(month_info.is_first_wednesday(2))

    def test_is_first_thursday(self):
        month_info = monthinfo.CurrentMonth(month=11, year=2022, first_week_day=5)
        self.assertTrue(month_info.is_first_thursday(3))

    def test_is_first_friday(self):
        month_info = monthinfo.CurrentMonth(month=11, year=2022, first_week_day=5)
        self.assertTrue(month_info.is_first_friday(4))

    def test_list_of_days(self):
        month_info = monthinfo.CurrentMonth(month=11, year=2022, first_week_day=5)
        self.assertEqual(month_info.list_of_days()[0], 1)
        self.assertEqual(month_info.list_of_days()[29], 30)

    def test_list_of_weeks(self):
        month_info = monthinfo.CurrentMonth(
            month=11, year=2022, first_week_day=5)
        self.assertEqual(month_info.list_of_weeks()[0], [0, 0, 0, 1, 2, 3, 4])
        self.assertEqual(month_info.list_of_weeks()[
                         1], [5, 6, 7, 8, 9, 10, 11])

    def test_list_of_saturdays(self):
        month_info = monthinfo.CurrentMonth(month=11, year=2022, first_week_day=5)
        self.assertEqual(month_info.list_of_saturdays(), [5, 12, 19, 26])

    def test_list_of_sundays(self):
        month_info = monthinfo.CurrentMonth(month=11, year=2022, first_week_day=5)
        self.assertEqual(month_info.list_of_sundays(), [6, 13, 20, 27])

    def test_list_of_mondays(self):
        month_info = monthinfo.CurrentMonth(month=11, year=2022, first_week_day=5)
        self.assertEqual(month_info.list_of_mondays(), [7, 14, 21, 28])

    def test_list_of_tuesdays(self):
        month_info = monthinfo.CurrentMonth(month=11, year=2022, first_week_day=5)
        self.assertEqual(month_info.list_of_tuesdays(), [1, 8, 15, 22, 29])

    def test_list_of_wednesdays(self):
        month_info = monthinfo.CurrentMonth(month=11, year=2022, first_week_day=5)
        self.assertEqual(month_info.list_of_wednesdays(), [2, 9, 16, 23, 30])

    def test_list_of_thursdays(self):
        month_info = monthinfo.CurrentMonth(month=11, year=2022, first_week_day=5)
        self.assertEqual(month_info.list_of_thursdays(), [3, 10, 17, 24])

    def test_list_of_fridays(self):
        month_info = monthinfo.CurrentMonth(month=11, year=2022, first_week_day=5)
        self.assertEqual(month_info.list_of_fridays(), [4, 11, 18, 25])

    def test_first_weekend(self):
        month_info = monthinfo.CurrentMonth(
            month=11, year=2022, first_week_day=5)
        self.assertTrue(month_info.is_weekend(day=5))
        self.assertFalse(month_info.is_weekend(1))

    def test_first_week_day(self):
        month_info = monthinfo.CurrentMonth(month=11, year=2022, first_week_day=5)
        self.assertEqual(month_info.first_week_day(), "Tuesday")

    def test_number_of_weeks(self):
        month_info = monthinfo.CurrentMonth(month=11, year=2022, first_week_day=5)
        self.assertEqual(month_info.number_of_weeks(), 5)

    def test_number_of_days(self):
        month_info = monthinfo.CurrentMonth(month=11, year=2022, first_week_day=5)
        self.assertEqual(month_info.number_of_days(), 30)

    def test_number_of_saturdays(self):
        month_info = monthinfo.CurrentMonth(month=11, year=2022, first_week_day=5)
        self.assertEqual(month_info.number_of_saturdays(), 4)

    def test_number_of_sundays(self):
        month_info = monthinfo.CurrentMonth(month=11, year=2022, first_week_day=5)
        self.assertEqual(month_info.number_of_sundays(), 4)

    def test_number_of_mondays(self):
        month_info = monthinfo.CurrentMonth(month=11, year=2022, first_week_day=5)
        self.assertEqual(month_info.number_of_mondays(), 4)

    def test_number_of_tuesdays(self):
        month_info = monthinfo.CurrentMonth(month=11, year=2022, first_week_day=5)
        self.assertEqual(month_info.number_of_tuesdays(), 5)

    def test_number_of_wednesdays(self):
        month_info = monthinfo.CurrentMonth(month=11, year=2022, first_week_day=5)
        self.assertEqual(month_info.number_of_wednesdays(), 5)

    def test_number_of_thursdays(self):
        month_info = monthinfo.CurrentMonth(month=11, year=2022, first_week_day=5)
        self.assertEqual(month_info.number_of_thursdays(), 4)

    def test_number_of_fridays(self):
        month_info = monthinfo.CurrentMonth(month=11, year=2022, first_week_day=5)
        self.assertEqual(month_info.number_of_fridays(), 4)

    def test_number_of_weekends(self):
        month_info = monthinfo.CurrentMonth(month=11, year=2022, first_week_day=5)
        self.assertEqual(month_info.number_of_weekends(), 4)

    def test_number_of_weekdays(self):
        month_info = monthinfo.CurrentMonth(month=11, year=2022, first_week_day=5)
        self.assertEqual(month_info.number_of_weekdays(), 22)

    def test_get_calendar_indexes_for_this_day(self):
        month_info = monthinfo.CurrentMonth(11, 2022, first_week_day=5)
        week, day = month_info.get_calendar_indexes_for_this_day(1)
        self.assertEqual(week, 0)
        self.assertEqual(day, 3)
        self.assertEqual(month_info.calendar()[week][day], 1)


if __name__ == '__main__':
    unittest.main()
