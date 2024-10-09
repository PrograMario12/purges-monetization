''' This module contains the queries for the database '''
import datetime
import database
import support

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

    def get_cost_wight_hour(self):
        ''' Get the cost and weight of a product '''

        query = """
        SELECT cost, gross_weight, hour_register
            FROM register_table
            WHERE date_register = current_date
        """
        self.db.create_connection()
        data_general = self.db.execute_query(query)
        self.db.close_connection()

        return data_general

class ProcessQueries:
    ''' This class is used to process the queries '''
    def __init__(self):
        self.query = Queries()

    def get_cost_and_weight(self):
        ''' Get the cost and weight of a product '''
        turns_init = {
            1: datetime.time(7, 0, 0),
            2: datetime.time(15, 0, 0),
            3: datetime.time(23, 0, 0)
        }
        turn = support.Support().get_turn()

        data_results = []
        data_results = self.query.get_cost_wight_hour()

         # Convertir las horas de los registros a offset-naive
        data_results = [(item[0], item[1], item[2].replace(tzinfo=None)) for item in data_results]

        cost = sum(item[0] for item in data_results)
        weight = sum(item[1] for item in data_results)

        if turn == 1:
            cost_turn = sum(item[0] for item in data_results
                            if item[2] >= turns_init[1]
                            and item[2] < turns_init[2])

            weight_turn = sum(item[1] for item in data_results
                              if item[2] >= turns_init[1]
                              and item[2] < turns_init[2])

        elif turn == 2:
            cost_turn = sum(item[0] for item in data_results
                            if item[2] >= turns_init[2]
                            and item[2] < turns_init[3])

            weight_turn = sum(item[1] for item in data_results
                              if item[2] >= turns_init[2]
                              and item[2] < turns_init[3])

        else:
            cost_turn = sum(item[0] for item in data_results
                            if item[2] >= turns_init[3]
                            or item[2] < turns_init[1])

            weight_turn = sum(item[1] for item in data_results
                              if item[2] >= turns_init[3]
                              or item[2] < turns_init[1])

        cost = round(cost, 2)
        weight = round(weight, 2)
        cost_turn = round(cost_turn, 2)
        weight_turn = round(weight_turn, 2)

        return cost, weight, cost_turn, weight_turn

if __name__ == "__main__":
    process_queries = ProcessQueries()
    cost_finally, weight_finally, cost_turn_finally, weight_turn_finally = (
        process_queries.get_cost_and_weight()
    )
    print(f"Costo total: {cost_finally}")
    print(f"Peso total: {weight_finally}")
    print(f"Costo por turno: {cost_turn_finally}")
    print(f"Peso por turno: {weight_turn_finally}")