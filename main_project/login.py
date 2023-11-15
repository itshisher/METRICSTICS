import tkinter as tk
from session import SessionManager
from tkinter import ttk, messagebox
from utils import create_label_entry
from calculator import StatisticsCalculator

class Login:
    def __init__(self, root, database, show_signup):
        self.root = root
        self.database = database
        self.show_signup = show_signup
        self.login_ui()        
        self.session_manager = SessionManager()


    def login_ui(self):
        self.clear_widgets()
        self.root.title("Login")

        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        title = ttk.Label(self.root, text="Login", font=("Arial", 24))
        title.pack(pady=20)

        create_label_entry(self.root, "Username:", self.username_var)
        create_label_entry(self.root, "Password:", self.password_var, True)

        # Main frame for all buttons
        main_btn_frame = ttk.Frame(self.root)

        # Frame for Login and Signup buttons
        login_signup_frame = ttk.Frame(main_btn_frame)
        login_btn = ttk.Button(login_signup_frame, text="Login", command=self.login)
        login_btn.pack(side=tk.LEFT, padx=10, pady=10)
        signup_btn = ttk.Button(login_signup_frame, text="Signup", command=self.show_signup)
        signup_btn.pack(side=tk.RIGHT, padx=10, pady=10)
        login_signup_frame.pack(side=tk.TOP, fill=tk.X)

        # Frame for Guest button
        guest_frame = ttk.Frame(main_btn_frame)
        guest_btn = ttk.Button(guest_frame, text="Guest", command=self.guest)
        guest_btn.pack(side=tk.TOP, fill=tk.X, padx=10)
        guest_frame.pack(side=tk.TOP, fill=tk.X, padx=0)

        # Packing the main frame
        main_btn_frame.pack(pady=10)

    def clear_widgets(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def login(self):
        username = self.username_var.get()
        password = self.password_var.get()
        if user_data := self.database.authenticate_user(username, password):
            # Assuming authenticate_user returns user-specific data on successful authentication
            session_id = self.session_manager.create_session(user_data)  # Create a new session
            app = StatisticsCalculator(self.root, session_id, username, self.login_ui)  # Pass the session ID to the application
        else:
            messagebox.showerror("Error", "User not found!")

    def guest(self):
        app = StatisticsCalculator(self.root, None, 'Guest', self.login_ui)  # Pass the session ID to the application
