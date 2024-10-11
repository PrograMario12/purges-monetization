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
        label_font_title = ("Arial", 12, "bold")
        label_font_text = ("Arial", 12)
        style = ttk.Style()
        style.configure("Custom.TButton", background="blue", font=("Arial", 12))

        window = tk.Toplevel()
        window.title("Información del Material")
        window.resizable(False, False)
        window.overrideredirect(True)

        # Obtener el tamaño de la pantalla
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        # Obtener el tamaño de la ventana
        window.update_idletasks()  # Actualizar la ventana para obtener el tamaño correcto
        window_width = 350
        window_height = 150

        # Calcular la posición x e y para centrar la ventana
        position_x = (screen_width // 2) - (window_width // 2)
        position_y = (screen_height // 2) - (window_height // 2)

        # Establecer la posición de la ventana
        window.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

        window.grid_columnconfigure(0, weight=1, minsize=100)
        window.grid_columnconfigure(1, weight=1, minsize=100)

        labels_text = {
            "Material:": data[3],
            "Cantidad:": data[6],
            "Precio:": f"{float(data[8]):.2f}"
        }

        # Crear etiquetas para mostrar la información
        for idx, (label, value) in enumerate(labels_text.items()):
            title_label = ttk.Label(window, text=label, font=label_font_title)
            title_label.grid(column=0, row=idx, padx=10, pady=5, sticky="e")

            value_label = ttk.Label(window, text=value, font=label_font_text)
            value_label.grid(column=1, row=idx, padx=10, pady=5, sticky="w")

        # Crear un botón para cerrar la ventana
        close_button = ttk.Button(window, text="Cerrar", command=window.destroy, style="Custom.TButton")
        close_button.grid(column=0, row=len(labels_text), padx=10, pady=10, columnspan=2)

        # Ejecutar el bucle principal de la ventana
        window.grab_set()
        window.wait_window()

    def start_scanning(self):
        ''' This function starts the QR code scanning in a separate thread.'''
        scanning_thread = threading.Thread(target=self.read_qr_code)
        scanning_thread.start()

# Example of use
if __name__ == "__main__":
    # scanner = Scanner()
    # scanner.read_qr_code()
    scanner = Scanner()
    data_test = ["2021-08-25", "07:00:00", "AAAAM3F", "ABS", "16 FL", "Josu de los Cumplido", "10.43", "12", 120.4324]
    scanner.show_message(data_test)
