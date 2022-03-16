from . import db
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
import json

class Book(db.Model):
    isbn: int
    title: str
    author: str
    published: str
    pages: int
    cover: str
    language: str
    # the ISBN number is set to be the primary key, because it is a unique id of a publication
    # and is necessary to tell is an issue already in database
    isbn = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    published = db.Column(db.String(20), nullable=False)
    pages = db.Column(db.Integer, nullable=False)
    cover = db.Column(db.String(200), nullable=False)
    language = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"Book(isbn = {self.isbn}, title = {self.title}," \
               f"author = {self.author}, published = {self.published}," \
               f"pages = {self.pages}, cover = {self.cover}," \
               f"language = {self.language})"

    def to_dict(self):
        return {k: v for k, v in self.__dict__.items() if not k.startswith('_')}

