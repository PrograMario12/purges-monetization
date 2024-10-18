''' This script displays an information message when a button is pressed 
in a Tkinter window. '''

import tkinter as tk
from tkinter import messagebox

def show_no_material_message():
    ''' This function displays an information message when a button is
      pressed. '''
    messagebox.showerror(
            "Número de material no válido",
            "Material no registrado en la base de datos"
        )

def create_main_window():
    ''' This function creates the main window with a button to show the message. '''
    # Crear la ventana principal
    root = tk.Tk()
    root.title("QR Scan")

    # Crear un botón para mostrar el mensaje
    button = tk.Button(root, text="Mostrar resultado del QR", command=show_no_material_message)
    button.pack(pady=20)

    # Ejecutar el bucle principal de la ventana
    root.mainloop()

if __name__ == "__main__":
    create_main_window()
