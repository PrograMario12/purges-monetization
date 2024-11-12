''' Window to generate reports '''

import locale
import tkinter as tk
from tkinter import ttk
from datetime import date
from PIL import Image, ImageTk
from tkcalendar import DateEntry
from .styles import apply_styles

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

class ReportWindow(tk.Toplevel):
    ''' Window to generate reports '''
    def __init__(self, parent, width=900, height=500):
        super().__init__(parent)
        self.setup_window(width, height)
        self.configure_grid_layout()
        self.initialize_configuration()
        self.create_top_frame()
        self.create_middle_frame()
        self.create_bottom_frame()
        self.set_icon("img/costos_purgas.ico")

    def setup_window(self, width, height):
        '''
        Setup window properties:
        - Set the window title to "Generar Reporte"
        - Set the window size to 900x500 pixels
        - Set the minimum window size to 900x500 pixels
        - Set the background color to BACKGROUND_COLOR
        '''
        self.title("Generar Reporte")
        self.geometry(f"{width}x{height}")
        self.minsize(width, height)
        self.configure(bg=BACKGROUND_COLOR)

    def configure_grid_layout(self):
        '''
        Setup window layout:
        - Configure the main window to have three rows and one column
        - The first row has a minimum size of 100 pixels and weight of 1
        - The second row has a weight of 2
        - The third row has a weight of 1
        '''
        self.columnconfigure(0, weight=1)
        row_configurations = [(0, 1, 100), (1, 2, None), (2, 1, None)]
        for row, weight, minsize in row_configurations:
            self.rowconfigure(row, weight=weight, minsize=minsize)

    def initialize_configuration(self):
        ''' Initialize configuration dictionary '''
        today = date.today()
        self.config = {
            'date_start': today,
            'date_end': today,
            'calendar_start': None,
            'calendar_end': None,
            'button_cancel': None,
            'generate_report': None
        }

    def set_icon(self, icon_path):
        ''' Set the window icon '''
        icon_image = Image.open(icon_path)
        icon = ImageTk.PhotoImage(icon_image)
        self.iconphoto(False, icon)

    def create_top_frame(self):
        ''' Create the top frame with date selection '''
        top_frame = ttk.Frame(self, style="TProject.TFrame", height=100)
        top_frame.grid(row=0, column=0, sticky="ns")
        top_frame.columnconfigure([0, 1, 2, 3], weight=1, minsize=100)
        top_frame.rowconfigure(0, weight=0, minsize=100)

        self.add_label(top_frame, "Fecha de inicio", 0, 0)
        self.add_label(top_frame, "Fecha de fin", 0, 2)

        locale.setlocale(locale.LC_TIME, 'es_ES')

        self.config['calendar_start'] = self.create_calendar(top_frame, 0, 1)
        self.config['calendar_end'] = self.create_calendar(top_frame, 0, 3)

    def add_label(self, parent, text, row, column):
        ''' Add a label to the specified parent '''
        label = ttk.Label(
            parent,
            text=text,
            style="TProject_Label_Title.TLabel"
        )
        label.grid(row=row, column=column, pady=20, padx=10)

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
        middle_frame = ttk.Frame(self, style="TProject.TFrame", height=300)
        middle_frame.grid(row=1, column=0, sticky="nsew")

        middle_frame.columnconfigure(0, weight=1)
        middle_frame.rowconfigure(0, weight=1, minsize=300)

        columns = ["ID", "Fecha", "Descripción", "Peso total", "Costo"]

        self.tree = ttk.Treeview(
            middle_frame,
            columns=columns,
            show="headings",
            selectmode="browse",
            height=10
        )
        for col in columns:
            self.tree.heading(col, text=col.replace("_", " ").title())
            self.tree.column(col, anchor=tk.CENTER, width=100)

        self.tree.column(2, width=250)
        self.tree.grid(row=0, column=0, sticky="nsew")

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

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

    def create_bottom_frame(self):
        ''' Create the bottom frame with the buttons '''
        bottom_frame = ttk.Frame(self, style="TProject.TFrame", height=100)
        bottom_frame.grid(row=2, column=0, sticky="nsew")

        bottom_frame.columnconfigure([0, 1], weight=1)
        bottom_frame.rowconfigure(0, weight=1, minsize=100)

        self.config['generate_report'] = self.add_button(
            bottom_frame, "Generar reporte", 0, 0)
        self.config['button_cancel'] = self.add_button(
            bottom_frame, "Cancelar", 0, 1)

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
            padx=10,
            pady=10,
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
    root = tk.Tk()
    root.title("QR Scan")
    root.geometry("200x200")
    apply_styles()

    report_window = ReportWindow(root)

    button = ttk.Button(
        root,
        text="Generar reporte",
        command=report_window.show,
        style="TProject.TButton"
    )
    button.pack(pady=20)

    root.mainloop()
