from tkinter import *
from tkinter import ttk
import sqlite3


class CriminalGroup:
    def __init__(self, root, tab_control):
        self.root = root
        self.tab_control = tab_control
        criminal_group_tab = ttk.Frame(self.tab_control)
        tab_control.add(criminal_group_tab, text="Криминальные группировки")

        tree_frame = Frame(criminal_group_tab)
        tree_frame.pack(pady=10)

        tree_scroll = Scrollbar(tree_frame)
        tree_scroll.pack(side=RIGHT, fill=Y)

        self.button_frame = LabelFrame(criminal_group_tab, text="Действия")
        self.data_frame = LabelFrame(criminal_group_tab, text="Данные")

        self.remove_button = None
        self.select_button = None
        self.update_button = None
        self.add_button = None

        self.id_entry = None
        self.id_label = None
        self.name_entry = None
        self.name_label = None
        self.features_entry = None
        self.features_label = None

        self.criminal_group_tree = None
        self.criminal_group_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended",
                                                height=10)
        self.criminal_group_tree.pack()

        tree_scroll.config(command=self.criminal_group_tree.yview)
        # Define columns
        self.criminal_group_tree['columns'] = ("id", "name", "features")
        self.run_criminal_group()

    def search(self):
        query = "SELECT crime.id, date_of_crime, place_of_crime, type_of_crime.name FROM crime JOIN type_of_crime on crime.type_c = type_of_crime.id WHERE 1=1"

        id = self.id_entry.get()
        pc = self.pc_entry.get()
        dc = self.dc_entry.get()
        tc = self.tc_combo.get()
        if tc != "":
            # tc = 'type_c'
            query += f" AND type_c = (SELECT id FROM type_of_crime WHERE name = '{tc}')"

        if id != "":
            # id = 'id'
            query += f" AND crime.id = {id}"

        if dc != "":
            # dc = 'date_of_crime'
            query += f" AND date_of_crime = '{dc}'"

        if pc != "":
            # pc = 'place_of_crime'
            query += f" AND place_of_crime = '{pc}'"

        conn = sqlite3.connect('Interpol.db')

        c = conn.cursor()
        c.execute(query)
        records = c.fetchall()
        # print(records)

        self.remove_all()
        global count
        count = 0
        for record in records:
            if count % 2 == 0:
                self.criminal_group_tree.insert(parent='', index='end', iid=count, text='',
                                                values=(record[0], record[1], record[2], record[3]), tags=('evenrow',))
            else:
                self.criminal_group_tree.insert(parent='', index='end', iid=count, text='',
                                                values=(record[0], record[1], record[2], record[3]), tags=('oddrow',))
            count += 1
        count = 0

        conn.commit()
        conn.close()

    def on_column_click(self, event):
        self.remove_all()
        col_index = self.criminal_group_tree.identify_column(event.x)
        conn = sqlite3.connect('Interpol.db')
        c = conn.cursor()
        global records
        # print("Нажатие на колонку номер", col_index.index(1))
        if col_index == '#1':
            c.execute("""SELECT crime.id, date_of_crime, place_of_crime, type_of_crime.name
                           FROM crime
                           join type_of_crime on crime.type_c = type_of_crime.id order by crime.id;
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
                self.criminal_group_tree.insert(parent='', index='end', iid=count, text='',
                                                values=(record[0], record[1], record[2], record[3]), tags=('evenrow',))
            else:
                self.criminal_group_tree.insert(parent='', index='end', iid=count, text='',
                                                values=(record[0], record[1], record[2], record[3]), tags=('oddrow',))
            count += 1

        conn.commit()
        conn.close()

    def remove_all(self):
        for record in self.criminal_group_tree.get_children():
            self.criminal_group_tree.delete(record)

    def update_data(self):
        conn = sqlite3.connect('Interpol.db')
        c = conn.cursor()
        c.execute(f"SELECT id FROM type_of_crime WHERE name = '{self.tc_combo.get()}'")
        type_of_crime = c.fetchall()
        # print(type_of_crime[0][0])
        # print(tc_combo.get())

        c.execute(
            "UPDATE crime SET date_of_crime = :date_of_crime, place_of_crime = :place_of_crime, type_c = :type_c WHERE id = :id",
            {
                'id': self.id_entry.get(),
                'date_of_crime': self.dc_entry.get(),
                'place_of_crime': self.pc_entry.get(),
                'type_c': type_of_crime[0][0]
            }
        )

        conn.commit()
        conn.close()
        self.remove_all()
        self.record_data()

    def delete_case(self):
        conn = sqlite3.connect('Interpol.db')
        c = conn.cursor()
        c.execute(f"DELETE FROM criminal_case WHERE id = {self.id_entry.get()}")
        c.execute(f"UPDATE person SET status = 'На свободе' WHERE id = {self.id_person_entry.get()}")
        conn.commit()
        conn.close()
        self.remove_all()
        self.record_data()

    def close_case(self):
        conn = sqlite3.connect('Interpol.db')
        c = conn.cursor()

        c.execute(f"UPDATE person SET status = 'Отбывает срок' WHERE id = {self.id_person_entry.get()}")
        c.execute(f"UPDATE criminal_case SET status = 'ЗАКРЫТО' WHERE id = {self.id_entry.get()}")
        conn.commit()
        conn.close()
        self.remove_all()
        self.record_data()

    def make_case(self):
        conn = sqlite3.connect('Interpol.db')
        c = conn.cursor()

        c.execute("INSERT INTO criminal_case (id_person, id_crime, details) VALUES (:id_person,:id_crime, :details)",
                  {
                      'id_crime': self.id_crime_entry.get(),
                      'id_person': self.id_person_entry.get(),
                      'details': self.features_entry.get('1.0', END)
                  }
                  )

        c.execute(f"UPDATE person SET status = 'В розыске' WHERE id = {self.id_person_entry.get()}")

        conn.commit()
        conn.close()
        self.remove_all()
        self.record_data()

    def select_record(self, event):
        self.id_entry.delete(0, END)
        self.name_entry.delete(0, END)
        self.features_entry.delete('1.0', END)

        selected = self.criminal_group_tree.focus()
        values = self.criminal_group_tree.item(selected, 'values')
        self.id_entry.insert(0, values[0])
        self.name_entry.insert(0, values[1])
        self.features_entry.insert('1.0', values[2])
        # self.status_entry.insert(0, values[5])

    def record_data(self):
        conn = sqlite3.connect('Interpol.db')
        c = conn.cursor()
        # c.execute("""SELECT criminal_case.id, id_crime, id_person, employee.name, status, details
        #     FROM criminal_case
        #     join employee on criminal_case.id_employee = employee.id;
        #     """)

        c.execute("""SELECT * 
                    FROM criminal_group;
                    """)
        records = c.fetchall()
        # print(records)
        global count
        count = 0
        for record in records:
            if count % 2 == 0:
                self.criminal_group_tree.insert(parent='', index='end', iid=count, text='',
                                                values=(
                                                    record[0], record[1], record[2]),
                                                tags=('evenrow',))
            else:
                self.criminal_group_tree.insert(parent='', index='end', iid=count, text='',
                                                values=(
                                                    record[0], record[1], record[2]),
                                                tags=('oddrow',))
            count += 1
        count = 0
        conn.commit()
        conn.close()

    def run_criminal_group(self):
        self.criminal_group_tree.column("#0", width=0, stretch=NO)
        self.criminal_group_tree.column("id", anchor=CENTER, width=50, minwidth=40)
        self.criminal_group_tree.column("name", anchor=CENTER, width=120, minwidth=120)
        self.criminal_group_tree.column("features", anchor=CENTER, width=500, minwidth=500)

        # Create headings
        self.criminal_group_tree.heading("#0", text="Label", anchor=W)  # anchor – положение данных в ячейке
        self.criminal_group_tree.heading("id", text="id", anchor=CENTER)
        self.criminal_group_tree.heading("name", text="Название", anchor=CENTER)
        self.criminal_group_tree.heading("features", text="Особенности", anchor=CENTER)

        # Create striped row tags

        self.criminal_group_tree.tag_configure('oddrow', background='white')
        self.criminal_group_tree.tag_configure('evenrow', background='lightblue')

        self.data_frame.pack(fill='x', expand=YES, padx=10)

        self.id_label = Label(self.data_frame, text="Идентификатор")
        self.id_label.grid(row=0, column=0, padx=10, pady=10, sticky='W')
        self.id_entry = Entry(self.data_frame)
        self.id_entry.grid(row=0, column=1, padx=10, pady=10, sticky='W')

        self.name_label = Label(self.data_frame, text="Название")
        self.name_label.grid(row=0, column=2, padx=10, pady=10, sticky='N')
        self.name_entry = Entry(self.data_frame)
        self.name_entry.grid(row=0, column=3, padx=10, pady=10, sticky='N')

        self.features_label = Label(self.data_frame, text="Особенности")
        self.features_label.grid(row=1, column=0, padx=10, pady=10, sticky='W')
        self.features_entry = Text(self.data_frame, height=5, width=100)
        self.features_entry.grid(row=1, column=1, padx=10, pady=10, sticky='W')

        # Add buttons
        self.button_frame.pack(fill='x', expand=YES, padx=20)

        self.add_button = Button(self.button_frame, text="Добавить", command=self.make_case)
        self.add_button.grid(row=0, column=0, padx=10, pady=10)

        self.update_button = Button(self.button_frame, text="Обновить", command=self.update_data)
        self.update_button.grid(row=0, column=1, padx=10, pady=10)

        self.remove_button = Button(self.button_frame, text="Удалить", command=self.delete_case)
        self.remove_button.grid(row=0, column=2, padx=10, pady=10)

        self.select_button = Button(self.button_frame, text="Поиск", command=self.search)
        self.select_button.grid(row=0, column=3, padx=10, pady=10)

        self.criminal_group_tree.pack(pady=20)

        self.criminal_group_tree.bind("<ButtonRelease-1>", self.select_record)
        # self.criminal_case_tree.bind("<Button-1>", self.on_column_click)
        # self.criminal_case_tree.bind("<ButtonRelease-2>", self.remove_all())

        self.record_data()
