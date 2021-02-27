from flaskr.db import MySqlDB, User, LogIn
import random
import string

class Auth:
    def __init__(self):
        self.db = MySqlDB("database2")
    
    def get_token(self, N):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=N))

    def login(self, username, password):
        credentials = self.db.query(User, {User.username: username, User.password: password})
        if(len(credentials) == 1):
            user = credentials[0]
            token = self.get_token(20)
            if user.login is not None:
                self.db.session.delete(user.login)
            login_entry = LogIn(token=token, is_logged_in=True)
            user.login = login_entry
            self.db.session.commit()
            return token
        return None

    def logout(self, username, password):
        credentials = self.db.query(User, {User.username: username, User.password: password})
        if(len(credentials) == 1):
            user = credentials[0]
            if user.login is not None:
                self.db.session.delete(user.login)  
                self.db.session.commit()      


if __name__ == "__main__":
    auth = Auth()
    print(auth.logout("carla", "harla123"))




