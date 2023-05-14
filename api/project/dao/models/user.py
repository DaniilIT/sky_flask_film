from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from project.setup.db import models


class User(models.Base):
    __tablename__ = 'users'

    email = Column(String(200), unique=True, nullable=False)
    password = Column(String(200), nullable=False)
    name = Column(String(100))
    surname = Column(String(100))
    favourite_genre = Column(Integer, ForeignKey('genres.id', ondelete='SET NULL'))

    favourite_genre_obj = relationship('Genre')
