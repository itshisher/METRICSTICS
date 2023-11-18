
import uuid
'''
this class is used to create and keep the session 
'''
class SessionManager:
    def __init__(self):
        # an instance method that initializes a newly created object
        self.sessions = {}

    def create_session(self, user_data):
        # function to create the session with different users
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = user_data
        return session_id

    def get_user_data(self, session_id):
        # function to get data from different users
        return self.sessions.get(session_id)

    def end_session(self, session_id):
        # function to end the session
        if session_id in self.sessions:
            del self.sessions[session_id]

    def all_sessions(self):
        return self.sessions
