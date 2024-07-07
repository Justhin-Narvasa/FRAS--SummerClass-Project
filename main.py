import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mess
import tkinter.simpledialog as tsd
import cv2, os
import csv
import numpy as np
from PIL import Image
import pandas as pd
import datetime
import time
import webbrowser
import re
import subprocess


def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)


def tick():
    time_string = time.strftime('%I:%M:%S %p')
    clock.config(text=time_string)
    clock.after(200, tick)


def contact():
    email_address = "justhin.narvasa@zdspgc.edu.ph"

    def open_email_client(event):
        webbrowser.open_new("mailto:" + email_address)

    message = f"Please contact us on {email_address}"
    result = mess.askyesno(title='Contact us', message=message, icon='info')
    if result:
        webbrowser.open_new("mailto:" + email_address)
    help_menu_window.destroy()


def exit_app():
    if mess.askokcancel("Exit", "Are you sure you want to exit the application?"):
        window.destroy()
        open_login_window()


def open_login_window():
    try:
        subprocess.run(['python', 'log_in.py'], check=True)
    except subprocess.CalledProcessError:
        mess.showerror("Error", "Failed to run log_in.py!")


def check_haarcascadefile():
    exists = os.path.isfile("haarcascade_frontalface_default.xml")
    if exists:
        pass
    else:
        mess._show(title='Some file missing', message='Please contact us for help')
        window.destroy()


def save_pass():
    assure_path_exists("PasswordDetails/")
    exists1 = os.path.isfile("PasswordDetails\\password.txt")

    if exists1:
        with open("PasswordDetails\\password.txt", "r") as tf:
            key = tf.read().strip()
        op = old.get()
        newp = new.get()
        nnewp = nnew.get()

        if not op or not newp or not nnewp:
            mess.showerror("Error", "Please fill in all the fields.")
            return

        if op == key:
            if newp == nnewp:
                with open("PasswordDetails\\password.txt", "w") as txf:
                    txf.write(newp)
                mess.showinfo("Password Changed", "Password changed successfully!!")
                master.destroy()
            else:
                mess.showerror("Error", "Confirm new password again!!!")
        else:
            mess.showerror("Error", "Please enter correct old password.")
            old.delete(0, 'end')
            new.delete(0, 'end')
            nnew.delete(0, 'end')
    else:
        master.destroy()
        new_pas = tsd.askstring('Old Password not found', 'Please enter a new password below', show='*')
        if new_pas is None:
            mess.showwarning('No Password Entered', 'Password not set!! Please try again')
        else:
            with open("PasswordDetails\\password.txt", "w") as tf:
                tf.write(new_pas)
            mess.showinfo('Password Registered', 'New password was registered successfully!!')


help_menu_window = None


def change_pass(help_menu_window):
    global master
    master = tk.Tk()
    master.geometry("400x160")
    master.resizable(False, False)
    master.title("Change Password")
    master.configure(background="#84b08d")
    master.attributes('-topmost', True)

    lbl4 = tk.Label(master, text='Enter Old Password', fg='black', bg='#84b08d', font=('times', 12, ' bold '))
    lbl4.place(x=10, y=10)
    global old
    old = tk.Entry(master, width=25, fg="black", relief='solid', font=('times', 12, ' bold '), show='*')
    old.place(x=180, y=10)
    lbl5 = tk.Label(master, text='Enter New Password', fg='black', bg='#84b08d', font=('times', 12, ' bold '))
    lbl5.place(x=10, y=45)
    global new
    new = tk.Entry(master, width=25, fg="black", relief='solid', font=('times', 12, ' bold '), show='*')
    new.place(x=180, y=45)
    lbl6 = tk.Label(master, text='Confirm New Password', fg='black', bg='#84b08d', font=('times', 12, ' bold '))
    lbl6.place(x=10, y=80)
    global nnew
    nnew = tk.Entry(master, width=25, fg="black", relief='solid', font=('times', 12, ' bold '), show='*')
    nnew.place(x=180, y=80)
    cancel = tk.Button(master, text="Cancel", command=lambda: (master.destroy(), help_menu_window.destroy()),
                       fg="white", bg="#262523", height=1, width=25, activebackground="white",
                       font=('times', 10, ' bold '))
    cancel.place(x=200, y=120)
    cancel.bind("<Enter>", Exit_on_enter)
    cancel.bind("<Leave>", Exit_on_leave)

    save1 = tk.Button(master, text="Save", command=lambda: save_pass(), fg='white',
                      bg='#262523', height=1, width=25, activebackground="white", font=('times', 10, ' bold '))
    save1.place(x=10, y=120)
    save1.bind("<Enter>", on_enter)
    save1.bind("<Leave>", on_leave)
    help_menu_window.destroy()
    master.mainloop()


