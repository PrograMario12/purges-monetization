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
        print("Showing window report...")
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

        self.view.report_window_instance.menu.entryconfigure(
            "Eliminar", command=self.delete_item
        )

        self.view.report_window_instance.config['calendar_end'].bind(
            "<<DateEntrySelected>>", lambda event: self.update_report(
                event, "end"
            )
        )
        self.view.report_window_instance.tree.bind(
            "<Button-3>", self.show_window_create
        )

    def delete_item(self):
        ''' Delete the selected item. '''
        selected_item = self.view.report_window_instance.tree.selection()
        if not selected_item:
            return

        item_values = self.view.report_window_instance.tree.item(
            selected_item)['values']
        id_item, date_item, description_item = (
            item_values[0],
            item_values[1],
            item_values[2]
        )

        if not self.model.validate_day(date_item):
            self.view.report_window_instance.show_error_message(
                "No se pudo eliminar el registro."
            )
            return

        response = self.view.report_window_instance.show_askquestion(
            f"¿Está seguro de que desea eliminar {description_item}?"
        )
        if response == "yes":
            self.model.delete_item(id_item)
            self.view.report_window_instance.tree.delete(selected_item)
            self.view.report_window_instance.show_info_message(
                "Registro eliminado exitosamente."
            )

    def show_window_create(self, event):
        ''' Show the window create. '''
        selected_item = self.view.report_window_instance.tree.selection()
        if selected_item:
            try:
                self.view.report_window_instance.menu.tk_popup(event.x_root,
                                                               event.y_root
                                                            )
            finally:
                self.view.report_window_instance.menu.grab_release()

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
        date_config = self.view.report_window_instance.config
        date_config[f'date_{date_type}'] = date_config[
            f'calendar_{date_type}'].get_date()

        self.update_treeview(
            self.model.fetch_data_report(
                date_config['date_start'],
                date_config['date_end']
            )
        )

    def update_treeview(self, data):
        ''' Update the treeview with new data. '''
        tree = self.view.report_window_instance.tree
        tree.delete(*tree.get_children())
        if data:
            for row in data:
                tree.insert("", "end", values=row)

if __name__ == "__main__":
    print("This script is not meant to be run directly.")
