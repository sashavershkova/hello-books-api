# external
from flask import Blueprint, abort, make_response, request, Response
# internal
from app.models.author import Author
from app.models.book import Book
from .route_utilities import validate_model, create_model
from ..db import db

bp = Blueprint("bp_author", __name__, url_prefix="/authors")

# POST ONE AUTHOR
@bp.post("")
def create_one_author():
    author_data = request.get_json()
    return create_model(Author, author_data)

# GET ALL AUTHORS
@bp.get("")
def get_all_authors():
    query = db.select(Author)

    name_param = request.args.get("name")
    if name_param:
        query = query.where(Author.name.ilike(f"%{name_param}%"))

    authors = db.session.scalars(query.order_by(Author.id))
    response = [author.to_dict() for author in authors]

    return response

# CREATE BOOK WITH AUTHOR
@bp.post("/<author_id>/books")
def create_book_with_author(author_id):
    author = validate_model(Author, author_id)

    book_data = request.get_json()
    book_data["author_id"] = author.id

    try:
        new_book = Book.from_dict(book_data)
    except KeyError as error:
        response = {"message": f"Invalid request: missing {error.args[0]}"}
        abort(make_response(response, 400))
    
    db.session.add(new_book)
    db.session.commit()

    return make_response(new_book.to_dict(), 201)

# GET ALL BOOKS FROM AUTHOR
@bp.get("<author_id>/books")
def get_books_by_author(author_id):
    author = validate_model(Author, author_id)
    response = [book.to_dict() for book in author.books]

    return response
