''' This module contains the queries for the database '''
import database

class Queries:
    ''' This class contains the queries for the database'''
    def __init__(self):
        self.db = database.DataBase()

    def get_price(self, material):
        ''' Get the price of a product '''
        query = f"""
        SELECT price, price_unit
          FROM table_resins
          WHERE material = '{material}'
        """

        print(query)
        self.db.create_connection()
        price = self.db.execute_query(query)
        self.db.close_connection()

        price = price[0][0] / price[0][1] if price else 0

        return price

    def get_cost_and_weight(self):
        ''' Get the cost and weight of a product '''
        query = """
        SELECT sum(cost), sum(gross_weight)
            FROM register_table
            WHERE date_register = current_date
        """
        print(query)
        self.db.create_connection()
        data = self.db.execute_query(query)
        self.db.close_connection()

        return data[0] if data else (0, 0)
