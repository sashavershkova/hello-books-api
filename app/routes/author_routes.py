# external
from flask import Blueprint, abort, make_response, request, Response
# internal
from app.models.author import Author
from app.models.book import Book
from .route_utilities import validate_model, create_model, get_models_with_filters
from ..db import db

bp = Blueprint("bp_author", __name__, url_prefix="/authors")

# POST ONE AUTHOR
@bp.post("")
def create_one_author():
    request_body = request.get_json()
    return create_model(Author, request_body)

# GET ALL AUTHORS
@bp.get("")
def get_all_authors():
    return get_models_with_filters(Author, request.args)

# GET ONE AUTHOR
@bp.get("/<author_id>")
def get_one_author(author_id):
    author = validate_model(Author, author_id)
    return author.to_dict()

# CREATE BOOK WITH AUTHOR
@bp.post("/<author_id>/books")
def create_book_with_author(author_id):
    author = validate_model(Author, author_id)

    book_data = request.get_json()
    book_data["author_id"] = author.id

    return make_response(create_model(Author, book_data), 200)

# GET ALL BOOKS FROM AUTHOR
@bp.get("<author_id>/books")
def get_books_by_author(author_id):
    author = validate_model(Author, author_id)
    response = [book.to_dict() for book in author.books]

    return response
