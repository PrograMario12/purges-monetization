''' This module is used to create the widgets of the interface '''

import tkinter as tk
from tkinter import ttk

class WidgetFactory:
    ''' This class is used to create the widgets of the interface '''
    def __init__(self):
        ''' Initialize the class '''
        self.icon = {}

    def create_button(
        self, **kwargs) -> ttk.Button:
        '''Create a button widget'''
        button = ttk.Button(
            kwargs.get('parent'),
            image=kwargs.get('icon'),
            style=kwargs.get('style'),
            command=kwargs.get('command'))
        grid_options = kwargs.get('grid_options') or {}
        button.grid(**grid_options)
        return button

    def create_label(
        self, parent: tk.Widget,
        text: str,
        style: str,
        grid_options: dict,
        **kwargs) -> ttk.Label:
        ''' Create a label widget '''

        label = ttk.Label(
            parent,
            text=text,
            style=style
        )
        label.grid(**grid_options, **kwargs)
        return label

    def create_input(
    self,
    parent: tk.Widget,
    style: str,
    grid_options: dict,
    placeholder: str,
    **kwargs) -> ttk.Entry:
        ''' Create an input widget with placeholder '''
        entry = ttk.Entry(
            parent,
            style=style,
            font=("Arial", 16, "italic"),
            justify="center"
        )
        entry.grid(**grid_options, **kwargs)

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

        return entry

    def create_frame(
    self,
    parent: tk.Widget,
    style: str,
    row: int,
    col: int,
    **kwargs) -> ttk.Frame:
        ''' Create a frame widget '''
        frame = ttk.Frame(parent, style=style)
        frame.grid(row=row, column=col, **kwargs)
        return frame

    def configure_grid(
        self,
        widget: tk.Widget,
        rows: int,
        cols: int,
        grid_options: dict = None
    ):
        '''Configure the grid layout of a widget.'''

        if grid_options is None:
            grid_options = {}

        row_weights = grid_options.get('row_weights') or [1] * rows
        col_weights = grid_options.get('col_weights') or [1] * cols
        min_row_sizes = grid_options.get('min_row_sizes') or [0] * rows
        min_col_sizes = grid_options.get('min_col_sizes') or [0] * cols

        for i in range(rows):
            widget.grid_rowconfigure(
                i,
                weight=row_weights[i],
                minsize=min_row_sizes[i]
            )

        for j in range(cols):
            widget.grid_columnconfigure(
                j,
                weight=col_weights[j],
                minsize=min_col_sizes[j])
