from flask import Blueprint, render_template, request, flash, jsonify, make_response
from .models import Book
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from . import db
from . import requests
import json

# fom werkzeug.security import generate_password_hash, check_password_hash

views = Blueprint('views', __name__)

"""resource_fields = {
    "isbn": fields.Integer,
    "title": fields.String,
    "author": fields.String,
    "published": fields.String,
    "pages": fields.Integer,
    "cover": fields.String,
    "language": fields.String
}"""

@views.route('/bookshelf', methods=['GET', 'POST', 'PUT', 'DELETE', 'UPDATE'])
def bookshelf():
    # if request.method == 'GET':

    return render_template("bookshelf.html")


@views.route('/add', methods=['GET', 'POST', 'PUT', 'DELETE', 'UPDATE'])
def add():
    if request.method == 'POST':
        isbn = request.form.get("isbn")
        title = request.form.get("title")
        author = request.form.get("author")
        published = request.form.get("published")
        pages = request.form.get("pages")
        cover = request.form.get("cover")
        language = request.form.get("language")
        if not isbn:
            flash('Enter ISBN number', category='error')
        elif type(isbn) != int:
            try:
                isbn = int(isbn)
                new_isbn = Book.query.filter_by(isbn=isbn).first()
                if new_isbn:
                    flash('You are about to edit the existing book', category='warning')
                    # TODO database update
                else:
                    flash('You added the new book', category='confirm')
                    new_book = Book(isbn=isbn, title=title, author=author, published=published,
                                    pages=pages, cover=cover, language=language)
                    db.session.add(new_book)
            except ValueError:
                flash('ISBN number must be a number', category='error')

    db.session.commit()

    return render_template("add.html")


@views.route('/find', methods=['GET', 'POST', 'PUT', 'DELETE', 'UPDATE'])
# @marshal_with(resource_fields)
def find():
    """if request.method == 'GET':
        response = requests.request("GET",
                                "https://www.googleapis.com/books/v1/volumes?q=hobbit")
        # book = make_response(jsonify(response))"""

    response = requests.get("https://www.googleapis.com/books/v1/volumes?q=hobbit")
    search_results = response.json()
    found_items = search_results['items']
    booklist = []
    keys = ['title', 'authors', 'publishedDate', 'industryIdentifiers', 'pageCount', 'imageLinks', 'language']
    for element in found_items:
        volume_info = element['volumeInfo']
        found_book = {}
        for key in keys:
            try:
                found_book[key] = volume_info[key]
            except KeyError:
                pass
        print(found_book)


    return render_template("find.html")