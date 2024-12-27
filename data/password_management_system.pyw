import customtkinter
from tkinter import *
from tkinter import ttk,filedialog
from tkinter import messagebox
from PIL import ImageTk,Image
import time
import pymysql
import pandas

def xor_encrypt_decrypt(text, key):
    return ''.join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(text))
key = "mysecretkey"

def clock():
    date = time.strftime("%d/%m/%Y")
    current_time = time.strftime("%H:%M:%S")
    date_time_label.config(text=f' Date : {date}\nTime : {current_time}',foreground="red")
    date_time_label.after(1000,clock)

def connect_database():
    if (len(connection_test)==0):
        def connect():
            global mycurser,con
            try:
                a.append(0)
                con=pymysql.connect(host=hostname_entry.get(),user=username_entry.get(),password=password_entry.get())
                mycurser = con.cursor()
                connect_button.destroy()

            except:
                messagebox.showerror("Error","Invalid Details")
                return

            try :
                query = "create database pas"
                mycurser.execute(query)
                query = "create table passwords(id INTEGER PRIMARY KEY AUTO_INCREMENT,website varchar(100) ,username varchar(100) not null,password varchar(100));"
                mycurser.execute(query)

            except:
                query = "use pas"
                mycurser.execute(query)

            messagebox.showinfo("Success","Database Connection is Successful",parent = login_window)
            login_window.destroy()
            connection_test.append(0)


    else:
        messagebox.showerror("Error","Database is already Connected")
        return
        
    login_window =Toplevel()
    login_window.geometry('670x450+550+250')
    login_window.title("Login for Connection")
    login_window.resizable(0,0)
    login_window.config(background="grey14")
    login_window.grab_set()
    hostname_label = Label(login_window,text="Hostname",font=('Century Gothic',25),bg="grey14",fg="white")
    hostname_label.grid(row=0,column=0,padx = 20,pady = 30)
    hostname_entry = customtkinter.CTkEntry(login_window,font=('Century Gothic',25),width=300) #localhost
    hostname_entry.grid(row=0,column = 1,padx = 20,pady = 30)

    username_label = Label(login_window,text="Username",font=('Century Gothic',25),bg="grey14",fg="white")
    username_label.grid(row=1,column=0,padx = 20,pady = 10)
    username_entry = customtkinter.CTkEntry(login_window,font=('Century Gothic',25),width=300) #root
    username_entry.grid(row=1,column = 1,padx = 20,pady = 10)

    password_label = Label(login_window,text="Password",font=('Century Gothic',25),bg="grey14",fg="white")
    password_label.grid(row=2,column=0,padx = 20,pady = 30)
    password_entry = customtkinter.CTkEntry(login_window,font=('Century Gothic',25),width=300,show="*") #1234
    password_entry.grid(row=2,column = 1,padx = 20,pady = 30)

    login_button = customtkinter.CTkButton(master=login_window,text="Login",height=35 ,width=320,command=lambda : connect())
    login_button.place(x=110,y=280)

