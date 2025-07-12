import tkinter as tk
from tkinter import *
import os, cv2
import shutil
import csv
import numpy as np
from PIL import ImageTk, Image
import pandas as pd
import datetime
import time
import tkinter.font as font
import pyttsx3

import takeImage
import trainImage
import automaticAttedance
import show_attendance


def text_to_speech(user_text):
    engine = pyttsx3.init()
    engine.say(user_text)
    engine.runAndWait()


haarcasecade_path = "haarcascade_frontalface_default.xml"
trainimagelabel_path = (
    "./TrainingImageLabel/Trainner.yml"
)
trainimage_path = "TrainingImage"
if not os.path.exists(trainimage_path):
    os.makedirs(trainimage_path)

studentdetail_path = (
    "./StudentDetails/studentdetails.csv"
)
attendance_path = "Attendance"


window = tk.Tk()
window.title("Face Recognition Based Entry")

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

window.geometry(f"{screen_width}x{screen_height}")

window.resizable(False, False)
window.configure(bg="#ffffff")


header_frame = Frame(window, bg="#2C3E50", height=60)
header_frame.pack(fill=X)


logo_img = Image.open("UI_Image/logo.png")  
logo_img = logo_img.resize((40, 40), Image.LANCZOS)
logo_photo = ImageTk.PhotoImage(logo_img)


logo_label = Label(
    header_frame,
    image=logo_photo,
    bg="#2C3E50"
)
logo_label.image = logo_photo 
logo_label.pack(side="left", padx=(20, 10), pady=10)

college_label = Label(
    header_frame,
    text="MGM'S COLLEGE OF ENGINEERING, NANDED.",
    bg="#2C3E50",
    fg="#ffffff",
    font=("Segoe UI", 18, "bold"),
    pady=10
)
college_label.pack(side="left", anchor="w")

menu_frame = Frame(header_frame, bg="#2C3E50")
menu_frame.pack(side="right", padx=20)

def open_page(title, message):
    top = Toplevel(window)
    top.title(title)
    top.geometry("500x300")
    top.configure(bg="#121212")

    Label(
        top,
        text=title,
        font=("Segoe UI", 20, "bold"),
        bg="#121212",
        fg="#00d4ff"
    ).pack(pady=20)

    Label(
        top,
        text=message,
        font=("Segoe UI", 14),
        bg="#121212",
        fg="#ffffff",
        wraplength=400,
        justify="left"
    ).pack(pady=10)

for text, title, content in [
    ("Home", "Welcome to MGM", "This is the home page of MGM's College of Engineering, Nanded."),
    ("About", "About Us", "MGM’s College of Engineering, Nanded, is a premier institute offering engineering and technology education."),
    ("Contact", "Contact Information", "Email: info@mgmcen.ac.in\nPhone: +91-1234567890\nAddress: Hingoli Gate, Nanded, Maharashtra")
]:
    Button(
        menu_frame,
        text=text,
        command=lambda t=title, m=content: open_page(t, m),
        bg="#34495E",
        fg="white",
        font=("Segoe UI", 10, "bold"),
        padx=10,
        pady=2,
        bd=0,
        activebackground="#1ABC9C",
        activeforeground="white",
        cursor="hand2"
    ).pack(side="left", padx=10, pady=10)


def del_sc1():
    sc1.destroy()


def err_screen():
    global sc1
    sc1 = tk.Tk()
    sc1.geometry("400x110")
    sc1.iconbitmap("AMS.ico")
    sc1.title("Warning!!")
    sc1.configure(background="#1c1c1c")
    sc1.resizable(0, 0)
    tk.Label(
        sc1,
        text="Enrollment & Name required!!!",
        fg="yellow",
        bg="#1c1c1c",  
        font=("Verdana", 16, "bold"),
    ).pack()
    tk.Button(
        sc1,
        text="OK",
        command=del_sc1,
        fg="yellow",
        bg="#333333", 
        width=9,
        height=1,
        activebackground="red",
        font=("Verdana", 16, "bold"),
    ).place(x=110, y=50)

