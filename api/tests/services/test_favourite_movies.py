from unittest.mock import patch

import pytest

from project.exceptions import ItemNotFound
from project.dao.models import FavouriteMovie
from project.services import FavouriteMoviesService


class TestFavouriteMoviesService:

    @pytest.fixture()
    @patch('project.dao.FavouriteMoviesDAO')
    def favourite_movies_dao_mock(self, dao_mock):
        dao = dao_mock()
        dao.get_by_id.return_value = FavouriteMovie(user_id=1, movie_id=1)
        dao.get_all.return_value = [
            FavouriteMovie(user_id=1, movie_id=1),
            FavouriteMovie(user_id=1, movie_id=2),
        ]
        return dao

    @pytest.fixture()
    def favourite_movies_service(self, favourite_movies_dao_mock):
        return FavouriteMoviesService(dao=favourite_movies_dao_mock)

    @pytest.fixture
    def favourite_movie(self, db):
        obj = FavouriteMovie(user_id=1, movie_id=1)
        db.session.add(obj)
        db.session.commit()
        return obj

    def test_get_favourite_movie(self, favourite_movies_service, favourite_movie):
        assert favourite_movies_service.get_item((favourite_movie.user_id, favourite_movie.movie_id))

    def test_favourite_movie_not_found(self, favourite_movies_dao_mock, favourite_movies_service):
        favourite_movies_dao_mock.get_by_id.return_value = None

        with pytest.raises(ItemNotFound):
            favourite_movies_service.get_item(10)

    @pytest.mark.parametrize('page', [1, None], ids=['with page', 'without page'])
    def test_get_favourite_movies(self, favourite_movies_dao_mock, favourite_movies_service, page):
        favourite_movies = favourite_movies_service.get_all(page=page)
        assert len(favourite_movies) == 2
        assert favourite_movies == favourite_movies_dao_mock.get_all.return_value
        favourite_movies_dao_mock.get_all.assert_called_with(page=page)
