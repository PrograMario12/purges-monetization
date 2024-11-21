'''
This file is used to import the interface class and create an
instance of it in the TaskView class
'''
import tkinter as tk
import logging
import os
from tkinter import PhotoImage
from tkinter import ttk, filedialog
import pandas as pd
from PIL import Image, ImageTk
import credentials
from . import create_widgets
from .interface import Interface
from .window_report import ReportWindow
from .view_statistics import ViewStatistics
from .view_validate import ViewValidate
from .styles import apply_styles

class TaskView(tk.Tk):
    ''' This class is used to create an instance of the interface class '''
    def __init__(self, *args, **kwargs):
        '''
        Initialize the TaskView class.

        Args:
            *args: Variable length argument list.
        icon_path = "img/costos_purgas.ico"
        if not os.path.exists(icon_path):
            raise FileNotFoundError(f"Icon file not found: {icon_path}")
        icon_image = Image.open(icon_path)

        Initializes the main window, sets the title, minimum size, and icon,
        creates the shared widgets and frames for different views.
        '''
        super().__init__(*args, **kwargs)
        self.title("Costo de purgas")
        self.attributes("-fullscreen", True)
        self.minsize(1000, 600)
        icon_image = Image.open("img/costos_purgas.ico")
        icon = ImageTk.PhotoImage(icon_image)
        self.iconphoto(False, icon)
        self.images = {}
        self.cw = create_widgets.WidgetFactory()
        for i, weight in enumerate([1, 25]):
            self.grid_rowconfigure(i, weight=weight)
        self.grid_columnconfigure(0, weight=1)
        apply_styles()

        # Global container for the views
        self.shared_frame = ttk.Frame(self, style="TProjectHeader.TFrame", height=100)
        self.shared_frame.grid(row=0, column=0, sticky="nsew")

        # Container for the views
        container = ttk.Frame(self)
        container.grid(row=1, column=0, sticky="nsew")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.create_shared_widgets()
        self.frames = {}

        for F in (Interface, ReportWindow, ViewValidate):
            page_name = F.__name__
            try:
                frame = F(parent=container, controller=self)
                self.frames[page_name] = frame
                frame.grid(row=0, column=0, sticky="nsew")
            except Exception as e:
                logging.error("Failed to initialize frame %s: %s", page_name, e)

        self.show_frame("Interface")

    def create_shared_widgets(self):
        ''' Create the shared widgets for the views '''
        self.shared_frame.grid_rowconfigure(0, weight=1)
        for i, weight in enumerate([25, 1, 1, 1, 1 ,1]):
            self.shared_frame.grid_columnconfigure(i, weight=weight)

        logo_path = os.getenv("LOGO_PATH", "./img/magna-logo.png")
        if not os.path.exists(logo_path):
            raise FileNotFoundError(f"Logo file not found: {logo_path}")
        pil_img = Image.open(logo_path)
        width, height = pil_img.size
        new_height = 100
        new_width = int((new_height / height) * width)
        pil_img = pil_img.resize((new_width, new_height), Image.LANCZOS)
        self.images["logo"] = ImageTk.PhotoImage(pil_img)
        image_label = self.cw.create_label(
            self.shared_frame,
            "",
            "TProjectHeader.TLabel",
            {'row': 0, 'column': 0, 'sticky': 'nsew'}
        )
        image_label.config(image=self.images["logo"])
        image_label.image = self.images["logo"]

        self.buttons = {}

        config_grid = {
            'row': 0,
            'column': 1,
            'pady': 20,
        }
        home_image = Image.open("./img/home.png")
        home_image = home_image.resize((40, 40), Image.LANCZOS)
        self.images["home"] = ImageTk.PhotoImage(home_image)
        kwargs = {
            'parent': self.shared_frame,
            'style': "TProject.TButton",
            'command': lambda: self.show_frame("Interface"),
            'icon': self.images["home"],
            'grid_options': config_grid
        }
        self.buttons["home"] = self.cw.create_button(**kwargs)

        config_grid = {
            'row' : 0,
            'column' : 2,
            'pady': 20,
        }
        report_image = Image.open("./img/report.png")
        report_image = report_image.resize((40, 40), Image.LANCZOS)
        self.images["report"] = ImageTk.PhotoImage(report_image)
        kwargs = {
            'parent': self.shared_frame,
            'style': "TProject.TButton",
            'icon': self.images["report"],
            'grid_options': config_grid
        }
        self.buttons["report"] = self.cw.create_button(**kwargs)

        config_grid = {
            'row' : 0,
            'column' : 3,
            'pady': 20,
        }
        validate_image = Image.open("./img/validate.png")
        validate_image = validate_image.resize((40, 40), Image.LANCZOS)
        self.images["validate"] = ImageTk.PhotoImage(validate_image)
        kwargs = {
            'parent': self.shared_frame,
            'style': "TProject.TButton",
            'command': lambda: self.show_frame("ViewValidate"),
            'icon': self.images["validate"],
            'grid_options': config_grid
        }
        self.buttons["validate"] = self.cw.create_button(**kwargs)

        config_grid = {
            'row' : 0,
            'column' : 4,
            'pady': 20,
        }
        report_image = Image.open("./img/statistics.png")
        report_image = report_image.resize((40, 40), Image.LANCZOS)
        self.images["statistics"] = ImageTk.PhotoImage(report_image)
        kwargs = {
            'parent': self.shared_frame,
            'style': "TProject.TButton",
            'command': lambda: os.system("start " + credentials.POWER_BI),
            'icon': self.images["statistics"],
            'grid_options': config_grid
        }
        self.buttons["statistics"] = self.cw.create_button(**kwargs)

        config_grid = {
            'row' : 0,
            'column' : 5,
            'pady': 20
        }
        report_image = Image.open("./img/close.png")
        report_image = report_image.resize((40, 40), Image.LANCZOS)
        self.images["close"] = ImageTk.PhotoImage(report_image)
        kwargs = {
            'parent': self.shared_frame,
            'style': "TProject.TButton",
            'command': self.quit,
            'icon': self.images["close"],
            'grid_options': config_grid
        }
        self.buttons["close"] = self.cw.create_button(**kwargs)

    def show_frame(self, page_name):
        ''' Show a frame for the given page name '''
        frame = self.frames[page_name]
        frame.tkraise()

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
