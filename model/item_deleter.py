"""
This module is responsible for deleting an item from the database
"""
class ItemDeleter:
    """
    This class is used to delete an item from the database
    """
    def __init__(self, database):
        """
        Initialize the ItemDeleter class.

        Parameters:
        database (Database): The database connection object used to
        execute delete queries.
        """
        self.database = database

    def delete_item(self, item_id):
        ''' Delete an item from the database '''

        self.database.create_connection()
        query = f"""
            DELETE FROM register_table WHERE id_register = {item_id}
        """
        self.database.execute_query_to_delete(query)
        self.database.close_connection()
