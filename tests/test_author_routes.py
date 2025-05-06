from werkzeug.exceptions import HTTPException
from app.routes.route_utilities import validate_model
import pytest

def test_get_all_authors_with_no_records(client):
    # Act
    response = client.get("/authors")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []

def test_get_one_author(client, two_saved_authors):
    # Act
    response = client.get("/authors/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {
        "id": 1,
        "name": "J.R.R. Tolkien"
    }

def test_create_one_book(client):
    # Act
    response = client.post("/authors", json={
        "name": "J.R.R. Tolkien"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body == {
        "id": 1,
        "name": "J.R.R. Tolkien"
    }

def test_create_one_book_no_data(client):
    # Arrange
    test_data = {}

    # Act
    response = client.post("/authors", json=test_data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {'message': 'Invalid request: missing name'}


def test_create_one_book_with_extra_keys(client):
    # Arrange
    test_data = {
        "extra": "some stuff",
        "name": "J.R.R. Tolkien",
        "another": "last value"
    }

    # Act
    response = client.post("/authors", json=test_data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body == {
        "id": 1,
        "name": "J.R.R. Tolkien",
    }

# When we have records, `get_all_books` returns a list containing a dictionary representing each `Book`
def test_get_all_authors_with_two_records(client, two_saved_authors):
    # Act
    response = client.get("/authors")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 2
    assert response_body[0] == {
        "id": 1,
        "name": "J.R.R. Tolkien"
    }
    assert response_body[1] == {
        "id": 2,
        "name": "Leo Tolstoy"
    }

# When we have records and a `title` query in the request arguments, `get_all_books` 
# returns a list containing only the `Book`s that match the query
def test_get_all_authors_with_name_query_matching_none(client, two_saved_authors):
    # Act
    data = {'name': 'J.K. Rowling'}
    response = client.get("/authors", query_string = data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []

def test_get_one_author_missing_record(client, two_saved_books):
    # Act
    response = client.get("/authors/3")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"message": "Author 3 not found"}

# When we call `get_one_book` with a non-numeric ID, we get the expected error message
def test_get_one_author_invalid_id(client, two_saved_books):
    # Act
    response = client.get("/authors/cat")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {"message": "Author cat invalid"}

# def test_update_book(client, two_saved_books):
#     # Arrange
#     test_data = {
#         "title": "New Book",
#         "description": "The Best!"
#     }

    # Act
    # response = client.put("/books/1", json=test_data)
    # response_body = response.get_json()

    # Assert
#     assert response.status_code == 200
#     assert response_body == "Book #1 successfully updated"

# def test_update_book_with_extra_keys(client, two_saved_books):
#     # Arrange
#     test_data = {
#         "extra": "some stuff",
#         "title": "New Book",
#         "description": "The Best!",
#         "another": "last value"
#     }

#     # Act
#     response = client.put("/books/1", json=test_data)
#     response_body = response.get_json()

#     # Assert
#     assert response.status_code == 200
#     assert response_body == "Book #1 successfully updated"

# def test_update_book_missing_record(client, two_saved_books):
#     # Arrange
#     test_data = {
#         "title": "New Book",
#         "description": "The Best!"
#     }

#     # Act
#     response = client.put("/books/3", json=test_data)
#     response_body = response.get_json()

#     # Assert
#     assert response.status_code == 404
#     assert response_body == {"message": "book 3 not found"}

# def test_update_book_invalid_id(client, two_saved_books):
#     # Arrange
#     test_data = {
#         "title": "New Book",
#         "description": "The Best!"
#     }

#     # Act
#     response = client.put("/books/cat", json=test_data)
#     response_body = response.get_json()

#     # Assert
#     assert response.status_code == 400
#     assert response_body == {"message": "book cat invalid"}

# def test_delete_book(client, two_saved_books):
#     # Act
#     response = client.delete("/books/1")
#     response_body = response.get_json()

#     # Assert
#     assert response.status_code == 200
# #     assert response_body == "Book #1 successfully deleted"

# def test_delete_book_missing_record(client, two_saved_books):
#     # Act
#     response = client.delete("/books/3")
#     response_body = response.get_json()

# #     # Assert
# #     assert response.status_code == 404
# #     assert response_body == {"message": "book 3 not found"}

# def test_delete_book_invalid_id(client, two_saved_books):
#     # Act
#     response = client.delete("/books/cat")
#     response_body = response.get_json()

#     # Assert
#     assert response.status_code == 400
#     assert response_body == {"message": "book cat invalid"}