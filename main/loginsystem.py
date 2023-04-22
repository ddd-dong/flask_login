from flask import Blueprint, render_template,redirect,url_for,request
from main.user import isLogin,loginState,signinState,logoutAct
app_route = Blueprint('loginsystem',__name__)

@app_route.route('/')
def index():
    return render_template('home.html')

@app_route.route('/users')
def userPage(): 
    _isLogin = isLogin()
    if _isLogin:
        return render_template('userPage.html',userN = _isLogin)
    return redirect(url_for('loginsystem.login'))

@app_route.route('/login',methods=['GET','POST'])
def login():
    if request.method!='POST':
        if isLogin():
            return redirect(url_for('loginsystem.userPage'))
        return render_template('login.html')
    
    _loginErro = loginState(request.form)
    if _loginErro:
        return render_template('login.html',login_m=_loginErro)
    return redirect(url_for('loginsystem.userPage'))

@app_route.route('/signin',methods=['GET','POST'])
def signin():
    if request.method !='POST':
        return render_template('signin.html')
    _signinErro = signinState(request.form)
    if _signinErro:
        return render_template('signin.html',signin_m=_signinErro)
    return redirect(url_for("loginsystem.login"))

@app_route.route('/logout')
def logout():
    logoutAct()
    return redirect(url_for('loginsystem.index'))