''' This script allows reading a QR code from the computer's camera.'''

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
    model = model.Model()
    view = views.TaskView()
    controller = controller.PurgeController(model, view)
    view.mainloop()
