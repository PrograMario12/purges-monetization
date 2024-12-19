"""
This module defines the ViewValidate class, which is a Tkinter Frame
used to validate user input through a QR code.
The class is responsible for creating and configuring the layout of the
validation view, including a top frame for QR code input and an
information frame to display instructions to the user.
Classes:
    ViewValidate: A Tkinter Frame subclass that sets up the user
    interface for QR code validation.
Methods:
    + __init__(self, parent, controller): Initializes the ViewValidate
    frame with the given parent and controller.
    + create_top_frame(self): Creates the top frame containing the QR
    code input field.
    + create_information_frame(self): Creates the information frame
    displaying instructions to the user.
"""

import tkinter as tk
from views.create_widgets import (
    GridConfigurator, FrameFactory, InputFactory, LabelFactory
)

class ViewValidate(tk.Frame):
    ''' Class to validate the user '''
    def __init__(self, parent, controller):
        ''' Initialize the class '''
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="#F9F9F9")
        self.grid_configurator = GridConfigurator()
        self.factory_panel = FrameFactory()
        self.factory_input = InputFactory()
        self.factory_label = LabelFactory()

        self.grid_configurator.configure(self, 2, 1, {
            'row_weights': [1, 9], 'col_weights': [1]})

        self.create_top_frame()
        self.create_information_frame()

    def create_top_frame(self):
        ''' Create the top frame with date selection '''
        top_panel = self.factory_panel.create(
            self, "TProject.TFrame", { 'row': 0, 'column': 0 }, padx=200,
            sticky="ew")

        self.grid_configurator.configure(top_panel, 1, 1)

        self.input_qr = self.factory_input.create(
            top_panel, "Project.TEntry", { 'row': 0, 'column': 0, 'padx': 20,
            'pady': 20, 'sticky': 'nsew'}, "Escanea tu QR aquí")

    def create_information_frame(self):
        ''' Create the top frame with date selection '''
        information_panel = self.factory_panel.create(
            self, "TProject.TFrame", { 'row': 1, 'column': 0 }, sticky="nsew")

        self.grid_configurator.configure(information_panel, 1, 1)

        self.information = self.factory_label.create(
            information_panel, "Escanea tu QR para validar que está registrado",
            "TProject_Label_Text.TLabel", { 'row': 0, 'column': 0, 'padx': 20,
            'pady': 20, 'sticky': 'n'})
