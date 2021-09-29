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


if __name__ == '__main__':
    app.run(debug=True)