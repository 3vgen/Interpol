from tkinter import *
from tkinter import ttk
import sqlite3
import textwrap


# def open_win():
#     win = Toplevel()
#     win.geometry('200x200+300+300')
#     l = Label(win, text='Toplevel', font='Arial 15 bold', fg='Black').pack()
#     # win.overrideredirect(1)


def on_column_click(event):
    remove_all()
    col_index = my_tree.identify_column(event.x)
    conn = sqlite3.connect('Interpol.db')
    c = conn.cursor()
    global records
    # print("Нажатие на колонку номер", col_index.index(1))
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
            my_tree.insert(parent='', index='end', iid=count, text='',
                           values=(record[0], record[1], record[2], record[3]), tags=('evenrow',))
        else:
            my_tree.insert(parent='', index='end', iid=count, text='',
                           values=(record[0], record[1], record[2], record[3]), tags=('oddrow',))
        count += 1


    conn.commit()
    conn.close()


def remove_all():
    for record in my_tree.get_children():
        my_tree.delete(record)


def update_data():
    conn = sqlite3.connect('Interpol.db')
    c = conn.cursor()
    c.execute(f"SELECT id FROM type_of_crime WHERE name = '{tc_combo.get()}'")
    type_of_crime = c.fetchall()
    # print(type_of_crime[0][0])
    # print(tc_combo.get())

    c.execute(
        "UPDATE crime SET date_of_crime = :date_of_crime, place_of_crime = :place_of_crime, type_c = :type_c WHERE id = :id",
        {
            'id': id_entry.get(),
            'date_of_crime': dc_entry.get(),
            'place_of_crime': pc_entry.get(),
            'type_c': type_of_crime[0][0]
        }
    )

    conn.commit()
    conn.close()
    remove_all()
    record_data()


def delete_data():
    conn = sqlite3.connect('Interpol.db')
    c = conn.cursor()
    c.execute(f"DELETE FROM crime WHERE id = {id_entry.get()}")
    conn.commit()
    conn.close()
    remove_all()
    record_data()


def add_data():
    conn = sqlite3.connect('Interpol.db')
    c = conn.cursor()
    c.execute(f"SELECT id FROM type_of_crime WHERE name = '{tc_combo.get()}'")
    type_of_crime = c.fetchall()
    # print(type_of_crime[0][0])
    # print(tc_combo.get())

    c.execute("INSERT INTO crime (date_of_crime, place_of_crime, type_c) "
              "VALUES (:date_of_crime, :place_of_crime, :type_c)",
              {
                  'date_of_crime': dc_entry.get(),
                  'place_of_crime': pc_entry.get(),
                  'type_c': type_of_crime[0][0]
              }
              )

    conn.commit()
    conn.close()
    remove_all()
    record_data()


def select_record(e):
    dc_entry.delete(0, END)
    id_entry.delete(0, END)
    # tc_entry.delete(0, END)
    pc_entry.delete(0, END)

    selected = my_tree.focus()
    values = my_tree.item(selected, 'values')

    id_entry.insert(0, values[0])
    dc_entry.insert(0, values[1])
    pc_entry.insert(0, values[2])
    tc_combo.set(values[3])


def record_data():
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
            my_tree.insert(parent='', index='end', iid=count, text='',
                           values=(record[0], record[1], record[2], record[3]), tags=('evenrow',))
        else:
            my_tree.insert(parent='', index='end', iid=count, text='',
                           values=(record[0], record[1], record[2], record[3]), tags=('oddrow',))
        count += 1
    conn.commit()
    conn.close()


root = Tk()
root.geometry('1000x500')
root.title('Картотека интерпола')
root.resizable(width=False, height=False)

# Style
style = ttk.Style()
style.theme_use('default')
style.configure('Treeview',
                background="#D3D3D3",
                foreground='black',
                roweight=25,
                fieldbackground='#D3D3D3',
                wrap="word")

style.map('Treeview',
          background=[('selected', "#347083")])

# Create frame
tree_frame = Frame(root)
tree_frame.pack(pady=10)

tree_scroll = Scrollbar(tree_frame)
tree_scroll.pack(side=RIGHT, fill=Y)

my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended", height=10)
my_tree.pack()

tree_scroll.config(command=my_tree.yview)
# Define columns
my_tree['columns'] = ("id", "date_of_crime", "place_of_crime", "type_c")

