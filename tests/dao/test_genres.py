import pytest
from sqlalchemy.exc import IntegrityError
from project.dao import GenresDAO
from project.dao.models import Genre


class TestGenresDAO:

    @pytest.fixture
    def genres_dao(self, db):
        return GenresDAO(db.session)

    @pytest.fixture
    def genre_1(self, db):
        genre = Genre(name='Боевик')
        db.session.add(genre)
        db.session.commit()
        return genre

    @pytest.fixture
    def genre_2(self, db):
        genre = Genre(name='Комедия')
        db.session.add(genre)
        db.session.commit()
        return genre

    def test_get_genre_by_id(self, genres_dao, genre_1):
        assert genres_dao.get_by_id(genre_1.id) == genre_1

    def test_get_genre_by_id_not_found(self, genres_dao):
        assert not genres_dao.get_by_id(1)
        assert genres_dao.get_all() == []

    def test_get_all_genres(self, genres_dao, genre_1, genre_2):
        assert genres_dao.get_all() == [genre_1, genre_2]

    def test_get_genres_by_page(self, app, genres_dao, genre_1, genre_2):
        app.config['ITEMS_PER_PAGE'] = 1
        assert genres_dao.get_all(page=1) == [genre_1]
        assert genres_dao.get_all(page=2) == [genre_2]
        assert genres_dao.get_all(page=3) == []

    def test_delete_genre(self, genres_dao, genre_1):
        pk = genre_1.id
        genres_dao.delete(genre_1)
        assert not genres_dao.get_by_id(pk)

    def test_update_genre(self, genres_dao, genre_1):
        genre_1.name = 'Детектив'
        genres_dao.update()
        assert genres_dao.get_by_id(genre_1.id).name == 'Детектив'

    def test_unique_genre(self, genres_dao, genre_1):
        genre_2 = Genre(name=genre_1.name)
        with pytest.raises(IntegrityError):
            genres_dao.create(genre_2)