def open_help_menu():
    global help_menu_window
    help_menu_window = tk.Toplevel(window)
    help_menu_window.geometry("400x200")
    help_menu_window.title("Help Menu")
    help_menu_window.configure(bg="#84b08d")
    help_menu_window.resizable(False, False)
    help_menu_window.attributes('-topmost', True)

    btn_change_pass = tk.Button(help_menu_window, text="Change Password", command=lambda: change_pass(help_menu_window),
                                width=20, fg="white", bg="#262523", font=('times', 15, ' bold '))
    btn_change_pass.pack(pady=10)
    btn_change_pass.bind("<Enter>", on_enter)
    btn_change_pass.bind("<Leave>", on_leave)

    btn_contact = tk.Button(help_menu_window, text="Contact Us", command=contact, width=20, fg="white", bg="#262523",
                            font=('times', 15, ' bold '))
    btn_contact.pack(pady=10)
    btn_contact.bind("<Enter>", on_enter)
    btn_contact.bind("<Leave>", on_leave)

    btn_exit = tk.Button(help_menu_window, text="Log out", command=exit_app, width=20, fg="white", bg="#262523",
                         font=('times', 15, ' bold '))
    btn_exit.pack(pady=10)
    btn_exit.bind("<Enter>", Exit_on_enter)
    btn_exit.bind("<Leave>", Exit_on_leave)


images_taken = False


def password():
    global images_taken
    assure_path_exists("PasswordDetails/")
    exists1 = os.path.isfile("PasswordDetails\\password.txt")
    if exists1:
        tf = open("PasswordDetails\\password.txt", "r")
        key = tf.read()
    else:
        new_pas = tsd.askstring('Old Password not found', 'Please enter a new password below', show='*')
        if new_pas == None:
            mess._show(title='No Password Entered', message='Password not set!! Please try again')
        else:
            tf = open("PasswordDetails\\password.txt", "w")
            tf.write(new_pas)
            mess._show(title='Password Registered', message='New password was registered successfully!!')
            return

    password = tsd.askstring('Password', 'Enter Password', show='*')
    if password == key:
        TrainImages()
    elif password is not None:
        mess._show(title='Wrong Password', message='You have entered wrong password')


def clear():
    txt.delete(0, 'end')
    res = "Take Images to Register"
    message1.configure(text=res)


def clear2():
    txt2.delete(0, 'end')
    res = "Take Images to Register"
    message1.configure(text=res)


def clear_attendance():
    if len(tv.get_children()) == 0:

        ts = time.time()
        date = datetime.datetime.fromtimestamp(ts).strftime('%B-%d-%Y')
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%I:%M:%S %p')
        mess.showerror(title='No Records Found', message=f'No attendance records found for {date} at {timestamp}.')
    else:
        for item in tv.get_children():
            tv.delete(item)
        ts = time.time()
        date = datetime.datetime.fromtimestamp(ts).strftime('%B-%d-%Y')
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%I:%M:%S %p')
        mess.showinfo(title='Attendance Cleared',
                      message=f'Attendance records for {date} at {timestamp} have been cleared!')


def on_enter(e):
    e.widget['background'] = '#3ece48'


def on_leave(e):
    e.widget['background'] = '#262523'


def Exit_on_enter(e):
    e.widget['background'] = 'red'


def Exit_on_leave(e):
    e.widget['background'] = '#262523'


def spaced_text(text):
    return '  '.join(text)


def is_valid_id(id_string):
    return bool(re.match(r'^[A-Z0-9]+$', id_string))


