import jwt
from enum import unique
from os import name
from flask import Flask,jsonify,request,make_response
from flask.helpers import make_response
import uuid
from werkzeug.security import generate_password_hash,check_password_hash
from flask_sqlalchemy import SQLAlchemy
import datetime
from functools import wraps

app = Flask(__name__)

app.config['SECRET_KEY'] = '1234LAME'
app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql+psycopg2://access:lawioti@localhost/somaonline'


db = SQLAlchemy(app)


# ======================================= Users Code By Melvin =======================================

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(100))
    password = db.Column(db.String(100))
    admin = db.Column(db.Boolean)




if __name__ == '__main__':
    app.run(debug=True)