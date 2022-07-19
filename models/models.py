import bcrypt
from app import login_manager
from bson.objectid import ObjectId
from flask_login import UserMixin

class User(UserMixin):
    __tablename__ = 'users'

    # columns
    id = ObjectId()
    name = str()
    pwd = bytes()

    def __init__(self, id, name, pwd):
        self.id = id
        self.name = name
        self.pwd = pwd
        # 實際存入的為password_hash，而非password本身
        # self.pwd = bcrypt.hashpw(pwd.encode('utf-8'), bcrypt.gensalt())
    
    def check_password(self, input_pwd, db_pwd):
        return bcrypt.checkpw(input_pwd.encode('utf-8'), db_pwd)

    def check_username(self):
        """檢查username"""
        if User.query.filter_by(username=self.name).first():
            raise "使用者名稱已經存在"
        return 

    def add_user(self, user):
        pass
        # user_col.insert_one({'name' : username, 'password' : hashpass})

