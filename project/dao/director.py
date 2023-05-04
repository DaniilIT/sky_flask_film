from project.dao.base import BaseDAO
from project.dao.models import Director


class DirectorsDAO(BaseDAO[Director]):
    __model__ = Director

    def create(self, director: Director):
        self._db_session.add(director)
        self._db_session.commit()
        return director

    update = create

    def delete(self, director: Director):
        self._db_session.delete(director)
        self._db_session.commit()
