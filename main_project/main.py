
from tkinter import Tk
from database import Database
from login import Login
from signup import Signup
from session import Session

class MainApp:
    def __init__(self, root):
        self.root = root
        self.database = Database()
        self.session = Session()
        self.start_app()

    def start_app(self):
        self.show_login()

    def show_login(self):
        self.login = Login(self.root, self.database, self.show_signup)

    def show_signup(self):
        self.signup = Signup(self.root, self.database, self.show_login)

    def clear_widgets(self):
        for widget in self.root.winfo_children():
            widget.destroy()

def main():
    root = Tk()
    root.title("Modularized Application")
    app = MainApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
