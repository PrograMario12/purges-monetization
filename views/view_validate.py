''' This module is responsible for the view of the validation of the user '''

import tkinter as tk
from views import create_widgets

class ViewValidate(tk.Frame):
    ''' Class to validate the user '''
    def __init__(self, parent, controller):
        ''' Initialize the class '''
        super().__init__(parent)
        self.controller = controller
        self.cw = create_widgets.WidgetFactory()

        self.cw.create_label(
            self,
            "Ingrese su usuario y contraseña",
            "Project_Label_Title.TLabel",
            { 'row': 0, 'column': 0, 'padx': 20, 'pady': 20})
