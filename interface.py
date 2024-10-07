''' This module contains the Interface class, which is responsible for
 creating the graphical user interface of the application. '''

import tkinter as tk
import scanner

class Interface:
    ''' This class creates the graphical user interface of the application. '''

    WINDOW_TITLE = "Monetización de purgas"
    LABEL_TEXT = "Escanear códigos"
    LABEL_FONT = ("Arial", 18)
    BUTTON_TEXT = "Iniciar escaneo"

    def __init__(self):
        ''' Initialize the Interface class '''
        self.sc = scanner.Scanner()
        self.create_window()
        self.create_widgets()

    def create_window(self):
        ''' Create the main application window '''
        self.window = tk.Tk()
        self.window.title(self.WINDOW_TITLE)
        self.window.state('zoomed')

    def create_widgets(self):
        ''' Create and pack the widgets '''
        self.label = tk.Label(self.window, text=self.LABEL_TEXT, font=self.LABEL_FONT)
        self.label.pack(pady=10)

        self.button_scanner = tk.Button(
            self.window, text=self.BUTTON_TEXT, command=self.sc.read_qr_code
        )
        self.button_scanner.pack()

    def run(self):
        ''' Run the graphical user interface '''
        self.window.mainloop()

# Example of use
if __name__ == "__main__":
    interface = Interface()
    interface.run()
