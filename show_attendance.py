import pandas as pd
from glob import glob
import os
import tkinter
import csv
import tkinter as tk
from tkinter import *

def subjectchoose(text_to_speech):
    def calculate_attendance():
        Subject = tx.get()
        if Subject=="":
            t='Please enter the event name.'
            text_to_speech(t)
    
        filenames = glob(
            f"Entry Records\\{Subject}\\{Subject}*.csv"
        )
        df = [pd.read_csv(f) for f in filenames]
        newdf = df[0]
        for i in range(1, len(df)):
            newdf = newdf.merge(df[i], how="outer")
        newdf.fillna(0, inplace=True)
        newdf.to_csv(f"Entry Records\\{Subject}\\entryRecords.csv", index=False)

        root = tkinter.Tk()
        root.title("Entry Records for "+Subject)
        root.configure(background="black")
        cs = f"Entry Records\\{Subject}\\entryRecords.csv"
        with open(cs) as file:
            reader = csv.reader(file)
            r = 0

            for col in reader:
                c = 0
                for row in col:

                    label = tkinter.Label(
                        root,
                        width=15,
                        height=1,
                        fg="#00d4ff",
                        font=("times", 12),
                        bg="black",
                        text=row,
                        relief=tkinter.RIDGE,
                    )
                    label.grid(row=r, column=c)
                    c += 1
                r += 1
        root.mainloop()
        print(newdf)

    subject = Tk()
    subject.title("Event...")
    subject.geometry("800x700")
    subject.resizable(0, 0)
    subject.configure(background="#121212")

    titl = tk.Label(
        subject,
        text="Which event are you looking ?",
        bg="#121212",
        fg="#00d4ff",
        font=("Segoe UI", 26, "bold"),
        pady=20
    )
    titl.place(x=150, y=15)

    def Attf():
        sub = tx.get()
        if sub == "":
            t="Please enter the event name!!!"
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
        text="View Entry Records",
        command=calculate_attendance,
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
