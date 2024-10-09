import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
import scanner
import queries
import threading

class Interface:
    ''' This class creates the graphical user interface of the application. '''

    WINDOW_TITLE = "Monetización de purgas"
    LABEL_TEXT = "Escanear códigos"
    LABEL_FONT = ("Arial", 20)
    BUTTON_TEXT = "Iniciar escaneo"
    REPORT_LABEL_FONT = ("Arial", 16)

    def __init__(self):
        ''' Initialize the Interface class '''
        self.query = queries.ProcessQueries()
        self.sc = scanner.Scanner(callback=self.update_report)
        self.report_data = {
            "peso_tirado": 0.0,
            "costo": 0.0,
            "peso_tirado_turn": 0.0,
            "costo_turn": 0.0
        }
        self.report_labels = {}
        self.create_window()
        self.create_widgets()
        self.update_report()
        self.cap = cv2.VideoCapture(1)  # OpenCV video capture
        self.start_update_frame_thread()

    def create_window(self):
        ''' Create the main application window '''
        self.window = tk.Tk()
        self.window.title(self.WINDOW_TITLE)
        self.window.state('zoomed')

        # Apply a theme
        # style = ttk.Style(self.window)
        # style.theme_use('default')  # You can try 'clam', 'alt', 'default', 'classic'

    def create_widgets(self):
        ''' Create and pack the widgets '''

        # Report section
        self.report_label = ttk.Label(self.window, text="Del día", font=self.LABEL_FONT)
        self.report_label.pack(pady=10)

        # Create a frame for the report labels
        report_frame = ttk.Frame(self.window)
        report_frame.pack(pady=10)

        self.report_labels["peso_tirado_label"] = ttk.Label(
            report_frame,
            text="Peso Tirado (kg):",
            font=self.REPORT_LABEL_FONT
            )
        self.report_labels["peso_tirado_label"].grid(row=0, column=0, padx=10)

        self.report_labels["peso_tirado_value"] = ttk.Label(report_frame, text=str(self.report_data["peso_tirado"]), font=self.REPORT_LABEL_FONT)
        self.report_labels["peso_tirado_value"].grid(row=1, column=0, padx=10)

        self.report_labels["costo_label"] = ttk.Label(report_frame, text="Costo ($):", font=self.REPORT_LABEL_FONT)
        self.report_labels["costo_label"].grid(row=0, column=1, padx=10)

        self.report_labels["costo_value"] = ttk.Label(report_frame, text=str(self.report_data["costo"]), font=self.REPORT_LABEL_FONT)
        self.report_labels["costo_value"].grid(row=1, column=1, padx=10)

        #Report section 2
        self.report_label = ttk.Label(self.window, text="Turno actual", font=self.LABEL_FONT)
        self.report_label.pack(pady=10)

        # Create a frame for the report labels
        self.report_frame_turn = ttk.Frame(self.window)
        self.report_frame_turn.pack(pady=10)

        self.report_labels["peso_tirado_label_turn"] = ttk.Label(self.report_frame_turn, text="Peso Tirado (kg):", font=self.REPORT_LABEL_FONT)
        self.report_labels["peso_tirado_label_turn"].grid(row=0, column=0, padx=10)

        self.report_labels["peso_tirado_value_turn"] = ttk.Label(self.report_frame_turn, text=str(self.report_data["peso_tirado_turn"]), font=self.REPORT_LABEL_FONT)
        self.report_labels["peso_tirado_value_turn"].grid(row=1, column=0, padx=10)

        self.report_labels["costo_label_turn"] = ttk.Label(self.report_frame_turn, text="Costo ($):", font=self.REPORT_LABEL_FONT)
        self.report_labels["costo_label_turn"].grid(row=0, column=1, padx=10)

        self.report_labels["costo_value_turn"] = ttk.Label(self.report_frame_turn, text=str(self.report_data["costo_turn"]), font=self.REPORT_LABEL_FONT)
        self.report_labels["costo_value_turn"].grid(row=1, column=1, padx=10)

        # Create a label for the OpenCV video
        self.video_label = ttk.Label(self.window)
        self.video_label.pack(pady=10)

    def update_report(self):
        ''' Update the report with new values '''
        costo, peso_tirado, cost_turn, weight_turn = self.query.get_cost_and_weight()

        # Verificar si los valores son None y asignar un valor predeterminado
        if costo is None:
            costo = 0.0
        if peso_tirado is None:
            peso_tirado = 0.0
        if cost_turn is None:
            cost_turn = 0.0
        if weight_turn is None:
            weight_turn = 0.0

        self.report_data["peso_tirado"] = round(peso_tirado, 2)
        self.report_data["costo"] = round(costo, 2)
        self.report_data["peso_tirado_turn"] = round(weight_turn, 2)
        self.report_data["costo_turn"] = round(cost_turn, 2)
        self.report_labels["peso_tirado_value"].config(text=f"{self.report_data['peso_tirado']:.2f}")
        self.report_labels["costo_value"].config(text=f"{self.report_data['costo']:.2f}")
        self.report_labels["peso_tirado_value_turn"].config(text=f"{self.report_data['peso_tirado_turn']:.2f}")
        self.report_labels["costo_value_turn"].config(text=f"{self.report_data['costo_turn']:.2f}")

    def update_frame(self):
        ''' Update the OpenCV frame '''
        ret, frame = self.cap.read()
        if ret:
            # Convert the frame to RGB
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            self.sc.read_qr_code_v2(gray)

            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)
        self.window.after(10, self.update_frame)

    def start_update_frame_thread(self):
        ''' Start the update_frame function in a separate thread '''
        update_thread = threading.Thread(target=self.update_frame)
        update_thread.daemon = True
        update_thread.start()

    def run(self):
        ''' Run the graphical user interface '''
        self.window.mainloop()

# Example of use
if __name__ == "__main__":
    interface = Interface()
    interface.run()
