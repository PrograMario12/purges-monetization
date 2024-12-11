''' This module is the model of the task. It contains the queries and
support classes. '''

import tkinter as tk
from model import database_model
from . import validate_qr_model
from .date_validation import DateValidator
from .item_deleter import ItemDeleter
from .report_fetcher import ReportFetcher
from .qr_validator import QRValidator

class Model:
    ''' This class is the model'''
    def __init__(self):
        ''' Initialize the class'''
        self.database = database_model.DatabaseModel()
        self.date_validation = DateValidator()
        self.item_deleter = ItemDeleter(self.database)
        self.report_fetcher = ReportFetcher(self.database)
        self.qr_validator = QRValidator(validate_qr_model.ValidateQrModel, self.database)

# Example of use
if __name__ == "__main__":
    pass
