'''
This file is used to import the interface class and create an
instance of it in the TaskView class
'''
import csv
from tkinter import filedialog
import credentials
from .interface import Interface
from .window_report import ReportWindow

class TaskView:
    ''' This class is used to create an instance of the interface class '''
    def __init__(self, root):
        self.root = root
        self.interface = Interface(self.root)
        self.report_window_instance = None

        if (self.report_window_instance is None or
            not self.report_window_instance.winfo_exists()):
            print("Creating new report window")
            self.report_window_instance = ReportWindow(self.root)
        else:
            self.report_window_instance.lift()

    def ask_save_as_filename(self):
        ''' Ask the user to save a file '''
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Guardar reporte como"
        )
        return file_path

    def save_report_to_csv(self, data, file_path):
        ''' Save the report to a CSV file '''
        with open(file_path, "w", newline="", encoding="utf-8-sig") as file:
            writer = csv.writer(file)
            writer.writerow([
                "Item",
                "Plant",
                "Número de parte",
                "Cantidad",
                "Locación",
                "Código",
                "Centro de costos",
                "G/L Account"
            ])

            i = 1
            for row in data:
                writer.writerow([
                    i,
                    credentials.ITEM_CONSTANT,
                    row[0],
                    row[1],
                    "0700",
                    "1136",
                    "31100Oh541",
                    "3031220000"
                ])
                i += 1

if __name__ == "__main__":
    print("This script is part of the TaskView module and should not be run directly.")
