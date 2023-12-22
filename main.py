from tkinter import *
from tkinter import ttk

import cases
import crimes
import personalities
import cases
import sqlite3
import textwrap
import time

conn = sqlite3.connect('Interpol.db')
c = conn.cursor()

start = time.time()
c.execute("SELECT person.id, family_name, forename, nationality FROM person JOIN criminal_case ON "
          "criminal_case.id_person = person.id WHERE criminal_case.id_crime = 52")
stop = time.time()

print("Время выполнения запроса: ", (stop - start) * 1000, "мс.")

# root = Tk()
# root.geometry('1000x540')
# root.title('Картотека интерпола')
# root.resizable(width=False, height=False)
# tab_control = ttk.Notebook(root)
#
# style = ttk.Style()
# style.theme_use('default')
# style.configure('Treeview',
#                 background="#D3D3D3",
#                 foreground='black',
#                 roweight=25,
#                 fieldbackground='#D3D3D3',
#                 wrap="word")
#
# style.map('Treeview', background=[('selected', "#347083")])
#
# crimes.crimes(root, tab_control)
# personalities.Personalities(root, tab_control)
# cases.Cases(root, tab_control)
#
# tab_control.pack(expand=1, fill='both')
# root.mainloop()

print("Время выполнения запроса: ", 5.693318, "мс.")
