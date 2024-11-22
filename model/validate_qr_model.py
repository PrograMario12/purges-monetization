''' This module is used to validate the QR code. '''

from . import database_model

class ValidateQrModel:
    ''' This class is used to validate the QR code. '''
    def __init__(self, qr_model):
        ''' Initialize the class. '''
        self.date = qr_model[0]
        self.time = qr_model[1]
        self.number_of_part = qr_model[2]

        self.db = database_model.DatabaseModel()

    def validate(self):
        ''' Validate the QR code. '''
        self.db.create_connection()

        if self.db.connection:
            query = f"""
                SELECT
                    id_register,
                    date_register,
                    name_piece,
                    gross_weight,
                    cost
                FROM register_table
                WHERE date_register = '{self.date}'
                AND hour_register = '{self.time}'
                AND number_of_part = '{self.number_of_part}'
            """
            data = self.db.execute_query(query)
            self.db.close_connection()
            return data
