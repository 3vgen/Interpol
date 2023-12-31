from tkinter import *
from tkinter import ttk

import cases
import crimes
import criminal_group
import personalities
import cases
import sqlite3
import textwrap
import time


root = Tk()
root.geometry('1100x540')
root.title('Картотека интерпола')
root.resizable(width=False, height=False)
tab_control = ttk.Notebook(root)

style = ttk.Style()
style.theme_use('default')
style.configure('Treeview',
                background="#D3D3D3",
                foreground='black',
                roweight=25,
                fieldbackground='#D3D3D3',
                wrap="word")

style.map('Treeview', background=[('selected', "#347083")])

crimes.crimes(root, tab_control)
personalities.Personalities(root, tab_control)
cases.Cases(root, tab_control)
criminal_group.CriminalGroup(root, tab_control)

tab_control.pack(expand=1, fill='both')
root.mainloop()


