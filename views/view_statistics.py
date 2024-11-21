''' This module is responsible for showing the statistics of the system '''

import tkinter as tk
import webview

class ViewStatistics(tk.Frame):
    ''' Class to show the statistics '''
    def __init__(self, parent, controller):
        ''' Initialize the class '''
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        ''' Create the widgets '''
        self.webview_frame = tk.Frame(self)
        self.webview_frame.grid(row=0, column=0, sticky="nsew")
        self.load_webview()

    def load_webview(self):
        ''' Load the webview '''
        webview.create_window('Statistics', 'https://www.google.com', frameless=True)
        webview.start(gui='tkinter', debug=True)

# Example usage
if __name__ == "__main__":
    root = tk.Tk()
    app = ViewStatistics(root, None)
    app.pack(fill="both", expand=True)
    root.mainloop()
