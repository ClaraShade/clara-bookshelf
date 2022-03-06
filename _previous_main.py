from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

# tu byc moze dodac abort ale nie wiem
app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class BookModel(db.Model):
    isbn = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    date_of_publishing = db.Column(db.String(30))
    pages = db.Column(db.Integer)
    cover = db.Column(db.String(200))
    language = db.Column(db.String(30))


    def __repr__(self):
        return f"Book(isbn = {book_isbn}, title = {title}, author = {author}, published " \
               f"=" \
               f" {date}, pages = {pages}, cover = {cover}, language = {language})"

# create the database if needed
# db.create_all()

book_put_args = reqparse.RequestParser()
book_put_args.add_argument("isbn", type=int, help="isbn of the book")
book_put_args.add_argument("title", type=str, help="Title of the book")
book_put_args.add_argument("author", type=str, help="Author of the book")
book_put_args.add_argument("date", type=str, help="Date of publishing")
book_put_args.add_argument("pages", type=int, help="Number of pages")

book_patch_args = reqparse.RequestParser()
book_patch_args.add_argument("isbn", type=int, help="isbn of the book")
book_patch_args.add_argument("title", type=str, help="Title of the book")
book_patch_args.add_argument("author", type=str, help="Author of the book")
book_patch_args.add_argument("date", type=str, help="Date of publishing")
book_patch_args.add_argument("pages", type=int, help="Number of pages")

resource_fields = {
    "isbn": fields.Integer,
    "title": fields.String,
    "author": fields.String,
    "published": fields.String,
    "pages": fields.Integer,
    "cover": fields.String,
    "language": fields.String
}


# making a class which inherits from Resource
class Book(Resource):
    @marshal_with(resource_fields)
    def get(self, book_isbn):
        result = BookModel.query.filter_by(isbn=book_isbn).first()
        return result

    @marshal_with(resource_fields)
    def put(self, book_isbn):
        args = book_put_args.parse_args()
        book = BookModel(isbn=book_isbn, title=args['title'], author=args['author'])
        db.session.add(book)
        db.session.commit()
        return book, 201

    @marshal_with(resource_fields)
    def patch(self, book_isbn):
        args = book_patch_args.parse_args()
        result = BookModel.query.filter_by(isbn=book_isbn).first()
        if not result:
            abort(404, message="Book doesn't exist")
        if args["isbn"]:
            result.book_isbn = args["isbn"]
        if args["title"]:
            result.title = args["title"]
        if args["author"]:
            result.author = args["author"]
        # if pages etcetera

        db.session.commit()

        return result



    def delete(self, book_isbn):
        del books[isbn]
        return '', 204

# this adds the resource in the endpoint "/hello"


api.add_resource(Book, "/book/<int:book_isbn>")


if __name__ == "__main__":
    app.run(debug=True)
