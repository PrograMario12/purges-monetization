''' This module allows reading QR codes from the computer's 
camera.'''

import threading
import tkinter as tk
from tkinter import messagebox, ttk
import cv2
from pyzbar import pyzbar
from pyzbar.pyzbar_error import PyZbarError
import database
import queries

class Scanner:
    ''' This class allows reading QR codes from the computer's camera'''

    def __init__(self, callback=None):
        ''' Initialize the Scanner class '''
        self.db = database.DataBase()
        self.db.create_connection()
        self.query = queries.Queries()
        self.callback = callback

    def read_qr_code_v2(self, gray):
        ''' This function reads a QR code from the computer's camera.'''
        try:
            resultados = pyzbar.decode(gray)
        except PyZbarError as e:
            print(f"Error decoding QR code: {e}")
        except cv2.error as e:
            print(f"OpenCV error: {e}")

        for resultado in resultados:
            try:
                datos = resultado.data.decode("utf-8")
                print(f"Resultado: {datos}")
                datos = self.add_price(self.get_values(datos))
                self.insert_data(datos)
                self.show_message(datos)
                if self.callback:
                    self.callback()
            except UnicodeDecodeError as e:
                print(f"Error de codificación: {e}")
                try:
                    datos = resultado.data.decode("latin-1")
                    print(f"Resultado: {datos}")
                    self.insert_data(datos)
                    self.show_message(datos)
                    if self.callback:
                        self.callback()
                except UnicodeDecodeError as e2:
                    print(f"Error de codificación con latin-1: {e2}")

    def read_qr_code(self):
        ''' This function reads a QR code from the computer's camera.'''
        video = cv2.VideoCapture(1)
        if not video.isOpened():
            root = tk.Tk()
            root.withdraw()  # Oculta la ventana principal de Tkinter
            messagebox.showerror("Error", "No se pudo abrir la cámara")
            root.destroy()
            return

        status = True
        while status:
            ret, frame = video.read()
            if not ret:
                print("Error al capturar el frame de la cámara.")
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            try:
                resultados = pyzbar.decode(gray)
            except PyZbarError as e:
                print(f"Error decoding QR code: {e}")
                continue
            except cv2.error as e:
                print(f"OpenCV error: {e}")
                break

            for resultado in resultados:
                try:
                    datos = resultado.data.decode("utf-8")
                    datos = self.add_price(self.get_values(datos))
                    self.insert_data(datos)
                    self.show_message(datos)
                    if self.callback:
                        self.callback()
                except UnicodeDecodeError as e:
                    print(f"Error de codificación: {e}")
                    try:
                        datos = resultado.data.decode("latin-1")
                        print(f"Resultado: {datos}")
                        self.insert_data(datos)
                        self.show_message(datos)
                        if self.callback:
                            self.callback()
                    except UnicodeDecodeError as e2:
                        print(f"Error de codificación con latin-1: {e2}")

            cv2.imshow("Escaneando código QR", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                status = False
                break

        video.release()
        cv2.destroyAllWindows()

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
        return [value.replace('kg', '').strip() for value in data.split(',')]

    def add_price(self, values):
        ''' This function adds the price to the values.'''
        price = self.query.get_price(values[2])
        values[-1] = float(price) * float(values[6])
        return values

    def show_message(self, data):
        ''' This function shows a message box with the captured data.'''
        # Crear una nueva ventana
        window = tk.Toplevel()
        window.title("Información del Material")

        # Crear etiquetas para mostrar la información
        material_label = ttk.Label(window, text=f"Material: {data[3]}")
        material_label.grid(column=0, row=0, padx=10, pady=5)

        cantidad_label = ttk.Label(window, text=f"Cantidad: {data[6]}")
        cantidad_label.grid(column=0, row=1, padx=10, pady=5)

        precio_label = ttk.Label(window, text=f"Precio: ${round(float(data[8]), 2)}")
        precio_label.grid(column=0, row=2, padx=10, pady=5)

        # Crear un botón para cerrar la ventana
        def on_close():
            window.destroy()

        close_button = ttk.Button(window, text="Cerrar", command=on_close)
        close_button.grid(column=0, row=3, padx=10, pady=10)

        # Ejecutar el bucle principal de la ventana
        window.grab_set()

        window.wait_window()

    def start_scanning(self):
        ''' This function starts the QR code scanning in a separate thread.'''
        scanning_thread = threading.Thread(target=self.read_qr_code)
        scanning_thread.start()

# Example of use
if __name__ == "__main__":
    scanner = Scanner()
    scanner.read_qr_code()
