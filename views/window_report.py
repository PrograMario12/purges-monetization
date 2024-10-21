''' Window to generate reports '''

import locale
import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from .styles import apply_styles
from tkinter import filedialog, messagebox

class ReportWindow:
    ''' This class creates a window to generate reports '''
    def __init__(self, parent):
        ''' Initialize the ReportWindow class '''
        self.parent = parent
        self.window = None
        self.columns = (
            "Fecha",
            "Nombre de la pieza",
            "Peso neto",
            "Costo")
        self.tree = None
        self.button_generate_report = None
        self.show()

    def show(self):
        ''' Show the window '''
        self.window = tk.Toplevel(self.parent)
        self.window.title("Generar Reporte")
        self.window.geometry("800x500")
        self.window.minsize(800, 500)
        self.window.configure(bg="#F9F9F9")
        style = ttk.Style()
        style.theme_use("default")
        style.configure("TProject.TFrame", background="#F9F9F9", height=50)
        style.configure(
                        "TProject_Label_Title.TLabel",
                        background="#F9F9F9",
                        font=("Arial", 16, "bold"),
                        foreground="#212529"
                    )

        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1, minsize=100)
        self.window.rowconfigure(1, weight=2)
        self.window.rowconfigure(2, weight=1)

        self.create_top_frame()
        self.create_middle_frame()
        self.create_bottom_frame()

    def create_top_frame(self):
        ''' Create the top frame with date selection '''
        top_frame = ttk.Frame(self.window, style="TProject.TFrame", height=100)
        top_frame.grid(row=0, column=0, sticky="ns")
        top_frame.columnconfigure([0, 1, 2, 3], weight=1, minsize=100)
        top_frame.rowconfigure(0, weight=0, minsize=100)


        label = ttk.Label(
            top_frame,
            text="Fecha de inicio",
            style="TProject_Label_Title.TLabel"
        )
        label.grid(row=0, column=0, pady=20, padx=10)

        label = ttk.Label(
            top_frame,
            text="Fecha de fin",
            style="TProject_Label_Title.TLabel"
        )
        label.grid(row=0, column=2, pady=20, padx=10)

        locale.setlocale(locale.LC_TIME, 'es_ES')

        calendar_options = {
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
            'locale': 'es_ES'
        }

        for i in range(2):
            calendar = DateEntry(top_frame, **calendar_options)
            calendar.grid(row=0, column=i*2 + 1)


    def create_middle_frame(self):
        ''' Create the middle frame with the table '''
        middle_frame = ttk.Frame(
                self.window,
                style="TProject.TFrame",height=300
            )
        middle_frame.grid(row=1, column=0, sticky="nsew")

        middle_frame.columnconfigure(0, weight=1)
        middle_frame.rowconfigure(0, weight=1, minsize=300)

        self.tree = ttk.Treeview(
                middle_frame,
                columns=self.columns,
                show="headings",
                selectmode="browse",
                height=10
            )
        for col in self.columns:
            self.tree.heading(col, text=col.replace("_", " ").title())
            self.tree.column(col, anchor=tk.CENTER, width=100)

        self.tree.column(1, width=250)
        self.tree.grid(row=0, column=0, sticky="nsew")

        self.window.grid_rowconfigure(1, weight=1)
        self.window.grid_columnconfigure(0, weight=1)

    def create_bottom_frame(self):
        ''' Create the bottom frame with the buttons '''
        bottom_frame = ttk.Frame(
                self.window,
                style="TProject.TFrame",
                height=100
            )
        bottom_frame.grid(row=2, column=0, sticky="nsew")

        bottom_frame.columnconfigure([0, 1], weight=1)
        bottom_frame.rowconfigure(0, weight=1, minsize=100)

        self.button_generate_report = ttk.Button(
            bottom_frame,
            text="Generar reporte",
            style="TProject.TButton",
            )
        self.button_generate_report.grid(row=0, column=0, padx=10, pady=10, sticky="we")

        button_cancel = ttk.Button(
                bottom_frame,
                text="Cancelar",
                style="TProject.TButton",
                command=self.window.destroy
            )
        button_cancel.grid(row=0, column=1, padx=10, pady=10, sticky="we")

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
