''' This module is the model of the task. It contains the queries and 
support classes. '''

import psycopg2
from psycopg2 import sql
import credentials
from model import database_model
import csv
import tkinter as tk
from tkinter import filedialog

class Model:
    ''' This class is the model'''
    def __init__(self):
        ''' Initialize the class'''
        self.database = database_model.DatabaseModel()

    def fetch_data_report(self):
        ''' Fetch data from the database for the report'''
        self.database.create_connection()
        if self.database.connection:
            data = self.database.execute_query(
                """
                SELECT date_register,
                    name_piece,
                    gross_weight,
                    cost
                    FROM register_table
                """
                )
            self.database.close_connection()
            return data
        return None

    def generate_report(self):
        ''' Generate a report'''
        self.database.create_connection()
        if self.database.connection:
            data = self.database.execute_query(
                """
                SELECT date_register,
                    name_piece,
                    gross_weight,
                    cost
                    FROM register_table
                """
            )
            self.database.close_connection()

        if data:
            root = tk.Tk()
            root.withdraw()  # Hide the root window

            file_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                title="Save report as"
            )

            if file_path:
                with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(['date_register', 'name_piece', 'gross_weight', 'cost'])
                    writer.writerows(data)

# Example of use
if __name__ == "__main__":
    pass
