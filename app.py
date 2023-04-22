from flask import Flask, render_template,request,url_for,redirect,flash,session,Blueprint
from main.loginsystem import app_route


app = Flask(__name__)
app.config['SECRET_KEY']= 'ddd'

app.register_blueprint(app_route)



if __name__=="__main__":
    app.run(debug=True)

    