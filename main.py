''' This script allows reading a QR code from the computer's camera.'''

import tkinter as tk
import logging
import views
import model
import controller

logging.basicConfig(
        filename="purgas.log",
        filemode="a",
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO
    )

if __name__ == "__main__":
    root = tk.Tk()
    model = model.Model()
    view = views.TaskView(root)
    controller = controller.PurgeController(model, view)
    root.mainloop()
