from typing import Optional, List

from flask_sqlalchemy.query import Query
from sqlalchemy import desc
from werkzeug.exceptions import NotFound

from project.dao.base import BaseDAO
from project.dao.models import Movie, FavouriteMovie


class MoviesDAO(BaseDAO[Movie]):
    __model__ = Movie

    def get_all(self, page: Optional[int] = None, status: Optional[str] = None) -> List[Movie]:
        stmt: Query = self._db_session.query(Movie)
        if status and status.lower() == "new":
            stmt = stmt.order_by(desc(Movie.year))
        if page:
            try:
                return stmt.paginate(page=page, per_page=self._items_per_page).items
            except NotFound:
                return []
        return stmt.all()

    def get_by_user(self, user_id: str, page: Optional[int] = None) -> List[Movie]:
        stmt: Query = self._db_session.query(Movie).outerjoin(FavouriteMovie)
        stmt = stmt.filter(FavouriteMovie.user_id == user_id)
        if page:
            try:
                return stmt.paginate(page=page, per_page=self._items_per_page).items
            except NotFound:
                return []
        return stmt.all()
