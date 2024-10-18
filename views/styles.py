''' This module contains the styles for the widgets in the application '''
import tkinter.ttk as ttk

def apply_styles():
    ''' Apply styles to the widgets '''
    style = ttk.Style()
    style.theme_use("default")
    style.configure("TProjectHeader.TFrame",
                        background="#285C6D"
                    )
    style.configure("TProjectHeader.TLabel",
                        background="#285C6D",
                        font = ("Arial", 20, "bold"),
                        foreground="#FFFFFF"
                    )
    style.configure("TProject.TFrame", background="#F9F9F9")
    style.configure("TProject_Label_Title.TLabel",
                        background="#F9F9F9",
                        foreground="#212529",
                        font = ("Arial", 20, "bold")
                    )
    style.configure("TProject_Label_Text.TLabel",
                        background="#F9F9F9",
                        font = ("Arial", 16),
                        foreground="#212529"
                    )
    style.configure("TProject.TButton", background="#6C757D",
                        font = ("Arial", 16),
                        foreground="#FFFFFF",
                        width=20,
                        height=10
                    )
    style.configure("Treeview.Heading",
                    font=("Arial", 14, "bold"),
                    background="#E9ECEF",
                    foreground="#000000"
                    )
    style.configure("Treeview",
                    background="#E9ECEF",
                    foreground="#000000",
                    fieldbackground="#E9ECEF",
                    font=("Arial", 12),
                    height=10
                    )

    style.map("Treeview", background=[('selected', '#285C6D')])
