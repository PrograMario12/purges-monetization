'''
This file is used to import the interface class and create an
instance of it in the TaskView class
'''
import logging
from tkinter import filedialog
import pandas as pd
import credentials
from .interface import Interface
from .window_report import ReportWindow

class TaskView:
    ''' This class is used to create an instance of the interface class '''
    def __init__(self, root):
        self.root = root
        self.interface = Interface(self.root)
        self.report_window_instance = None

    def show_window_report(self):
        ''' Show the report window '''
        if (not self.report_window_instance
            or not self.report_window_instance.winfo_exists()):
            print("Creating new report window")
            self.report_window_instance = ReportWindow(self.root)
        else:
            self.report_window_instance.lift()
            logging.info("Creating new report window")

    def ask_save_as_filename(self):
        '''
        Prompt the user to select a file path to save the report as an 
        Excel file
        '''
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
            title="Guardar reporte como"
        )
        return file_path

    def save_report_to_excel(self, data, file_path):
        ''' Save the report to an Excel file '''
        df = pd.DataFrame(data, columns=[
            "Número de parte",
            "Cantidad"
        ])
        df.insert(0, "Item", range(1, len(df) + 1))
        plant_value = getattr(credentials, 'ITEM_CONSTANT', 'default_value')
        df.insert(1, "Plant", plant_value)
        df["Código"] = "1136"
        df["Centro de costos"] = "31100Oh541"
        df["G/L Account"] = "3031220000"

        df.to_excel(file_path, index=False)

if __name__ == "__main__":
    print("""This script is part of the TaskView module and should not be run
           directly.""")
