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

## User Token
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token=request.headers['x-access-token']

        if not token:
            return jsonify({'message' : 'Token is missing for authentication'}), 401


        # if token is there 
        try:
            data =jwt(token, app.config['SECRET_KEY']) 
            current_user =User.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return  f(current_user, *args , **kwargs)  
    return decorated

## User login
@app.route('/login')
def login():
    auth=request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})
    user=User.query.filter_by(name=auth.username).first()

    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})
    if check_password_hash(user.password, auth.password):
        token= jwt.encode({'public_id' : user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=20)}, app.config['SECRET_KEY'])

        return jsonify({'token': token})

    return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})    

## Getting All Users
@app.route('/user', methods=['GET'])
# @token_required  
def get_all_users():
    
    # # Give users authentication to update the content
    # if not current_user.admin:
    #     return jsonify({'message': "You cannot perform that action"})


    users = User.query.all()
    output = []
    for user in users:
        user_data ={}
        user_data['public_id']=user.public_id
        user_data['name']=user.name
        user_data['password']=user.password
        user_data['admin']=user.admin
        output.append(user_data)
    return jsonify({'users' : output})

## Getting Single User
@app.route('/user/<public_id>', methods=['GET'])
# @token_required
def get_one_user(public_id):
    
    # # Give user authentication to update the content
    # if not current_user.admin:
    #     return jsonify({'message': "You cannot perform that action"})

    user=User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message' :'No user found with that name'})
    user_data={}
    user_data['public_id']=user.public_id
    user_data['name']=user.name
    user_data['password']=user.password
    user_data['admin']=user.admin    
    return jsonify({'user': user_data})   

## Create User
@app.route('/user', methods=['POST'])
# @token_required
def create_user():
    
    # # Give user authentication to update the content
    # if not current_user.admin:
    #     return jsonify({'message': "You cannot perform that action"})
    
    data=request.get_json()

    hashed_password=generate_password_hash(data['password'], method='sha256')

    new_user=User(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, admin=False)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message" : "New user created successfully!"})   

## Update/Promote/Put User
@app.route('/user/<public_id>', methods=['PUT'])
# @token_required
def promote_user(public_id):

    # # Give user authentication to update the content
    # if not current_user.admin:
    #     return jsonify({'message': "You cannot perform that action"})

    user=User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message' :'No user found'})
    
    user.admin=True
    db.session.commit()   
    
    return jsonify({'message': 'The user has been promoted to Admin'})

## Delete User 
@app.route('/user/<public_id>', methods=['DELETE'])  
# @token_required
def delete_user( public_id):

    # # Give user authentication to update the content
    # if not current_user.admin:
    #     return jsonify({'message': "You cannot perform that action"})

    user=User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message' :'No user found'})
    
    db.session.delete(user)
    db.session.commit()
    
    return jsonify({'message': 'User deleted successfully'})    




# ======================================= Books Code By Lawrence =======================================

#book_title, book_author, publisher
class Book(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    book_title=db.Column(db.String(300), unique=True)
    book_author=db.Column(db.String(100))
    publisher=db.Column(db.String(100))



## Getting All Books
@app.route('/books', methods=['GET'])
def get_all_books():
    books = Book.query.all()
    output = []
    for book in books:
        book_data ={}
        book_data['book_title']=book.book_title
        book_data['book_author']=book.book_author
        book_data['publisher']=book.publisher

        output.append(book_data)

    return jsonify({'books' : output})


## Getting Single book
@app.route('/book/<book_title>', methods=['GET'])
def get_one_book(book_title):

    book=Book.query.filter_by(book_title=book_title).first()

    if not book:
        return jsonify({'message' :'No book found with that name'})

    book_data={}
    book_data['book_title']=book.book_title
    book_data['book_author']=book.book_author
    book_data['publisher']=book.publisher

    return jsonify({'book': book_data})

# ## Create Single Book
# @app.route('/book/', methods=['POST'])
# def create_book():

#     data=request.get_json()

#     new_book=Book(book_title=data['book_title'], book_author=data['book_author'],publisher=data['publisher'])

#     db.session.add(new_book)
#     db.session.commit()

#     return jsonify({"message" : "New book  created successfully!"})


# ## Update/Promote/Put Single Book
# @app.route('/book/<book_title>', methods=['PUT'])
# def promote_book(book_title):
#     book=Book.query.filter_by(book_title=book_title).first()

#     if not book:
#         return jsonify({'message' :'No book found'})

#     book.admin=True
#     db.session.commit()

#     return jsonify({'message': 'The book has been promoted to be the most trending book '})

# ## Delete Single Book
# @app.route('/book/<book_title>', methods=['DELETE'])  
# def delete_book(book_title):

#     book=Book.query.filter_by(book_title=book_title).first()

#     if not book:
#         return jsonify({'message' :'No book  found'})

#     db.session.delete(book)
#     db.session.commit()

#     return jsonify({'message': 'The book has been deleted successfully'})


if __name__ == '__main__':
    app.run(debug=True)