import pytest
from sqlalchemy.exc import IntegrityError
from project.dao import FavouriteMoviesDAO
from project.dao.models import FavouriteMovie


class TestGenresDAO:

    @pytest.fixture
    def favourite_movies_dao(self, db):
        return FavouriteMoviesDAO(db.session)

    @pytest.fixture
    def favourite_movie_1(self, db):
        favourite_movie = FavouriteMovie(
            user_id=1,
            movie_id=1
        )
        db.session.add(favourite_movie)
        db.session.commit()
        return favourite_movie

    @pytest.fixture
    def favourite_movie_2(self, db):
        favourite_movie = FavouriteMovie(
            user_id=1,
            movie_id=2
        )
        db.session.add(favourite_movie)
        db.session.commit()
        return favourite_movie

    def test_get_favourite_movie_by_id(self, favourite_movies_dao, favourite_movie_1):
        assert favourite_movies_dao.get_by_id(
            (favourite_movie_1.user_id, favourite_movie_1.movie_id)
        ) == favourite_movie_1

    def test_get_favourite_movie_by_id_not_found(self, favourite_movies_dao):
        assert not favourite_movies_dao.get_by_id((1, 1))
        assert favourite_movies_dao.get_all() == []

    def test_get_all_favourite_movies(self, favourite_movies_dao, favourite_movie_1, favourite_movie_2):
        assert favourite_movies_dao.get_all() == [favourite_movie_1, favourite_movie_2]

    def test_get_favourite_movies_by_page(self, app, favourite_movies_dao, favourite_movie_1, favourite_movie_2):
        app.config['ITEMS_PER_PAGE'] = 1
        assert favourite_movies_dao.get_all(page=1) == [favourite_movie_1]
        assert favourite_movies_dao.get_all(page=2) == [favourite_movie_2]
        assert favourite_movies_dao.get_all(page=3) == []

    def test_delete_favourite_movie(self, favourite_movies_dao, favourite_movie_1):
        pk = (favourite_movie_1.user_id, favourite_movie_1.movie_id)
        favourite_movies_dao.delete(favourite_movie_1)
        assert not favourite_movies_dao.get_by_id(pk)

    @pytest.mark.filterwarnings("ignore::sqlalchemy.exc.SAWarning")
    def test_unique_favourite_movie(self, favourite_movies_dao, favourite_movie_1):
        favourite_movie_2 = FavouriteMovie(
            user_id=favourite_movie_1.user_id,
            movie_id=favourite_movie_1.movie_id,
        )
        with pytest.raises(IntegrityError):
            favourite_movies_dao.create(favourite_movie_2)
