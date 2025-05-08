# external
from flask import Blueprint, abort, make_response, request, Response
# internal
from app.models.author import Author
from app.models.book import Book
from app.models.genre import Genre
from .route_utilities import validate_model, create_model, get_models_with_filters
from ..db import db

bp = Blueprint("genre_bp", __name__, url_prefix="/genres")

@bp.get("")
def get_all_genres():
    return get_models_with_filters(Genre, request.args)

@bp.post("")
def create_genre():
    request_body = request.get_json()
    return create_model(Genre, request_body)