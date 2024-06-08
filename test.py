import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import json
import os
import subprocess

# File to store user data
USER_DATA_FILE = 'user_data.json'

# Load user data from file
def load_user_data():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r') as file:
            return json.load(file)
    else:
        return {}

# Save user data to file
def save_user_data(data):
    with open(USER_DATA_FILE, 'w') as file:
        json.dump(data, file)

# User data dictionary
user_data = load_user_data()

# Initialize main window for login/signup
root = tk.Tk()
root.title("Game Login System")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}")
root.state('zoomed')

# Background image
bg_image = Image.open("Image\login.png")
bg_photo = ImageTk.PhotoImage(bg_image)

# Canvas for background
canvas = tk.Canvas(root, width=screen_width, height=screen_height)
canvas.pack(fill="both", expand=True)
canvas.create_image(screen_width / 2, screen_height / 2, anchor="center", image=bg_photo)

# Frames for login and signup
login_frame = tk.Frame(canvas, bg="white", width=400, height=600)
signup_frame = tk.Frame(canvas, bg="white", width=400, height=600)

def show_frame(frame):
    frame.tkraise()

for frame in (login_frame, signup_frame):
    canvas.create_window(screen_width / 2, screen_height / 2, window=frame, anchor="center")

def login():
    username = username_entry.get()
    password = password_entry.get()

    if username in user_data and user_data[username]['password'] == password:
        messagebox.showinfo("Login Successful", f"Welcome back {username}! You were on level {user_data[username]['level']}.")
        root.destroy()
        subprocess.Popen(["python", "Index.py"])
    else:
        messagebox.showerror("Error", "User doesn't exist or wrong password")

def signup():
    username = new_username_entry.get()
    password = new_password_entry.get()

    if username in user_data:
        messagebox.showerror("Error", "User already exists")
    else:
        user_data[username] = {'password': password, 'level': 1}
        save_user_data(user_data)
        messagebox.showinfo("Signup Successful", "User created successfully! You can now login.")
        show_frame(login_frame)

# Login frame widgets
tk.Label(login_frame, text="Login", font=("Arial", 24)).pack(pady=10)
tk.Label(login_frame, text="Username").pack(pady=5)
username_entry = tk.Entry(login_frame)
username_entry.pack(pady=5)
tk.Label(login_frame, text="Password").pack(pady=5)
password_entry = tk.Entry(login_frame, show="*")
password_entry.pack(pady=5)
tk.Button(login_frame, text="Login", command=login).pack(pady=10)
tk.Button(login_frame, text="Sign Up", command=lambda: show_frame(signup_frame)).pack(pady=10)

# Signup frame widgets
tk.Label(signup_frame, text="Sign Up", font=("Arial", 24)).pack(pady=10)
tk.Label(signup_frame, text="Username").pack(pady=5)
new_username_entry = tk.Entry(signup_frame)
new_username_entry.pack(pady=5)
tk.Label(signup_frame, text="Password").pack(pady=5)
new_password_entry = tk.Entry(signup_frame, show="*")
new_password_entry.pack(pady=5)
tk.Button(signup_frame, text="Sign Up", command=signup).pack(pady=10)
tk.Button(signup_frame, text="Back to Login", command=lambda: show_frame(login_frame)).pack(pady=10)

# Start with login frame
show_frame(login_frame)

# Main loop for login/signup window
root.mainloop()