''' This file is used to import the interface class and create an 
instance of it in the TaskView class '''
from .interface import Interface
from .window_report import ReportWindow

class TaskView:
    ''' This class is used to create an instance of the interface class '''
    def __init__(self, root):
        self.root = root
        self.interface = Interface(self.root)
        self.report_window_instance = None

    def show_window_report(self):
        ''' Show the window report '''
        self.report_window_instance = ReportWindow(self.root)

if __name__ == "__main__":
    print("This script is not meant to be run directly.")
