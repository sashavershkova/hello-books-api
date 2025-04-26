from flask import Blueprint, abort, make_response, request, Response
from app.models.book import Book
from ..db import db

books_bp = Blueprint("books_bp", __name__, url_prefix="/books")

# POST ONE BOOK
@books_bp.post("")
def create_book():
    request_body = request.get_json()
    title = request_body["title"]
    description = request_body["description"]
    # checking the content of request_body itself is redundant 
    # because constructor of a class do it, but checking a legitimate keys makes sense
    if not title.strip() or not description.strip():
        response = {"message": "Invalid request. Both title and description must be provided."}
        abort(make_response(response, 400))

    # Check for duplicates
    existing_book = Book.query.filter_by(title=title, description=description).first()
    if existing_book:
        response = {"message": "This book already exists in the database."}
        abort(make_response(response, 400))


    new_book = Book(title=title, description=description)
    db.session.add(new_book)
    db.session.commit()

    response = {
        "id": new_book.id,
        "title": new_book.title,
        "description": new_book.description,
    }

    return response, 201

# GET ALL BOOKS
@books_bp.get("")
def get_all_books():
    query = db.select(Book).order_by(Book.id)
    books = db.session.scalars(query)

    books_response = []
    for book in books:
        books_response.append(
            {
                "id": book.id,
                "title": book.title,
                "description": book.description
                }
        )
    return books_response

# GET ONE BOOK
@books_bp.get("/<book_id>")
def get_one_book(book_id):
    book = validate_book(book_id)

    return {
        "id": book.id,
        "title": book.title,
        "description": book.description,
    }

# UPDATE A BOOK
@books_bp.put("/<book_id>")
def update_one_book(book_id):
    book = validate_book(book_id)
    request_body = request.get_json()

    book.title = request_body["title"]
    book.description = request_body["description"]
    db.session.commit()

    return Response(status=204, mimetype="application/json")

# DELETE ONE BOOK
@books_bp.delete("/<book_id>")
def delete_one_book(book_id):
    book = validate_book(book_id)

    db.session.delete(book)
    db.session.commit()

    return Response(status=204, mimetype="application/json")


# HELPER FUNCTION VALIDATING A BOOK
def validate_book(book_id):
    try:
        book_id = int(book_id)
    except:
        response = {"message": f"book {book_id} invalid"}
        abort(make_response(response, 400))

    query = db.select(Book).where(Book.id == book_id)
    book = db.session.scalar(query)

    if not book:
        response = {"message": f"book {book_id} not found"}
        abort(make_response(response, 404))

    return book



