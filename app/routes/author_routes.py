# external
from flask import Blueprint, abort, make_response, request, Response
# internal
from app.models.author import Author
from .route_utilities import validate_model
from ..db import db

bp = Blueprint("bp_author", __name__, url_prefix="/authors")

# POST ONE AUTHOR
@bp.post("")
def create_one_author():
    author_data = request.get_json()
    try:
        new_author = Author.from_dict(author_data)
    except KeyError as error:
        response = {"message": f"Invalid request: missing {error.args[0]}"}
        abort(make_response(response, 400))
    
    db.session.add(new_author)
    db.session.commit()

    return make_response(new_author.to_dict(), 201)

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

