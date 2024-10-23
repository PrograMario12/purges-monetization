''' Test the ReportWindow class '''
import unittest
import tkinter as tk
import re
import datetime
from views.window_report import ReportWindow
# views/test_window_report.py

class TestReportWindow(unittest.TestCase):
    ''' Test the ReportWindow class'''
    def setUp(self):
        self.root = tk.Tk()
        self.report_window = ReportWindow(self.root)

    def tearDown(self):
        self.report_window.destroy()
        self.root.destroy()

    def test_window_title(self):
        ''' Test the title of the window '''
        self.assertEqual(self.report_window.title(), "Generar Reporte")

    def test_window_geometry(self):
        ''' Test the geometry of the window '''
        geometry = self.report_window.geometry()
        size = re.match(r'\d+x\d+', geometry).group()
        self.assertEqual(size, "800x500")

    def test_window_minsize(self):
        ''' Test the minimum size of the window '''
        self.assertEqual(self.report_window.minsize(), (800, 500))

    def test_window_background(self):
        ''' Test the background color of the window '''
        self.assertEqual(self.report_window.cget("bg"), "#F9F9F9")

    def test_columns(self):
        ''' Test the columns of the treeview '''
        self.assertEqual(self.report_window.columns, [
            "Fecha",
            "Descripción",
            "Peso total",
            "Costo"
        ])

    def test_date_attributes(self):
        ''' Test the date attributes '''
        self.assertEqual(self.report_window.date_start, datetime.date.today())
        self.assertEqual(self.report_window.date_end, datetime.date.today())

    def test_frames_and_widgets_creation(self):
        ''' Test the creation of the frames and widgets '''
        self.assertIsNotNone(self.report_window.calendar_start)
        self.assertIsNotNone(self.report_window.calendar_end)
        self.assertIsNotNone(self.report_window.button_cancel)

if __name__ == "__main__":
    unittest.main()
