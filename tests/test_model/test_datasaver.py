"""Tests for datasaver module."""
import unittest
from model.datasaver import ExcelSaver

class TestExcelSaver(unittest.TestCase):
    """Tests for ExcelSaver."""

    def setUp(self):
        self.saver = ExcelSaver()

    def test_save_data(self):
        """Test save_data method."""
        data = [['header1', 'header2'], ['value1', 'value2']]
        file_path = 'test.xlsx'

        # Since the method is not implemented, we just call it to ensure
        # no exceptions are raised
        try:
            self.saver.save_data(data, file_path)
        except NotImplementedError:
            self.fail("save_data() raised NotImplementedError unexpectedly!")

if __name__ == "__main__":
    unittest.main()
