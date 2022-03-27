from datetime import date
from flask import Blueprint, render_template, request, flash, jsonify, make_response
from .models import Book
from flask_restful import Api, Resource, reqparse, fields
from . import db
from . import requests
import json

views = Blueprint('views', __name__)

resource_fields = {
    "isbn": fields.Integer,
    "title": fields.String,
    "author": fields.String,
    "published": fields.String,
    "pages": fields.Integer,
    "cover": fields.String,
    "language": fields.String
}

@views.route('/', methods=['GET', 'POST', 'PUT', 'DELETE', 'UPDATE'])
def bookshelf():
    booklist = []
    books = Book.query.all()
    for book in books:
        book_dicted = book.to_dict()
        booklist.append(book_dicted)
    print(booklist)
    if request.method=='POST':
        title = request.form.get("title")
        author = request.form.get("author")
        published_from = request.form.get("published_from")
        published_to = request.form.get("published_to")
        language = request.form.get("language")
        if published_from == '':
            published_from = '0000-01-01'
        if published_to == '':
            today = date.today()
            published_to = today.isoformat()

        my_books = Book.query.filter(Book.title.ilike(f'%{title}%'),
                                     Book.author.ilike(f'%{author}%'),
                                     Book.language.ilike(f'%{language}%'))\
            .filter((Book.published == '') |(Book.published >= published_from)&
                    (Book.published <= published_to)).all()
        print(my_books)
        if my_books:
            booklist = []
            for book in my_books:
                filtered_dict = book.to_dict()
                print(filtered_dict)
                booklist.append(filtered_dict)
        else:
            flash('There is no book matching your criteria', category='error')

    return render_template("bookshelf.html", booklist=booklist)


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
                    print(new_book)
                    db.session.add(new_book)
            except ValueError:
                flash('ISBN number must be a number', category='error')

    db.session.commit()

    return render_template("add.html")


@views.route('/find', methods=['GET', 'POST', 'PUT', 'DELETE', 'UPDATE'])
def find():
    """ if request.method == 'GET':
        response = requests.request("GET",
                                "https://www.googleapis.com/books/v1/volumes?q=hobbit")
        book = make_response(jsonify(response)) """

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


@views.route('/api/find')
def find_api():
    response = requests.get(
        "https://www.googleapis.com/books/v1/volumes?q=hobbit")
    search_results = response.json()

    return jsonify(search_results)