def add_password():
    b.append(1)
    
    def add_password_data():
        websiteCheck = add_website_entry.get()
        usernameCheck = add_username_entry.get()
        query = "SELECT * FROM passwords WHERE website = %s and username = %s"
        mycurser.execute(query, (websiteCheck,usernameCheck))
        result = mycurser.fetchone()
        if(add_username_entry.get() == '' or add_password_entry.get() == '' or add_website_entry.get()==''):
            messagebox.showerror("Error","Please Enter All Fields")
        
        
        elif(result):
            messagebox.showerror("Error","Website or Username already Exist.Please update the Data from Update Password",parent=add_password())
            return

        else:
            try:
                query = "insert into passwords (website,username,password) values (%s,%s,%s)"
                encrypted_text1 = add_website_entry.get()
                encrypted_text2 = add_username_entry.get()
                encrypted_text3 = xor_encrypt_decrypt(add_password_entry.get(), key)
                mycurser.execute(query,(encrypted_text1,encrypted_text2,encrypted_text3))
                con.commit()
                messagebox.showinfo("Success","Data Inserted Successfully")
                add_window.destroy()
            except:
                messagebox.showerror("Error","ID cannot be repeated",parent=add_password())
                return
            
            query = "select website,username,password from passwords"
            mycurser.execute(query)
            fetched_data= mycurser.fetchall()
            password_table.delete(*password_table.get_children())
            show_password()
            for data in fetched_data:
                decrypted_text = xor_encrypt_decrypt(data, key)
                password_table.insert('',END,values=decrypted_text)

            

    if(len(a)== 0):
        messagebox.showerror("Error","Please Connect to Data Base First")
        return


    add_window =Toplevel()
    add_window.geometry('670x450+550+250')
    add_window.title("Add Password")
    add_window.resizable(0,0)
    add_window.config(background="grey14")
    add_window.grab_set()

    add_website_label = Label(add_window,text="Website",font=('Century Gothic',25),bg="grey14",fg="white")
    add_website_label.grid(row=0,column=0,padx = 20,pady = 30)
    add_website_entry = customtkinter.CTkEntry(add_window,font=('Century Gothic',25),width=300)
    add_website_entry.grid(row=0,column = 1,padx = 20,pady = 30)

    add_username_label = Label(add_window,text="Username",font=('Century Gothic',25),bg="grey14",fg="white")
    add_username_label.grid(row=1,column=0,padx = 20,pady = 10)
    add_username_entry = customtkinter.CTkEntry(add_window,font=('Century Gothic',25),width=300)
    add_username_entry.grid(row=1,column = 1,padx = 20,pady = 10)

    add_password_label = Label(add_window,text="Password",font=('Century Gothic',25),bg="grey14",fg="white")
    add_password_label.grid(row=2,column=0,padx = 20,pady = 30)
    add_password_entry = customtkinter.CTkEntry(add_window,font=('Century Gothic',25),width=300,show="*")
    add_password_entry.grid(row=2,column = 1,padx = 20,pady = 30)

    add_password_button = customtkinter.CTkButton(master=add_window,text="Add Password",height=35 ,width=320,command=lambda:add_password_data())
    add_password_button.place(x=110,y=280)
    
def search_password():
    if(len(a)== 0):
        messagebox.showerror("Error","Please Connect to Data Base First")
        return
    if(len(a)== 0):
        messagebox.showerror("Error","Please View Data First")
        return

    def search_data():
        query = "select website,username,password from passwords where website=%s or username=%s"
        mycurser.execute(query,(search_website_entry.get(),search_username_entry.get()))
        password_table.delete(*password_table.get_children())
        fetched_data=mycurser.fetchall()
        for data in fetched_data:
            list1 = list(data)
            newdata = xor_encrypt_decrypt(list1[2],key) 
            print(newdata)
            list1[2] = newdata;
            t = tuple(list1)
            password_table.insert('',END,values=t)
    
    search_window =Toplevel()
    search_window.geometry('670x450+550+250')
    search_window.title("Search Password")
    search_window.resizable(0,0)
    search_window.config(background="grey14")
    search_window.grab_set()

    search_website_label = Label(search_window,text="Website",font=('Century Gothic',25),bg="grey14",fg="white")
    search_website_label.grid(row=0,column=0,padx = 20,pady = 30)
    search_website_entry = customtkinter.CTkEntry(search_window,font=('Century Gothic',25),width=300)
    search_website_entry.grid(row=0,column = 1,padx = 20,pady = 30)

    search_username_label = Label(search_window,text="Username",font=('Century Gothic',25),bg="grey14",fg="white")
    search_username_label.grid(row=1,column=0,padx = 20,pady = 10)
    search_username_entry = customtkinter.CTkEntry(search_window,font=('Century Gothic',25),width=300)
    search_username_entry.grid(row=1,column = 1,padx = 20,pady = 10)

    search_password_button = customtkinter.CTkButton(master=search_window,text="Search Password",height=35 ,width=320,command=lambda:search_data())
    search_password_button.place(x=110,y=280)
   
