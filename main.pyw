import customtkinter
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk,Image

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

app = customtkinter.CTk()
app.geometry("1366x768+0+0")
app.config(padx=20,pady=20)
app.resizable()

alist = [line.rstrip() for line in open('data/pass.txt')]

def check(username_entry,password_entry):
    username = username_entry.get()
    password = password_entry.get()
    if(username == alist[0] and password == alist[1]):
        messagebox.showinfo("Login Successful","Welcome! to Password Management System")
        app.destroy()
        from data import password_management_system
    else:
        messagebox.showerror("Login Failed","Please Enter Correct Information")

image1=ImageTk.PhotoImage(Image.open("./data/Pattern.png"))
label1=customtkinter.CTkLabel(master=app,image=image1)
label1.pack()

frame=customtkinter.CTkFrame(master=label1, width=420, height=330, corner_radius=15,border_width=5)
frame.place(relx=0.5, rely=0.5, anchor=CENTER)

label2=customtkinter.CTkLabel(master=frame, text="Log In",font=('Century Gothic',35))
label2.place(relx=0.40,y=25,x=-3)

entry_of_username=customtkinter.CTkEntry(master=frame, height=35 ,width=320, placeholder_text='Username',font=('Century Gothic',25))
entry_of_username.place(x=50, y=110)

entry_of_password=customtkinter.CTkEntry(master=frame,height=35 ,width=320, placeholder_text='Password', show="*",font=('Century Gothic',25))
entry_of_password.place(x=50, y=180)

login_button = customtkinter.CTkButton(master=frame,text="Login",height=35 ,width=320, command = lambda : check(entry_of_username,entry_of_password) )
login_button.place(x=50, y=250)

app.mainloop()