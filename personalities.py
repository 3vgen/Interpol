from tkinter import *
from tkinter import ttk
import sqlite3
import textwrap


class SubRoot:
    def __init__(self, id_):
        self.id = id_
        print(self.id)
        self.label = None
        self.win = None

    def run(self):
        self.win = Toplevel()
        self.win.geometry('600x400')
        self.label = Label(self.win, text='Личные данные преступника', font='Arial 15 bold', fg='Black')
        self.label.pack()


# def open_win():
#     win = Toplevel()
#     win.geometry('600x400')
#     l = Label(win, text='Toplevel', font='Arial 15 bold', fg='Black').pack()
#     # win.overrideredirect(1)


class Personalities:
    def __init__(self, root, tab_control):
        self.sb_rt = None
        self.root = root
        self.tab_control = tab_control
        person_tab = ttk.Frame(self.tab_control)
        tab_control.add(person_tab, text="Люди")

        tree_frame = Frame(person_tab)
        tree_frame.pack(pady=10)

        tree_scroll = Scrollbar(tree_frame)
        tree_scroll.pack(side=RIGHT, fill=Y)

        self.button_frame = LabelFrame(person_tab, text="Действия")
        self.data_frame = LabelFrame(person_tab, text="Данные")

        self.remove_button = None
        self.select_button = None
        self.update_button = None
        self.add_button = None
        self.f_entry = None
        self.n_entry = None
        self.n_label = None
        self.id_entry = None
        self.id_label = None
        self.person_tree = None
        self.f_label = None
        self.db_label = None
        self.db_entry = None
        self.nt_label = None
        self.nt_entry = None

        self.person_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended", height=10)
        self.person_tree.pack()

        tree_scroll.config(command=self.person_tree.yview)
        # Define columns
        self.person_tree['columns'] = ("id", "forename", "family_name", "date_of_birth", "nationality")
        self.run_personalities()

    def on_column_click(self, event):
        self.remove_all()
        col_index = self.person_tree.identify_column(event.x)
        conn = sqlite3.connect('Interpol.db')
        c = conn.cursor()
        global records
        # print("Нажатие на колонку номер", col_index.index(1))
        if col_index == '#1':
            c.execute("""SELECT *
                           FROM person
                           OREDER BY id;
                           """)
            records = c.fetchall()
        if col_index == '#2':
            c.execute("""SELECT crime.id, date_of_crime, place_of_crime, type_of_crime.name
                    FROM crime
                    join type_of_crime on crime.type_c = type_of_crime.id order by date_of_crime desc;
                    """)
            records = c.fetchall()

        if col_index == '#3':
            c.execute("""SELECT crime.id, date_of_crime, place_of_crime, type_of_crime.name
                    FROM crime
                    join type_of_crime on crime.type_c = type_of_crime.id order by place_of_crime;
                    """)
            records = c.fetchall()

        if col_index == '#4':
            c.execute("""SELECT crime.id, date_of_crime, place_of_crime, type_of_crime.name
                    FROM crime
                    join type_of_crime on crime.type_c = type_of_crime.id order by type_c;
                    """)
            records = c.fetchall()

        global count
        count = 0
        for record in records:
            if count % 2 == 0:
                self.person_tree.insert(parent='', index='end', iid=count, text='',
                                        values=(record[0], record[1], record[2], record[3]), tags=('evenrow',))
            else:
                self.person_tree.insert(parent='', index='end', iid=count, text='',
                                        values=(record[0], record[1], record[2], record[3]), tags=('oddrow',))
            count += 1

        conn.commit()
        conn.close()

    def remove_all(self):
        for record in self.person_tree.get_children():
            self.person_tree.delete(record)

    def update_data(self):
        conn = sqlite3.connect('Interpol.db')
        c = conn.cursor()
        # print(type_of_crime[0][0])
        # print(tc_combo.get())

        c.execute(
            "UPDATE person SET forename = :forename, family_name = :family_name, date_of_birth = :date_of_birth, "
            "nationality = :nationality WHERE id = :id",
            {
                'forename': self.n_entry.get(),
                'family_name': self.f_entry.get(),
                'date_of_birth': self.db_entry.get(),
                'nationality': self.nt_entry.get(),
                'id': self.id_entry.get()

            }
        )

        conn.commit()
        conn.close()
        self.remove_all()
        self.record_data()

    def delete_data(self):
        conn = sqlite3.connect('Interpol.db')
        c = conn.cursor()
        c.execute(f"DELETE FROM person WHERE id = {self.id_entry.get()}")
        conn.commit()
        conn.close()
        self.remove_all()
        self.record_data()

    def add_data(self):
        conn = sqlite3.connect('Interpol.db')
        c = conn.cursor()

        c.execute("INSERT INTO person (forename, family_name, nationality, date_of_birth) "
                  "VALUES (:forename, :family_name, :nationality, :date_of_birth)",
                  {
                      'forename': self.n_entry.get(),
                      'family_name': self.f_entry.get(),
                      'nationality': self.nt_entry.get(),
                      'date_of_birth': self.db_entry.get(),

                  }
                  )

        conn.commit()
        conn.close()
        self.remove_all()
        self.record_data()

    def select_record(self, event):
        self.id_entry.delete(0, END)
        self.n_entry.delete(0, END)
        self.f_entry.delete(0, END)
        self.db_entry.delete(0, END)
        self.nt_entry.delete(0, END)

        selected = self.person_tree.focus()
        values = self.person_tree.item(selected, 'values')

        self.id_entry.insert(0, values[0])
        self.n_entry.insert(0, values[1])
        self.f_entry.insert(0, values[2])
        self.db_entry.insert(0, values[3])
        self.nt_entry.insert(0, values[4])
        self.sb_rt = SubRoot(self.id_entry.get())

    def record_data(self):
        conn = sqlite3.connect('Interpol.db')
        c = conn.cursor()
        c.execute("""SELECT * FROM person""")
        records = c.fetchall()
        global count
        count = 0
        for record in records:
            if count % 2 == 0:
                self.person_tree.insert(parent='', index='end', iid=count, text='',
                                        values=(record[0], record[1], record[2], record[3], record[4]),
                                        tags=('evenrow',))
            else:
                self.person_tree.insert(parent='', index='end', iid=count, text='',
                                        values=(record[0], record[1], record[2], record[3], record[4]),
                                        tags=('oddrow',))
            count += 1
        count = 0
        conn.commit()
        conn.close()

    # Style

    # Create frame

    # Format columns
    def run_personalities(self):
        self.person_tree.column("#0", width=0, stretch=NO)
        self.person_tree.column("id", anchor=CENTER, width=50, minwidth=40)
        self.person_tree.column("forename", anchor=CENTER, width=120, minwidth=120)
        self.person_tree.column("family_name", anchor=CENTER, width=120, minwidth=120)
        self.person_tree.column("date_of_birth", anchor=CENTER, width=130, minwidth=130)
        self.person_tree.column("nationality", anchor=CENTER, width=250, minwidth=250)

        # Create headings
        self.person_tree.heading("#0", text="Label", anchor=W)  # anchor – положение данных в ячейке
        self.person_tree.heading("id", text="id", anchor=CENTER)
        self.person_tree.heading("forename", text="Имя", anchor=CENTER)
        self.person_tree.heading("family_name", text="Фамилия", anchor=CENTER)
        self.person_tree.heading("date_of_birth", text="Дата рождения", anchor=CENTER)
        self.person_tree.heading("nationality", text="Национальность", anchor=CENTER)

        # my_tree.heading("details", text="Детали", anchor=CENTER)

        # Create striped row tags

        self.person_tree.tag_configure('oddrow', background='white')
        self.person_tree.tag_configure('evenrow', background='lightblue')

        self.data_frame.pack(fill='x', expand=YES, padx=10)

        self.id_label = Label(self.data_frame, text="Идентификатор")
        self.id_label.grid(row=0, column=0, padx=10, pady=10)
        self.id_entry = Entry(self.data_frame)
        self.id_entry.grid(row=0, column=1, padx=10, pady=10)

        self.n_label = Label(self.data_frame, text="Имя")
        self.n_label.grid(row=0, column=2, padx=10, pady=10)
        self.n_entry = Entry(self.data_frame)
        self.n_entry.grid(row=0, column=3, padx=10, pady=10)

        self.f_label = Label(self.data_frame, text="Фамилия")
        self.f_label.grid(row=1, column=0, padx=10, pady=10)
        self.f_entry = Entry(self.data_frame)
        self.f_entry.grid(row=1, column=1, padx=10, pady=10)

        self.db_label = Label(self.data_frame, text="Дата рождения")
        self.db_label.grid(row=1, column=2, padx=10, pady=10)
        self.db_entry = Entry(self.data_frame)
        self.db_entry.grid(row=1, column=3, padx=10, pady=10)

        self.nt_label = Label(self.data_frame, text="Национальность")
        self.nt_label.grid(row=1, column=4, padx=10, pady=10)
        self.nt_entry = Entry(self.data_frame)
        self.nt_entry.grid(row=1, column=5, padx=10, pady=10)

        # Add buttons
        self.button_frame.pack(fill='x', expand=YES, padx=20)

        self.add_button = Button(self.button_frame, text="Добавить", command=self.add_data)
        self.add_button.grid(row=0, column=0, padx=10, pady=10)

        self.update_button = Button(self.button_frame, text="Обновить", command=self.update_data)
        self.update_button.grid(row=0, column=1, padx=10, pady=10)

        self.remove_button = Button(self.button_frame, text="Удалить", command=self.delete_data)
        self.remove_button.grid(row=0, column=2, padx=10, pady=10)

        self.sb_rt = SubRoot(self.id_entry.get())
        self.select_button = Button(self.button_frame, text="Открыть подробную информацию", command=self.sb_rt.run)
        self.select_button.grid(row=0, column=3, padx=10, pady=10)

        self.person_tree.pack(pady=20)

        self.person_tree.bind("<ButtonRelease-1>", self.select_record)
        # self.person_tree.bind("<Button-1>", self.on_column_click)
        # self.person_tree.bind("<ButtonRelease-2>", self.prprpr())
        self.record_data()
