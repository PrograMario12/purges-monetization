''' This script allows reading a QR code from the computer's camera.'''

import tkinter as tk
import views
import model
import controller

if __name__ == "__main__":
    root = tk.Tk()
    model = model.Model()
    view = views.TaskView(root)
    controller = controller.PurgeController(model, view)
    root.mainloop()
