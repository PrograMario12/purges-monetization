''' This script allows reading a QR code from the computer's camera.'''

import tkinter as tk
from tkinter import messagebox
import cv2
from pyzbar import pyzbar
from pyzbar.pyzbar_error import PyZbarError
import database

def insert_data(data):
    ''' Esta función inserta un código QR de prueba en la base de datos.'''
    db = database.DataBase()
    db.create_connection()

    if db.connection:
        table = "register_table"
        columns = [
            "date_register", "hour_register", "number_of_part",
            "name_piece", "station", "name_operator", "net_weight",
            "gross_weight", "total_weight"
        ]
        values = [value.replace('kg', '').strip() for value in
                  data.split(',')]
        print (values)
        db.insert_data(table, columns, values)

# Crear la ventana de la aplicación
ventana = tk.Tk()
ventana.title("App de Escaneo de Código QR")
ventana.state('zoomed')

# Crear la etiqueta y el campo de entrada
label = tk.Label(ventana, text="Escanea código QR", font=("Arial", 18))
label.pack(pady=10)

# Crear el botón para iniciar el escaneo
boton = tk.Button(ventana, text="Iniciar Escaneo", command=read_qr_code)
boton.pack()

# Iniciar el bucle de la interfaz gráfica
ventana.mainloop()
