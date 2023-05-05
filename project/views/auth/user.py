from flask import request
from flask_restx import Namespace, Resource

from project.container import user_service
from project.exceptions import BadRequest
from project.setup.api.models import user
from project.tools.token_required import token_required

api = Namespace('user', description='Пользователи')


@api.route('/')
class UserView(Resource):
    @api.response(400, 'Bad request')
    @api.response(401, 'Unauthorized')
    @api.marshal_with(user, code=200, description='OK')
    @token_required
    def get(self, user_email):
        """
        Get user.
        """
        return user_service.get_by_email(user_email)

    @api.response(400, 'Bad request')
    @api.doc(responses={201: 'OK'})
    @token_required
    def patch(self, user_email):
        """
        Change user.
        """
        data = request.json
        print(data)
        name = data.get('name')
        surname = data.get('surname')
        favourite_genre = data.get('favourite_genre')

        user = user_service.patch(user_email, name, surname, favourite_genre)
        return 'OK', 201  # {'Location': f'/user/{user.id}/'}  # Headers


@api.route('/password/')
class PasswordView(Resource):
    @api.response(400, 'Bad request')
    @api.doc(responses={201: 'OK'})
    @token_required
    def put(self, user_email):
        """
        Refresh JWT tokens.
        """
        data = request.json
        password_1 = data.get('old_password')
        password_2 = data.get('new_password')

        if not password_1 or not password_2:
            raise BadRequest("Invalid password data")

        user_service.set_password(user_email, password_1, password_2)

        return 'OK', 201
