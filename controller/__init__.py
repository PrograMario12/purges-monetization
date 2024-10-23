''' Controller package for the Purge application. '''

class PurgeController:
    ''' Controller class for the Purge application. '''
    def __init__(self, model, view):
        ''' Initialize the controller with the model and view. '''
        self.model = model
        self.view = view

        self.view.interface.button_create_report.config(
            command=self.show_window_report
        )

    def show_window_report(self):
        ''' Show the window report. '''
        self.view.show_window_report()
        self._initialize_report_window()

    def _initialize_report_window(self):
        ''' Initialize the report window with data and event bindings. '''
        data = self.model.fetch_data_report(
            self.view.report_window_instance.config['date_start'],
            self.view.report_window_instance.config['date_end']
        )
        self.update_treeview(data)

        self.view.report_window_instance.config['generate_report'].config(
            command=self.generate_report
        )
        self.view.report_window_instance.config['button_cancel'].config(
            command=self.view.report_window_instance.destroy
        )
        self.view.report_window_instance.config['calendar_start'].bind(
            "<<DateEntrySelected>>", lambda event: self.update_report(
                event, "start"
            )
        )
        self.view.report_window_instance.config['calendar_end'].bind(
            "<<DateEntrySelected>>", lambda event: self.update_report(
                event, "end"
            )
        )

    def generate_report(self):
        ''' Generate a report. '''
        data = self.model.fetch_data_report_csv(
            self.view.report_window_instance.config['date_start'],
            self.view.report_window_instance.config['date_end']
        )
        if data:
            file_path = self.view.ask_save_as_filename()
            if file_path:
                self.view.save_report_to_csv(data, file_path)

    def update_report(self, event, date_type):
        ''' Update the report with new values. '''
        if date_type == "start":
            self.view.report_window_instance.config['date_start'] = (
                self.view.report_window_instance.config['calendar_start'].get_date()
            )
        else:
            self.view.report_window_instance.config['date_end'] = (
                self.view.report_window_instance.config['calendar_end'].get_date()
            )

        data = self.model.fetch_data_report(
            self.view.report_window_instance.config['date_start'],
            self.view.report_window_instance.config['date_end']
        )
        self.update_treeview(data)

    def update_treeview(self, data):
        ''' Update the treeview with new data. '''
        self.view.report_window_instance.tree.delete(
            *self.view.report_window_instance.tree.get_children()
        )
        if data:
            for row in data:
                self.view.report_window_instance.tree.insert(
                    "", "end", values=row
                )

if __name__ == "__main__":
    print("This script is not meant to be run directly.")
