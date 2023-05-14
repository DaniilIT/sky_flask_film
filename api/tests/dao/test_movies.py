import pytest
from sqlalchemy.exc import IntegrityError
from project.dao import MoviesDAO
from project.dao.models import Movie, FavouriteMovie


class TestGenresDAO:

    @pytest.fixture
    def movies_dao(self, db):
        return MoviesDAO(db.session)

    @pytest.fixture
    def movie_1(self, db):
        movie = Movie(
            title='Йеллоустоун',
            description='Владелец ранчо пытается...',
            trailer='https://www.youtube.com/watch?v=UKei_d0cbP4',
            year=2018,
            rating=8.6,
            genre_id=17,
            director_id=1
        )
        db.session.add(movie)
        db.session.commit()
        return movie

    @pytest.fixture
    def movie_2(self, db):
        movie = Movie(
            title='Омерзительная восьмерка',
            description='США после Гражданской...',
            trailer='https://www.youtube.com/watch?v=lmB9VWm0okU',
            year=2015,
            rating=7.8,
            genre_id=4,
            director_id=2
        )
        db.session.add(movie)
        db.session.commit()
        return movie

    @pytest.fixture
    def favourite_movie_1(self, db):
        favourite_movie = FavouriteMovie(
            user_id=1,
            movie_id=1
        )
        db.session.add(favourite_movie)
        db.session.commit()
        return favourite_movie

    def test_get_movie_by_id(self, movies_dao, movie_1):
        assert movies_dao.get_by_id(movie_1.id) == movie_1

    def test_get_movie_by_id_not_found(self, movies_dao):
        assert not movies_dao.get_by_id(1)
        assert movies_dao.get_all() == []

    def test_get_all_movies(self, movies_dao, movie_1, movie_2):
        assert movies_dao.get_all() == [movie_1, movie_2]

    def test_get_movies_by_page(self, app, movies_dao, movie_1, movie_2):
        app.config['ITEMS_PER_PAGE'] = 1
        assert movies_dao.get_all(page=1) == [movie_1]
        assert movies_dao.get_all(page=2) == [movie_2]
        assert movies_dao.get_all(page=3) == []

    def test_delete_movie(self, movies_dao, movie_1):
        pk = movie_1.id
        movies_dao.delete(movie_1)
        assert not movies_dao.get_by_id(pk)

    def test_update_movie(self, movies_dao, movie_1):
        movie_1.rating = 8.5
        movies_dao.update()
        assert movies_dao.get_by_id(movie_1.id).rating == 8.5

    def test_unique_movie(self, movies_dao, movie_1):
        movie_2 = Movie(title=movie_1.title)
        with pytest.raises(IntegrityError):
            movies_dao.create(movie_2)

    def test_get_movies_by_user(self, movies_dao, movie_1, movie_2, favourite_movie_1):
        assert movies_dao.get_by_user(user_id=1) == [movie_1]
