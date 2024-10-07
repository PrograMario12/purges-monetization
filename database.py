''' Module for connecting to and manipulating a PostgreSQL database'''

import psycopg2
from psycopg2 import sql
import credentials 

def create_connection():
    ''' Create a connection to the database'''
    try:
        # Configura los parámetros de conexión
        # connection = psycopg2.connect(
        #     database= '10.98.16.70',
        #     user= 'developer',
        #     password= 'd3v3l0p3r!',
        #     host= 5432,
        #     port= 
        # )
        connection = psycopg2.connect(
            database= credentials.DATABASE_NAME,
            user= credentials.DATABASE_USER,
            password= credentials.DATABASE_PASSWORD,
            host= credentials.DATABASE_HOST,
            port= credentials.DATABASE_PORT
        )

        print("Successful connection to the database")
        return connection
    except psycopg2.Error as error:
        print(f"""Error connecting to the database:
              {error.pgcode} - {error.pgerror}""")
    except UnicodeDecodeError as error:
        print(f"Encoding error: {error}")
    except psycopg2.OperationalError as error:
        print(f"Operational error: {error}")
    except psycopg2.DatabaseError as error:
        print(f"Database error: {error}")

    return None

def insert_data(connection, table, columns, values):
    ''' Insert data into a table'''
    try:
        cursor = connection.cursor()
        insert_query = sql.SQL("""INSERT INTO {} (
            {}) VALUES ({})""").format(
            sql.Identifier(table),
            sql.SQL(', ').join(map(sql.Identifier, columns)),
            sql.SQL(', ').join(map(sql.Literal, values))
        )
    except psycopg2.Error as error:
        print(f"Error creating the query: {error}")
        return None
    except psycopg2.DatabaseError as error:
        print(f"Database error: {error}")
        return None

    try:
        cursor.execute(insert_query)
        connection.commit()
        print("Data inserted successfully.")
    except psycopg2.Error as error:
        print(f"Error inserting data: {error}")
        return None
    except psycopg2.DatabaseError as error:
        print(f"Database error: {error}")
        return None
    finally:
        cursor.close()

    return True

# Example of use
if __name__ == "__main__":
    conn = create_connection()
    if conn:
        # Ejemplo de inserción de datos
        # insert_data(conn, 'mi_tabla', ['columna1', 'columna2'],
        # ['valor1', 'valor2'])
        conn.close()
