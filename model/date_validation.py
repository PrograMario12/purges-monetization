"""
This module contains the DateValidator class which is responsible for
validating the date input.
"""

import datetime

class DateValidator:
    """
    This class is used to validate the date input.
    """
    @staticmethod
    def validate_day(date_input):
        """
        Validate the date input.
        """
        return date_input == str(datetime.date.today())
