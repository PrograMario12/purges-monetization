''' This module allows reading QR codes from the computer's camera. '''

from tkinter import messagebox
import cv2
from pyzbar import pyzbar
from pyzbar.pyzbar_error import PyZbarError
import database

class Scanner:
    ''' This class allows reading QR codes from the computer's camera'''

    def __init__(self):
        ''' Initialize the Scanner class '''
        self.db = database.DataBase()
        self.db.create_connection()

    def read_qr_code(self):
        ''' This function reads a QR code from the computer's camera.'''
        video = cv2.VideoCapture(1)
        if not video.isOpened():
            messagebox.showerror("Error", "No se pudo abrir la cámara.")
            return

        status = True
        while status:
            ret, frame = video.read()
            if not ret:
                print("Error al capturar el frame de la cámara.")
                break

            gray = cv2.cvtColor(
                frame, cv2.COLOR_BGR2GRAY
            )

            try:
                resultados = pyzbar.decode(gray)
            except PyZbarError as e:
                print(f"Error decoding QR code: {e}")
                continue
            except cv2.error as e: # pylint: disable=E0712
                print(f"OpenCV error: {e}")
                break

            for resultado in resultados:
                try:
                    datos = resultado.data.decode("utf-8")
                    messagebox.showinfo("Resultado", datos)
                    self.insert_data(datos)
                except UnicodeDecodeError as e:
                    print(f"Error de codificación: {e}")
                    # Manejar el error de codificación aquí
                    try:
                        datos = resultado.data.decode("latin-1")
                        messagebox.showinfo("Resultado", datos)
                        self.insert_data(datos)
                    except UnicodeDecodeError as e2:
                        print(
                            f"Error de codificación con latin-1: {e2}"
                            )
                        # Manejar el error de codificación aquí

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
                "gross_weight", "total_weight"
            ]
            values = [value.replace('kg', '').strip()
                      for value in data.split(',')]
            print(values)
            self.db.insert_data(table, columns, values)

# Example of use
if __name__ == "__main__":
    scanner = Scanner()
    scanner.read_qr_code()
