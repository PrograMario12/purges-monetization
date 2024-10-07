import tkinter as tk
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
        self.query = queries.Queries()
        self.sc = scanner.Scanner(callback=self.update_report)
        self.report_data = {
            "peso_tirado": 0.0,
            "costo": 0.0
        }
        self.report_labels = {}
        self.create_window()
        self.create_widgets()

    def create_window(self):
        ''' Create the main application window '''
        self.window = tk.Tk()
        self.window.title(self.WINDOW_TITLE)
        self.window.state('zoomed')

    def create_widgets(self):
        ''' Create and pack the widgets '''
        self.label = tk.Label(self.window, text=self.LABEL_TEXT, font=self.LABEL_FONT)
        self.label.pack(pady=10)

        self.button_scanner = tk.Button(
            self.window, text=self.BUTTON_TEXT, command=self.sc.start_scanning
        )
        self.button_scanner.pack(pady=10)

        # Report section
        self.report_label = tk.Label(self.window, text="Reporte", font=self.LABEL_FONT)
        self.report_label.pack(pady=10)

        self.report_labels["peso_tirado_label"] = tk.Label(self.window, text="Peso Tirado (kg):", font=self.REPORT_LABEL_FONT)
        self.report_labels["peso_tirado_label"].pack()

        self.report_labels["peso_tirado_value"] = tk.Label(self.window, text=str(self.report_data["peso_tirado"]), font=self.REPORT_LABEL_FONT)
        self.report_labels["peso_tirado_value"].pack()

        self.report_labels["costo_label"] = tk.Label(self.window, text="Costo ($):", font=self.REPORT_LABEL_FONT)
        self.report_labels["costo_label"].pack()

        self.report_labels["costo_value"] = tk.Label(self.window, text=str(self.report_data["costo"]), font=self.REPORT_LABEL_FONT)
        self.report_labels["costo_value"].pack()

    def update_report(self):
        ''' Update the report with new values '''
        costo, peso_tirado = self.query.get_cost_and_weight()
        self.report_data["peso_tirado"] = peso_tirado
        self.report_data["costo"] = costo
        self.report_labels["peso_tirado_value"].config(text=str(self.report_data["peso_tirado"]))
        self.report_labels["costo_value"].config(text=str(self.report_data["costo"]))

    def run(self):
        ''' Run the graphical user interface '''
        self.window.mainloop()

# Example of use
if __name__ == "__main__":
    interface = Interface()
    interface.run()
