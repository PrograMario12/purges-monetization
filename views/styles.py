''' This module contains the styles for the widgets in the application '''
from tkinter import ttk

def apply_styles():
    ''' Apply styles to the widgets '''
    style = ttk.Style()
    style.theme_use("default")
    style.configure("TProjectHeader.TFrame",
                        background="#285C6D",
                        height=100
                    )

    style.configure("TFrame",
                        background="#F9F9F9"
                    )

    style.configure("TProjectHeader.TLabel",
                        background="#285C6D",
                        font = ("Arial", 20, "bold"),
                        foreground="#FFFFFF"
                    )

    style.configure("Project_Label_Title.TLabel",
                        background="#F9F9F9",
                        foreground="#212529",
                        font = ("Arial", 36, "bold"),
                        justify="center"
                    )

    style.configure("Project_Label_Title_2.TLabel",
                        background="#F9F9F9",
                        foreground="#212529",
                        font = ("Arial", 24, "bold"),
                        justify="center"
                    )

    style.configure("TProject_Label_Text.TLabel",
                        background="#F9F9F9",
                        font = ("Arial", 16),
                        foreground="#212529"
                    )

    style.configure("TProject.TButton", background="#6C757D",
                        font = ("Arial", 12),
                        foreground="#FFFFFF",
                        relief="flat",
                        padding=10,
                        borderwidth=0
                    )

    style.configure("Treeview.Heading",
                    font=("Arial", 20, "bold"),
                    background="#285C6D",
                    foreground="#FFFFFF"
                    )

    style.configure("Treeview",
                    background="#E9ECEF",
                    foreground="#000000",
                    fieldbackground="#E9ECEF",
                    font=("Arial", 12),
                    height=10
                    )

    style.configure(
            "TProject_Label_Title.TLabel",
            background="#F9F9F9",
            font=("Arial", 24, "bold"),
            foreground="#212529"
        )

    style.configure(
            "DataEntry.TCombobox",
            fieldbackground="#E9ECEF",
            background="#285C6D",
            foreground="black",
            bordercolor="#285C6D",
            arrowcolor="white",
            arrowsize=20,
            padding=5,
            font=("Arial", 12),
        )

    style.map("Treeview", background=[('selected', '#285C6D')])


    style.configure(
            "Test.TLabel",
            background="#4f3",
            font=("Arial", 24, "bold"),
    )

    style.configure(
        "Test.TFrame",
        background="#4f3",
    )

    return style
