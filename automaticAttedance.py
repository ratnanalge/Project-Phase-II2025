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
import tkinter.ttk as tkk
import tkinter.font as font

haarcasecade_path = "haarcascade_frontalface_default.xml"
trainimagelabel_path = (
    "TrainingImageLabel\\Trainner.yml"
)
trainimage_path = "TrainingImage"
studentdetail_path = (
    "StudentDetails\\studentdetails.csv"
)
prn_mapping_path = "prn_mapping.csv"

attendance_path = "Entry Records"
def subjectChoose(text_to_speech):
    def FillAttendance():
        sub = tx.get()
        now = time.time()
        future = now + 20
        print(now)
        print(future)
        if sub == "":
            t = "Please enter the Event name!!!"
            text_to_speech(t)
        else:
            try:
                recognizer = cv2.face.LBPHFaceRecognizer_create()
                try:
                    recognizer.read(trainimagelabel_path)
                except:
                    e = "Model not found,please train model"
                    Notifica.configure(
                        text=e,
                        bg="black",
                        fg="#00d4ff",
                        width=33,
                        font=("times", 16, "bold"),
                    )
                    Notifica.place(x=180, y=350)
                    text_to_speech(e)
                facecasCade = cv2.CascadeClassifier(haarcasecade_path)
                df = pd.read_csv(studentdetail_path)
                prn_mapping_df = pd.read_csv(prn_mapping_path)
                cam = cv2.VideoCapture(0)
                font = cv2.FONT_HERSHEY_SIMPLEX
                col_names = ["PRN", "Name"]
                attendance = pd.DataFrame(columns=col_names)
                while True:
                    ___, im = cam.read()
                    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                    faces = facecasCade.detectMultiScale(gray, 1.2, 5)
                    for (x, y, w, h) in faces:
                        global Id
                        global prn
                        Id = None
                        prn = None
                        Id, conf = recognizer.predict(gray[y : y + h, x : x + w])
                        prn = prn_mapping_df.loc[prn_mapping_df["label"] == Id, "PRN"].values[0] #if not prn_mapping_df.loc[prn_mapping_df["label"] == Id].empty else "Unknown"
                        if conf < 70:
                            print(conf)
                            global Subject
                            global aa
                            global date
                            global timeStamp
                            Subject = tx.get()
                            ts = time.time()
                            date = datetime.datetime.fromtimestamp(ts).strftime(
                                "%Y-%m-%d"
                            )
                            timeStamp = datetime.datetime.fromtimestamp(ts).strftime(
                                "%H:%M:%S"
                            )
                            aa = df.loc[df["PRN"] == prn]["Name"].values
                            
                            global tt
                            tt = str(prn) + "-" + aa
                            attendance.loc[len(attendance)] = [
                                prn,
                                aa,
                            ]
                            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 260, 0), 4)
                            cv2.putText(
                                im, str(tt), (x + h, y), font, 1, (255, 255, 0,), 4
                            )
                        else:
                            prn = "Unknown"
                            tt = str(prn)
                            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 25, 255), 7)
                            cv2.putText(
                                im, str(tt), (x + h, y), font, 1, (0, 25, 255), 4
                            )
                    if time.time() > future:
                        break

                    attendance = attendance.drop_duplicates(["PRN"], keep="first")
                    cv2.imshow("Filling Entry...", im)
                    key = cv2.waitKey(30) & 0xFF
                    if key == 27:
                        break

                ts = time.time()
                attendance[date] = 1
                date = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S")
                Hour, Minute, Second = timeStamp.split(":")
                path = os.path.join(attendance_path, Subject)
                if not os.path.exists(path):
                    os.makedirs(path)
                fileName = (
                    f"{path}/"
                    + Subject
                    + "_"
                    + date
                    + "_"
                    + Hour
                    + "-"
                    + Minute
                    + "-"
                    + Second
                    + ".csv"
                )
                attendance = attendance.drop_duplicates(["PRN"], keep="first")
                attendance.to_csv(fileName, index=False)

                m = "Valid Entry for " + Subject
                Notifica.configure(
                    text=m,
                    bg="black",
                    fg="#00d4ff",
                    width=33,
                    relief=RIDGE,
                    bd=5,
                    font=("times", 16, "bold"),
                )
                text_to_speech(m)

                Notifica.place(x=180, y=350)

                cam.release()
                cv2.destroyAllWindows()

                import csv
                import tkinter

                root = tkinter.Tk()
                root.title("Entry for " + Subject)
                root.configure(background="black")
                cs = os.path.join(path, fileName)
                print(cs)
                with open(cs, newline="") as file:
                    reader = csv.reader(file)
                    r = 0

                    for col in reader:
                        c = 0
                        for row in col:

                            label = tkinter.Label(
                                root,
                                width=10,
                                height=1,
                                fg="yellow",
                                font=("times", 15, " bold "),
                                bg="black",
                                text=row,
                                relief=tkinter.RIDGE,
                            )
                            label.grid(row=r, column=c)
                            c += 1
                        r += 1
                root.mainloop()
                print(attendance)
            except:
                f = "No Face found for event"
                text_to_speech(f)
                cv2.destroyAllWindows()

    subject = Tk()
    subject.title("Event...")
    subject.geometry("800x500")
    subject.resizable(0, 0)
    subject.configure(background="#121212")

  
    titl = tk.Label(
        subject,
        text="Enter Event Name",
        bg="#121212",
        fg="#00d4ff",
        font=("Segoe UI", 26, "bold"),
        pady=20
    )
    titl.place(x=250, y=15)
    
    Notifica = tk.Label(
        subject,
        text="Valid Entry for Event",
        bg="yellow",
        fg="black",
        width=33,
        height=2,
        font=("times", 15, "bold"),
    )

    def Attf():
        sub = tx.get()
        if sub == "":
            t = "Please enter the event name!!!"
            text_to_speech(t)
        else:
            os.startfile(
                f"Entry Records\\{sub}"
            )

    attf = tk.Button(
        subject,
        text="Check Sheets",
        command=Attf,
        bg="#00d4ff",
        fg="#000000",
        font=("Segoe UI", 12, "bold"),
        relief="flat",
        bd=0,
        height=1,
        width=20,    
        cursor="hand2"
    )
    attf.place(x=400, y=250)

    sub = tk.Label(
        subject,
        text="Enter Event",
        bg="#121212",
        fg="#ffffff",
        font=("Segoe UI", 14)
    )
    sub.place(x=150, y=180)



    tx = tk.Entry(
        subject,
        width=30,
        bd=2,
        bg="#1f1f1f",
        fg="#00ff88",
        insertbackground="#00ff88",
        font=("Segoe UI", 14)
    )
    tx.place(x=300, y=180)


    fill_a = tk.Button(
        subject,
        text="Check Entry",
        command=FillAttendance,
        bg="#00d4ff",
        fg="#000000",
        font=("Segoe UI", 12, "bold"),
        relief="flat",
        bd=0,
        height=1,
        width=20,    
        cursor="hand2"
    )
    fill_a.place(x=150, y=250)

    subject.mainloop()
    
