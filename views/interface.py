''' This script shows how to display a video stream from OpenCV in a
Tkinter label. '''
import tkinter as tk
from tkinter import ttk
import scanner
import queries
from views import create_widgets

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
        self.scanner_var = scanner.Scanner(callback=self.update_report)
        self.cw = create_widgets.WidgetFactory()
        self.create_widgets()
        self.update_report()

    def create_widgets(self):
        ''' Create and pack the widgets '''
        grid_options = {
            'row_weights': [1, 19],
            'col_weights': [1],
        }
        self.cw.configure_grid(self, 2, 1, grid_options)

        ### Definition of widgets
        ## Definition principal panels
        bottom_panel = self.cw.create_frame(
            self,
            "TProject.TFrame",
            1,
            0,
            sticky="nsew"
        )

        top_panel = self.cw.create_frame(
            self,
            "TProject.TFrame",
            0,
            0,
            sticky="nsew",
            padx=200
        )

        self.cw.configure_grid(top_panel, 1, 1)

        def on_input_change(event, self) -> None:
            ''' Function to be called when input changes '''
            input_value: str = self.data_input.get()
            self.data_input.delete(0, tk.END)
            self.scanner_var.process_qr_code(input_value)

        self.data_input = self.cw.create_input(
            top_panel,
            "TProject_Label_Text.TEntry",
            {'column': 0, 'row': 0},
            placeholder="Escanea el QR",
            sticky="ew",
            padx=10,
        )
        self.data_input.bind("<Return>", lambda event: on_input_change(event, self))

        # Left frame
        self.cw.configure_grid(bottom_panel, 2, 2, { 'row_weights': [1, 9]})

        # Report section
        self.cw.create_label(
            bottom_panel,
            "Reportes",
            "Project_Label_Title.TLabel",
            { 'row': 0, 'column': 0, 'columnspan': 2 }
        )

        self.create_report_today(bottom_panel)

        self.create_report_turn(bottom_panel)

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

        self.cw.configure_grid(report_frame_turn, 3, 2, { 'row_weights': [1, 3, 3]})

        # Report section 2
        self.cw.create_label(
            report_frame_turn,
            "Turno actual",
            "Project_Label_Title_2.TLabel",
            { 'row': 0, 'column': 0, 'columnspan': 2 }
        )
        self.report_labels["peso_tirado_label_turn"] = self.cw.create_label(
            report_frame_turn,
            "Peso scrap (kg):",
            "TProject_Label_Title.TLabel",
            { 'row': 1, 'column': 0, 'padx': 10 }
        )
        self.report_labels["peso_tirado_value_turn"] = self.cw.create_label(
            report_frame_turn,
            str(self.report_data["peso_tirado_turn"]),
            "TProject_Label_Text.TLabel",
            { 'row': 2, 'column': 0, 'padx': 10, 'sticky': 'n' }
        )
        self.report_labels["costo_label_turn"] = self.cw.create_label(
            report_frame_turn,
            "Costo ($):",
            "TProject_Label_Title.TLabel",
            { 'row': 1, 'column': 1, 'padx': 10 }
        )
        self.report_labels["costo_value_turn"] = self.cw.create_label(
            report_frame_turn,
            str(self.report_data["costo_turn"]),
            "TProject_Label_Text.TLabel",
            { 'row': 2, 'column': 1, 'padx': 10, 'sticky': 'n' }
        )

    def create_report_today(self, parent):
        ''' Create the report labels '''
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

        self.cw.configure_grid(report_all_day_frame, 3, 2, { 'row_weights': [1, 3, 3]})

        self.cw.create_label(
            report_all_day_frame,
            "Hoy",
            "Project_Label_Title_2.TLabel",
            { 'row': 0, 'column': 0, 'columnspan': 2}
        )

        self.report_labels["peso_tirado_label"] = self.cw.create_label(
            report_all_day_frame,
            "Peso scrap (kg):",
            "Project_Label_Title_2.TLabel",
            { 'row': 1, 'column': 0, 'padx': 10 }
        )
        self.report_labels["peso_tirado_value"] = self.cw.create_label(
            report_all_day_frame,
            str(self.report_data["peso_tirado"]),
            "TProject_Label_Text.TLabel",
            { 'row': 2, 'column': 0, 'padx': 10, 'sticky': 'n' }
        )
        self.report_labels["costo_label"] = self.cw.create_label(
            report_all_day_frame,
            "Costo ($):",
            "Project_Label_Title_2.TLabel",
            { 'row': 1, 'column': 1, 'padx': 10 }
        )
        self.report_labels["costo_value"] = self.cw.create_label(
            report_all_day_frame,
            str(self.report_data["costo"]),
            "TProject_Label_Text.TLabel",
            { 'row': 2, 'column': 1, 'padx': 10, 'sticky': 'n' }
        )

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

# Example of use
if __name__ == "__main__":
    print("This script is not meant to be run directly.")
