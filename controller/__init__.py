"""
Controller module for the Purge application.
"""

from controller.qr_validator_controller import QRValidatorController
from controller import report_window_controller as rwc

class PurgeController:
    """ Controller class for the Purge application. """
    def __init__(self, model, view):
        """ Initialize the PurgeController. """
        self.model = model
        self.view = view
        self.qr_validator_controller = QRValidatorController(model, view)
        self.report_window_controller = rwc.ReportWindowController(model, view)

        self.view.buttons["report"].config(
            command=self.report_window_controller.initialize_report_window
        )
        self.view.frames["ViewValidate"].input_qr.bind(
            "<Return>", self.qr_validator_controller.validate_qr
        )
