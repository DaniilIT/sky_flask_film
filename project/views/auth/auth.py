from flask import request
from flask_restx import Namespace, Resource

from project.container import user_service
from project.exceptions import BadRequest
from project.setup.api.models import token

api = Namespace('auth', description='Аутентификация')


@api.route('/register/')
class RegisterView(Resource):
    @api.response(400, 'Bad request')
    @api.doc(responses={201: 'OK'})
    def post(self):
        """
        Register user.
        """
        data = request.json
        user_email = data.get('email')
        user_password = data.get('password')
        # user_email = request.form.get('email')
        # user_password = request.form.get('password')
        if not (user_email and user_password):
            raise BadRequest()
        user = user_service.register(user_email, user_password)
        return 'OK', 201, {'Location': '/users/'}  # Headers


@api.route('/login/')
class LoginView(Resource):
    @api.response(400, 'Bad request')
    @api.marshal_with(token, code=201, description='OK')
    def post(self):
        """
        Get JWT tokens.
        """
        data = request.json
        user_email = data.get('email')
        user_password = data.get('password')
        if not (user_email and user_password):
            raise BadRequest()
        return user_service.login(user_email, user_password)

    @api.response(400, 'Bad request')
    @api.marshal_with(token, code=201, description='OK')
    def put(self):
        """
        Refresh JWT tokens.
        """
        data = request.json
        refresh_token = data.get('refresh_token')
        if not refresh_token:
            raise BadRequest()
        return user_service.refresh(refresh_token)
