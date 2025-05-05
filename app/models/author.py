# external
from sqlalchemy.orm import Mapped, mapped_column
# internal
from ..db import db

class Author(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }
    @classmethod
    def from_dict(cls, author_data):
        return Author(name=author_data["name"])