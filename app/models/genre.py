# external
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import Optional
# internal
from ..db import db

class Genre(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]

    def to_dict(self):
        return dict(
            id=self.id,
            name=self.name
        )
    
    @classmethod
    def from_dict(cls, data):
        return cls(name=data["name"])