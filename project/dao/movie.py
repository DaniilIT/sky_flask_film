from typing import Optional, List

from flask_sqlalchemy import BaseQuery
from sqlalchemy import desc
from werkzeug.exceptions import NotFound

from project.dao.base import BaseDAO
from project.dao.models import Movie


class MoviesDAO(BaseDAO[Movie]):
    __model__ = Movie

    def get_all(self, page: Optional[int] = None, status: Optional[str] = None) -> List[Movie]:
        stmt: BaseQuery = self._db_session.query(Movie)
        if status and status.lower() == "new":
            stmt = stmt.order_by(desc(Movie.year))
        if page:
            try:
                return stmt.paginate(page=page, per_page=self._items_per_page).items
            except NotFound:
                return []
        return stmt.all()

    def create(self, movie: Movie):
        self._db_session.add(movie)
        self._db_session.commit()
        return movie

    update = create

    def delete(self, movie: Movie):
        self._db_session.delete(movie)
        self._db_session.commit()
