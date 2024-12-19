"""
This module will fetch the report from the server
"""

import datetime

class ReportFetcher:
    """
    This class will fetch the report from the server
    """

    def __init__(self, database):
        """
        Initialize the class
        """
        self.database = database

    def _get_default_dates(self, date_start_input, date_end_input):
        if not date_start_input or not date_end_input:
            today = datetime.date.today()
            date_start_input = today - datetime.timedelta(days=today.weekday())
            date_end_input = today + datetime.timedelta(days=6 - today.weekday())
        return date_start_input, date_end_input

    def fetch_all_data(self, date_start_input=None, date_end_input=None):
        """
        Fetch all data from the database
        """
        date_start_input, date_end_input = self._get_default_dates(
            date_start_input, date_end_input)
        self.database.create_connection()
        if self.database.connection:
            data = self.database.execute_query(
                f"""SELECT * FROM register_table
                WHERE date_register BETWEEN '{date_start_input}'
                AND '{date_end_input}'"""
            )
            self.database.close_connection()
            return data
        return None

    def fetch_data_report(self, date_start_input=None, date_end_input=None):
        """
        Fetch data from the database for the report
        """
        date_start_input, date_end_input = self._get_default_dates(
            date_start_input, date_end_input)

        self.database.create_connection()
        if self.database.connection:
            query = f"""
                SELECT
                    id_register,
                    date_register,
                    name_piece,
                    gross_weight,
                    cost
                FROM register_table
                WHERE date_register BETWEEN '{date_start_input}'
                AND '{date_end_input}'
            """
            data = self.database.execute_query(query)
            self.database.close_connection()
            return data
        return None

    def fetch_data_report_csv(
            self, date_start_input=None, date_end_input=None):
        """
        Fetch data from the database for the report
        """
        date_start_input, date_end_input = self._get_default_dates(
            date_start_input, date_end_input)
        self.database.create_connection()
        if self.database.connection:
            data = self.database.execute_query(
                f"""
                SELECT
                    number_of_part,
                    sum(gross_weight)
                    FROM register_table
                    WHERE date_register BETWEEN '{date_start_input}'
                    AND '{date_end_input}'
                    GROUP BY number_of_part
                """
                )
            self.database.close_connection()
            return data
        return None
