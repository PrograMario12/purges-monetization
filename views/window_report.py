"""This module contains the ReportWindow class, which is responsible for
generating reports using the tkcalendar library.
The ReportWindow class creates a user interface with calendar widgets
to select date ranges and a table to display report data.
Classes:
    ReportWindow: A class that represents the report generation window.
Functions:
    __init__(self, parent, controller): Initializes the ReportWindow.
    initialize_configuration(self): Initializes the configuration
    dictionary with default values.
    create_top_frame(self): Creates the top frame containing calendar
    widgets and buttons.
    create_calendar(self, parent, row, column): Creates a DateEntry
    calendar widget.
    create_middle_frame(self): Creates the middle frame containing a
    table to display report data.
    add_button(self, parent, text, row, column): Adds a button to the
    specified parent widget.
    show_error_message(self, message): Displays an error message in a
    message box.
    show_askquestion(self, message): Displays a question message in a
    message box and returns the user's response.
    show_info_message(self, message): Displays an information message in
    a message box.
"""

import locale
import tkinter as tk
from tkinter import ttk
from datetime import date
from tkcalendar import DateEntry
from views.create_widgets import(
    GridConfigurator, FrameFactory, LabelFactory, ButtonFactory)
from views.config import BACKGROUND_COLOR, CALENDAR_OPTIONS

class ReportWindow(tk.Frame):
    ''' Window to generate reports '''
    def __init__(self, parent, controller):
        """
        Initialize the ReportWindow.

        :param parent: The parent widget.
        :param controller: The controller managing this window.
        """
        super().__init__(parent)
        self.controller = controller
        self.configure(bg=BACKGROUND_COLOR)

        self.grid_configurator = GridConfigurator()
        self.frame_factory = FrameFactory()
        self.label_factory = LabelFactory()
        self.button_factory = ButtonFactory()

        self.grid_configurator.configure(
            self, 2, 1, { 'row_weights': [1, 19], 'col_weights': [1]})

        self.initialize_configuration()
        self.create_top_frame()
        self.create_middle_frame()

    def initialize_configuration(self):
        """
        Initialize the configuration dictionary.
        """
        today = date.today()
        self.config = {
            'date_start': today,
            'date_end': today,
            'calendar_start': None,
            'calendar_end': None,
            'generate_report': None
        }

    def create_top_frame(self):
        """
        Create the top frame with the calendar widgets.
        """
        top_frame = self.frame_factory.create(
            self, "TFrame", { 'row': 0, 'column': 0}, pady=10)

        self.label_factory.create(
            top_frame, "Desde", "Project_Label_Title_2.TLabel",
            { 'row': 0, 'column': 0, 'padx': 20})

        self.label_factory.create(
            top_frame, "Hasta", "Project_Label_Title_2.TLabel",
            { 'row': 0, 'column': 2, 'padx': 20})

        locale.setlocale(locale.LC_TIME, 'es_ES')

        self.config['calendar_start'] = self.create_calendar(top_frame, 0, 1)
        self.config['calendar_end'] = self.create_calendar(top_frame, 0, 3)

        self.config['generate_report'] = self.button_factory.create(
            top_frame, {'text': 'Reporte SAP', 'style': 'TProject.TButton',
            'grid_options': {'row': 0, 'column': 5}})

        self.config['generate_normal_report'] = self.button_factory.create(
            top_frame, {'text': 'Reporte por pieza', 'style': 'TProject.TButton',
            'grid_options': {'row': 0, 'column': 4}})

    def create_calendar(self, parent, row, column):
        ''' Create a DateEntry calendar widget '''
        calendar = DateEntry(
            parent,
            **CALENDAR_OPTIONS,
            style="DataEntry.TCombobox",
            state='readonly'
        )
        calendar.grid(row=row, column=column)
        return calendar

    def create_middle_frame(self):
        ''' Create the middle frame with the table '''
        middle_frame = self.frame_factory.create(
            self, "TFrame", { 'row': 1, 'column': 0, 'sticky': "nsew" })

        self.grid_configurator.configure(
            middle_frame, 1, 1, { 'row_weights': [1], 'col_weights': [1]})

        columns = ["ID", "Fecha", "Descripción", "Peso total", "Costo"]

        self.tree = ttk.Treeview(
            middle_frame,
            columns=columns,
            show="headings",
            selectmode="browse",
        )
        for col in columns:
            self.tree.heading(col, text=col.replace("_", " ").title())

        self.tree.column(1, width=250)
        self.tree.grid(row=0, column=0, sticky="nsew")

        # Add a menu
        self.menu = tk.Menu(
            self,
            tearoff=0,
            bg="#E9ECEF",
            fg="black",
            activebackground="#285C6D",
            activeforeground="white",
            bd=1,
            relief="flat",
            font=("Arial", 10)
        )

        self.menu.add_command(label="Eliminar")

    def show_error_message(self, message):
        ''' Show an error message '''
        tk.messagebox.showerror("Registro no eliminado", message)

    def show_askquestion(self, message):
        ''' Show a question message '''
        return tk.messagebox.askquestion("Eliminar registro", message)

    def show_info_message(self, message):
        ''' Show an information message '''
        tk.messagebox.showinfo("Registro eliminado", message)

if __name__ == "__main__":
    pass
