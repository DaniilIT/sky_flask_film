import pytest
from sqlalchemy.exc import IntegrityError
from project.dao import DirectorsDAO
from project.dao.models import Director


class TestGenresDAO:

    @pytest.fixture
    def directors_dao(self, db):
        return DirectorsDAO(db.session)

    @pytest.fixture
    def director_1(self, db):
        director = Director(name='Тейлор Шеридан')
        db.session.add(director)
        db.session.commit()
        return director

    @pytest.fixture
    def director_2(self, db):
        director = Director(name='Квентин Тарантино')
        db.session.add(director)
        db.session.commit()
        return director

    def test_get_director_by_id(self, directors_dao, director_1):
        assert directors_dao.get_by_id(director_1.id) == director_1

    def test_get_director_by_id_not_found(self, directors_dao):
        assert not directors_dao.get_by_id(1)
        assert directors_dao.get_all() == []

    def test_get_all_directors(self, directors_dao, director_1, director_2):
        assert directors_dao.get_all() == [director_1, director_2]

    def test_get_directors_by_page(self, app, directors_dao, director_1, director_2):
        app.config['ITEMS_PER_PAGE'] = 1
        assert directors_dao.get_all(page=1) == [director_1]
        assert directors_dao.get_all(page=2) == [director_2]
        assert directors_dao.get_all(page=3) == []

    def test_delete_director(self, directors_dao, director_1):
        pk = director_1.id
        directors_dao.delete(director_1)
        assert not directors_dao.get_by_id(pk)

    def test_update_director(self, directors_dao, director_1):
        director_1.name = 'Владимир Вайншток'
        directors_dao.update()
        assert directors_dao.get_by_id(director_1.id).name == 'Владимир Вайншток'

    def test_unique_director(self, directors_dao, director_1):
        director_2 = Director(name=director_1.name)
        with pytest.raises(IntegrityError):
            directors_dao.create(director_2)
