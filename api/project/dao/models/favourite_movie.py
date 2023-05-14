from sqlalchemy import Column, Integer, ForeignKey

from project.setup.db import db


class FavouriteMovie(db.Model):
    __tablename__ = 'favorite_movies'

    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    movie_id = Column(Integer, ForeignKey('movies.id', ondelete='CASCADE'), primary_key=True)
