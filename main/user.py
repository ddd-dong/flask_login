import hashlib
from flask import session
from pymongo import MongoClient
from bson import ObjectId

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
    def check_password(self,_password)->bool:
        return self.password == hashlib.sha256(_password.encode()).hexdigest()
    
def isLogin()->dict:
    if session:
        return collection.find_one({"_id":ObjectId(session['user_id'])})
    return None

def loginState(_Rform)->str:
        if _Rform['account'] == "":
            return "帳號欄位為空"
        _user = collection.find_one({"name":_Rform['account']})
        if not _user:
            return "帳號不存在"
        userN = User(_user)
        if not userN.check_password(_Rform['password']):
            return "帳號或密碼錯誤"
        session['user_id']=str(userN.data["_id"])
        return None
            
def signinState(_Rform)->str:
    if _Rform['password']!=_Rform['password_c']:
        return "密碼確認與密碼不同"
    if _Rform['account'] == "":
        return "帳號欄位為空"
    if collection.find_one({"name":_Rform['account']}):
        return "帳號名稱不可用"
    userN=User({"name":_Rform['account'],"password":_Rform['password'],"email":_Rform['email']})
    collection.insert_one(userN.data)
    return None
    
def logoutAct()->None:
    session.clear()