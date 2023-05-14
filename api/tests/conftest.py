import json

import pytest

from project.config import TestingConfig
from project.server import create_app
from project.setup.db import db as database


@pytest.fixture
def app():
    app = create_app(TestingConfig)
    with app.app_context():
        yield app


@pytest.fixture
def db(app):
    # database.init_app(app)
    database.drop_all()
    database.create_all()
    database.session.commit()

    yield database

    database.session.close()


@pytest.fixture
def client(app, db):
    with app.test_client() as client:
        yield client


@pytest.fixture
def tokens(client):
    data = json.dumps({
        'email': 'example@mail.ru',
        'password': '1Aa#2Bb#3Cc#'
    })

    client.post(
        "/auth/register/",
        data=data,
        content_type='application/json'
        # content_type = 'multipart/form-data'
    )

    response = client.post(
        "/auth/login/",
        data=data,
        content_type='application/json'
    )

    return response.json
