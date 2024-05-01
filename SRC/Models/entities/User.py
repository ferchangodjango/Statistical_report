from werkzeug.security import check_password_hash
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self,id,USERNAME,PASSWORD) -> None:
        self.id=id
        self.USERNAME=USERNAME
        self.PASSWORD=PASSWORD

    @classmethod
    def CheckPassword(self,cryptopassword,password):
        return check_password_hash(cryptopassword,password)


    