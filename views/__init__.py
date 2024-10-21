''' This file is used to import the interface class and create an
instance of it in the TaskView class '''
import csv
import tkinter as tk
from tkinter import filedialog
from .interface import Interface
from .window_report import ReportWindow

class TaskView:
    ''' This class is used to create an instance of the interface class '''
    def __init__(self, root):
        self.root = root
        self.interface = Interface(self.root)
        self.report_window_instance = None

    def show_window_report(self):
        ''' Show the window report '''
        self.report_window_instance = ReportWindow(self.root)

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
        with open(file_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["data_register, name_piece, gross_weight, cost"])
            for row in data:
                writer.writerow(row)

if __name__ == "__main__":
    print("This script is not meant to be run directly.")
