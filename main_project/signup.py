import tkinter as tk
from tkinter import ttk, messagebox
from utils import create_label_entry
import mysql.connector

class Signup:
    def __init__(self, root, database, show_login):
        self.root = root
        self.database = database
        self.show_login = show_login
        self.signup_ui()

    def signup_ui(self):
        self.clear_widgets()
        self.root.title("Signup")

        self.fullname_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.confirm_password_var = tk.StringVar()

        title = ttk.Label(self.root, text="Signup", font=("Arial", 24))
        title.pack(pady=20)

        create_label_entry(self.root, "Full Name:", self.fullname_var)
        create_label_entry(self.root, "Email:", self.email_var)
        create_label_entry(self.root, "Username:", self.username_var)
        create_label_entry(self.root, "Password:", self.password_var, True)
        create_label_entry(self.root, "Confirm Password:", self.confirm_password_var, True)

        signup_btn = ttk.Button(self.root, text="Register", command=self.signup)
        signup_btn.pack(pady=20)
        back_btn = ttk.Button(self.root, text="Back to Login", command=self.show_login)
        back_btn.pack(pady=10)

    def clear_widgets(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def signup(self):
        fullname = self.fullname_var.get()
        email = self.email_var.get()
        username = self.username_var.get()
        password = self.password_var.get()
        confirm_password = self.confirm_password_var.get()

        if password == confirm_password:
            try:
                if result := self.database.create_user(
                    fullname, email, username, password
                ):
                    messagebox.showinfo("Success", "Registration Successful!")
                    self.show_login()
                else:
                    messagebox.showerror("Error", "Failed to update in database")
            except mysql.connector.errors.IntegrityError:
                messagebox.showerror("Error", "Username or Email already exists!")
        else:
            messagebox.showerror("Error", "Passwords do not match!")
