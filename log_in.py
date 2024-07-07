import tkinter as tk
from tkinter import messagebox as mess
import subprocess


def authenticate_login():
    username = username_entry.get().strip()
    password = password_entry.get().strip()

    admin_username = "admin"
    admin_password_file = "PasswordDetails\\password.txt"

    try:
        with open(admin_password_file, 'r') as file:
            admin_password = file.read().strip()
    except FileNotFoundError:
        mess.showerror("Error", "Password file not found!")
        return

    if username == admin_username and password == admin_password:
        login_window.destroy()
        open_main_window()
    else:
        mess.showerror("Login Failed", "Invalid username or password")


def open_main_window():
    try:
        subprocess.run(['python', 'main.py'], check=True)
    except subprocess.CalledProcessError:
        mess.showerror("Error", "Failed to run main.py!")


def exit_app():
    if mess.askokcancel("Exit", "Are you sure you want to exit the application?"):
        login_window.destroy()


def on_enter(e):
    e.widget['background'] = '#3ece48'


def on_leave(e):
    e.widget['background'] = '#262523'


def Exit_on_enter(e):
    e.widget['background'] = 'red'


def Exit_on_leave(e):
    e.widget['background'] = '#262523'


login_window = tk.Tk()
login_window.geometry("1280x720")
login_window.title("Login")
login_window.resizable(False, False)
login_window.configure(background='#262523')

login_window.protocol("WM_DELETE_WINDOW", exit_app)

title_label = tk.Label(login_window, text="Facial Recognition Attendance System", fg="white", bg="#262523",
                       font=('times', 35, 'bold'))
title_label.place(x=280, y=50)

frame1 = tk.Frame(login_window, bg="#84b08d", bd=2, relief=tk.SOLID)
frame1.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

username_label = tk.Label(frame1, text="Username:", fg="black", bg="#84b08d", font=('times', 14, 'bold'))
username_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

username_entry = tk.Entry(frame1, width=30, fg="black", font=('times', 12))
username_entry.grid(row=0, column=1, padx=10, pady=10)

password_label = tk.Label(frame1, text="Password:", fg="black", bg="#84b08d", font=('times', 14, 'bold'))
password_label.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)

password_entry = tk.Entry(frame1, width=30, fg="black", font=('times', 12), show='*')
password_entry.grid(row=1, column=1, padx=10, pady=10)

login_button = tk.Button(frame1, text="Login", command=authenticate_login, fg='white',
                         bg='#262523', font=('times', 12, 'bold'), width=20, height=2, activebackground="#84b08d")
login_button.grid(row=2, column=0, columnspan=2, pady=20)
login_button.bind("<Enter>", on_enter)
login_button.bind("<Leave>", on_leave)

exit_button = tk.Button(login_window, text="Exit", command=exit_app, fg="white", bg="#262523",
                        font=('times', 12, 'bold'), width=15, height=2, activebackground="#84b08d")
exit_button.place(x=1100, y=10)
exit_button.bind("<Enter>", Exit_on_enter)
exit_button.bind("<Leave>", Exit_on_leave)

login_window.mainloop()
