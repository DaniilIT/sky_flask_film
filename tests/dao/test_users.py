import pytest
from sqlalchemy.exc import IntegrityError
from project.dao import UsersDAO
from project.dao.models import User


class TestGenresDAO:

    @pytest.fixture
    def users_dao(self, db):
        return UsersDAO(db.session)

    @pytest.fixture
    def user_1(self, db):
        user = User(
            email='example_1@mail.ru',
            password='password',
            name='Иван',
            surname='Иванов',
            favourite_genre=1
        )
        db.session.add(user)
        db.session.commit()
        return user

    @pytest.fixture
    def user_2(self, db):
        user = User(
            email='example_2@mail.ru',
            password='password',
            name='Петр',
            surname='Петрович',
            favourite_genre=1
        )
        db.session.add(user)
        db.session.commit()
        return user

    def test_get_user_by_id(self, users_dao, user_1):
        assert users_dao.get_by_id(user_1.id) == user_1

    def test_get_user_by_id_not_found(self, users_dao):
        assert not users_dao.get_by_id(1)
        assert users_dao.get_all() == []

    def test_get_all_users(self, users_dao, user_1, user_2):
        assert users_dao.get_all() == [user_1, user_2]

    def test_get_users_by_page(self, app, users_dao, user_1, user_2):
        app.config['ITEMS_PER_PAGE'] = 1
        assert users_dao.get_all(page=1) == [user_1]
        assert users_dao.get_all(page=2) == [user_2]
        assert users_dao.get_all(page=3) == []

    def test_delete_user(self, users_dao, user_1):
        pk = user_1.id
        users_dao.delete(user_1)
        assert not users_dao.get_by_id(pk)

    def test_update_user(self, users_dao, user_1):
        user_1.name = 'Василий'
        users_dao.update()
        assert users_dao.get_by_id(user_1.id).name == 'Василий'

    def test_unique_user(self, users_dao, user_1):
        user_2 = User(
            email=user_1.email,
            password='password',
        )
        with pytest.raises(IntegrityError):
            users_dao.create(user_2)

    def test_get_user_by_email(self, users_dao, user_1):
        assert users_dao.get_by_email(user_1.email) == user_1