def TakeImages():
    global images_taken

    check_haarcascadefile()

    columns = ['SERIAL NO.', '', 'ID', '', 'NAME']

    if os.path.isfile("StudentDetails\\StudentDetails.txt"):
        with open("StudentDetails\\StudentDetails.txt", 'r') as csvFile1:
            reader1 = csv.reader(csvFile1)
            serial_numbers = set()
            for row in reader1:
                if len(row) > 1 and row[0].strip().lower() != "serial no.":
                    serial_numbers.add(int(row[0]))

            if serial_numbers:
                serial = max(serial_numbers) + 1
            else:
                serial = 0
    else:
        with open("StudentDetails\\StudentDetails.txt", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(columns)
        serial = 0

    Id = txt.get().strip()
    name = txt2.get().strip()

    if not Id or not name:
        mess.showerror("Error", "Please fill in all fields")
        return

    if not is_valid_id(Id):
        mess.showerror("Error", "ID should contain only numbers and uppercase letters")
        return

    if not all(char.isalpha() or char.isspace() for char in name):
        mess.showerror("Error", "Name should only contain alphabet letters (capital or small) and spaces")
        return

    with open("StudentDetails\\StudentDetails.txt", 'r') as csvFile:
        reader = csv.reader(csvFile)
        for row in reader:
            if row and row[0].strip().isdigit() and int(row[0]) == serial:
                mess.showerror("Error", f"Serial number {serial} is already assigned.")
                return

    cam = cv2.VideoCapture(0)
    harcascadePath = "haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(harcascadePath)
    sampleNum = 0

    while True:
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            sampleNum += 1
            filename = f"TrainImage/{name}.{serial}.{Id}.{sampleNum}.jpg"
            cv2.imwrite(filename, gray[y:y + h, x:x + w])
            cv2.imshow('Taking Images', img)

        if cv2.waitKey(1) & 0xFF == ord('q') or cv2.waitKey(1) & 0xFF == ord('Q') or sampleNum > 50:
            break

    cam.release()
    cv2.destroyAllWindows()

    if sampleNum > 0:
        images_taken = True
        res = f"Images Taken for ID : {Id}"
        row = [serial, '', Id, '', name]

        confirm_register = mess.askyesno("Images Taken Successfully!",
                                         "Do you want to Register?")

        if confirm_register:
            with open("StudentDetails\\StudentDetails.txt", 'a+', newline='') as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow(row)
                TrainImages()
        else:
            mess.showinfo("Not Registering", "The registration process was canceled.")
            txt.delete(0, 'end')
            txt2.delete(0, 'end')
            for i in range(1, sampleNum + 1):
                img_path = f"TrainImage/{name}.{serial}.{Id}.{i}.jpg"
                if os.path.exists(img_path):
                    os.remove(img_path)
                txt.delete(0, 'end')
                txt2.delete(0, 'end')

    else:
        mess.showwarning("No Images Taken", "No images were taken!")


def TrainImages():
    check_haarcascadefile()
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    harcascadePath = "haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(harcascadePath)
    faces, Ids = getImagesAndLabels("TrainImage")
    try:
        recognizer.train(faces, np.array(Ids))
    except:
        mess._show(title='No Registrations', message='Please Register someone first!!!')
        return

    recognizer.save("Trainner.yml")

    mess.showinfo("Success", "Registration Completed Successfully")

    global total_registrations
    total_registrations += 1
    message.configure(text='Total Registrations  : ' + str(total_registrations))

    txt.delete(0, 'end')
    txt2.delete(0, 'end')
    message1.configure(text="Take Images to Register")


def getImagesAndLabels(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    faces = []
    Ids = []
    for imagePath in imagePaths:
        pilImage = Image.open(imagePath).convert('L')
        imageNp = np.array(pilImage, 'uint8')
        ID = int(os.path.split(imagePath)[-1].split(".")[1])
        faces.append(imageNp)
        Ids.append(ID)
    return faces, Ids


def TrackImages():
    check_haarcascadefile()
    assure_path_exists("AttendanceDetails/")
    assure_path_exists("StudentDetails/")
    student_details_path = "StudentDetails/StudentDetails.txt"

    if not os.path.isfile(student_details_path):
        mess.showwarning('Details Missing', 'No students registered yet. Please register students first.')
        return

    df = pd.read_csv(student_details_path)
    if df.empty or df.shape[0] == 0:
        mess.showwarning('No Students Registered', 'No students registered yet. Please register students first.')
        return

    for k in tv.get_children():
        tv.delete(k)

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    exists3 = os.path.isfile("Trainner.yml")
    if exists3:
        recognizer.read("Trainner.yml")
    else:
        mess._show(title='Data Missing', message='Please click on Save Profile to reset data!!')
        return

    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath)
    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX

    displayed_ids = set()
    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime('%B-%d-%Y')
    attendance_file = f"AttendanceDetails/Attendance_{date}.txt"

    while True:
        ret, im = cam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (225, 0, 0), 2)
            serial, conf = recognizer.predict(gray[y:y + h, x:x + w])

            name = 'Unknown'
            student_id = 'Unknown'

            if conf < 50:
                row = df[df['SERIAL NO.'] == serial]
                if not row.empty:
                    name = row.iloc[0]['NAME']
                    student_id = row.iloc[0]['ID']

                    attendance = [student_id, name, date, datetime.datetime.now().strftime('%I:%M:%S %p')]

                    if student_id not in displayed_ids:
                        tv.insert('', 0, text=student_id,
                                  values=(name, date, datetime.datetime.now().strftime('%I:%M:%S %p')))
                        displayed_ids.add(student_id)

                        with open(attendance_file, 'a+', newline='') as csvFile:
                            writer = csv.writer(csvFile)
                            if csvFile.tell() == 0:
                                writer.writerow(['ID', 'NAME', 'DATE', 'TIME'])
                            writer.writerow(attendance)

            cv2.putText(im, str(name), (x, y + h), font, 1, (255, 255, 255), 2)

        cv2.imshow('Taking Attendance', im)

        if cv2.waitKey(1) == ord('q') or cv2.waitKey(1) == ord('Q'):
            break

    cam.release()
    cv2.destroyAllWindows()


