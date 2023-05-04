from project.dao.base import BaseDAO
from project.dao.models import User


class UsersDAO(BaseDAO[User]):
    __model__ = User

    # def get_by_email(self, email: str) -> User:

    def create(self, user: User):
        self._db_session.add(user)
        self._db_session.commit()
        return user

    update = create

    def delete(self, user: User):
        self._db_session.delete(user)
        self._db_session.commit()
