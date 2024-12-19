"""
This module contains classes that are used to create and configure
various widgets for a Tkinter-based graphical user interface. The
classes provided include factories for creating buttons, labels, input
fields, and frames, as well as a mixin for applying grid options and a
configurator for setting up grid layouts.
Classes:
    GridOptionsMixin:
        A mixin class that provides a method to apply grid options to a
        widget.
    ButtonFactory:
        A factory class for creating button widgets with optional
        configuration for icon, style, command, and grid options.
    LabelFactory:
        A factory class for creating label widgets with specified text,
        style, and grid options.
    InputFactory:
        A factory class for creating input (entry) widgets with
        specified style, grid options, and placeholder text. It also
        handles placeholder text behavior on focus in and out events.
    FrameFactory:
        A factory class for creating frame widgets with specified style
        and grid options.
    GridConfigurator:
        A class for configuring the grid layout of a widget, allowing
        the specification of row and column weights.
"""

import tkinter as tk
from tkinter import ttk

class GridOptionsMixin:
    """ Mixin class to add grid options to a widget """
    def apply_grid_options(self, widget: tk.Widget, grid_options: dict,
            **kwargs):
        """ Apply grid options to a widget """
        if grid_options:
            widget.grid(**grid_options, **kwargs)

class ButtonFactory:
    """
    A factory class for creating button widgets using the tkinter
    library.
    Methods
    -------
    create(parent: tk.Widget, config: dict = None) -> ttk.Button
        Creates and returns a ttk.Button widget with the specified
        configuration.
    create method
    -------------
    Parameters
    ----------
    parent : tk.Widget
        The parent widget in which the button will be placed.
    config : dict, optional
        A dictionary containing configuration options for the button.
        Possible keys include:
        - 'icon': The image to be displayed on the button (default is None).
        - 'style': The style to be applied to the button (default is None).
        - 'command': The function to be called when the button is clicked
          (default is None).
        - 'grid_options': A dictionary of grid options to be applied to
        the button (default is None).
    Returns
    -------
    ttk.Button
        The created button widget with the specified configuration.
    """
    def create(self, parent: tk.Widget, config: dict = None) -> ttk.Button:
        """ Create a button widget """
        if config is None:
            config = {}
        icon = config.get('icon', None)
        style = config.get('style', None)
        command = config.get('command', None)
        grid_options = config.get('grid_options', None)
        text = config.get('text', None)

        button = ttk.Button(parent, text=text, image=icon, style=style, command=command)
        GridOptionsMixin().apply_grid_options(button, grid_options)
        return button

class LabelFactory:
    """ Class to create label widgets """
    def create(self, parent: tk.Widget, text: str, style: str,
            grid_options: dict, **kwargs) -> ttk.Label:
        """ Create a label widget """
        label = ttk.Label(parent, text=text, style=style)
        GridOptionsMixin().apply_grid_options(label, grid_options, **kwargs)
        return label

class InputFactory:
    """ Class to create input widgets """
    def create(self, parent: tk.Widget, style: str, grid_options: dict,
            placeholder: str, **kwargs) -> ttk.Entry:
        """ Create an input widget """
        entry = ttk.Entry(parent, style=style, font=("Arial", 16, "italic"),
            justify="center")
        GridOptionsMixin().apply_grid_options(entry, grid_options, **kwargs)
        self._add_placeholder(entry, placeholder)
        return entry

    def _add_placeholder(self, entry: ttk.Entry, placeholder: str):
        """ Add placeholder text to an entry widget """
        def on_focus_in(event):
            if entry.get() == placeholder:
                entry.delete(0, tk.END)
                entry.config(foreground='#000000')

        def on_focus_out(event):
            if entry.get() == '':
                entry.insert(0, placeholder)
                entry.config(foreground='grey')

        entry.insert(0, placeholder)
        entry.config(foreground='grey')
        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)

class FrameFactory:
    """ Class to create frame widgets """
    def create(self, parent: tk.Widget, style: str, grid_options: dict, **kwargs) -> ttk.Frame:
        """
        Create a frame widget with specified style and grid options.

        Args:
            parent (tk.Widget): The parent widget to attach the frame to.
            style (str): The style to apply to the frame.
            grid_options (dict): A dictionary of grid options to configure the frame's layout.
            **kwargs: Additional keyword arguments to pass to the grid options.

        Returns:
            ttk.Frame: The created frame widget.
        """
        frame = ttk.Frame(parent, style=style)
        GridOptionsMixin().apply_grid_options(frame, grid_options, **kwargs)
        return frame

class GridConfigurator:
    """ Class to configure the grid of a widget """
    def configure(self, widget: tk.Widget, rows: int, cols: int,
            grid_options: dict = None):
        """ Configure the grid of a widget """
        if grid_options is None:
            grid_options = {}
        for i in range(rows):
            widget.grid_rowconfigure(i, weight=grid_options.get('row_weights',
                [1] * rows)[i])
        for j in range(cols):
            widget.grid_columnconfigure(j, weight=grid_options.get(
                'col_weights', [1] * cols)[j])
