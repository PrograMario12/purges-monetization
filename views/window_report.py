''' Window to generate reports '''

import locale
import tkinter as tk
from tkinter import ttk
from datetime import date
from tkcalendar import DateEntry
from views import create_widgets

# Constantes para configuraciones repetidas
BACKGROUND_COLOR = "#F9F9F9"
CALENDAR_OPTIONS = {
    'selectmode': 'day',
    'font': ("Arial", 16),
    'background': "#E9ECEF",
    'foreground': "black",
    'selectbackground': "#285C6D",
    'selectforeground': "white",
    'bordercolor': "white",
    'normalbackground': "#E9ECEF",
    'normalforeground': "black",
    'weekendbackground': "#B0CCD5",
    'headersbackground': "#285C6D",
    'headersforeground': "white",
    'othermonthbackground': '#4298B5',
    'othermonthwebackground': '#B0CCD5',
    'locale': 'es_ES',
}

class ReportWindow(tk.Frame):
    ''' Window to generate reports '''
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg=BACKGROUND_COLOR)
        self.cw = create_widgets.WidgetFactory()

        self.cw.configure_grid(self, 2, 1, {
            'row_weights': [1, 19],
            'col_weights': [1]})

        self.initialize_configuration()
        self.create_top_frame()
        self.create_middle_frame()

    def initialize_configuration(self):
        ''' Initialize configuration dictionary '''
        today = date.today()
        self.config = {
            'date_start': today,
            'date_end': today,
            'calendar_start': None,
            'calendar_end': None,
            'generate_report': None
        }


    def create_top_frame(self):
        ''' Create the top frame with date selection '''
        top_frame = self.cw.create_frame(
            self,
            "TFrame",
            0,
            0,
            pady=10
        )

        self.cw.create_label(
            top_frame,
            "Desde",
            "Project_Label_Title_2.TLabel",
            { 'row': 0, 'column': 0, 'padx': 20})

        self.cw.create_label(
            top_frame,
            "Hasta",
            "Project_Label_Title_2.TLabel",
            { 'row': 0, 'column': 2, 'padx': 20})

        locale.setlocale(locale.LC_TIME, 'es_ES')

        self.config['calendar_start'] = self.create_calendar(top_frame, 0, 1)
        self.config['calendar_end'] = self.create_calendar(top_frame, 0, 3)

        self.config['generate_report'] = self.add_button(
            top_frame, "Generar reporte", 0, 4)

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
        middle_frame = self.cw.create_frame(
            self,
            "Test.TFrame",
            1,
            0,
            sticky="nsew"
        )

        self.cw.configure_grid(
                middle_frame,
                1,
                1,
                { 'row_weights': [1], 'col_weights': [1]}
            )

        columns = ["ID", "Fecha", "Descripción", "Peso total", "Costo"]

        self.tree = ttk.Treeview(
            middle_frame,
            columns=columns,
            show="headings",
            selectmode="browse",
        )
        for col in columns:
            self.tree.heading(col, text=col.replace("_", " ").title())

        self.tree.column(2, width=250)
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

    def add_button(self, parent, text, row, column):
        ''' Add a button to the specified parent '''
        button_result = ttk.Button(
            parent,
            text=text,
            style="TProject.TButton"
        )
        button_result.grid(
            row=row,
            column=column,
            sticky="we")
        return button_result

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
