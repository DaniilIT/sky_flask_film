from flask_sqlalchemy.query import Query

from project.dao.base import BaseDAO
from project.dao.models import User


class UsersDAO(BaseDAO[User]):
    __model__ = User

    def get_by_email(self, email: str) -> User:
        query: Query = self._db_session.query(self.__model__)
        query = query.filter(User.email == email)
        return query.one_or_none()

    def create(self, user: User):
        self._db_session.add(user)
        self._db_session.commit()
        return user

    def update(self):
        self._db_session.commit()

    def delete(self, user: User):
        self._db_session.delete(user)
        self._db_session.commit()
