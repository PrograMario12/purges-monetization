"""
    Class that validates the QR code
"""

import textwrap

class QRValidator:
    """
        Class that validates the QR code
    """
    def __init__(self, validate_qr_model, database_model):
        """
            Initialize the QRValidator class
        """
        self.validate_qr_model = validate_qr_model
        self.database_model = database_model

    def validate_qr(self, qr_code):
        """
            Validate the QR code
        """
        qr_model = self.validate_qr_model(qr_code, self.database_model)
        data = qr_model.validate()

        if data:
            response = textwrap.dedent(f"""
                Registro encontrado: {data[0][0]}
                Fecha: {data[0][1]}
                Nombre de la pieza: {data[0][2]}
                Peso bruto: {data[0][3]}
                Costo: {data[0][4]}
            """)
            return response
        return "Registro no encontrado"
