''' This script shows how to display a video stream from OpenCV in a
Tkinter label. '''
import tkinter as tk
from tkinter import ttk
import datetime
import threading
import webbrowser
from PIL import Image, ImageTk
import cv2
import scanner
import queries
from views.styles import apply_styles


class Interface:
    ''' This class creates the graphical user interface of the
    application. '''
    WINDOW_TITLE = "Costo de purgas"

    def __init__(self, root):
        ''' Initialize the Interface class '''
        self.root = root
        self.query = queries.ProcessQueries()
        self.images = {}
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

    def create_window(self):
        ''' Create the main application window '''
        self.root.geometry("1000x600")
        self.root.minsize(1000, 600)
        self.root.resizable(False, False)
        self.root.title(self.WINDOW_TITLE)
        self.root.configure(bg="#F9F9F9")

        apply_styles()

    def create_widgets(self):
        ''' Create and pack the widgets '''
        today = datetime.datetime.now().strftime("%Y-%m-%d")

        def configure_grid(widget, rows, cols, grid_options=None):
            ''' Configure the grid layout of a widget '''
            grid_options = grid_options or {}
            row_weights = grid_options.get('row_weights', [1] * rows)
            col_weights = grid_options.get('col_weights', [1] * cols)
            min_row_sizes = grid_options.get('min_row_sizes', [0] * rows)
            min_col_sizes = grid_options.get('min_col_sizes', [0] * cols)

            for i in range(rows):
                widget.grid_rowconfigure(
                    i,
                    weight=row_weights[i],
                    minsize=min_row_sizes[i]
                )

            for j in range(cols):
                widget.grid_columnconfigure(
                    j,
                    weight=col_weights[j],
                    minsize=min_col_sizes[j])

        def create_label(parent, text, style, row, col, **kwargs):
            ''' Create a label widget '''
            label = ttk.Label(parent, text=text, style=style)
            label.grid(row=row, column=col, **kwargs)
            return label

        def create_input(parent, style, row, col, placeholder, **kwargs):
            ''' Create an input widget with placeholder '''
            entry = ttk.Entry(
                parent,
                style=style,
                font=("Arial", 16, "italic"),
                justify="center"
            )
            entry.grid(row=row, column=col, **kwargs)

            def on_focus_in(event):
                if entry.get() == placeholder:
                    entry.delete(0, tk.END)
                    entry.config(foreground='#000000')

            def on_focus_out(event):
                if entry.get() == '':
                    entry.insert(0, placeholder)
                    entry.config(foreground='grey')

            entry.insert(0, placeholder)
            entry.config(foreground='grey')
            entry.bind("<FocusIn>", on_focus_in)
            entry.bind("<FocusOut>", on_focus_out)

            return entry

        def create_frame(parent, style, row, col, **kwargs):
            frame = ttk.Frame(parent, style=style)
            frame.grid(row=row, column=col, **kwargs)
            return frame

        ### Definition of widgets
        ## Definition principal panels
        left_panel = create_frame(
            self.root,
            "TProject.TFrame",
            2,
            0,
            sticky="ns"
        )
        right_panel = create_frame(
            self.root,
            "TProject.TFrame",
            1,
            0,
            columnspan=2,
            sticky="nsew"
        )
        top_panel = create_frame(
            self.root,
            "TProjectHeader.TFrame",
            0,
            0,
            columnspan=2,
            sticky="nsew"
        )
        bottom_panel = create_frame(
            self.root,
            "TProject.TFrame",
            3,
            0,
            columnspan=2,
            sticky="n"
        )

        grid_options = {
            'row_weights': [1, 1, 1, 1],
            'col_weights': [1],
            'min_row_sizes': [80, 50, 370, 100],
            'min_col_sizes': [600]
        }
        configure_grid(self.root, 3, 1, grid_options)
        configure_grid(
            top_panel,
            1,
            2,
            {'min_row_sizes': [100], 'min_col_sizes': [200, 200]}
        )

        pil_img = Image.open("img/magna-logo.png")
        width, height = pil_img.size
        new_height = 70
        new_width = int((new_height / height) * width)
        pil_img = pil_img.resize((new_width, new_height), Image.LANCZOS)
        self.images["logo"] = ImageTk.PhotoImage(pil_img)
        image_label = create_label(
            top_panel,
            "",
            "TProjectHeader.TLabel",
            0,
            0,
            sticky="nw",
            padx=10,
            pady=10
        )
        image_label.config(image=self.images["logo"])
        image_label.image = self.images["logo"]

        create_label(
            top_panel,
            today,
            "TProjectHeader.TLabel",
            0,
            1,
            sticky="ne",
            padx=20,
            pady=20
        )

        # Left frame
        configure_grid(left_panel, 3, 2)

        # Create a frame for the report labels
        report_all_day_frame = ttk.Frame(
            left_panel,
            style="TProject.TFrame",
            borderwidth=5,
            relief="sunken"
        )
        report_all_day_frame.grid(
            row=1,
            column=0,
            sticky="nsew",
            pady=10
        )

        # Report section
        create_label(
            left_panel,
            "Reportes",
            "TProject_Label_Title.TLabel",
            0,
            0,
            columnspan=2
        )
        create_label(
            report_all_day_frame,
            "Hoy",
            "TProject_Label_Title.TLabel",
            1,
            0,
            columnspan=2
        )

        self.report_labels["peso_tirado_label"] = create_label(
            report_all_day_frame,
            "Peso scrap (kg):",
            "TProject_Label_Title.TLabel",
            2,
            0,
            padx=10
        )
        self.report_labels["peso_tirado_value"] = create_label(
            report_all_day_frame,
            str(self.report_data["peso_tirado"]),
            "TProject_Label_Text.TLabel",
            3,
            0,
            padx=10
        )
        self.report_labels["costo_label"] = create_label(
            report_all_day_frame,
            "Costo ($):",
            "TProject_Label_Title.TLabel",
            2,
            1,
            padx=10
        )
        self.report_labels["costo_value"] = create_label(
            report_all_day_frame,
            str(self.report_data["costo"]),
            "TProject_Label_Text.TLabel",
            3,
            1,
            padx=10
        )

        # Create a frame for the report labels
        report_frame_turn = ttk.Frame(
            left_panel,
            style="TProject.TFrame",
            borderwidth=5,
            relief="sunken"
        )
        report_frame_turn.grid(
            row=1,
            column=1,
            sticky="nsew",
            pady=10
        )

        # Report section 2
        create_label(
            report_frame_turn,
            "Turno actual",
            "TProject_Label_Title.TLabel",
            0,
            0,
            columnspan=2
        )
        self.report_labels["peso_tirado_label_turn"] = create_label(
            report_frame_turn,
            "Peso scrap (kg):",
            "TProject_Label_Title.TLabel",
            1,
            0,
            padx=10
        )
        self.report_labels["peso_tirado_value_turn"] = create_label(
            report_frame_turn,
            str(self.report_data["peso_tirado_turn"]),
            "TProject_Label_Text.TLabel",
            2,
            0,
            padx=10
        )
        self.report_labels["costo_label_turn"] = create_label(
            report_frame_turn,
            "Costo ($):",
            "TProject_Label_Title.TLabel",1,
            1,
            padx=10
        )
        self.report_labels["costo_value_turn"] = create_label(
            report_frame_turn,
            str(self.report_data["costo_turn"]),
            "TProject_Label_Text.TLabel",
            2,
            1,
            padx=10
        )

        # Right frame
        configure_grid(right_panel, 1, 1)

        def on_input_change(event):
            ''' Function to be called when input changes '''
            input_value = self.data_input.get()
            self.data_input.delete(0, tk.END)
            scanner_var = scanner.Scanner(callback=self.update_report)
            scanner_var.process_qr_code(input_value)

        self.data_input = create_input(
            right_panel,
            "TProject_Label_Text.TEntry",
            0,
            0,
            placeholder="Escanea el QR",
            sticky="ew",
            padx=10,
        )
        self.data_input.bind("<Return>", on_input_change)

        # Bottom frame
        configure_grid(bottom_panel, 1, 2)

        self.button_create_report = ttk.Button(
            bottom_panel,
            text="Generar reporte",
            style="TProject.TButton"
        )
        self.button_create_report.grid(
            row=0,
            column=0,
            padx=10,
            pady=10,
            sticky="nsew"
        )

        def open_statistics():
            webbrowser.open("http://www.google.com")

        button_other = ttk.Button(
            bottom_panel,
            text="Estadísticas",
            command=open_statistics,
            style="TProject.TButton"
        )
        button_other.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

    def update_report(self):
        ''' Update the report with new values '''
        costo, peso_tirado, cost_turn, weight_turn = (
            self.query.get_cost_and_weight()
        )

        costo = costo or 0.0
        peso_tirado = peso_tirado or 0.0
        cost_turn = cost_turn or 0.0
        weight_turn = weight_turn or 0.0

        self.report_data["peso_tirado"] = round(peso_tirado, 2)
        self.report_data["costo"] = round(costo, 2)
        self.report_data["peso_tirado_turn"] = round(weight_turn, 2)
        self.report_data["costo_turn"] = round(cost_turn, 2)
        self.report_labels["peso_tirado_value"].config(text=f"""
                {self.report_data['peso_tirado']:.2f}"""
            )
        self.report_labels["costo_value"].config(text=f"""
                {self.report_data['costo']:.2f}"""
            )
        self.report_labels["peso_tirado_value_turn"].config(text=f"""
                {self.report_data['peso_tirado_turn']:.2f}"""
            )
        self.report_labels["costo_value_turn"].config(text=f"""
                {self.report_data['costo_turn']:.2f}"""
            )

    def update_frame(self):
        ''' Update the OpenCV frame '''
        ret, frame = self.cap.read()
        if ret:
            # Convert the frame to RGB
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            self.sc.read_qr_code_v2(gray)

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

# Example of use
if __name__ == "__main__":
    print("This script is not meant to be run directly.")