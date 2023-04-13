from flask import Flask, render_template,request,url_for,redirect,flash,session
import hashlib
from pymongo import MongoClient
from bson import ObjectId

app=Flask(__name__)
app.config['SECRET_KEY']= 'ddd'
client = MongoClient("mongodb+srv://user_tst_1:aaa@mongodblearning.bafyb7n.mongodb.net/?retryWrites=true&w=majority",tls=True,tlsAllowInvalidCertificates=True)
print(client.list_database_names())

db = client["pwtst"]
collection = db["pwt"]
class User(): 
    def __init__(self,_data:dict):
        self.password = hashlib.sha256(_data["password"].encode()).hexdigest()
        self.name=_data["name"]
        self.email=_data["email"]
        self.data=_data
    def check_password(self,_password):
        return self.password == hashlib.sha256(_password.encode()).hexdigest()

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/users')
def userPage():
    # print(session)
    if session:
        # print(collection.find_one({"_id":ObjectId(session['user_id'])}))
        return render_template('userPage.html',userN = collection.find_one({"_id":ObjectId(session['user_id'])}))
    return redirect(url_for('login'))

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        # print(request.form)
        # print(session)
        if request.form['account'] == "":
            return render_template('login.html',login_m="帳號欄位為空")
        _user = collection.find_one({"name":request.form['account']})
        if not _user:
            return render_template('login.html',login_m="帳號或密碼錯誤")
        userN = User(_user)
        if userN.check_password(request.form['password']):
            session['user_id']=str(userN.data["_id"])
            return redirect(url_for('userPage'))
        else:
            return render_template('login.html',login_m="帳號或密碼錯誤")
    else:
        return render_template('login.html')

@app.route('/signin',methods=['GET','POST'])
def signin():
    if request.method !='POST':
        return render_template('signin.html')
    # print(request.form)
    if request.form['password']!=request.form['password_c']:
        return render_template('signin.html',signin_m="密碼確認與密碼不同")
    if request.form['account'] == "":
        return render_template('signin.html',signin_m="帳號欄位為空")
    if not(collection.find_one({"name":request.form['account']})):
        userN=User({"name":request.form['account'],"password":request.form['password'],"email":request.form['email']})
        collection.insert_one(userN.data)
        return redirect(url_for('login'))
    else:
        return render_template('signin.html',signin_m="帳號名稱不可用")

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__=="__main__":
    app.run(debug=True)
    