from flask import Blueprint, render_template, request, flash
from .models import Book
from . import db
from . import requests
# fom werkzeug.security import generate_password_hash, check_password_hash

views = Blueprint('views', __name__)


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
def find():
    response = requests.get("https://www.googleapis.com / books / v1 / volumes?q = flowers + "
                    "inauthor:keyes")
    book = response.json()
    response.close()
    print(book)

    return render_template("find.html")
