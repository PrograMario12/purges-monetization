"""Module for saving data to a file.
This module defines an abstract base class `DataSaver` for saving data
and a concrete implementation `ExcelSaver` for saving data to an Excel
file. The `ExcelSaver` class provides methods to prompt the user to
select a file path and save data to an Excel file.
Classes:
    DataSaver: Abstract base class for saving data.
    ExcelSaver: Concrete class for saving data to an Excel file.
Methods:
    DataSaver.ask_save_as_filename(self):
        Prompt the user to select a file path.
    DataSaver.save_data(self, data, file_path):
        Save data to a file.
    ExcelSaver.ask_save_as_filename(self):
        Prompt the user to select a file path to save the report as an
        Excel file.
    ExcelSaver.save_data(self, data, file_path):
        Save data to an Excel file.
    ExcelSaver.save_report_to_excel(self, data):
        Save the report to an Excel file by prompting the user to select
        a file path and then saving the data to the selected path.
"""
from abc import ABC, abstractmethod
from tkinter import filedialog
import datetime
import pandas as pd

class DataSaver(ABC):
    """Abstract base class for saving data.
    This class provides an interface for saving data to a file.
    Subclasses must implement the following abstract methods:
    Methods
    -------
    ask_save_as_filename():
        Prompt the user to select a file path where the data will be
        saved.
    save_data(data, file_path):
        Save the provided data to the specified file path.
    Attributes
    ----------
    None
    """
    @abstractmethod
    def ask_save_as_filename(self):
        """ Prompt the user to select a file path """

    @abstractmethod
    def save_data(self, data, file_path):
        """ Save data to a file """

class ExcelSaver(DataSaver):
    """ A class for saving data to an Excel file.
    Methods
    -------
    ask_save_as_filename():
        Prompts the user to select a file path to save the report as an
        Excel file.
    save_data(data, file_path):
        Saves the provided data to an Excel file at the specified file
        path.
    save_report_to_excel(data):
        Prompts the user for a file path and saves the provided data to
        an Excel file.
    """
    def ask_save_as_filename(self):
        """Prompt the user to select a file path to save the report as
        an Excel file.

        This method opens a file dialog that allows the user to choose a
        location and filename for saving a report. The default file
        extension is set to ".xlsx", and the dialog filters the file
        types to show only Excel files and all files.

        Returns:
            str: The selected file path where the report will be saved,
            or an empty string if the user cancels the dialog.
        """
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
            title="Guardar reporte como")
        return file_path

    def save_data(self, data, file_path):
        """Save data to an Excel file.

        Parameters:
        data (list or dict): The data to be saved. It can be a list of
        dictionaries or a dictionary of lists.
        file_path (str): The path where the Excel file will be saved.

        Returns:
        None
        """
        df = pd.DataFrame(data)

        df = self.normalize_date(df)

        df = self.add_columns_names(df)

        df.to_excel(file_path, index=False)

    def save_report_to_excel(self, data):
        """Save the report to an Excel file.

        Parameters:
        data (any): The data to be saved in the Excel file.

        Returns:
        None
        """
        file_path = self.ask_save_as_filename()
        self.save_data(data, file_path)

    def normalize_date(self, data):
        """Normalize the date in the third column to time format.

        Parameters:
        data (DataFrame): The DataFrame containing the data.

        Returns:
        DataFrame: The DataFrame with the third column converted to time format.
        """
        for column in data.columns:
            if pd.api.types.is_datetime64_any_dtype(data[column]):
                data[column] = data[column].apply(
                    lambda x: x.tz_localize(None) if isinstance(
                        x, pd.Timestamp) and x.tzinfo is not None else x)
            elif pd.api.types.is_timedelta64_dtype(data[column]):
                pass
            elif pd.api.types.is_object_dtype(data[column]):
                data[column] = data[column].apply(
                    lambda x: x.strftime('%H:%M:%S') if isinstance(
                        x, datetime.time) else x)

        return data

    def add_columns_names(self, data):
        """Add column names to the DataFrame.

        Parameters:
        data (DataFrame): The DataFrame containing the data.

        Returns:
        DataFrame: The DataFrame with column names added.
        """
        data.columns = [
            'ID', 'Fecha', 'Hora', 'Número de partes', 'Nombre de la pieza',
            'Estación', 'Nombre del operador', 'Peso bruto', 'Peso neto',
            'Costo']
        return data
