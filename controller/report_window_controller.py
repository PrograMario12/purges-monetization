"""
This module contains the ReportWindowController class.
"""

class ReportWindowController:
    """
    Controller class for the ReportWindow.
    """
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def initialize_report_window(self):
        """
        Initialize the report window with data and event bindings.
        """
        self.view.show_frame("ReportWindow")
        self.load_report_data()
        self.configure_report_window_buttons()
        self.bind_report_events()

    def load_report_data(self):
        """
        Load the report data.
        """
        data = self.model.report_fetcher.fetch_data_report(
            self.view.frames["ReportWindow"].config['date_start'],
            self.view.frames["ReportWindow"].config['date_end']
        )

        self.update_treeview(data)

    def configure_report_window_buttons(self):
        """
        Configure the buttons in the report window.
        """
        self.view.frames["ReportWindow"].config['generate_report'].config(
            command=self.generate_report
        )

    def bind_report_events(self):
        """ Bind events to the report window. """
        self.view.frames["ReportWindow"].config['calendar_start'].bind(
            "<<DateEntrySelected>>", lambda event: self.update_report(
                event, "start"
            )
        )
        self.view.frames["ReportWindow"].menu.entryconfigure(
            "Eliminar", command=self.delete_item
        )
        self.view.frames["ReportWindow"].config['calendar_end'].bind(
            "<<DateEntrySelected>>", lambda event: self.update_report(
                event, "end"
            )
        )
        self.view.frames["ReportWindow"].tree.bind(
            "<Button-3>", self.show_window_create
        )

    def delete_item(self):
        """ Delete an item from the report. """
        selected_tree_item = self.view.frames["ReportWindow"].tree.selection()
        if not selected_tree_item:
            return

        item_values = self.view.frames["ReportWindow"].tree.item(
            selected_tree_item
        )['values']
        id_item = item_values[0]
        date_item = item_values[1]
        description_item = item_values[2]

        if not self.model.date_validation.validate_day(date_item):
            self.view.frames["ReportWindow"].show_error_message(
                "No se pudo eliminar el registro."
            )
            return

        response = self.view.frames["ReportWindow"].show_askquestion(
            f"¿Está seguro de que desea eliminar {description_item}?"
        )
        if response == "yes":
            self.view.frames["ReportWindow"].tree.delete(selected_tree_item)
            self.view.frames["ReportWindow"].show_info_message(
                "Registro eliminado exitosamente.")
            try:
                self.model.item_deleter.delete_item(id_item)
            except Exception as e:
                self.view.frames["ReportWindow"].show_error_message(
                    f"Error al eliminar el registro: {str(e)}"
                )
                return

    def update_treeview(self, data):
        ''' Update the treeview with new data '''
        tree = self.view.frames["ReportWindow"].tree
        tree.delete(*tree.get_children())
        if data:
            for row in data:
                tree.insert("", "end", values=row)

    def generate_report(self):
        """ Generate a report """
        data = self.model.report_fetcher.fetch_data_report_csv(
            self.view.frames["ReportWindow"].config['date_start'],
            self.view.frames["ReportWindow"].config['date_end']
        )

        if data:
            file_path = self.view.ask_save_as_filename()
            if file_path:
                self.view.save_report_to_excel(data, file_path)

    def update_report(self, event, date_type):
        ''' Update the report with new values. '''
        date_config = self.view.frames["ReportWindow"].config
        date_config[f'date_{date_type}'] = date_config[
            f'calendar_{date_type}'].get_date()

        self.update_treeview(
            self.model.report_fetcher.fetch_data_report(
                date_config['date_start'],
                date_config['date_end']
            )
        )

    def show_window_create(self, event):
        ''' Show the window create. '''
        selected_tree_item = self.view.frames["ReportWindow"].tree.selection()
        if selected_tree_item:
            try:
                self.view.frames["ReportWindow"].menu.tk_popup(
                    event.x_root,
                    event.y_root
                )
            finally:
                self.view.frames["ReportWindow"].menu.grab_release()
