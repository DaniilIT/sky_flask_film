from unittest.mock import patch

import pytest

from project.exceptions import ItemNotFound
from project.dao.models import User
from project.services import UsersService


class TestUsersService:

    @pytest.fixture()
    @patch('project.dao.UsersDAO')
    def users_dao_mock(self, dao_mock):
        dao = dao_mock()
        dao.get_by_id.return_value = User(id=1, email='e@mail.ru', password="1Aa#2Bb#3Cc#")
        dao.get_all.return_value = [
            User(id=1, email='e_1@mail.ru', password="1Aa#2Bb#3Cc#"),
            User(id=2, email='e_2@mail.ru', password="1Aa#2Bb#3Cc#"),
        ]
        return dao

    @pytest.fixture()
    def users_service(self, users_dao_mock):
        return UsersService(dao=users_dao_mock)

    @pytest.fixture
    def user(self, db):
        obj = User(email="e@mail.ru", password="1Aa#2Bb#3Cc#")
        db.session.add(obj)
        db.session.commit()
        return obj

    def test_get_user(self, users_service, user):
        assert users_service.get_item(user.id)

    def test_user_not_found(self, users_dao_mock, users_service):
        users_dao_mock.get_by_id.return_value = None

        with pytest.raises(ItemNotFound):
            users_service.get_item(10)

    @pytest.mark.parametrize('page', [1, None], ids=['with page', 'without page'])
    def test_get_users(self, users_dao_mock, users_service, page):
        users = users_service.get_all(page=page)
        assert len(users) == 2
        assert users == users_dao_mock.get_all.return_value
        users_dao_mock.get_all.assert_called_with(page=page)
