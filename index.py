''' This script allows reading a QR code from the computer's camera.'''

import tkinter as tk
from tkinter import messagebox
import cv2
from pyzbar import pyzbar
from pyzbar.pyzbar_error import PyZbarError
import database

def insert_data(data):
    ''' Esta función inserta un código QR de prueba en la base de datos.'''
    conn = database.create_connection()
    if conn:
        table = "register_table"
        columns = [
            "date_register", "hour_register", "number_of_part", "name_piece",
            "station", "name_operator", "net_weight", "gross_weight",
            "total_weight"
        ]
        values = [value.replace('kg', '').strip() for value in data.split(',')]
        print (values)
        database.insert_data(conn, table, columns, values)

def leer_codigo_qr():
    ''' Esta función permite leer un código QR desde la cámara de
    la computadora.'''
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
            datos = resultado.data.decode("utf-8")
            messagebox.showinfo("Resultado", datos)
            insert_data(datos)

        cv2.imshow("Escaneando código QR", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            status = False
            break

    video.release()
    cv2.destroyAllWindows()

# Crear la ventana de la aplicación
ventana = tk.Tk()
ventana.title("App de Escaneo de Código QR")
ventana.state('zoomed')

# Crear la etiqueta y el campo de entrada
label = tk.Label(ventana, text="Escanea código QR", font=("Arial", 18))
label.pack(pady=10)

# Crear el botón para iniciar el escaneo
boton = tk.Button(ventana, text="Iniciar Escaneo", command=leer_codigo_qr)
boton.pack()

# Iniciar el bucle de la interfaz gráfica
ventana.mainloop()
