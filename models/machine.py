import hashlib
from pymongo import MongoClient
from bson import ObjectId

client = MongoClient("mongodb+srv://user_tst_1:aaa@mongodblearning.bafyb7n.mongodb.net/?retryWrites=true&w=majority",tls=True,tlsAllowInvalidCertificates=True)
db = client["pwtst"]
collection = db["pwt"]
print(client.list_database_names())

class User(): 
    def __init__(self,_data:dict):
        self.password = hashlib.sha256(_data["password"].encode()).hexdigest()
        self.name=_data["name"]
        self.email=_data["email"]
        self.data=_data
    def check_password(self,_password):
        return self.password == hashlib.sha256(_password.encode()).hexdigest()
    
