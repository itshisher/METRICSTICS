
class Session:
    def __init__(self):
        self.user_data = None

    def login(self, user_data):
        self.user_data = user_data

    def logout(self):
        self.user_data = None

    def get_user_data(self):
        return self.user_data
