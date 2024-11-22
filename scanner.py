''' This module allows reading QR codes from the computer's camera.'''

import tkinter as tk
from tkinter import ttk
import database
import queries
from views import window_no_material

class Scanner:
    ''' This class allows reading QR codes from the computer's camera'''

    def __init__(self, callback=None):
        ''' Initialize the Scanner class '''
        self.db = database.DataBase()
        self.db.create_connection()
        self.query = queries.Queries()
        self.callback = callback

    def process_qr_code(self, data):
        ''' This function processes the data read from a QR code.'''
        processed_data = self.add_price(self.get_values(data))
        try:
            if processed_data[2] == "":
                window_no_material.show_no_material_message()
                return
        except IndexError:
            window_no_material.show_no_material_message()
            return
        self.insert_data(processed_data)
        self.show_message(processed_data)
        if self.callback:
            self.callback()

    def insert_data(self, data):
        ''' This function inserts a test QR code into the database.'''
        if self.db.connection:
            table = "register_table"
            columns = [
                "date_register", "hour_register", "number_of_part",
                "name_piece", "station", "name_operator", "net_weight",
                "gross_weight", "cost"
            ]

            self.db.insert_data(table, columns, data)

    def get_values(self, data):
        ''' This function returns the values of a QR code.'''
        return [
            value.replace('kg', '').strip().replace('Ñ', ':')
            for value in data.split(',')
        ]

    def add_price(self, values):
        ''' This function adds the price to the values.'''
        price = self.query.get_price(values[2])
        values[-1] = round(float(price) * float(values[6]), 2)
        return values

    def show_message(self, data):
        """
        Show a message box with the captured data.

        Parameters:
        data (list): The data to be displayed in the message box.
        """
        def configure_window(window):
            ''' Configure the window properties '''
            window.title("Información del material")
            window.resizable(False, False)
            window.overrideredirect(True)
            window.configure(background="#F9F9F9")

            # Obtener el tamaño de la pantalla
            screen_width = window.winfo_screenwidth()
            screen_height = window.winfo_screenheight()

            window_width = 350
            window_height = 200

            # Calcular la posición x e y para centrar la ventana
            position_x = (screen_width // 2) - (window_width // 2)
            position_y = (screen_height // 2) - (window_height // 2)

            # Establecer la posición de la ventana
            window.geometry(
                f"{window_width}x{window_height}+{position_x}+{position_y}"
            )

            window.grid_columnconfigure(0, weight=1, minsize=100)
            window.grid_columnconfigure(1, weight=1, minsize=100)

        def create_labels(window, labels_text):
            ''' Create labels to display the information '''
            label_font_title = ("Arial", 12, "bold")
            label_font_text = ("Arial", 12)
            for i, (key, value) in enumerate(labels_text.items(), start=1):
                label_title = ttk.Label(
                    window,
                    text=key,
                    font=label_font_title,
                    background="#F9F9F9"
                )
                label_title.grid(row=i, column=0, padx=10, pady=5, sticky="e")
                label_text = ttk.Label(
                    window,
                    text=value,
                    font=label_font_text,
                    background="#F9F9F9"
                )
                label_text.grid(row=i, column=1, padx=10, pady=5, sticky="w")

        style = ttk.Style()
        style.configure(
            "Custom.TButton",
            background="#6C757D",
            font=("Arial", 12)
        )

        window = tk.Toplevel()
        configure_window(window)

        label_title = ttk.Label(
            window,
            text="Registrado con éxito",
            font=("Arial", 16, "bold"),
            background="#F9F9F9"
        )
        label_title.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        labels_text = {
            "Material:": data[3],
            "Cantidad:": data[6],
            "Precio:": f"{float(data[8]):.2f}"
        }

        create_labels(window, labels_text)
        # Crear un botón para cerrar la ventana
        close_button = ttk.Button(
            window,
            text="Limpiar",
            command=window.destroy,
            style="Custom.TButton"
        )
        close_button.grid(
            column=0,
            row=len(labels_text) + 1,
            padx=10,
            pady=10,
            columnspan=2
        )

        # Ejecutar el bucle principal de la ventana
        window.grab_set()
        window.wait_window()

# Example of use
if __name__ == "__main__":
    # scanner = Scanner()
    # scanner.read_qr_code()
    scanner = Scanner()
    data_test = [
        "2021-08-25",
        "07:00:00",
        "AAAAM3F",
        "ABS",
        "16 FL",
        "Josu de los Cumplido",
        "10.43",
        "12",
        120.4324
    ]
    scanner.show_message(data_test)
