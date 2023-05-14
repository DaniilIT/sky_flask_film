import pytest

from project.dao.models import FavouriteMovie, Movie


class TestFavouriteMoviesView:

    @pytest.fixture
    def user_1(self, client, tokens):
        response = client.get(
            '/user/',
            headers={'Authorization': f'Bearer {tokens["access_token"]}'}
        )
        return response.json

    @pytest.fixture
    def favorite_1(self, app, user_1, db):
        with app.app_context():
            favourite = FavouriteMovie(user_id=user_1['id'], movie_id=1)
            db.session.add(favourite)
            db.session.commit()
        return favourite

    @pytest.fixture
    def favorite_2(self, app, user_1, db):
        with app.app_context():
            favourite = FavouriteMovie(user_id=user_1['id'], movie_id=2)
            db.session.add(favourite)
            db.session.commit()
        return favourite

    @pytest.fixture
    def movies(self, db):
        for i in range(1, 4):
            obj = Movie(
                id=i,
                title=f'film_{i}',
            )
            db.session.add(obj)
            db.session.commit()

    def test_get_movies_by_user(self, client, tokens, user_1, favorite_1, favorite_2, movies):
        response = client.get(
            '/favorites/movies/',
            headers={'Authorization': f'Bearer {tokens["access_token"]}'}
        )

        assert response.status_code == 200
        data = response.json
        assert data
        assert isinstance(data, list)
        assert len(data) == 2

    def test_post(self, client, tokens, user_1, favorite_1, favorite_2, movies):
        response = client.post(
            '/favorites/movies/3/',
            headers={'Authorization': f'Bearer {tokens["access_token"]}'}
        )

        assert response.status_code == 201

        response = client.get(
            '/favorites/movies/',
            headers={'Authorization': f'Bearer {tokens["access_token"]}'}
        )

        data = response.json
        assert len(data) == 3

    def test_delete(self, client, tokens, user_1, favorite_1, favorite_2, movies):
        response = client.delete(
            '/favorites/movies/2/',
            headers={'Authorization': f'Bearer {tokens["access_token"]}'}
        )

        assert response.status_code == 204

        response = client.get(
            '/favorites/movies/',
            headers={'Authorization': f'Bearer {tokens["access_token"]}'}
        )

        data = response.json
        assert len(data) == 1