global key
key = ''

ts = time.time()
date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
day, month, year = date.split("-")

mont = {'01': 'January',
        '02': 'February',
        '03': 'March',
        '04': 'April',
        '05': 'May',
        '06': 'June',
        '07': 'July',
        '08': 'August',
        '09': 'September',
        '10': 'October',
        '11': 'November',
        '12': 'December'
        }

window = tk.Tk()
window.geometry("1280x720")
window.resizable(False, False)
window.title("Facial Recognition Attendance System")
window.configure(background='#262523')

frame1 = tk.Frame(window, bg="#84b08d")
frame1.place(relx=0.51, rely=0.17, relwidth=0.38, relheight=0.80)
frame2 = tk.Frame(window, bg="#84b08d")
frame2.place(relx=0.11, rely=0.17, relwidth=0.39, relheight=0.80)
message3 = tk.Label(window, text="Facial Recognition Attendance System", fg="white", bg="#262523", width=55,
                    height=1, font=('times', 29, ' bold '))
message3.place(x=9, y=9)

datef = tk.Label(window, text=f"{mont[month]}/{day}/{year}", fg="#3ece48", bg="#262523",
                 height=1, font=('times', 15, ' bold '))
datef.place(x=80, y=50)
month_label_text = tk.Label(window, text="Month:", fg="white", bg="#262523", height=1, font=('times', 15, 'bold'))
month_label_text.place(x=10, y=50)
clock = tk.Label(window, fg="#3ece48", bg="#262523", height=1, font=('times', 15, ' bold '))
clock.place(x=80, y=80)
time_label = tk.Label(window, text="Time:", fg="white", bg="#262523", height=1, font=('times', 15, 'bold'))
time_label.place(x=10, y=80)
tick()

head2 = tk.Label(frame2, text="                 For New Students Registrations                         ", fg="white",
                 bg="#0a5133", font=('times', 17, ' bold '))
head2.grid(row=0, column=0)
head1 = tk.Label(frame1, text="          For Students that Already Registered                       ", fg="white",
                 bg="#0a5133", font=('times', 17, ' bold '))
head1.place(x=0, y=0)
lbl = tk.Label(frame2, text="Enter Enrollment ID", width=20, height=1, fg="black", bg="#84b08d",
               font=('times', 17, ' bold '))
lbl.place(x=80, y=55)
txt = tk.Entry(frame2, width=32, fg="black", font=('times', 15, ' bold '))
txt.place(x=30, y=88)
lbl2 = tk.Label(frame2, text="Enter Student Name", width=20, fg="black", bg="#84b08d", font=('times', 17, ' bold '))
lbl2.place(x=80, y=140)
txt2 = tk.Entry(frame2, width=32, fg="black", font=('times', 15, ' bold '))
txt2.place(x=30, y=173)
message1 = tk.Label(frame2, text="Take Images to Register", bg="#84b08d", fg="black", width=39, height=1,
                    font=('times', 15, ' bold '))
