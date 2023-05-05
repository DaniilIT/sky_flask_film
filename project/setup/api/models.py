from flask_restx import fields, Model

from project.setup.api import api

genre: Model = api.model('Жанр', {
    'id': fields.Integer(required=True, example=1),
    'name': fields.String(required=True, max_length=100, example='Комедия'),
})

director: Model = api.model('Режиссер', {
    'id': fields.Integer(required=True, example=1),
    'name': fields.String(required=True, max_length=100, example='Тейлор Шеридан'),
})

movie: Model = api.model('Фильм', {
    'id': fields.Integer(required=True, example=1),
    'title': fields.String(required=True, example='Йеллоустоун'),
    'description': fields.String(example='Владелец ранчо пытается сохранить землю своих предков.'
                                         'Кевин Костнер в неовестерне от автора «Ветреной реки»'),
    'trailer': fields.String(example='https://www.youtube.com/watch?v=UKei_d0cbP4'),
    'year': fields.Integer(example=2018),
    'rating': fields.Float(example=8.6),

    'genre': fields.Nested(genre),
    'director': fields.Nested(director),
})

user: Model = api.model('Пользователь', {
    'id': fields.Integer(required=True, example=1),
    'email': fields.String(required=True, example='example@mail.ru'),
    'name': fields.String(required=True, example='Иван'),
    'surname': fields.String(required=True, example='Иванов'),

    'favourite_genre': fields.Nested(genre),
})

token: Model = api.model('JWT токены', {
    'access_token': fields.String(),
    'refresh_token': fields.String(),
})
