from . import main
from .. import db
from ..models import User, Book
from enum import unique
from os import name
from flask import Flask,jsonify,request,make_response
import uuid
from werkzeug.security import generate_password_hash,check_password_hash

# "name","password"
## Getting All Users
## Getting Single User
## Create User
## Update/Promote/Put User
## Delete Single User

# "book_title", "book_author", "publisher", "book_url"
## Getting All Books
## Getting Single book
## Create Single Book
## Update/Promote/Put Single Book
## Delete Single Book



# ======================================= Users Code By Melvin =======================================

# ## User login
# @main.route('/login')
# def login():
#     auth=request.authorization

#     if not auth or not auth.username or not auth.password:
#         return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})
#     user=User.query.filter_by(name=auth.username).first()

#     if not user:
#         return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})
#     if check_password_hash(user.password, auth.password):
#         token= jwt.encode({'public_id' : user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=20)}, app.config['SECRET_KEY'])

#         return jsonify({'token': token})

#     return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})    



## Getting All Users
@main.route('/users', methods=['GET'])
# @token_required  
def get_all_users():
    
    ## Give user authentication to update the content
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
@main.route('/user/<public_id>', methods=['GET'])
# @token_required
def get_one_user(public_id):

    ## Give user authentication to update the content
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

# Create User
@main.route('/user', methods=['POST'])
# @token_required
def create_user():

    ## Give user authentication to update the content
    # if not current_user.admin:
    #     return jsonify({'message': "You cannot perform that action"})

    data=request.get_json()
    hashed_password=generate_password_hash(data['password'], method='sha256')
    new_user=User(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, admin=False)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message" : "New user created successfully!"})

## Update/Promote/Put User 
@main.route('/user/<public_id>', methods=['PUT'])
# @token_required
def promote_user(public_id):

    ## Give user authentication to update the content
    # if not current_user.admin:
    #     return jsonify({'message': "You cannot perform that action"})

    user=User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message' :'No user found'})

    user.admin=True
    db.session.commit()

    return jsonify({'message': 'User has been promoted to admin'})


## Delete Single User
@main.route('/user/<public_id>', methods=['DELETE'])  
# @token_required
def delete_user( public_id):

    ## Give user authentication to update the content
    # if not current_user.admin:
    #     return jsonify({'message': "You cannot perform that action"})

    user=User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message' :'No user found'})

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': 'User deleted successfully'}) 


# ======================================= Books Code By Lawrence =======================================

## Getting All Books
@main.route('/books', methods=['GET'])
def get_all_books():
    books = Book.query.all()
    output = []
    for book in books:
        book_data ={}
        book_data['book_title']=book.book_title
        book_data['book_author']=book.book_author
        book_data['publisher']=book.publisher
        book_data['book_url']=book.book_url

        output.append(book_data)

    return jsonify({'books' : output})


## Getting Single book
@main.route('/book/<book_title>', methods=['GET'])
def get_one_book(book_title):

    book=Book.query.filter_by(book_title=book_title).first()

    if not book:
        return jsonify({'message' :'No book found with that name'})

    book_data={}
    book_data['book_title']=book.book_title
    book_data['book_author']=book.book_author
    book_data['publisher']=book.publisher
    book_data['book_url']=book.book_url

    return jsonify({'book': book_data})

## Create Single Book
@main.route('/book', methods=['POST'])
def create_book():

    data=request.get_json()

    new_book=Book(book_title=data['book_title'], book_author=data['book_author'],publisher=data['publisher'],book_url=data['book_url'])
    # ,book_url=data['book_url']

    db.session.add(new_book)
    db.session.commit()

    return jsonify({"message" : "New book  created successfully!"})


## Update/Promote/Put Single Book
@main.route('/book/<book_title>', methods=['PUT'])
def promote_book(book_title):
    book=Book.query.filter_by(book_title=book_title).first()

    if not book:
        return jsonify({'message' :'No book found'})

    book.admin=True
    db.session.commit()

    return jsonify({'message': 'The book has been promoted to be the most trending book '})

## Delete Single Book
@main.route('/book/<book_title>', methods=['DELETE'])  
def delete_book(book_title):

    book=Book.query.filter_by(book_title=book_title).first()

    if not book:
        return jsonify({'message' :'No book  found'})

    db.session.delete(book)
    db.session.commit()

    return jsonify({'message': 'The book has been deleted successfully'})

