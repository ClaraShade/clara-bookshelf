from . import db


class Book(db.Model):
    # the ISBN number is set to be the primary key, because it is a unique id of a publication
    # and is necessary to tell is an issue already in database
    isbn = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    published = db.Column(db.DateTime)
    pages = db.Column(db.Integer)
    cover = db.Column(db.String(200))
    language = db.Column(db.String(30))
