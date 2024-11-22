''' This module is responsible for the view of the validation of the user '''

import tkinter as tk
from views import create_widgets

class ViewValidate(tk.Frame):
    ''' Class to validate the user '''
    def __init__(self, parent, controller):
        ''' Initialize the class '''
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="#F9F9F9")
        self.cw = create_widgets.WidgetFactory()

        self.cw.configure_grid(self, 2, 1, {
            'row_weights': [1, 9],
            'col_weights': [1]})

        self.create_top_frame()
        self.create_information_frame()

    def create_top_frame(self):
        ''' Create the top frame with date selection '''
        top_panel = self.cw.create_frame(
            self,
            "TProject.TFrame",
            0,
            0,
            sticky="ew",
            padx=200
        )

        self.cw.configure_grid(top_panel, 1, 1)

        self.input_qr = self.cw.create_input(
            top_panel,
            "Project.TEntry",
            { 'row': 0, 'column': 0, 'padx': 20, 'pady': 20, 'sticky': 'nsew'},
            "Escanea tu QR aquí",
        )

    def create_information_frame(self):
        ''' Create the top frame with date selection '''
        information_panel = self.cw.create_frame(
            self,
            "TProject.TFrame",
            1,
            0,
            sticky="nsew"
        )

        self.cw.configure_grid(information_panel, 1, 1)

        self.information = self.cw.create_label(
            information_panel,
            "Escanea tu QR para validar que está registrado",
            "TProject_Label_Text.TLabel",
            { 'row': 0, 'column': 0, 'padx': 20, 'pady': 20, 'sticky': 'n'}
        )
