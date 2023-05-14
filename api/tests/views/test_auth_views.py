import json

import pytest

from project.dao import UsersDAO
from project.services import UsersService


class TestAuthView:

    @pytest.fixture
    def user_service(self, db):
        return UsersService(UsersDAO(db.session))

    def test_auth_registration_post(self, client, user_service):
        response = client.post(
            '/auth/register/',
            data=json.dumps({
                'email': 'example_1@mail.ru',
                'password': '1Aa#2Bb#3Cc#'
            }),
            content_type='application/json'
        )

        assert response.status_code == 201
        assert 'location' in response.headers

    def test_auth_login_post(self, client, user_service):
        data = json.dumps({
            'email': 'example_2@mail.ru',
            'password': '1Aa#2Bb#3Cc#'
        })

        client.post(
            '/auth/register/',
            data=data,
            content_type='application/json'
        )

        response = client.post(
            '/auth/login/',
            data=data,
            content_type='application/json'
        )

        assert response.status_code == 200
        tokens = response.json
        assert 'access_token' in tokens
        assert 'refresh_token' in tokens

    def test_auth_login_put(self, client, user_service, tokens):
        refresh_token = tokens['refresh_token']
        response = client.put(
            '/auth/login/',
            data=json.dumps({'refresh_token': refresh_token}),
            content_type='application/json'
        )

        assert response.status_code == 200
        tokens = response.json
        assert 'access_token' in tokens
        assert 'refresh_token' in tokens