# Format columns
my_tree.column("#0", width=0, stretch=NO)
my_tree.column("id", anchor=CENTER, width=50, minwidth=40)
my_tree.column("date_of_crime", anchor=CENTER, width=200, minwidth=180)
my_tree.column("place_of_crime", anchor=CENTER, width=200, minwidth=180)
my_tree.column("type_c", anchor=CENTER, width=200, minwidth=200)
# my_tree.column("details", anchor=CENTER, width=200, minwidth=180)

# Create headings
my_tree.heading("#0", text="Label", anchor=W)  # anchor – положение данных в ячейке
my_tree.heading("id", text="id", anchor=CENTER)
my_tree.heading("date_of_crime", text="Дата преступления", anchor=CENTER)
my_tree.heading("place_of_crime", text="Место преступления", anchor=CENTER)
my_tree.heading("type_c", text="Тип преступления", anchor=CENTER)
# my_tree.heading("details", text="Детали", anchor=CENTER)


# Create striped row tags

my_tree.tag_configure('oddrow', background='white')
my_tree.tag_configure('evenrow', background='lightblue')

data_frame = LabelFrame(root, text="Добавить")
data_frame.pack(fill='x', expand=YES, padx=10)

id_label = Label(data_frame, text="Идентификатор")
id_label.grid(row=0, column=0, padx=10, pady=10)
id_entry = Entry(data_frame)
id_entry.grid(row=0, column=1, padx=10, pady=10)

dc_label = Label(data_frame, text="Дата преступления")
dc_label.grid(row=0, column=2, padx=10, pady=10)
dc_entry = Entry(data_frame)
dc_entry.grid(row=0, column=3, padx=10, pady=10)

pc_label = Label(data_frame, text="Место преступления")
pc_label.grid(row=1, column=0, padx=10, pady=10)
pc_entry = Entry(data_frame)
pc_entry.grid(row=1, column=1, padx=10, pady=10)

tc_label = Label(data_frame, text="Тип преступления")
tc_label.grid(row=1, column=2, padx=10, pady=10)
tc_combo = ttk.Combobox(data_frame, width=40, values=['КОРРУПЦИЯ', 'ПОДДЕЛКА ВАЛЮТЫ И ДОКУМЕНТОВ', 'ПРЕСТУПЛЕНИЕ ПРОТИВ ДЕТЕЙ',
                                            'ПРЕСТУПЛЕНИЕ ПРОТИВ КУЛЬТУРНОГО НАСЛЕДИЯ', 'КИБЕР ПРИСТУПЛЕНИЕ',
                                            'НЕЗАКОННЫЙ ОБОРОТ НАРКОТИКОВ', 'ЭКОЛОГИЧЕСКОЕ ПРЕСТУПЛЕНИЕ',
                                            'ФИНАНСОВЫЕ ПРЕСТУПЛЕНИЯ', 'НЕЗАКОННЫЙ ОБОРОТ ОГНЕСТРЕЛЬНОГО ОРУЖИЯ',
                                            'ТОРГОВЛЯ ЛЮДЬМИ И НЕЗАКОННЫЙ ВВОЗ МИГРАНТОВ', 'НЕЗАКОННЫЕ ТОВАРЫ',
                                            'ПРЕСТУПЛЕНИЕ НА МОРЕ', 'ОРГАНИЗОВАННАЯ ПРЕСТУПНОСТЬ', 'ТЕРРОРИЗМ',
                                            'ТРАНСПОРТНОЕ ПРЕСТУПЛЕНИЕ'])
tc_combo.grid(row=1, column=3, padx=10, pady=10)

# Add buttons
button_frame = LabelFrame(root, text="Действия")
button_frame.pack(fill='x', expand=YES, padx=20)

add_button = Button(button_frame, text="Добавить", command=add_data)
add_button.grid(row=0, column=0, padx=10, pady=10)

update_button = Button(button_frame, text="Обновить", command=update_data)
update_button.grid(row=0, column=1, padx=10, pady=10)

remove_button = Button(button_frame, text="Удалить", command=delete_data)
remove_button.grid(row=0, column=2, padx=10, pady=10)

select_button = Button(button_frame, text="Выбрать")
select_button.grid(row=0, column=3, padx=10, pady=10)

my_tree.pack(pady=20)

my_tree.bind("<ButtonRelease-1>", select_record)
my_tree.bind("<Button-1>", on_column_click)

record_data()
root.mainloop()
