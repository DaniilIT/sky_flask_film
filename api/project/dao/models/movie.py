from sqlalchemy import Column, String, Text, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship

from project.setup.db import models


class Movie(models.Base):
    __tablename__ = 'movies'

    title = Column(String(200), unique=True, nullable=False)
    description = Column(Text)
    trailer = Column(String(200))
    year = Column(Integer)
    rating = Column(Float)
    genre_id = Column(Integer, ForeignKey('genres.id', ondelete='SET NULL'))
    director_id = Column(Integer, ForeignKey('directors.id', ondelete='CASCADE'))

    genre = relationship('Genre', backref='movies')
    director = relationship('Director', backref='movies')
