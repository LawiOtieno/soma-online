from . import db

# ======================================= Books Code By Melvin =======================================
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(100))
    password = db.Column(db.String(100))
    admin = db.Column(db.Boolean)



# ======================================= Books Code By Lawrence =======================================
#book_title, book_author, publisher
class Book(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    book_title=db.Column(db.String(200), unique=True)
    book_author=db.Column(db.String(100))
    publisher=db.Column(db.String(100))
    book_url=db.Column(db.String(250), unique=True)

