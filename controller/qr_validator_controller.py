"""
QR Validator Controller
"""

from scanner import Scanner

class QRValidatorController:
    """
    Controller class for the QR Validator.
    """
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def validate_qr(self, event):
        """
        Validate the QR code.
        """
        sc = Scanner()
        input_value = self.view.frames["ViewValidate"].input_qr.get()
        self.view.frames["ViewValidate"].input_qr.delete(0, 'end')
        input_value = sc.get_values(input_value)

        input_value = [input_value[0], input_value[1], input_value[2]]

        text = self.model.qr_validator.validate_qr(input_value)
        self.view.frames["ViewValidate"].information.config(text=text)
