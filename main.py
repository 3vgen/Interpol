from tkinter import *
from tkinter import ttk
import crimes
import sqlite3
import textwrap

root = Tk()
root.geometry('1000x500')
root.title('Картотека интерпола')
root.resizable(width=False, height=False)

style = ttk.Style()
style.theme_use('default')
style.configure('Treeview',
                background="#D3D3D3",
                foreground='black',
                roweight=25,
                fieldbackground='#D3D3D3',
                wrap="word")

style.map('Treeview', background=[('selected', "#347083")])

crimes.crimes(root)

root.mainloop()
