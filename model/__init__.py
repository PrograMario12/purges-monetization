''' This module is the model of the task. It contains the queries and 
support classes. '''

import csv
import tkinter as tk
from tkinter import filedialog
import psycopg2
from psycopg2 import sql
import credentials
from model import database_model
import datetime

class Model:
    ''' This class is the model'''
    def __init__(self):
        ''' Initialize the class'''
        self.database = database_model.DatabaseModel()

    def fetch_data_report(self, date_start_input=None, date_end_input=None):
        ''' Fetch data from the database for the report'''

        if date_start_input and date_end_input:
            date_start = date_start_input
            date_end = date_end_input
        else:
            today = datetime.date.today()
            date_start = today - datetime.timedelta(days=today.weekday())
            date_end = today + datetime.timedelta(days=6 - today.weekday())

        self.database.create_connection()
        if self.database.connection:
            data = self.database.execute_query(
                f"""
                SELECT date_register,
                    name_piece,
                    gross_weight,
                    cost
                    FROM register_table
                    WHERE date_register BETWEEN '{date_start}' AND '{date_end}'
                """
                )
            self.database.close_connection()
            return data
        return None

    def fetch_data_report_csv(self):
        ''' Fetch data from the database for the report'''
        self.database.create_connection()
        if self.database.connection:
            data = self.database.execute_query(
                """
                SELECT
                    number_of_part,
                    sum(gross_weight)
	                FROM register_table
                    GROUP BY number_of_part
                """
                )
            self.database.close_connection()
            return data
        return None

# Example of use
if __name__ == "__main__":
    pass
