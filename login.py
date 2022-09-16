from chat import *
from flask import Flask
from flask import make_response
from flask import render_template
from flask import url_for
from flask import request



app = Flask(__name__)
DB_PATH = "./data/login.db"

def escape(s):
    "Escape the string S"
    return s


@app.get("/login")
def login():
    "The login page upon a GET request"
       
    return ""

@app.post("/login")
def login():
    "The login page upon a POST request"
       
    username = escape(str(request.form['username']))
    password = escape(str(request.form['password']))

   
    return ""

