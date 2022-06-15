from cProfile import label
from re import L
from tkinter import *
import sqlite3
from tkinter import messagebox
cr= Tk()
pr=sqlite3.connect("address_book.db")
p=pr.cursor()
# p.execute("""CREATE TABLE addresses(
#     first_name text, 
#     last_name text, 
#     address text, 
#     city text, 
#     state text, 
#     zipcode integer) """)
# print("Table created successfully")
#create text boxes############################3
def submit():
    pr=sqlite3.connect("address_book.db")
    p=pr.cursor()
    p.execute("INSERT INTO addresses VALUES ( :f_name,:l_name, :address, :city, :state, :zipcode)",{
        "f_name":f_name.get(),
        "l_name":l_name.get(),
        "address": address.get(),
        "city":city.get(),
        "state":state.get(),
        "zipcode":zipcode.get()
    })    
    messagebox.showinfo("Address", "Inserted Successfully")
    pr.commit()
    pr.close()
    f_name.delete(0,END)
    l_name.delete(0, END)
    address.delete(0, END)
    city.delete(0,END)
    state.delete(0, END)
    zipcode.delete(0, END)
def query():
    pr = sqlite3.connect("address_book.db")
    p=pr.cursor()
    p.execute("SELECT *, oid FROM addresses")
    records= p.fetchall()
    # print(records)
    print_records=""
    for record in records: 
        print_records+=str(record[0])+""+str(record[1])+""+"\t"+str(record[6])+ "\n" 
    query_label = Label (cr, text=print_records)
    query_label.grid(row=8, column=0, columnspan=2)

    pr.commit()
    pr.close() 

def delete():
    pr = sqlite3.connect("address_book.db")
    p=pr.cursor()

    p.execute("DELETE from addresses WHERE oid="+delete_box.get())
    print("Deleted Successfully")

    delete_box.delete(0, END)
    pr.commit()
    pr.close()


def update():
    pr = sqlite3.connect("address_book.db")
    p=pr.cursor()

    record_id= update_box.get()
    p.execute(""" UPDATE addresses SET
         first_name = :first,
         last_name = :last,
         address = :address,
         city= :city,
         state= :state,
         zipcode= :zipcode
         WHERE oid = :oid""",
         {"first": f_name_editor.get(),
          "last": l_name_editor.get(),
          "address": address_editor.get(),
          "city": city_editor.get(),
          "state": state_editor.get(),
          "zipcode": zipcode_editor.get(),
          "oid": record_id
         })
    pr.commit()
    pr.close()
    editor.destroy()

def edit():
    global editor
    editor=Toplevel()
    editor.title("Updated Data")
    editor.geometry("300x400")
    
    pr = sqlite3.connect("address_book.db")
    p=pr.cursor()
    record_id= update_box.get()
    p.execute("SELECT * FROM addresses WHERE oid="+record_id)
    records= p.fetchall()
    global f_name_editor
    global l_name_editor
    global address_editor
    global city_editor
    global state_editor
    global zipcode_editor

    f_name_editor= Entry(editor,width=30)
    f_name_editor.grid(row=0, column=1, padx=20, pady=(10,0))

    l_name_editor= Entry(editor,width=30)
    l_name_editor.grid(row=1, column=1)

    address_editor = Entry(editor, width=30)
    address_editor.grid(row=2, column=1)

    city_editor=Entry(editor, width=30)
    city_editor.grid(row=3, column=1)

    state_editor=Entry(editor, width=30)
    state_editor.grid(row=4, column=1)

    zipcode_editor=Entry(editor, width=30)
    zipcode_editor.grid(row=5, column=1)

    f_name_label = Label(editor, text="Firstname")
    f_name_label.grid(row=0, column=0)

    l_name_label = Label(editor, text="lastname")
    l_name_label.grid(row=1, column=0)

    address_label = Label(editor, text="address")
    address_label.grid(row=2, column=0)

    city_label = Label(editor, text="city")
    city_label.grid(row=3, column=0)

    state_label = Label(editor, text="state")
    state_label.grid(row=4, column=0)

    zipcode_label = Label(editor, text= "Zipcode")
    zipcode_label.grid(row=5, column=0)

    for record in records:
        f_name_editor.insert(0, record[0])
        l_name_editor.insert(0, record[1])
        address_editor.insert(0, record[2])
        city_editor.insert(0, record[3])
        state_editor.insert(0, record[4])
        zipcode_editor.insert(0, record[5])

    edit_btn = Button(editor, text="SAVE", command= update)
    edit_btn.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=125)

f_name = Entry (cr, width= 30)
f_name.grid(row=0, column=1, padx=20)

l_name=Entry(cr, width= 30)
l_name.grid(row=1, column=1)

address= Entry(cr, width=30)
address.grid(row=2, column=1)

city= Entry(cr, width=30)
city.grid(row=3, column=1)

state= Entry(cr, width=30)
state.grid(row=4, column=1)

zipcode= Entry(cr, width=30)
zipcode.grid(row=5, column=1)

delete_box= Entry(cr, width=30)
delete_box.grid(row=9, column=1, pady=5)

update_box= Entry(cr, width=30)
update_box.grid(row=11, column=1, pady=5)

f_name_label = Label(cr, text="Firstname")
f_name_label.grid(row=0, column=0)

l_name_label = Label(cr, text="lastname")
l_name_label.grid(row=1, column=0)

address_label = Label(cr, text="address")
address_label.grid(row=2, column=0)

city_label = Label(cr, text="city")
city_label.grid(row=3, column=0)

state_label = Label(cr, text="state")
state_label.grid(row=4, column=0)

zipcode_label = Label(cr, text= "Zipcode")
zipcode_label.grid(row=5, column=0)

delete_label= Label(cr, text="Delete ID")
delete_label.grid(row=9,column=0, pady=5)

Update_label= Label(cr, text= "Update ID")
Update_label.grid(row= 11, column=0, pady=5)

submit_btn = Button(cr, text="Add record", command=submit)
submit_btn.grid(row=6, column=0, columnspan= 2, pady=10, padx=10, ipadx=100)

quary_btn = Button(cr, text="Show Records", command=query)
quary_btn.grid(row=7, column=0, columnspan=2,pady=10, padx=10, ipadx= 100)

delete_btn= Button(cr, text="Delete", command= delete)
delete_btn.grid(row=10, column= 0, columnspan= 2, padx=10, pady=10, ipadx=120)

edit_btn= Button(cr, text="Update", command= edit)
edit_btn.grid(row=12, column=0, columnspan=2, padx=10, pady=10, ipadx=120)
pr.commit()
pr.close()
cr.mainloop()