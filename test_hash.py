from flask import Flask, render_template,request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import hashlib

app=Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask_test.db'
db=SQLAlchemy(app)
migrate = Migrate(app,db)

class User(db.Model):
    __tablename__="user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128),unique=True,nullable=False)
    email = db.Column(db.String(128))
    password = db.Column(db.String(128))
    def __init__(self,_name,_email,_password):
        self.password = hashlib.sha256(_password.encode()).hexdigest()
        self.name=_name
        self.email=_email
    def check_password(self,_password):
        return self.password == hashlib.sha256(_password.encode()).hexdigest()

for i in range(3):
    user=User(input("name:"),input("email:"),input("password:"))
    with app.app_context():
        db.session.add(user)
        db.session.commit()

print(User.query.filter_by(name=input("Your name:")).first())

if __name__=="__main__":
    app.run(debug=True)
    

# from flask import Flask, render_template,request
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
# import hashlib

# app=Flask(__name__)

# db = SQLAlchemy()
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask_test.db'
# db=SQLAlchemy(app)
# # migrate = Migrate(app,db)

# class user(db.Model):
#     __tablename__="user"
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     name = db.Column(db.String(128),unique=True,nullable=False)
#     email = db.Column(db.String(128))
#     password = db.Column(db.String(128))
#     def __init__(self,_name,_email,_password):
#         self.password = hashlib.sha256(_password.encode()).hexdigest()
#         self.name=_name
#         self.email=_email
#     def check_password(self,_password):
#         return self.password == hashlib.sha256(_password.encode()).hexdigest()

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/login',methods=['GET','POST'])
# def login():
#     if request.method=='POST':
#         print(request.values)
#         return render_template('index.html',login_m="NO!!!!")
#     else:
#         return render_template('index.html')
# if __name__=="__main__":
#     app.run(debug=True)