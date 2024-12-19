"""
This module defines the Interface class, which creates the graphical
user interface (GUI) for the application using the Tkinter library. The
interface includes input fields, labels, and graphical representations
of data such as bar and line charts. The Interface class is responsible
for initializing the GUI components, handling user input, and updating
the displayed data based on queries and scanner input.

Classes:
    Interface: A class that creates and manages the GUI of the application.

Functions:
    create_widgets: Creates and packs the widgets in the GUI.
    create_report_turn: Creates the report labels for the current turn.
    create_report_today: Creates the report labels for the current day.
    update_report: Updates the report with new values.
    create_graphics: Creates the graphical representations of data.
"""

import logging
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import scanner
import queries
from views.create_widgets import (
    ButtonFactory, LabelFactory, InputFactory, FrameFactory, GridConfigurator
)

class Interface(tk.Frame):
    ''' This class creates the graphical user interface of the
    application. '''

    def __init__(self, parent, controller):
        ''' Initialize the class '''
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="#F9F9F9")

        self.images = {}
        self.query = queries.ProcessQueries()
        self.report_data = {
            "peso_tirado": 0.0,
            "costo": 0.0,
            "peso_tirado_turn": 0.0,
            "costo_turn": 0.0
        }
        self.report_labels = {}
        self.ax_bar = None
        self.scanner_var = scanner.Scanner(callback=self.update_report)

        self.button_factory = ButtonFactory()
        self.label_factory = LabelFactory()
        self.input_factory = InputFactory()
        self.frame_factory = FrameFactory()
        self.grid_configurator = GridConfigurator()

        self.create_widgets()
        self.update_report()

    def create_widgets(self):
        ''' Create and pack the widgets '''
        grid_options = {
            'row_weights': [3, 8],
            'col_weights': [1],
        }
        self.grid_configurator.configure(self, 2, 1, grid_options)

        ### Definition of widgets
        ## Definition principal panels
        bottom_panel = self.frame_factory.create(
            self, "TProject.TFrame", {'row': 1, 'column': 0}, sticky="nsew")

        top_panel = self.frame_factory.create(
            self, "TProject.TFrame", {'row': 0, 'column': 0}, sticky="nsew",
            padx=200)

        self.grid_configurator.configure(top_panel, 1, 1)


        def on_input_change(event, self) -> None:
            ''' Function to be called when input changes '''
            input_value: str = self.data_input.get()
            self.data_input.delete(0, tk.END)
            self.scanner_var.process_qr_code(input_value)

        self.data_input = self.input_factory.create(
            top_panel, "TProject_Label_Text.TEntry", {'column': 0, 'row': 0},
            placeholder="Escanea el QR", sticky="ew", padx=10)
        self.data_input.bind(
            "<Return>", lambda event: on_input_change(event, self))

        # Left frame
        self.grid_configurator.configure(
            bottom_panel, 2, 2, {'row_weights': [1, 9]})

        # Report section
        self.label_factory.create(
            bottom_panel, "Reportes", "Project_Label_Title.TLabel", {'row': 0,
            'column': 0, 'columnspan': 2})

        self.create_report_today(bottom_panel)

        self.create_report_turn(bottom_panel)

        # graphic_frame = self.cw.create_frame(
        #     self,
        #     "TProject.TFrame",
        #     2,
        #     0,
        #     sticky="ns"
        # )
        # self.create_graphics(graphic_frame)

    def create_report_turn(self, parent):
        ''' Create the report labels '''
        report_frame_turn = ttk.Frame(
            parent,
            style="TProject.TFrame"
        )
        report_frame_turn.grid(
            row=1,
            column=1,
            sticky="nsew",
            pady=10
        )

        self.grid_configurator.configure(report_frame_turn, 3, 2,
            { 'row_weights': [1, 3, 3] })

        # Report section 2
        self.label_factory.create(
            report_frame_turn, "Reporte de turno",
            "Project_Label_Title_2.TLabel",{ 'row': 0, 'column': 0,
            'columnspan': 2 })
        self.report_labels[
            "peso_tirado_label_turn"] = self.label_factory.create(
            report_frame_turn, "Peso scrap (kg):",
            "TProject_Label_Title.TLabel", { 'row': 1, 'column': 0, 'padx': 10 })

        self.report_labels["peso_tirado_value_turn"] = self.label_factory.create(
            report_frame_turn, str(self.report_data["peso_tirado_turn"]),
            "TProject_Label_Text.TLabel", { 'row': 2, 'column': 0, 'padx': 10,
            'sticky': 'n' })

        self.report_labels["costo_label_turn"] = self.label_factory.create(
            report_frame_turn, "Costo ($):","TProject_Label_Title.TLabel",
            { 'row': 1, 'column': 1, 'padx': 10 })

        self.report_labels["costo_value_turn"] = self.label_factory.create(
            report_frame_turn, str(self.report_data["costo_turn"]),
            "TProject_Label_Text.TLabel", { 'row': 2, 'column': 1, 'padx': 10,
            'sticky': 'n' })

    def create_report_today(self, parent):
        """
        Create the report labels for today's data.

        This method creates and configures the labels that display the
        )
        report_all_day_frame.grid(
            labels will be placed.
        """

        report_all_day_frame = ttk.Frame(
            parent,
            style="TProject.TFrame"
        )

        report_all_day_frame.grid(
            row=1,
            column=0,
            sticky="nsew",
            pady=10
        )

        self.grid_configurator.configure(report_all_day_frame, 3, 2, 
            {'row_weights': [1, 3, 3] })

        self.label_factory.create(
            report_all_day_frame, "Hoy", "Project_Label_Title_2.TLabel",
            { 'row': 0, 'column': 0, 'columnspan': 2}
        )

        self.report_labels["peso_tirado_label"] = self.label_factory.create(
            report_all_day_frame, "Peso scrap (kg):",
            "TProject_Label_Title_2.TLabel", { 'row': 1, 'column': 0, 'padx': 10 }
        )

        self.report_labels["peso_tirado_value"] = self.label_factory.create(
            report_all_day_frame, str(self.report_data["peso_tirado"]),
            "TProject_Label_Text.TLabel", { 'row': 2, 'column': 0, 'padx': 10,
            'sticky': 'n' }
        )

        self.report_labels["costo_label"] = self.label_factory.create(
            report_all_day_frame, "Costo ($):", "Project_Label_Title_2.TLabel",
            { 'row': 1, 'column': 1, 'padx': 10 })

        self.report_labels["costo_value"] = self.label_factory.create(
            report_all_day_frame, str(self.report_data["costo"]),
            "TProject_Label_Text.TLabel", { 'row': 2, 'column': 1, 'padx': 10,
            'sticky': 'n' })

    def update_report(self):
        ''' Update the report with new values '''
        print("Updating report")

        costo, peso_tirado, cost_turn, weight_turn = (
            self.query.get_cost_and_weight()
        )

        costo = costo or 0.0
        peso_tirado = peso_tirado or 0.0
        cost_turn = cost_turn or 0.0
        weight_turn = weight_turn or 0.0

        self.report_data["peso_tirado"] = round(peso_tirado, 2)
        self.report_data["costo"] = round(costo, 2)
        self.report_data["peso_tirado_turn"] = round(weight_turn, 2)
        self.report_data["costo_turn"] = round(cost_turn, 2)
        self.report_labels["peso_tirado_value"].config(text=f"""
                {self.report_data['peso_tirado']:.2f}"""
            )
        self.report_labels["costo_value"].config(text=f"""
                {self.report_data['costo']:.2f}"""
            )
        self.report_labels["peso_tirado_value_turn"].config(text=f"""
                {self.report_data['peso_tirado_turn']:.2f}"""
            )
        self.report_labels["costo_value_turn"].config(text=f"""
                {self.report_data['costo_turn']:.2f}"""
            )

        # self.ax_bar.clear()
        # self.ax_bar.bar(
        #     ['Peso', 'Costo'],
        #     [self.report_data['peso_tirado'], self.report_data['costo']],
        #     color=['blue', 'green']
        # )

    def create_graphics(self, parent):
        ''' Create the graphics '''
        fig_bar = Figure(figsize=(5, 4), dpi=100)
        self.ax_bar = fig_bar.add_subplot(111)
        categories = ['Peso', 'Costo']
        values = [self.report_data['peso_tirado'], self.report_data['costo']]
        logging.basicConfig(level=logging.INFO)
        logging.info(values)
        self.ax_bar.bar(categories, values, color=['blue', 'green'])
        self.ax_bar.set_title("Peso y Costo")
        self.ax_bar.set_ylabel("Valores")

        canvas_bar = FigureCanvasTkAgg(fig_bar, master=parent)
        canvas_bar.draw()
        canvas_bar.get_tk_widget().grid(row=0, column=0)

        fig_line = Figure(figsize=(5, 4), dpi=100)
        ax_line = fig_line.add_subplot(111)
        x_values = list(range(10))
        y_values = [i**2 for i in x_values]
        ax_line.plot(x_values, y_values, marker='o', linestyle='-', color='r')
        ax_line.set_title("Tendencia")
        ax_line.set_xlabel("X")
        ax_line.set_ylabel("Y")

        canvas_line = FigureCanvasTkAgg(fig_line, master=parent)
        canvas_line.draw()
        canvas_line.get_tk_widget().grid(row=0, column=1)

if __name__ == "__main__":
    print("This script is not meant to be run directly.")
