''' This module contains the class DatabaseModel that is used to
interact with the database'''

import psycopg2
from psycopg2 import sql
import credentials

class DatabaseModel:
    ''' This class is used to interact with the database'''
    def __init__(self):
        ''' Initialize the class'''
        self.connection = None

    def create_connection(self):
        ''' Create a connection to the database'''
        try:
            self.connection = psycopg2.connect(
                database=credentials.DATABASE_NAME,
                user=credentials.DATABASE_USER,
                password=credentials.DATABASE_PASSWORD,
                host=credentials.DATABASE_HOST,
                port=credentials.DATABASE_PORT
            )
            print("Successful connection to the database")
        except (
            psycopg2.Error,
            UnicodeDecodeError,
            psycopg2.OperationalError,
            psycopg2.DatabaseError
            ) as error:
            print(f"Error connecting to the database: {error}")
            self.connection = None

        self.execute_query(f"SET search_path TO {credentials.DATABASE_SCHEMA}")

    def close_connection(self):
        ''' Close the connection to the database'''
        if self.connection:
            self.connection.close()
            print("Connection closed")

    def insert_data(self, table, columns, values):
        ''' Insert data into a table'''
        if not self.connection:
            print("No connection to the database")
            return False

        try:
            with self.connection.cursor() as cursor:
                insert_query = sql.SQL("""INSERT INTO {} ({})
                                       VALUES ({})""").format(
                    sql.Identifier(table),
                    sql.SQL(', ').join(map(sql.Identifier, columns)),
                    sql.SQL(', ').join(map(sql.Literal, values))
                )
                cursor.execute(insert_query)
                self.connection.commit()
                print("Data inserted successfully.")
                return True
        except (psycopg2.Error, psycopg2.DatabaseError) as error:
            print(f"Error inserting data: {error}")
            return False

    def execute_query(self, query):
        ''' Execute a query to the database'''
        if not self.connection:
            print("No connection to the database")
            return False

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query)
                data = cursor.fetchall()
                return data
        except (psycopg2.Error, psycopg2.DatabaseError) as error:
            print(f"Error executing query: {error}")
            return None

    def execute_query_to_delete(self, query):
        ''' Execute a query to the database'''
        if not self.connection:
            print("No connection to the database")
            return False

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query)
                self.connection.commit()
                print("Data deleted successfully.")
                return True
        except (psycopg2.Error, psycopg2.DatabaseError) as error:
            print(f"Error executing query: {error}")
            return False
