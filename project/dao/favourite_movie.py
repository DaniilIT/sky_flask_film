from typing import Optional, List

from flask_sqlalchemy.query import Query
from werkzeug.exceptions import NotFound

from project.dao.base import BaseDAO
from project.dao.models import Movie
from project.dao.models.favourite_movie import FavouriteMovie


class FavouriteMoviesDAO(BaseDAO[FavouriteMovie]):
    __model__ = FavouriteMovie

    def get_all(self, user_id: str, page: Optional[int] = None) -> List[Movie]:
        stmt: Query = self._db_session.query(self.__model__).outerjoin(Movie)
        stmt = stmt.filter(FavouriteMovie.user_id == user_id)
        if page:
            try:
                return stmt.paginate(page=page, per_page=self._items_per_page).items
            except NotFound:
                return []
        return stmt.all()

    def create(self, movie: FavouriteMovie):
        self._db_session.add(movie)
        self._db_session.commit()
        return movie

    def delete(self, movie: FavouriteMovie):
        self._db_session.delete(movie)
        self._db_session.commit()
