
from tkinter import Tk
from database import Database
from login import Login
from signup import Signup
from session import SessionManager
'''
main class to execute 
include all other classes 
'''
class MainApp:
    def __init__(self, root):
        # an instance method that initializes a newly created object
        self.root = root
        self.database = Database()
        self.session = SessionManager()
        self.start_app()

    def start_app(self):
        # when execute the program first show login page
        self.show_login()

    def show_login(self):
        # login functionalities are included here
        self.login = Login(self.root, self.database, self.show_signup)

    def show_signup(self):
        # users can choose to signup by clicking on signup button
        self.signup = Signup(self.root, self.database, self.show_login)

    def clear_widgets(self):
        # end the program
        for widget in self.root.winfo_children():
            widget.destroy()

def main():
    root = Tk()
    root.title("Modularized Application")
    app = MainApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
