''' Controller package for the Purge application. '''

class PurgeController:
    ''' Controller class for the Purge application. '''
    def __init__(self, model, view):
        ''' Initialize the controller with the model and view. '''
        self.model = model
        self.view = view

        self.view.interface.button_create_report.config(command=self.show_window_report)

    def show_window_report(self):
        ''' Show the window report. '''
        self.view.show_window_report()
        data = self.model.fetch_data_report()
        if data:
            for row in data:
                self.view.report_window_instance.tree.insert("", "end", values=row)



if __name__ == "__main__":
    print("This script is not meant to be run directly.")
