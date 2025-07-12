import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image

def open_about_page():
    about_window = tk.Toplevel()
    about_window.title("About - Face Recognition Entry System")
    about_window.geometry("1000x700")
    about_window.configure(bg="#f9fafb")
    about_window.resizable(False, False)

    # Title
    title = tk.Label(
        about_window,
        text="Face Recognition Entry System",
        bg="#f9fafb",
        fg="#1f2937",
        font=("Segoe UI", 22, "bold"),
        pady=10
    )
    title.pack()

    # Vision Section
    vision_frame = Frame(about_window, bg="white", bd=2, relief="solid")
    vision_frame.pack(padx=30, pady=20, fill="x")
    Label(
        vision_frame,
        text="Vision",
        bg="white",
        fg="#1e3a8a",
        font=("Segoe UI", 18, "bold"),
        pady=10
    ).pack()
    Label(
        vision_frame,
        text="Our vision is to create a secure and smart entry experience using facial recognition. "
             "We aim to make event entries more streamlined, contactless, and efficient using AI technology.",
        wraplength=900,
        bg="white",
        fg="#374151",
        font=("Segoe UI", 12),
        justify=LEFT,
        padx=20,
        pady=10
    ).pack()

    # Mission Section
    mission_frame = Frame(about_window, bg="white", bd=2, relief="solid")
    mission_frame.pack(padx=30, pady=10, fill="x")
    Label(
        mission_frame,
        text="Mission",
        bg="white",
        fg="#047857",
        font=("Segoe UI", 18, "bold"),
        pady=10
    ).pack()
    Label(
        mission_frame,
        text="Our mission is to develop a facial recognition-based entry system that reduces human intervention, enhances security, "
             "and provides real-time attendance tracking in public or private events.",
        wraplength=900,
        bg="white",
        fg="#374151",
        font=("Segoe UI", 12),
        justify=LEFT,
        padx=20,
        pady=10
    ).pack()

    # Our Team Section
    team_frame = Frame(about_window, bg="white", bd=2, relief="solid")
    team_frame.pack(padx=30, pady=20, fill="x")

    Label(
        team_frame,
        text="Our Team",
        bg="white",
        fg="#b45309",
        font=("Segoe UI", 18, "bold"),
        pady=10
    ).pack()

    team_members_frame = Frame(team_frame, bg="white")
    team_members_frame.pack(pady=10)

    def create_member(frame, image_path, name, link):
        member_frame = Frame(frame, bg="white", bd=1, relief="solid", padx=10, pady=10)
        member_frame.pack(side=LEFT, padx=20)

        try:
            img = Image.open(image_path).resize((80, 80))
            photo = ImageTk.PhotoImage(img)
            img_label = Label(member_frame, image=photo, bg="white")
            img_label.image = photo  
            img_label.pack()
        except Exception:
            Label(member_frame, text="No Image", bg="white", fg="gray").pack()

        Label(member_frame, text=name, font=("Segoe UI", 12, "bold"), bg="white").pack(pady=5)
        link_label = Label(member_frame, text=link, fg="#3b82f6", cursor="hand2", bg="white", font=("Segoe UI", 10, "underline"))
        link_label.pack()

    # Add team members
    create_member(team_members_frame, "images/somesh.jpg", "Somesh Alone", "LinkedIn Profile")
    create_member(team_members_frame, "images/yadnyesh.jpg", "Yadnyesh Pande", "LinkedIn Profile")
    create_member(team_members_frame, "images/pratik.jpg", "Pratik Papanwar", "LinkedIn Profile")