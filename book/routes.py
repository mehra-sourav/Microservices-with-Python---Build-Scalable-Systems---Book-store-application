from flask import Blueprint, request, jsonify, make_response
from models import Book, db

book_blueprint = Blueprint('book_api_routes', __name__, url_prefix='/api/book')


@book_blueprint.route('/all', methods=["GET"])
def get_all_books():
    all_books = Book.query.all()
    result = [book.serialize() for book in all_books]
    response = {
        "message": "Returning all books",
        "result": result
    }
    return jsonify(response)


@book_blueprint.route('/create', methods=["POST"])
def create_book():
    try:
        book = Book()
        book.name = request.form["name"]
        book.image = request.form["image"]
        book.price = request.form["price"]
        book.slug = request.form["slug"]

        db.session.add(book)
        db.session.commit()

        response = {
            'message': 'Book created successfully',
            'result': book.serialize()
        }
    except Exception as e:
        print("Error -->", str(e))
        response = {
            'message': 'Book creation failed'
        }

    return jsonify(response)


@book_blueprint.route('/<slug>', methods=["GET"])
def book_details(slug):
    book = Book.query.filter_by(slug=slug).first()

    if book:
        response = {
            "message": "Book found",
            "result": book.serialize()
        }
    else:
        response = {
            "message": "Book not found!!"
        }

    return jsonify(response)
