"""
Tests for QR Validator Controller.
"""

import unittest
from unittest.mock import MagicMock, patch
from controller.qr_validator_controller import QRValidatorController

class TestQRValidatorController(unittest.TestCase):
    """Tests for QR Validator Controller."""
    def setUp(self):
        self.model = MagicMock()
        self.view = MagicMock()
        self.controller = QRValidatorController(self.model, self.view)

    @patch('controller.qr_validator_controller.Scanner')
    def test_validate_qr(self, MockScanner):
        """Test validate_qr method."""
        mock_scanner_instance = MockScanner.return_value
        mock_scanner_instance.get_values.return_value = [
            'value1', 'value2', 'value3'
            ]

        self.view.frames = {
            "ViewValidate": MagicMock()
        }
        self.view.frames["ViewValidate"].input_qr.get.return_value = 'mock_qr_code'

        self.controller.validate_qr(None)

        self.view.frames[
            "ViewValidate"].input_qr.delete.assert_called_once_with(
            0, 'end'
        )
        mock_scanner_instance.get_values.assert_called_once_with('mock_qr_code')
        self.model.qr_validator.validate_qr.assert_called_once_with(
            ['value1', 'value2', 'value3'])
        self.view.frames[
            "ViewValidate"
            ].information.config.assert_called_once_with(
            text=self.model.qr_validator.validate_qr.return_value
        )

if __name__ == "__main__":
    unittest.main()