message1.place(x=7, y=230)
message = tk.Label(frame2, text="", bg="#84b08d", fg="black", width=39, height=1,
                   font=('times', 16, ' bold '))
message.place(x=7, y=450)
lbl3 = tk.Label(frame1, text=spaced_text("ATTENDANCE"), width=25, fg="black", bg="#84b08d", height=2,
                font=('times', 25, ' bold '))
lbl3.place(x=5, y=55)

global total_registrations
total_registrations = 0

exists = os.path.isfile("StudentDetails\\StudentDetails.txt")

if exists:
    with open("StudentDetails\\StudentDetails.txt", 'r') as csvFile1:
        reader1 = csv.reader(csvFile1)
        for row in reader1:
            if len(row) > 1 and row[0].strip().lower() != "serial no.":
                total_registrations += 1
else:
    total_registrations = 0

message.configure(text='Total Registrations: ' + str(total_registrations))

tv = ttk.Treeview(frame1, height=13, columns=('name', 'date', 'time'))
tv.column('#0', width=82)
tv.column('name', width=130)
tv.column('date', width=133)
tv.column('time', width=133)
tv.grid(row=2, column=0, padx=(0, 0), pady=(150, 0), columnspan=4)
tv.heading('#0', text='ID')
tv.heading('name', text='NAME')
tv.heading('date', text='DATE')
tv.heading('time', text='TIME')

scroll = ttk.Scrollbar(frame1, orient='vertical', command=tv.yview)
scroll.grid(row=2, column=4, padx=(0, 100), pady=(150, 0), sticky='ns')
tv.configure(yscrollcommand=scroll.set)
clearButton = tk.Button(frame2, text="Clear", command=clear, fg="white", bg="#262523", width=11, height=1,
                        activebackground="white", font=('times', 11, ' bold '))
clearButton.place(x=335, y=88)
clearButton.bind("<Enter>", Exit_on_enter)
clearButton.bind("<Leave>", Exit_on_leave)

clearButton2 = tk.Button(frame2, text="Clear", command=clear2, fg="white", bg="#262523", width=11, height=1,
                         activebackground="white", font=('times', 11, ' bold '))
clearButton2.place(x=335, y=172)
clearButton2.bind("<Enter>", Exit_on_enter)
clearButton2.bind("<Leave>", Exit_on_leave)

takeImg = tk.Button(frame2, text="Take Images", command=TakeImages, fg="white", bg="#262523", width=24, height=2,
                    activebackground="white", font=('times', 15, ' bold '))
takeImg.place(x=100, y=300)
takeImg.bind("<Enter>", on_enter)
takeImg.bind("<Leave>", on_leave)

trackImg = tk.Button(frame1, text="Take Attendance", command=TrackImages, fg="white", bg="#262523", width=35, height=1,
                     activebackground="white", font=('times', 15, ' bold '))
trackImg.place(x=30, y=450)
trackImg.bind("<Enter>", on_enter)
trackImg.bind("<Leave>", on_leave)

clearAttendanceButton = tk.Button(frame1, text="Clear Attendance", command=clear_attendance, fg="white", bg="#262523",
                                  width=35, height=1,
                                  activebackground="white", font=('times', 15, ' bold '))
clearAttendanceButton.place(x=30, y=510)
clearAttendanceButton.bind("<Enter>", Exit_on_enter)
clearAttendanceButton.bind("<Leave>", Exit_on_leave)

quitWindow = tk.Button(window, text="Log out", command=exit_app, fg="white", bg="#262523", width=10, height=1,
                       activebackground="white", font=('times', 15, ' bold '))
quitWindow.place(x=1140, y=10)
quitWindow.bind("<Enter>", Exit_on_enter)
quitWindow.bind("<Leave>", Exit_on_leave)

btn_help = tk.Button(window, text="Help", command=open_help_menu, fg="white", bg="#262523", width=10, height=1,
                     activebackground="white", font=('times', 15, ' bold '))
btn_help.place(x=1140, y=70)
btn_help.bind("<Enter>", on_enter)
btn_help.bind("<Leave>", on_leave)

message4 = tk.Label(window, text="Press 'Q' or 'q' to stop the webcam.", bg="#262523", fg="white", width=39, height=1,
                    activebackground="yellow", font=('times', 15, ' bold '))
message4.place(x=400, y=80)

window.mainloop()