def update_password():
    if(len(a)== 0):
        messagebox.showerror("Error","Please Connect to Data Base First")
        return
    if(len(b)== 0):
        messagebox.showerror("Error","Please view Data First")
        return
    
    def update_data():
        query = "update passwords set website=%s,password=%s where username=%s"

        encrypted_text1 = update_website_entry.get()
        encrypted_text2 = update_password_entry.get()
        encrypted_text3 = xor_encrypt_decrypt(update_password_entry.get(), key)
        mycurser.execute(query,(encrypted_text1,encrypted_text3,update_username_entry.get()))
        con.commit()

        messagebox.showinfo("Success","Your Data is Updated Successfully")
        update_window.destroy()
        show_password()

    indexing = password_table.focus()
    if(len(indexing)==0):
        messagebox.showerror("Error","Please Select Data to Update")
        return
    
    update_window =Toplevel()
    update_window.geometry('670x450+550+250')
    update_window.title("Update Password")
    update_window.resizable(0,0)
    update_window.config(background="grey14")
    update_window.grab_set()

    update_website_label = Label(update_window,text="Website",font=('Century Gothic',25),bg="grey14",fg="white")
    update_website_label.grid(row=0,column=0,padx = 20,pady = 30)
    update_website_entry = customtkinter.CTkEntry(update_window,font=('Century Gothic',25),width=300)
    update_website_entry.grid(row=0,column = 1,padx = 20,pady = 30)

    update_username_label = Label(update_window,text="Username",font=('Century Gothic',25),bg="grey14",fg="white")
    update_username_label.grid(row=1,column=0,padx = 20,pady = 10)
    update_username_entry = customtkinter.CTkEntry(update_window,font=('Century Gothic',25),width=300)
    update_username_entry.grid(row=1,column = 1,padx = 20,pady = 10)

    update_password_label = Label(update_window,text="Password",font=('Century Gothic',25),bg="grey14",fg="white")
    update_password_label.grid(row=2,column=0,padx = 20,pady = 30)
    update_password_entry = customtkinter.CTkEntry(update_window,font=('Century Gothic',25),width=300,show="*")
    update_password_entry.grid(row=2,column = 1,padx = 20,pady = 30)

    update_password_button = customtkinter.CTkButton(master=update_window,text="Update Password",height=35 ,width=320,command=lambda:update_data())
    update_password_button.place(x=110,y=280)

    
    content = password_table.item(indexing)
    list_data= content['values']
    update_website_entry.insert(0,list_data[0])
    update_username_entry.insert(0,list_data[1])
    update_password_entry.insert(0,list_data[2])

def delete_password():
    if(len(a)== 0):
        messagebox.showerror("Error","Please Connect to Data Base First")
        return
    if(len(b)== 0):
        messagebox.showerror("Error","Please view Data First")
        return
    
    indexing = password_table.focus()
    
    if(len(indexing)==0):
        messagebox.showerror("Error","Please Select Data to Delete")
        return
    content= password_table.item(indexing)
    content_data = content['values'][1]
    query = 'delete from passwords where username=""%s""'
    mycurser.execute(query,content_data)
    con.commit()
    messagebox.showinfo("Succesful","This Data is deleted Succcessfully")
    query="select * from passwords"
    mycurser.execute(query)
    fetched_data = mycurser.fetchall()
    password_table.delete(*password_table.get_children())
    show_password()

    indexing = 0

def show_password():
    b.append(0)
    if(len(a)== 0):
        messagebox.showerror("Error","Please Connect to Data Base First")
        return
    query = "select website,username,password from passwords"
    mycurser.execute(query)
    fetched_data= mycurser.fetchall()
    password_table.delete(*password_table.get_children())
    for data in fetched_data:
        list1 = list(data)
        newdata = xor_encrypt_decrypt(list1[2],key) 
        print(newdata)
        list1[2] = newdata;
        t = tuple(list1)
        password_table.insert('',END,values=t)

