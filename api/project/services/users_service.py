import re
from calendar import timegm
from datetime import datetime, timedelta

import jwt
from flask import current_app
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from project.dao import UsersDAO
from project.dao.models import User
from project.exceptions import BaseServiceError, BadRequest
from project.services.base import BaseService
from project.tools.security import generate_password_hash, compose_passwords


class UsersService(BaseService[UsersDAO]):
    def get_by_email(self, email: str) -> User:
        try:
            return self.dao.get_by_email(email)
        except SQLAlchemyError:
            raise BadRequest("Invalid user email")

    def create(self, user: User):
        try:
            return self.dao.create(user)
        except IntegrityError as e:
            if 'email' in str(e):
                raise BadRequest('A user with the same email address already exists')
            raise BaseServiceError('Something went wrong')
        except SQLAlchemyError:
            raise BaseServiceError()

    @staticmethod
    def validate_email(email):
        pattern = re.compile(
            r'^\S+@\S+\.\S+$'
        )
        if pattern.search(email):
            return True

    @staticmethod
    def validate_password(password):
        pattern = re.compile(
            r'^(?=.*?[a-z])(?=.*?[A-Z])(?=.*?\d)\S{8,}$'
        )
        if pattern.search(password):
            return True

    def register(self, email: str, password: str):
        if not self.validate_email(email):
            raise BadRequest('incorrect email')
        if not self.validate_password(password):
            raise BadRequest('Simple password')

        user = User(email=email, password=generate_password_hash(password),
                    name='', surname='', favourite_genre=None)
        return self.create(user)

    @staticmethod
    def generate_tokens(user: User):
        jwt_data = {
            'email': user.email,
        }

        min30 = datetime.utcnow() + timedelta(minutes=current_app.config['TOKEN_EXPIRE_MINUTES'])
        jwt_data['exp'] = timegm(min30.timetuple())
        access_token = jwt.encode(jwt_data, current_app.config['SECRET_KEY'],
                                  algorithm=current_app.config['TOKEN_ALGORITHM'])

        days30 = datetime.utcnow() + timedelta(days=current_app.config['TOKEN_EXPIRE_DAYS'])
        jwt_data['exp'] = timegm(days30.timetuple())
        refresh_token = jwt.encode(jwt_data, current_app.config['SECRET_KEY'],
                                   algorithm=current_app.config['TOKEN_ALGORITHM'])

        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
        }

    def login(self, email: str, password: str):
        user = self.get_by_email(email)

        if user is None:
            raise BadRequest("Email not found")

        if not compose_passwords(user.password, password):
            raise BadRequest("Invalid user password")

        return self.generate_tokens(user)

    def refresh(self, refresh_token):
        jwt_data = jwt.decode(jwt=refresh_token, key=current_app.config['SECRET_KEY'],
                              algorithms=[current_app.config['TOKEN_ALGORITHM']])
        user_email = jwt_data.get('email')

        user = self.get_by_email(user_email)

        if user is None:
            raise BadRequest("Email not found")

        return self.generate_tokens(user)

    def patch(self, user_email: str, name: str, surname: str, favourite_genre: int) -> User:
        user = self.get_by_email(user_email)

        if name:
            user.name = name
        if surname:
            user.surname = surname
        if favourite_genre:
            user.favourite_genre = favourite_genre

        self.dao.update()
        return user

    def set_password(self, user_email: str, password_1, password_2):
        user = self.get_by_email(user_email)

        if not compose_passwords(user.password, password_1):
            raise BadRequest("Invalid user password")

        if not self.validate_password(password_2):
            raise BadRequest('Simple password')

        user.password = generate_password_hash(password_2)
        self.dao.update()
        return user
