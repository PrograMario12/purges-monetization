''' This module is the model of the task. It contains the queries and
support classes. '''

import tkinter as tk
import datetime
from model import database_model

class Model:
    ''' This class is the model'''
    def __init__(self):
        ''' Initialize the class'''
        self.database = database_model.DatabaseModel()

    def fetch_data_report(self, date_start_input=None, date_end_input=None):
        ''' Fetch data from the database for the report'''

        if not date_start_input or not date_end_input:
            today = datetime.date.today()
            date_start_input = today - datetime.timedelta(days=today.weekday())
            date_end_input = today + datetime.timedelta(days=6 - today.weekday())

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
            print (query)
            data = self.database.execute_query(query)
            self.database.close_connection()
            return data
        return None

    def _get_fetch_data_report_query(self, date_start, date_end):
        ''' Get the SQL query for fetching data report '''
        return f"""
                SELECT
                    id_register,
                    date_register,
                    name_piece,
                    gross_weight,
                    cost
                    FROM register_table
                    WHERE date_register BETWEEN '{date_start}' AND '{date_end}'
                """

    def fetch_data_report_csv(
            self, date_start_input=None, date_end_input=None):
        ''' Fetch data from the database for the report'''
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

    def validate_day(self, date_input):
        ''' Validate the day of the week '''
        if date_input == str(datetime.date.today()):
            return True
        return False

    def delete_item(self, id_item):
        ''' Delete the selected item. '''
        self.database.create_connection()
        if self.database.connection:
            self.database.execute_query_to_delete(
                f"""
                DELETE FROM register_table
                WHERE id_register = {id_item}
                """
            )
            self.database.close_connection()

# Example of use
if __name__ == "__main__":
    pass
