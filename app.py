from flask import Flask, render_template,request,url_for,redirect,flash,session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import hashlib

# flask-login
# from flask_login import LoginManager,login_required,login_user,UserMixin,logout_user

app=Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask_test.db'
app.config['SECRET_KEY']= 'ddd'
db=SQLAlchemy(app)
migrate = Migrate(app,db)

# # __flask-login__
# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = 'login'
# ________________


class User(db.Model): #,UserMixin
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

# __flask-login___
# @login_manager.user_loader
# def load_user(user_id):
#     return db.session.get(User,user_id)
# _______________


@app.route('/')
def index():
    return render_template('home.html')

@app.route('/users')
# @login_required
def userPage():
    print(session)
    if session:
        print(db.session.get(User,session['user_id']))
        return render_template('userPage.html',userN=db.session.get(User,session['user_id']))
    return redirect(url_for('login'))

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        print(request.form)
        userN = User.query.filter_by(name=request.form['account']).first()
        # print(userN)
        if userN and userN.check_password(request.form['password']):
            # login_user(userN)
            session['user_id']=userN.id
            return redirect(url_for('userPage'))
        else:
            return render_template('login.html',login_m="帳號或密碼錯誤")
    else:
        return render_template('login.html')

@app.route('/signin',methods=['GET','POST'])
def signin():
    if request.method=='POST':
        print(request.form)
        if request.form['password']==request.form['password_c']:
            if not(User.query.filter_by(name=request.form['account']).first()):
                userN=User(request.form['account'],request.form['email'],request.form['password'])
                with app.app_context():
                    db.session.add(userN)
                    db.session.commit()
                return redirect(url_for('login'))
            else:
                return render_template('signin.html',signin_m="帳號名稱不可用")
        else:
            return render_template('signin.html',signin_m="密碼確認與密碼不同")
    else:
        return render_template('signin.html')

@app.route('/logout')
def logout():
    # logout_user()
    # session.pop('user_id')
    session.clear()
    return redirect(url_for('index'))

# with app.app_context():
#     print(User.query.filter_by(name=input("Your name:")).first().check_password(input("Your password:")))

if __name__=="__main__":
    app.run(debug=True)
    