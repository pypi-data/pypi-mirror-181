import calendar
import datetime


class CurrentMonth():
    def __init__(self, month, year, first_week_day):
        calendar.setfirstweekday(first_week_day)
        self.month = month
        self.year = year

    def calendar(self):
        """
        Returns a matrix representing a month's calendar.

        Each row represents a week, and each column represents a day of the week.
        Days that are not part of the current month are represented by zeros.

        Returns:
            A list of lists containing integers representing the days of the month.
        """
        return calendar.monthcalendar(self.year, self.month)

    def first_week_day(self) -> str:
        """
        Returns the day of the week of the first day of the current month.

        Returns:
            A string representing the day of the week (e.g. "Monday").
        """
        week_days = {0: "Monday", 1: "Tuesday", 2: "Wednesday",
                     3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"}
        return week_days[datetime.date(self.year, self.month, 1).weekday()]

    def list_of_days(self) -> list:
        """
        Returns a list of the days in the current month.

        The list contains integers representing the days of the month, starting from 1.

        Returns:
            A list of integers representing the days of the month.
        """
        return list(range(1, calendar.monthrange(self.year, self.month)[1]+1))

    def list_of_weeks(self) -> list:
        """
        Returns a list of the weeks in the current month.

        Each element of the list is a list of integers representing the days of the week.
        Days that are not part of the current month are represented by zeros.

        Returns:
            A list of lists containing integers representing the days of the month.
        """
        return list(calendar.monthcalendar(self.year, self.month))

    def number_of_weeks(self) -> int:
        """
        Returns the number of weeks in the current month.

        Returns:
            An integer representing the number of weeks in the current month.
        """
        return len(calendar.monthcalendar(self.year, self.month))

    def number_of_days(self) -> int:
        """
        Returns the number of days in the current month.

        Returns:
            An integer representing the number of days in the current month.
        """
        return calendar.monthrange(self.year, self.month)[1]

    def get_calendar_indexes_for_this_day(self, day):
        """
        Returns the indexes of the specified day in the month's calendar.

        The first index represents the week number (starting from 0), and the second
        index represents the day of the week (starting from 0). Days that are not
        part of the current month are represented by zeros in the calendar.

        Args:
            day: An integer representing the day of the month (1-31).

        Returns:
            A tuple containing two integers representing the indexes of the specified
            day in the month's calendar.

        Raises:
            ValueError: If the specified day is not in the current month.
        """
        for i, week in enumerate(self.calendar()):
            for j, d in enumerate(week):
                if d == day:
                    return i, j

    def is_saturday(self, day) -> bool:
        """
        Returns True if the specified day is a Saturday, False otherwise.

        Args:
            day: An integer representing the day of the month (1-31).

        Returns:
            A boolean indicating whether the specified day is a Saturday.

        Raises:
            ValueError: If the specified day is not in the current month.
        """
        return datetime.date(self.year, self.month, day).weekday() == 5

    def is_first_saturday(self, day) -> bool:
        """
        Returns True if the specified day is the first Saturday of the month, False otherwise.

        Args:
            day: An integer representing the day of the month (1-31).

        Returns:
            A boolean indicating whether the specified day is the first Saturday of the month.

        Raises:
            ValueError: If the specified day is not in the current month.
        """
        return self.is_first_weekend(day) and self.is_saturday(day)

    def list_of_saturdays(self) -> list:
        """
        Returns a list of the days in the current month that are Saturdays.

        The list contains integers representing the days of the month, starting from 1.

        Returns:
            A list of integers representing the days of the month that are Saturdays.
        """
        return [day for day in self.list_of_days() if self.is_saturday(day)]

    def number_of_saturdays(self) -> int:
        """
        Returns the number of Saturdays in the current month.

        Returns:
            An integer representing the number of Saturdays in the current month.
        """
        return len(self.list_of_saturdays())

    def is_sunday(self, day) -> bool:
        """
        Returns True if the specified day is a Sunday, False otherwise.

        Args:
            day: An integer representing the day of the month (1-31).

        Returns:
            A boolean indicating whether the specified day is a Sunday.

        Raises:
            ValueError: If the specified day is not in the current month.
        """
        return datetime.date(self.year, self.month, day).weekday() == 6

    def is_first_sunday(self, day) -> bool:
        """
        Returns True if the specified day is the first Sunday of the month, False otherwise.

        Args:
            day: An integer representing the day of the month (1-31).

        Returns:
            A boolean indicating whether the specified day is the first Sunday of the month.

        Raises:
            ValueError: If the specified day is not in the current month.
        """
        return self.is_first_weekend(day) and self.is_sunday(day)

    def list_of_sundays(self) -> list:
        """
        Returns a list of the days in the current month that are Sundays.

        The list contains integers representing the days of the month, starting from 1.

        Returns:
            A list of integers representing the days of the month that are Sundays.
        """
        return [day for day in self.list_of_days() if self.is_sunday(day)]

    def number_of_sundays(self) -> int:
        """
        Returns the number of Sundays in the current month.

        Returns:
            An integer representing the number of Sundays in the current month.
        """
        return len(self.list_of_sundays())

    def is_weekend(self, day) -> bool:
        """
        Returns True if the specified day is a weekend day (Saturday or Sunday), False otherwise.

        Args:
            day: An integer representing the day of the month (1-31).

        Returns:
            A boolean indicating whether the specified day is a weekend day.

        Raises:
            ValueError: If the specified day is not in the current month.
        """
        return datetime.date(self.year, self.month, day).weekday() >= 5

    def is_first_weekend(self, day) -> bool:
        """
        Returns True if the specified day is in the first weekend of the month (Saturday or Sunday), False otherwise.

        Args:
            day: An integer representing the day of the month (1-31).

        Returns:
            A boolean indicating whether the specified day is in the first weekend of the month.

        Raises:
            ValueError: If the specified day is not in the current month.
        """
        return self.is_weekend(day) and day < 8

    def number_of_weekends(self) -> int:
        """
        Returns the number of weekend days (Saturdays and Sundays) in the current month.

        The number of weekend days is calculated as the maximum number of Saturdays or Sundays in the month.

        Returns:
            An integer representing the number of weekend days in the current month.
        """
        if self.number_of_saturdays() >= self.number_of_sundays():
            return self.number_of_saturdays()

        return self.number_of_sundays()

    def is_weekend(self, day) -> bool:
        """
        Returns True if the specified day is a weekend day (Saturday or Sunday), False otherwise.

        Args:
            day: An integer representing the day of the month (1-31).

        Returns:
            A boolean indicating whether the specified day is a weekend day.

        Raises:
            ValueError: If the specified day is not in the current month.
        """
        return datetime.date(self.year, self.month, day).weekday() >= 5

    def is_first_weekend(self, day) -> bool:
        """
        Returns True if the specified day is in the first weekend of the month (Saturday or Sunday), False otherwise.

        Args:
            day: An integer representing the day of the month (1-31).

        Returns:
            A boolean indicating whether the specified day is in the first weekend of the month.

        Raises:
            ValueError: If the specified day is not in the current month.
        """
        return self.is_weekend(day) and day < 8

    def is_monday(self, day) -> bool:
        """
        Returns True if the specified day is a Monday, False otherwise.

        Args:
            day: An integer representing the day of the month (1-31).

        Returns:
            A boolean indicating whether the specified day is a Monday.

        Raises:
            ValueError: If the specified day is not in the current month.
        """
        return datetime.date(self.year, self.month, day).weekday() == 0

    def is_first_monday(self, day) -> bool:
        """
        Returns True if the specified day is the first Monday of the month, False otherwise.

        Args:
            day: An integer representing the day of the month (1-31).

        Returns:
            A boolean indicating whether the specified day is the first Monday of the month.

        Raises:
            ValueError: If the specified day is not in the current month.
        """
        return self.is_monday(day) and day < 8

    def list_of_mondays(self) -> list:
        """
        Returns a list of days in the current month that are Mondays.

        Returns:
            A list of integers representing the days of the month that are Mondays.

        Example:
            If the current month is December 2022, the method would return [5, 12, 19, 26].
        """
        return [day for day in self.list_of_days() if self.is_monday(day)]

    def number_of_mondays(self) -> int:
        """
        Returns the number of Mondays in the current month.

        The number of Mondays is calculated by generating a list of all the days in the current month that are Mondays, and then returning the length of that list.

        Returns:
            An integer representing the number of Mondays in the current month.

        Example:
            If the current month is December 2022, the method would return 4.
        """
        return len(self.list_of_mondays())

    def is_tuesday(self, day) -> bool:
        """
        Returns True if the specified day is a Tuesday, False otherwise.

        Args:
            day: An integer representing the day of the month (1-31).

        Returns:
            A boolean indicating whether the specified day is a Tuesday.

        Raises:
            ValueError: If the specified day is not in the current month.
        """
        return datetime.date(self.year, self.month, day).weekday() == 1

    def is_first_tuesday(self, day) -> bool:
        """
        Returns True if the specified day is the first Tuesday of the month, False otherwise.

        Args:
            day: An integer representing the day of the month (1-31).

        Returns:
            A boolean indicating whether the specified day is the first Tuesday of the month.

        Raises:
            ValueError: If the specified day is not in the current month.
        """
        return self.is_tuesday(day) and day < 8

    def list_of_tuesdays(self) -> list:
        """
        Returns a list of days in the current month that are Tuesdays.

        Returns:
            A list of integers representing the days of the month that are Tuesdays.

        Example:
            If the current month is December 2022, the method would return [6, 13, 20, 27].
        """
        return [day for day in self.list_of_days() if self.is_tuesday(day)]

    def number_of_tuesdays(self) -> int:
        """
        Returns the number of Tuesdays in the current month.

        This method counts the number of occurrences of Tuesday in the current month,
        by calling the `list_of_tuesdays` method and returning the length of the
        resulting list of dates.

        Returns:
            The number of Tuesdays in the current month.
        """
        return len(self.list_of_tuesdays())

    def is_wednesday(self, day) -> bool:
        """
        Returns True if the specified day is a Wednesday, False otherwise.

        This method checks whether the specified day falls on a Wednesday in the current
        month, by using the `datetime` module to extract the weekday of the given date.

        Args:
            day: An integer representing the day of the month (1-31).

        Returns:
            A boolean indicating whether the specified day is a Wednesday.

        Raises:
            ValueError: If the specified day is not in the current month.
        """
        return datetime.date(self.year, self.month, day).weekday() == 2

    def is_first_wednesday(self, day) -> bool:
        """Returns True if the specified day is the first Wednesday of the month, False otherwise.

        This method checks whether the specified day is both a Wednesday and the first
        Wednesday of the month. It does this by first calling the `is_wednesday` method
        to check whether the given day falls on a Wednesday, and then checking whether
        the day is before the 8th of the month (since the first week of the month always
        contains at most 7 days).

        Args:
            day: An integer representing the day of the month (1-31).

        Returns:
            A boolean indicating whether the specified day is the first Wednesday of the month.

        Raises:
            ValueError: If the specified day is not in the current month.
        """
        return self.is_wednesday(day) and day < 8

    def list_of_wednesdays(self) -> list:
        """
        Returns a list of days in the current month that are Wednesdays.

        Returns:
            A list of integers representing the days of the month that are Wednesdays.

        Example:
            If the current month is December 2022, the method would return [7, 14, 21, 28].
        """
        return [day for day in self.list_of_days() if self.is_wednesday(day)]

    def number_of_wednesdays(self) -> int:
        """
        Returns the number of Wednesdays in the current month.

        This method counts the number of occurrences of Wednesday in the current month,
        by calling the `list_of_wednesdays` method and returning the length of the
        resulting list of dates.

        Returns:
            The number of Wednesdays in the current month.
        """
        return len(self.list_of_wednesdays())

    def is_thursday(self, day) -> bool:
        """
        Returns True if the specified day is a Thursday, False otherwise.

        This method checks whether the specified day falls on a Thursday in the current
        month, by using the `datetime` module to extract the weekday of the given date.

        Args:
            day: An integer representing the day of the month (1-31).

        Returns:
            A boolean indicating whether the specified day is a Thursday.

        Raises:
            ValueError: If the specified day is not in the current month.
        """
        return datetime.date(self.year, self.month, day).weekday() == 3

    def is_first_thursday(self, day) -> bool:
        """
        Returns True if the specified day is the first Thursday of the month, False otherwise.

        This method checks whether the specified day is both a Thursday and the first
        Thursday of the month. It does this by first calling the `is_thursday` method
        to check whether the given day falls on a Thursday, and then checking whether
        the day is before the 8th of the month (since the first week of the month always
        contains at most 7 days).

        Args:
            day: An integer representing the day of the month (1-31).

        Returns:
            A boolean indicating whether the specified day is the first Thursday of the month.

        Raises:
            ValueError: If the specified day is not in the current month.
        """
        return self.is_thursday(day) and day < 8

    def list_of_thursdays(self) -> list:
        """
        Returns a list of days in the current month that are Thursdays.

        Returns:
            A list of integers representing the days of the month that are Thursdays.

        Example:
            If the current month is December 2022, the method would return [8, 15, 22, 29].
        """
        return [day for day in self.list_of_days() if self.is_thursday(day)]

    def number_of_thursdays(self) -> int:
        """
        Returns the number of Thursdays in the current month.

        This method counts the number of occurrences of Thursday in the current month,
        by calling the `list_of_thursdays` method and returning the length of the
        resulting list of dates.

        Returns:
            The number of Thursdays in the current month.
        """
        return len(self.list_of_thursdays())

    def is_friday(self, day) -> bool:
        """
        Returns True if the specified day is a Friday, False otherwise.

        This method checks whether the specified day falls on a Friday in the current
        month, by using the `datetime` module to extract the weekday of the given date.

        Args:
            day: An integer representing the day of the month (1-31).

        Returns:
            A boolean indicating whether the specified day is a Friday.

        Raises:
            ValueError: If the specified day is not in the current month.
        """
        return datetime.date(self.year, self.month, day).weekday() == 4

    def is_first_friday(self, day) -> bool:
        """
        Returns True if the specified day is the first Friday of the month, False otherwise.

        This method checks whether the specified day is both a Friday and the first
        Friday of the month. It does this by first calling the `is_friday` method
        to check whether the given day falls on a Friday, and then checking whether
        the day is before the 8th of the month (since the first week of the month always
        contains at most 7 days).

        Args:
            day: An integer representing the day of the month (1-31).

        Returns:
            A boolean indicating whether the specified day is the first Friday of the month.

        Raises:
            ValueError: If the specified day is not in the current month.
        """
        return self.is_friday(day) and day < 8

    def list_of_fridays(self) -> list:
        """
        Returns a list of days in the current month that are Fridays.

        Returns:
            A list of integers representing the days of the month that are Fridays.

        Example:
            If the current month is December 2022, the method would return [9, 16, 23, 30].
        """
        return [day for day in self.list_of_days() if self.is_friday(day)]

    def number_of_fridays(self) -> int:
        """
        Returns the number of Fridays in the current month.

        This method counts the number of occurrences of Friday in the current month,
        by calling the `list_of_fridays` method and returning the length of the
        resulting list of dates.

        Returns:
            The number of Fridays in the current month.
        """
        return len(self.list_of_fridays())

    def number_of_weekdays(self) -> int:
        """
        Returns the number of weekdays in the current month.

        This method returns the number of weekdays in the current month, by calling the
        `number_of_sundays` and `number_of_mondays` methods.

        Returns:
            The number of weekdays in the current month.
        """
        return self.number_of_days() - (self.number_of_saturdays() + self.number_of_sundays())
