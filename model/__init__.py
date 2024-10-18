''' This module is the model of the task. It contains the queries and 
support classes. '''

import psycopg2
from psycopg2 import sql
import credentials
from model import database_model

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
                """SELECT date_register,
                    name_piece,
                    gross_weight,
                    cost
                    FROM register_table
                    LIMIT 30
                """
                )
            self.database.close_connection()
            return data
        return None

# Example of use
if __name__ == "__main__":
    pass
