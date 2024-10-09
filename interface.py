import tkinter as tk
from tkinter import ttk
import scanner
import queries

class Interface:
    ''' This class creates the graphical user interface of the application. '''

    WINDOW_TITLE = "Monetización de purgas"
    LABEL_TEXT = "Escanear códigos"
    LABEL_FONT = ("Arial", 18)
    BUTTON_TEXT = "Iniciar escaneo"
    REPORT_LABEL_FONT = ("Arial", 14)

    def __init__(self):
        ''' Initialize the Interface class '''
        self.query = queries.ProcessQueries()
        self.sc = scanner.Scanner(callback=self.update_report)
        self.report_data = {
            "peso_tirado": 0.0,
            "costo": 0.0
        }
        self.report_labels = {}
        self.create_window()
        self.create_widgets()
        self.update_report()

    def create_window(self):
        ''' Create the main application window '''
        self.window = tk.Tk()
        self.window.title(self.WINDOW_TITLE)
        self.window.state('zoomed')

        # Apply a theme
        style = ttk.Style(self.window)
        style.theme_use('clam')  # You can try 'clam', 'alt', 'default', 'classic'

    def create_widgets(self):
        ''' Create and pack the widgets '''
        self.label = ttk.Label(self.window, text=self.LABEL_TEXT, font=self.LABEL_FONT)
        self.label.pack(pady=10)

        self.button_scanner = ttk.Button(
            self.window, text=self.BUTTON_TEXT, command=self.sc.start_scanning
        )
        self.button_scanner.pack(pady=10)

        # Report section
        self.report_label = ttk.Label(self.window, text="Reporte diario", font=self.LABEL_FONT)
        self.report_label.pack(pady=10)

        # Create a frame for the report labels
        report_frame = ttk.Frame(self.window)
        report_frame.pack(pady=10)

        self.report_labels["peso_tirado_label"] = ttk.Label(report_frame, text="Peso Tirado (kg):", font=self.REPORT_LABEL_FONT)
        self.report_labels["peso_tirado_label"].grid(row=0, column=0, padx=10)

        self.report_labels["peso_tirado_value"] = ttk.Label(report_frame, text=str(self.report_data["peso_tirado"]), font=self.REPORT_LABEL_FONT)
        self.report_labels["peso_tirado_value"].grid(row=1, column=0, padx=10)

        self.report_labels["costo_label"] = ttk.Label(report_frame, text="Costo ($):", font=self.REPORT_LABEL_FONT)
        self.report_labels["costo_label"].grid(row=0, column=1, padx=10)

        self.report_labels["costo_value"] = ttk.Label(report_frame, text=str(self.report_data["costo"]), font=self.REPORT_LABEL_FONT)
        self.report_labels["costo_value"].grid(row=1, column=1, padx=10)

    def update_report(self):
        ''' Update the report with new values '''
        costo, peso_tirado, cost_turn, weight_turn = self.query.get_cost_and_weight()
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
        self.report_labels["peso_tirado_value"].config(text=f"{self.report_data['peso_tirado']:.2f}")
        self.report_labels["costo_value"].config(text=f"{self.report_data['costo']:.2f}")

    def run(self):
        ''' Run the graphical user interface '''
        self.window.mainloop()

# Example of use
if __name__ == "__main__":
    interface = Interface()
    interface.run()