def export_data():
    if(len(a)== 0):
        messagebox.showerror("Error","Please Connect to Data Base First")
        return
    if(len(b)== 0):
        messagebox.showerror("Error","Please view Data First")
        return
    url=filedialog.asksaveasfilename(defaultextension='.csv')
    indexing = password_table.get_children()
    newlist=[]
    for index in indexing:
        content=password_table.item(index)
        datalist= content['values']
        newlist.append(datalist)
    table=pandas.DataFrame(newlist,columns=['Website','Username','Password'])
    table.to_csv(url,index=False)
    messagebox.showinfo("Success","Your Data is Exported Successfully")

def exit_password():
    result=messagebox.askyesno('Confirm',"Do You Want to Exit?")
    if result==True:
        app.destroy()

a= []
b= []
indexing = []
connection_test=[]

app = customtkinter.CTk()  
app.geometry("1174x680+0+0")
app.title('Password Management System')
app.resizable(False,False)
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

connect_button = customtkinter.CTkButton(app,text="Connect to Data Base",command=lambda:connect_database())
connect_button.place(x=980,y=10)

date_time_label = Label(app,font=('Century Gothic',35),bg="grey14")
date_time_label.place(x=5,y=10)
clock()

left_frame = Label(app,bg="grey14")
left_frame.place(x=5,y=150,width=420,height=680)

add_password_button = customtkinter.CTkButton(left_frame,text="Add Password",height=35 ,width=220,command=lambda:add_password())
add_password_button.grid(row = 1 ,column = 0 ,padx = 50, pady = 20)

search_password_button = customtkinter.CTkButton(left_frame,text="Search Password",height=35 ,width=220,command=lambda:search_password())
search_password_button.grid(row = 2 ,column = 0 ,padx = 50, pady = 20)

update_password_button = customtkinter.CTkButton(left_frame,text="Update Password",height=35 ,width=220,command=lambda:update_password())
update_password_button.grid(row = 3 ,column = 0 ,padx = 50, pady = 20)

delete_password_button = customtkinter.CTkButton(left_frame,text="Delete Password",height=35 ,width=220,command=lambda:delete_password())
delete_password_button.grid(row = 4 ,column = 0 ,padx = 50, pady = 20)

show_password_button = customtkinter.CTkButton(left_frame,text="Show Password",height=35 ,width=220,command=lambda:show_password())
show_password_button.grid(row = 5 ,column = 0 ,padx = 50, pady = 20)

export_password_button = customtkinter.CTkButton(left_frame,text="Export Password",height=35 ,width=220,command=lambda : export_data())
export_password_button.grid(row = 6 ,column = 0 ,padx = 50, pady = 20)

exit_password_button = customtkinter.CTkButton(left_frame,text="Exit",height=35 ,width=220,command=lambda:exit_password())
exit_password_button.grid(row = 7 ,column = 0 ,padx = 50, pady = 20)

right_frame = Label(app,bg="grey14")
right_frame.place(x=400,y=150,width=1050,height=680)

password_table = ttk.Treeview(right_frame,columns=('Website','Username','Password'))
password_table.pack(fill=BOTH,expand=1)
password_table.heading('Website',text="Website")
password_table.heading('Username',text="Username")
password_table.heading('Password',text="Password")
password_table.config(show='headings')
password_table.column('Website',anchor=CENTER)
password_table.column('Username',anchor=CENTER)
password_table.column('Password',anchor=CENTER)

style = ttk.Style()
style.configure('Treeview',rowheight=30,font=('Century Gothic',15))
style.configure('Treeview.Heading',rowheight=50,font=('Century Gothic',15,'bold'))

app.mainloop()