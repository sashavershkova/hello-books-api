from flask import Blueprint
from app.models.book import books

books_bp = Blueprint("books_bp", __name__, url_prefix="/books")

@books_bp.get("")
def get_all_books():
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

@books_bp.get("/<book_id>")
def get_one_book(book_id):
    book_id = int(book_id)
    book_response = {}
    for book in books:
        if book.id == book_id:
            book_response = {
                "id": book.id,
                "title": book.title,
                "description": book.description
            }
    return book_response

