from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from os import path
import json
import requests

db = SQLAlchemy()
DB_Name = "My_books.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'pseudomonas aureus'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_Name}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    db.init_app(app)

    from .views import views

    app.register_blueprint(views, url_prefix='/')

    from .models import Book as models

    create_database(app)
    api = Api(app)
    return app, api

def create_database(app):
    if not path.exists('books_web/' + DB_Name):
        db.create_all(app=app)
        print('Congratulations! Your bookshelf was created')
