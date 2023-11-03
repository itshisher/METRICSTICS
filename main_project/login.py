import tkinter as tk
from tkinter import ttk, messagebox
from utils import create_label_entry
from calculator import StatisticsCalculator

class Login:
    def __init__(self, root, database, show_signup):
        self.root = root
        self.database = database
        self.show_signup = show_signup
        self.login_ui()

    def login_ui(self):
        self.clear_widgets()
        self.root.title("Login")

        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        title = ttk.Label(self.root, text="Login", font=("Arial", 24))
        title.pack(pady=20)

        create_label_entry(self.root, "Username:", self.username_var)
        create_label_entry(self.root, "Password:", self.password_var, True)

        btn_frame = ttk.Frame(self.root)
        login_btn = ttk.Button(btn_frame, text="Login", command=self.login)
        login_btn.pack(side=tk.LEFT, padx=10)
        signup_btn = ttk.Button(btn_frame, text="Signup", command=self.show_signup)
        signup_btn.pack(side=tk.LEFT, padx=10)
        btn_frame.pack(pady=20)

    def clear_widgets(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def login(self):
        username = self.username_var.get()
        password = self.password_var.get()

        if result := self.database.authenticate_user(username, password):
            app = StatisticsCalculator(self.root)
        else:
            messagebox.showerror("Error", "User not found!")

