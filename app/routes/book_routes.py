# external
from flask import Blueprint, abort, make_response, request, Response
# internal
from app.models.book import Book
from ..db import db

bp = Blueprint("bp", __name__, url_prefix="/books")

# CREATE ONE BOOK
@bp.post("")
def create_book():
    request_body = request.get_json()

    try:
        new_book = Book.from_dict(request_body)

    except KeyError as error:
        response = {"message": f"Invalid request: missing {error.args[0]}"}
        abort(make_response(response, 400))

    db.session.add(new_book)
    db.session.commit()

    return new_book.to_dict(), 201

# GET ALL BOOKS
@bp.get("")
def get_all_books():
    query = db.select(Book)

    title_param = request.args.get("title")
    if title_param:
        query = query.where(Book.title.ilike(f"%{title_param}%"))

    description_param = request.args.get("description")
    if description_param:
        query = query.where(Book.description.ilike(f"%{description_param}%"))

    books = db.session.scalars(query.order_by(Book.id))
    
    books_response = []
    for book in books:
        books_response.append(book.to_dict())
    return books_response

# GET ONE BOOK
@bp.get("/<book_id>")
def get_one_book(book_id):
    book = validate_book(book_id)

    return book.to_dict()

# UPDATE A BOOK
@bp.put("/<book_id>")
def update_one_book(book_id):
    book = validate_book(book_id)
    request_body = request.get_json()

    book.title = request_body["title"]
    book.description = request_body["description"]
    db.session.commit()

    return Response(status=204, mimetype="application/json")

# DELETE ONE BOOK
@bp.delete("/<book_id>")
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
        response = {"message": f"Book {book_id} invalid"}
        abort(make_response(response, 400))

    query = db.select(Book).where(Book.id == book_id)
    book = db.session.scalar(query)

    if not book:
        response = {"message": f"Book {book_id} not found"}
        abort(make_response(response, 404))

    return book



