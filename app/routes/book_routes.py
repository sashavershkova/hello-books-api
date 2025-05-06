# external
from flask import Blueprint, abort, make_response, request, Response
# internal
from app.models.book import Book
from app.models.author import Author
from .route_utilities import validate_model, create_model
from ..db import db

bp = Blueprint("bp_book", __name__, url_prefix="/books")

# CREATE ONE BOOK
@bp.post("")
def create_book():
    request_body = request.get_json()
    return create_model(Book, request_body)

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
    book = validate_model(Book, book_id)

    return book.to_dict()

# UPDATE A BOOK
@bp.put("/<book_id>")
def update_one_book(book_id):
    book = validate_model(Book, book_id)
    request_body = request.get_json()

    book.title = request_body["title"]
    book.description = request_body["description"]

    if "author_id" in request_body:
        author = validate_model(Author, request_body["author_id"])
        book.author = author

    db.session.commit()
    return Response(status=204, mimetype="application/json")

# DELETE ONE BOOK
@bp.delete("/<book_id>")
def delete_one_book(book_id):
    book = validate_model(Book, book_id)

    db.session.delete(book)
    db.session.commit()

    return Response(status=204, mimetype="application/json")



