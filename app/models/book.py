from sqlalchemy.orm import Mapped, mapped_column
from ..db import db

class Book(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]

    
# class Book:
#     def __init__(self, id, title, description):
#         self.id = id
#         self.title = title
#         self.description = description

# books = [
#     Book(1, "The Lord of the Rings", "An epic fantasy saga by J.R.R. Tolkien about the struggle to destroy a powerful ring."),
#     Book(2, "The Wheel of Time", "A long-running fantasy series by Robert Jordan that follows the battle between light and shadow."),
#     Book(3, "A Game of Thrones", "The first book in George R.R. Martin's series about noble families vying for control of a kingdom."),
#     Book(4, "The Name of the Wind", "A lyrical fantasy novel by Patrick Rothfuss about a gifted young man who grows into a legendary figure."),
#     Book(5, "Mistborn: The Final Empire", "A high fantasy heist story by Brandon Sanderson set in a world of ash and oppression.")
# ]