def testVal(inStr, acttyp):
    if acttyp == "1":  
        if not inStr.isdigit():
            return False
        if len(inStr) > 13:  
            return False
    return True

def create_gradient_label(master, text, font_size=20, height=40, width=screen_width):
    canvas = tk.Canvas(master, width=width, height=height, highlightthickness=0)
    canvas.pack()

    r1, g1, b1 = (22, 160, 133)  
    r2, g2, b2 = (41, 128, 185)  
    steps = width
    for i in range(steps):
        r = int(r1 + (r2 - r1) * i / steps)
        g = int(g1 + (g2 - g1) * i / steps)
        b = int(b1 + (b2 - b1) * i / steps)
        color = f"#{r:02x}{g:02x}{b:02x}"
        canvas.create_line(i, 0, i, height, fill=color)

    canvas.create_text(width // 2, height // 2, text=text, fill="#ffffff", font=("Segoe UI", font_size, "bold"))
    return canvas

gradient_label1 = create_gradient_label(window, "🎭 WELCOME TO THE CULTURAL GATHERING 2025 🎉", font_size=20, height=50)

gradient_label2 = create_gradient_label(window, "Experience Seamless and Secure Entry with Face Recognition", font_size=14, height=50)

titl = tk.Label(
    window,
    text="Why Choose Face Recognition?",
    bg="#ffffff",        
    fg="#000000", 
    font=("Segoe UI", 18, "bold"),  
    pady=5
)
titl.pack(pady=10) 

titl2 = tk.Label(
    window,
    text="Say goodbye to traditional ID checks and embrace the future of secure and contactless entry. With facial recognition, your event experience is faster, safer, and more convenient!",
    bg="#ffffff",        
    fg="#000000", 
    font=("Segoe UI", 12),  
    pady=2  
)
titl2.pack(pady=(0, 10))  

separator = tk.Frame(window, bg="#cccccc", height=2, width=window.winfo_screenwidth())
separator.pack(fill="x", padx=20, pady=(5, 15))

def create_feature_card(image_path, text, x, y):
    card_frame = tk.Frame(window, bg="#ffffff")
    card_frame.place(x=x, y=y)

    image = Image.open(image_path).resize((120, 120), Image.LANCZOS)
    photo = ImageTk.PhotoImage(image)
    label_img = tk.Label(card_frame, image=photo, bg="#ffffff")
    label_img.image = photo
    label_img.pack()

    label_text = tk.Label(
        card_frame,
        text=text,
        bg="#ffffff",
        fg="#000000",
        font=("Segoe UI", 14, "bold")
    )
    label_text.pack(pady=8)

create_feature_card("UI_Image/register.png", "Register Student", 140, 350)
create_feature_card("UI_Image/verifyy.png", "Check Live Entry", 610, 350)
create_feature_card("UI_Image/attendance.png", "All Records", 1060, 350)

def TakeImageUI():
    ImageUI = Tk()
    ImageUI.title("Register Student Face")
    ImageUI.geometry("800x500")
    ImageUI.configure(background="#121212")
    ImageUI.resizable(0, 0)

    title = tk.Label(
        ImageUI,
        text="🎓 Register Your Face",
        bg="#121212",
        fg="#00d4ff",
        font=("Segoe UI", 28, "bold"),
        pady=20
    )
    title.pack()


    subtitle = tk.Label(
        ImageUI,
        text="Please enter the details below",
        bg="#121212",
        fg="#ffffff",
        font=("Segoe UI", 16, "italic")
    )
    subtitle.pack(pady=(0, 20))

    lbl1 = tk.Label(
        ImageUI,
        text="PRN :",
        bg="#121212",
        fg="#ffffff",
        font=("Segoe UI", 14)
    )
    lbl1.place(x=100, y=150)

    txt1 = tk.Entry(
        ImageUI,
        width=30,
        bd=2,
        bg="#1f1f1f",
        fg="#00ff88",
        insertbackground="#00ff88",
        font=("Segoe UI", 14)
    )
    txt1.place(x=260, y=150)
    txt1["validate"] = "key"
    txt1["validatecommand"] = (txt1.register(testVal), "%P", "%d")

    lbl2 = tk.Label(
        ImageUI,
        text="Name:",
        bg="#121212",
        fg="#ffffff",
        font=("Segoe UI", 14)
    )
    lbl2.place(x=100, y=200)

    txt2 = tk.Entry(
        ImageUI,
        width=30,
        bd=2,
        bg="#1f1f1f",
        fg="#00ff88",
        insertbackground="#00ff88",
        font=("Segoe UI", 14)
    )
    txt2.place(x=260, y=200)

    lbl3 = tk.Label(
        ImageUI,
        text="Notification:",
        bg="#121212",
        fg="#ffffff",
        font=("Segoe UI", 14)
    )
    lbl3.place(x=100, y=250)

    message = tk.Label(
        ImageUI,
        text="",
        bg="#1f1f1f",
        fg="#fdd835",
        width=30,
        height=2,
        font=("Segoe UI", 12, "bold"),
        relief=RIDGE,
        bd=2
    )
    message.place(x=260, y=245)

    def take_image():
        l1 = txt1.get()
        l2 = txt2.get()
        takeImage.TakeImage(
            l1,
            l2,
            haarcasecade_path,
            trainimage_path,
            message,
            err_screen,
            text_to_speech,
        )
        txt1.delete(0, "end")
        txt2.delete(0, "end")

    takeImg = tk.Button(
        ImageUI,
        text="📸 New Registration",
        command=take_image,
        bg="#00d4ff",
        fg="#000000",
        font=("Segoe UI", 12, "bold"),
        relief="flat",
        bd=0,
        height=1,
        width=20,    
        cursor="hand2"
    )
    takeImg.place(x=100, y=330)


    def train_image():
        trainImage.TrainImage(
            haarcasecade_path,
            trainimage_path,
            trainimagelabel_path,
            message,
            text_to_speech,
        )


    trainImg = tk.Button(
        ImageUI,
        text="📸 Train Image",
        command=train_image,
        bg="#00d4ff",
        fg="#000000",
        font=("Segoe UI", 12, "bold"),
        relief="flat",
        bd=0,
        height=1,
        width=20,    
        cursor="hand2"
    )
    trainImg.place(x=360, y=330)


r = tk.Button(
    window,
    text="🆕 Register New Student",
    command=TakeImageUI,
    bd=0,
    font=("Segoe UI", 12, "bold"),
    bg="#2C3E50",       
    fg="#ffffff",       
    activebackground="#00a982",  
    activeforeground="#ffffff",
    height=1,
    width=20,
    relief="flat",     
    cursor="hand2"   
)
r.place(x=110, y=520)


def automatic_attedance():
    automaticAttedance.subjectChoose(text_to_speech)


r = tk.Button(
    window,
    text="🆕 Check Live Entry",
    command=automatic_attedance,
    bd=0,
    font=("Segoe UI", 12, "bold"),
    bg="#2C3E50",       
    fg="#ffffff",       
    activebackground="#00a982",  
    activeforeground="#ffffff",
    height=1,
    width=20,
    relief="flat",     
    cursor="hand2"
)
r.place(x=580, y=520)


def view_attendance():
    show_attendance.subjectchoose(text_to_speech)


r = tk.Button(
    window,
    text="🆕 Check Records",
    command=view_attendance,
    bd=0,
    font=("Segoe UI", 12, "bold"),
    bg="#2C3E50",       
    fg="#ffffff",       
    activebackground="#00a982",  
    activeforeground="#ffffff",
    height=1,
    width=20,
    relief="flat",     
    cursor="hand2"
)
r.place(x=1020, y=520)



button_pixel_width = 10 * 10  
button_x = int((screen_width - button_pixel_width) / 2)

r = tk.Button(
    window,
    text="❌ EXIT",
    bd=0,  
    command=quit,
    font=("Segoe UI", 12, "bold"),
    bg="#ff4d4d",  
    fg="#ffffff",  
    activebackground="#e60000",  
    activeforeground="#ffffff",
    height=1,
    width=10,
    relief="flat", 
    cursor="hand2",  
)
r.place(x=button_x, y=650)


window.mainloop()
