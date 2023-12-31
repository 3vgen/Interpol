import tkinter.messagebox
from tkinter import *
from tkinter import ttk
import sqlite3
import textwrap


# def open_win():
#     win = Toplevel()
#     win.geometry('200x200+300+300')
#     l = Label(win, text='Toplevel', font='Arial 15 bold', fg='Black').pack()
#     # win.overrideredirect(1)

class crimes:
    def __init__(self, root, tab_control):
        self.show_all_data_button = None
        self.show_my_crimes_button = None
        self.current_user = 2
        self.label_cr = None
        self.label = None
        self.win = None
        self.root = root
        self.tab_control = tab_control
        crime_tab = ttk.Frame(self.tab_control)
        tab_control.add(crime_tab, text="Преступления")

        tree_frame = Frame(crime_tab)
        tree_frame.pack(pady=10)

        tree_scroll = Scrollbar(tree_frame)
        tree_scroll.pack(side=RIGHT, fill=Y)

        self.button_frame = LabelFrame(crime_tab, text="Действия")
        self.data_frame = LabelFrame(crime_tab, text="Данные")

        self.tc_label = None
        self.remove_button = None
        self.tc_combo = None
        self.select_button = None
        self.update_button = None
        self.add_button = None
        self.pc_entry = None
        self.dc_entry = None
        self.dc_label = None
        self.id_entry = None
        self.id_label = None
        self.my_tree = None
        self.pc_label = None

        self.my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended", height=10)
        self.my_tree.pack()

        tree_scroll.config(command=self.my_tree.yview)
        # Define columns
        self.my_tree['columns'] = ("id", "date_of_crime", "place_of_crime", "type_c")
        self.run_crimes()

    def show_all_data(self):
        self.remove_all()
        self.record_data()

    def show_my_crimes(self):
        self.remove_all()
        conn = sqlite3.connect('Interpol.db')
        c = conn.cursor()
        c.execute(f"""SELECT crime.id, date_of_crime, place_of_crime, type_of_crime.name
                    FROM crime
                    join type_of_crime on crime.type_c = type_of_crime.id
                    WHERE userlabel = '{self.current_user}';
                    """)
        records = c.fetchall()

        global count
        count = 0
        for record in records:
            if count % 2 == 0:
                self.my_tree.insert(parent='', index='end', iid=count, text='',
                                    values=(record[0], record[1], record[2], record[3]), tags=('evenrow',))
            else:
                self.my_tree.insert(parent='', index='end', iid=count, text='',
                                    values=(record[0], record[1], record[2], record[3]), tags=('oddrow',))
            count += 1
        count = 0
        conn.commit()
        conn.close()

    def show_criminals(self):
        conn = sqlite3.connect('Interpol.db')
        c = conn.cursor()
        self.win = Toplevel()
        self.win.geometry('800x1000')
        self.label = Label(self.win, text='Участники преступления', font='Arial 15 bold', fg='Black')
        self.label.pack()
        self.data_frame = LabelFrame(self.win, text="Данные", background='#B6D7E4')
        self.data_frame.pack()
        c.execute("SELECT person.id, family_name, forename, nationality FROM person JOIN criminal_case ON "
                  "criminal_case.id_person = person.id WHERE criminal_case.id_crime = 52")
        records = c.fetchall()
        print(records[0][0])
        text = ""
        for record in records:
            for rc in record:
                text += str(rc) + " "
            text += '\n\n\n'
        label = Label(self.data_frame, text=text, font='Arial 14')
        label.pack()
        # self.label_cr = Label(self.data_frame, font='Arial 15 bold', fg='Black')
        conn.commit()
        conn.close()

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
                self.my_tree.insert(parent='', index='end', iid=count, text='',
                                    values=(record[0], record[1], record[2], record[3]), tags=('evenrow',))
            else:
                self.my_tree.insert(parent='', index='end', iid=count, text='',
                                    values=(record[0], record[1], record[2], record[3]), tags=('oddrow',))
            count += 1
        count = 0

        conn.commit()
        conn.close()

    def on_column_click(self, event):
        self.remove_all()
        col_index = self.my_tree.identify_column(event.x)
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
                self.my_tree.insert(parent='', index='end', iid=count, text='',
                                    values=(record[0], record[1], record[2], record[3]), tags=('evenrow',))
            else:
                self.my_tree.insert(parent='', index='end', iid=count, text='',
                                    values=(record[0], record[1], record[2], record[3]), tags=('oddrow',))
            count += 1

        conn.commit()
        conn.close()

    def remove_all(self):
        for record in self.my_tree.get_children():
            self.my_tree.delete(record)

    def update_data(self):
        conn = sqlite3.connect('Interpol.db')
        c = conn.cursor()
        c.execute(f"SELECT id_role FROM employee WHERE id = {self.current_user}")
        role = c.fetchone()[0]
        c.execute(f"SELECT userlabel FROM crime WHERE id = {self.id_entry.get()}")
        user = c.fetchone()[0]

        if (role == 1 or role == 2) and self.current_user == user:
            result = tkinter.messagebox.askquestion("Подтверждение действия",
                                                    "Вы уверены, что хотите изменить данное преступление")
            if result == "yes":
                c.execute(f"SELECT id FROM type_of_crime WHERE name = '{self.tc_combo.get()}'")
                type_of_crime = c.fetchall()
                c.execute(
                    "UPDATE crime SET date_of_crime = :date_of_crime, place_of_crime = :place_of_crime, type_c = :type_c "
                    "WHERE id = :id",
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

        else:
            tkinter.messagebox.showwarning(
                message="Внимание, вы не можете изменять эти данные")

    def delete_data(self):
        result = tkinter.messagebox.askquestion("Подтверждение действия",
                                                "Вы уверены, что хотите удалить данное преступление")
        if result == "yes":
            conn = sqlite3.connect('Interpol.db')
            c = conn.cursor()
            c.execute(f"DELETE FROM crime WHERE id = {self.id_entry.get()}")
            conn.commit()
            conn.close()
            self.remove_all()
            self.record_data()

    def add_data(self):
        conn = sqlite3.connect('Interpol.db')
        c = conn.cursor()
        c.execute(f"SELECT id_role FROM employee WHERE id = {self.current_user}")
        role = c.fetchone()[0]
        if role == 1 or role == 2:
            result = tkinter.messagebox.askquestion("Подтверждение действия", "Вы уверены, что хотите добавить данное преступление")
            if result == "yes":
                c.execute(f"SELECT id FROM type_of_crime WHERE name = '{self.tc_combo.get()}'")
                type_of_crime = c.fetchall()
                c.execute("INSERT INTO crime (date_of_crime, place_of_crime, type_c, userlabel) "
                          "VALUES (:date_of_crime, :place_of_crime, :type_c, :userlabel)",
                          {
                              'date_of_crime': self.dc_entry.get(),
                              'place_of_crime': self.pc_entry.get(),
                              'type_c': type_of_crime[0][0],
                              'userlabel': self.current_user
                          }
                          )

                self.remove_all()
                self.record_data()
                conn.commit()
                conn.close()


        else:
            tkinter.messagebox.showwarning(
                message="Внимание, вы не являетесь криминалистом, поэтому не можете регистрировать "
                        "новые преступления")

    def select_record(self, event):
        self.dc_entry.delete(0, END)
        self.id_entry.delete(0, END)
        self.tc_combo.set("")
        self.pc_entry.delete(0, END)

        selected = self.my_tree.focus()
        values = self.my_tree.item(selected, 'values')

        self.id_entry.insert(0, values[0])
        self.dc_entry.insert(0, values[1])
        self.pc_entry.insert(0, values[2])
        self.tc_combo.set(values[3])

    def record_data(self):
        conn = sqlite3.connect('Interpol.db')
        c = conn.cursor()
        c.execute("""SELECT crime.id, date_of_crime, place_of_crime, type_of_crime.name
            FROM crime
            join type_of_crime on crime.type_c = type_of_crime.id;
            """)
        records = c.fetchall()

        global count
        count = 0
        for record in records:
            if count % 2 == 0:
                self.my_tree.insert(parent='', index='end', iid=count, text='',
                                    values=(record[0], record[1], record[2], record[3]), tags=('evenrow',))
            else:
                self.my_tree.insert(parent='', index='end', iid=count, text='',
                                    values=(record[0], record[1], record[2], record[3]), tags=('oddrow',))
            count += 1
        count = 0
        conn.commit()
        conn.close()

    # Style

    # Create frame

    # Format columns
    def run_crimes(self):
        self.my_tree.column("#0", width=0, stretch=NO)
        self.my_tree.column("id", anchor=CENTER, width=50, minwidth=40)
        self.my_tree.column("date_of_crime", anchor=CENTER, width=120, minwidth=120)
        self.my_tree.column("place_of_crime", anchor=CENTER, width=130, minwidth=130)
        self.my_tree.column("type_c", anchor=CENTER, width=250, minwidth=250)
        # my_tree.column("details", anchor=CENTER, width=200, minwidth=180)

        # Create headings
        self.my_tree.heading("#0", text="Label", anchor=W)  # anchor – положение данных в ячейке
        self.my_tree.heading("id", text="id", anchor=CENTER)
        self.my_tree.heading("date_of_crime", text="Дата преступления", anchor=CENTER)
        self.my_tree.heading("place_of_crime", text="Место преступления", anchor=CENTER)
        self.my_tree.heading("type_c", text="Тип преступления", anchor=CENTER)
        # my_tree.heading("details", text="Детали", anchor=CENTER)

        # Create striped row tags

        self.my_tree.tag_configure('oddrow', background='white')
        self.my_tree.tag_configure('evenrow', background='lightblue')

        self.data_frame.pack(fill='x', expand=YES, padx=10)

        self.id_label = Label(self.data_frame, text="Идентификатор")
        self.id_label.grid(row=0, column=0, padx=10, pady=10)
        self.id_entry = Entry(self.data_frame)
        self.id_entry.grid(row=0, column=1, padx=10, pady=10)

        self.dc_label = Label(self.data_frame, text="Дата преступления")
        self.dc_label.grid(row=0, column=2, padx=10, pady=10)
        self.dc_entry = Entry(self.data_frame)
        self.dc_entry.grid(row=0, column=3, padx=10, pady=10)

        self.pc_label = Label(self.data_frame, text="Место преступления")
        self.pc_label.grid(row=1, column=0, padx=10, pady=10)
        self.pc_entry = Entry(self.data_frame)
        self.pc_entry.grid(row=1, column=1, padx=10, pady=10)

        self.tc_label = Label(self.data_frame, text="Тип преступления")
        self.tc_label.grid(row=1, column=2, padx=10, pady=10)
        self.tc_combo = ttk.Combobox(self.data_frame, width=40,
                                     values=['КОРРУПЦИЯ', 'ПОДДЕЛКА ВАЛЮТЫ И ДОКУМЕНТОВ', 'ПРЕСТУПЛЕНИЕ ПРОТИВ ДЕТЕЙ',
                                             'ПРЕСТУПЛЕНИЕ ПРОТИВ КУЛЬТУРНОГО НАСЛЕДИЯ', 'КИБЕР ПРИСТУПЛЕНИЕ',
                                             'НЕЗАКОННЫЙ ОБОРОТ НАРКОТИКОВ', 'ЭКОЛОГИЧЕСКОЕ ПРЕСТУПЛЕНИЕ',
                                             'ФИНАНСОВЫЕ ПРЕСТУПЛЕНИЯ', 'НЕЗАКОННЫЙ ОБОРОТ ОГНЕСТРЕЛЬНОГО ОРУЖИЯ',
                                             'ТОРГОВЛЯ ЛЮДЬМИ И НЕЗАКОННЫЙ ВВОЗ МИГРАНТОВ', 'НЕЗАКОННЫЕ ТОВАРЫ',
                                             'ПРЕСТУПЛЕНИЕ НА МОРЕ', 'ОРГАНИЗОВАННАЯ ПРЕСТУПНОСТЬ', 'ТЕРРОРИЗМ',
                                             'ТРАНСПОРТНОЕ ПРЕСТУПЛЕНИЕ'])
        self.tc_combo.grid(row=1, column=3, padx=10, pady=10)

        # Add buttons
        self.button_frame.pack(fill='x', expand=YES, padx=20)

        self.add_button = Button(self.button_frame, text="Добавить", command=self.add_data)
        self.add_button.grid(row=0, column=0, padx=10, pady=10)

        self.update_button = Button(self.button_frame, text="Обновить", command=self.update_data)
        self.update_button.grid(row=0, column=1, padx=10, pady=10)

        self.remove_button = Button(self.button_frame, text="Удалить", command=self.delete_data)
        self.remove_button.grid(row=0, column=2, padx=10, pady=10)

        self.select_button = Button(self.button_frame, text="Поиск", command=self.search)
        self.select_button.grid(row=0, column=3, padx=10, pady=10)

        self.select_button = Button(self.button_frame, text="Посмотреть подельников", command=self.show_criminals)
        self.select_button.grid(row=0, column=4, padx=10, pady=10)

        self.show_my_crimes_button = Button(self.button_frame, text="Посмотреть мои преступления", command=self.show_my_crimes)
        self.show_my_crimes_button.grid(row=0, column=5, padx=10, pady=10)

        self.show_all_data_button = Button(self.button_frame, text="Все данные", command=self.show_all_data)
        self.show_all_data_button.grid(row=0, column=6, padx=10, pady=10)

        self.my_tree.pack(pady=20)

        self.my_tree.bind("<ButtonRelease-1>", self.select_record)
        # self.my_tree.bind("<Button-1>", self.on_column_click)
        # self.my_tree.bind("<ButtonRelease-2>", self.remove_all())

        self.record_data()
