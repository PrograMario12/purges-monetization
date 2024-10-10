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
    LABEL_FONT_TITLE = ("Arial", 20, "bold")
    BUTTON_TEXT = "Iniciar escaneo"
    LABEL_FONT_TEXT = ("Arial", 16)

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
        self.window.geometry("1000x600")
        self.window.minsize(1000, 600)
        self.window.title(self.WINDOW_TITLE)

        style = ttk.Style()
        style.configure("TFrame", borderwidth=5)

    def create_widgets(self):
        ''' Create and pack the widgets '''

        ### Definition of widgets
        ## Definition principal panels
        left_panel = ttk.Frame(self.window)
        right_panel = ttk.Frame(self.window)
        top_panel = ttk.Frame(self.window)
        bottom_panel = ttk.Frame(self.window)

        self.window.grid_columnconfigure(0, weight=1, minsize=500)
        self.window.grid_columnconfigure(1, weight=1, minsize=500)
        self.window.grid_rowconfigure(1, weight=1, minsize=400)
        self.window.grid_rowconfigure(0, weight=1, minsize=100)
        self.window.grid_rowconfigure(2, weight=1, minsize=100)

        # Distribution of the frames
        top_panel.grid(row=0, column=0, columnspan=2, sticky="nsew")
        left_panel.grid(row=1, column=0, sticky="n")
        right_panel.grid(row=1, column=1, sticky="n")
        bottom_panel.grid(row=2, column=0, columnspan=2)

        #Top frame
        top_panel.grid_rowconfigure(0, weight=1, minsize=100)
        top_panel.grid_columnconfigure(0, weight=1, minsize=200)
        top_panel.grid_columnconfigure(1, weight=1, minsize=200)

        pil_img = Image.open("img/logo-magna.jpg")
        pil_img = pil_img.resize((200, 100), Image.LANCZOS)
        img = ImageTk.PhotoImage(pil_img)
        image_label = ttk.Label(top_panel, text="Magna", font=self.LABEL_FONT_TITLE)
        image_label.grid(row=0, column=0, sticky="nw", padx=20, pady=20)
        image_label.image = img  # Guardar una referencia a la imagen

        date_label = ttk.Label(top_panel, text="Fecha: 2021-09-01", font=self.LABEL_FONT_TITLE, justify='right')
        date_label.grid(row=0, column=1, sticky="ne", padx=20, pady=20)

        # Create a frame for the report labels
        report_all_day_frame = ttk.Frame(left_panel, borderwidth=5, relief="sunken")
        report_all_day_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=10)

        # Report section
        ttk.Label(left_panel, text="Reportes", font=self.LABEL_FONT_TITLE).grid(row=0, column=0, columnspan=2)
        ttk.Label(report_all_day_frame, text="Del día", font=self.LABEL_FONT_TITLE).grid(row=1, column=0, columnspan=2)

        self.report_labels["peso_tirado_label"] = ttk.Label(
            report_all_day_frame,
            text="Peso Tirado (kg):",
            font=self.LABEL_FONT_TEXT
        )
        self.report_labels["peso_tirado_label"].grid(row=2, column=0, padx=10)

        self.report_labels["peso_tirado_value"] = ttk.Label(report_all_day_frame, text=str(self.report_data["peso_tirado"]), font=self.LABEL_FONT_TEXT)
        self.report_labels["peso_tirado_value"].grid(row=3, column=0, padx=10)

        self.report_labels["costo_label"] = ttk.Label(report_all_day_frame, text="Costo (💰):", font=self.LABEL_FONT_TEXT)
        self.report_labels["costo_label"].grid(row=2, column=1, padx=10)

        self.report_labels["costo_value"] = ttk.Label(report_all_day_frame, text=str(self.report_data["costo"]), font=self.LABEL_FONT_TEXT)
        self.report_labels["costo_value"].grid(row=3, column=1, padx=10)

        # Create a frame for the report labels
        report_frame_turn = ttk.Frame(left_panel,
                borderwidth=5,
                relief="sunken"
            )
        report_frame_turn.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=10)

        # Report section 2
        ttk.Label(report_frame_turn, text="Turno actual", font=self.LABEL_FONT_TITLE).grid(row=0, column=0, columnspan=2)

        self.report_labels["peso_tirado_label_turn"] = ttk.Label(report_frame_turn, text="Peso Tirado (kg):", font=self.LABEL_FONT_TEXT)
        self.report_labels["peso_tirado_label_turn"].grid(row=1, column=0, padx=10)

        self.report_labels["peso_tirado_value_turn"] = ttk.Label(report_frame_turn, text=str(self.report_data["peso_tirado_turn"]), font=self.LABEL_FONT_TEXT)
        self.report_labels["peso_tirado_value_turn"].grid(row=2, column=0, padx=10)

        self.report_labels["costo_label_turn"] = ttk.Label(report_frame_turn, text="Costo (💰):", font=self.LABEL_FONT_TEXT)
        self.report_labels["costo_label_turn"].grid(row=1, column=1, padx=10)

        self.report_labels["costo_value_turn"] = ttk.Label(report_frame_turn, text=str(self.report_data["costo_turn"]), font=self.LABEL_FONT_TEXT)
        self.report_labels["costo_value_turn"].grid(row=2, column=1, padx=10)

        self.video_label = ttk.Label(right_panel)
        self.video_label.grid(row=0, column=0, sticky="nsew", padx=20)

        # Bottom frame
        bottom_panel.grid_rowconfigure(0, weight=1)
        bottom_panel.grid_columnconfigure(0, weight=1)
        bottom_panel.grid_columnconfigure(1, weight=1)

        button_create_report = ttk.Button(bottom_panel, text="Generar reporte", command=self.sc.start_scanning, width=20)
        button_create_report.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        button_other = ttk.Button(bottom_panel, text="Estadísticas", command=self.sc.start_scanning, width=20)
        button_other.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

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

            # Resize the frame to a width of 200 while maintaining aspect ratio
            height, width, _ = cv2image.shape
            new_width = 460
            new_height = int((new_width / width) * height)
            resized_image = cv2.resize(cv2image, (new_width, new_height))

            img = Image.fromarray(resized_image)
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
