# monthinfo

[![test](https://github.com/marco-ostaska/monthinfo/actions/workflows/unit_test.yml/badge.svg)](https://github.com/marco-ostaska/monthinfo/actions/workflows/unit_test.yml)

A package that that gives you information about the month

## Installation

```
pip install monthinfo
```

### Usage

```python
from monthinfo import monthinfo

# initialize month_info object with Nov/2022 and the first day of month as Saturday
# range of 0=Monday, 6=Sunday
month_info = monthinfo.CurrentMonth(month=11, year=2022, first_day_of_week=5)
```

## Features

### calendar()

Returns the calendar in the month.

### first_week_day()

Returns the first week day in the month

### get_calendar_indexes_for_this_day(day)

Returns a tuple with the indexes that can be used with calendar() for the given day.

### is_first_monday(day)

Returns True if the given day is the first Monday in the month

### is_first_tuesday(day)

Returns True if the given day is the first Tuesday in the month

### is_first_wednesday(day)

Returns True if the given day is the first Wednesday in the month

### is_first_thursday(day)

Returns True if the given day is the first Thursday in the month

### is_first_friday(day)

Returns True if the given day is the first Friday in the month

### is_first_saturday(day)

Returns True if the given day is the first Saturday in the month

### is_first_sunday(day)

Returns True if the given day is the first Sunday in the month

### is_first_weekend(day)

Returns True if the given day is the first weekend in the month

### is_monday(day)

Returns True if the given day is Monday

### is_tuesday(day)

Returns True if the given day is Tuesday

### is_wednesday(day)

Returns True if the given day is Wednesday

### is_thursday(day)

Returns True if the given day is Thursday

### is_friday(day)
Returns True if the given day is Friday

### is_saturday(day)

Returns True if the given day is Saturday

### is_sunday(day)

Returns True if the given day is Sunday

### is_weekend(day)

Returns True if the given day in a weekend

### list_of_days()

Returns a list of days in the month

### list_of_mondays()

Returns a list of Mondays in the month

### list_of_tuesdays()

Returns a list of Tuesdays in the month

### list_of_wednesdays

Returns a list of Wednesday in the month

### list_of_thursdays()

Returns a list of Thursday in the month

### list_of_fridays()

Returns a list of Fridays in the month

### list_of_saturdays()

Returns a list of Saturdays in the month

### list_of_sundays()

Returns a list of Sundays in the month

### list_of_weeks()

Returns a list of weeks in the month. (Each week is a list of days.)

### number_of_days()

Returns the number of days in the month

### number_of_weekdays()

Returns the number of week days in the month

### number_of_weekends()

Returns the number of weekends in the month

### number_of_weeks()

Returns the number of weeks in the month

### number_of_mondays()

Returns the number of Mondays in the month

### number_of_tuesdays()

Returns the number of Tuesdays in the month

### number_of_wednesdays()

Returns the number of Wednesday in the month

### number_of_thursdays()

Returns the number of Thursday in the month

### number_of_fridays()

Returns the number of Fridays in the month

### number_of_saturdays()

Returns the number of Saturdays in the month

### number_of_sundays()

Returns the number of Sundays in the month
