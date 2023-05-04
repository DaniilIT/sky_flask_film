from project.dao.base import BaseDAO
from project.dao.models import Genre


class GenresDAO(BaseDAO[Genre]):
    __model__ = Genre

    def create(self, genre: Genre):
        self._db_session.add(genre)
        self._db_session.commit()
        return genre

    update = create

    def delete(self, genre: Genre):
        self._db_session.delete(genre)
        self._db_session.commit()
