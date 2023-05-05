import re
from calendar import timegm
from datetime import datetime, timedelta
from typing import Optional

import jwt
from flask import current_app
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from project.dao.base import BaseDAO
from project.dao.models import User
from project.exceptions import BaseServiceError, ItemNotFound, BadRequest
from project.tools.security import generate_password_hash, compose_passwords


class UsersService:
    def __init__(self, dao: BaseDAO) -> None:
        self.dao = dao

    def get_item(self, pk: int) -> User:
        if user := self.dao.get_by_id(pk):
            return user
        raise ItemNotFound(f'User with pk={pk} not exists.')

    def get_all(self, page: Optional[int] = None) -> list[User]:
        return self.dao.get_all(page=page)

    def create(self, user: User):
        try:
            return self.dao.create(user)
        except IntegrityError as e:
            if "email" in str(e):
                raise BadRequest("A user with the same email address already exists")
            raise BaseServiceError("Something went wrong")
        except SQLAlchemyError:
            raise BaseServiceError()

    @staticmethod
    def validate_email(email):
        pattern = re.compile(
            r'^\S+@\S+\.\S+$'
        )
        print(email)
        print(pattern.search(email))
        if pattern.search(email):
            return True
        return False

    @staticmethod
    def validate_password(password):
        pattern = re.compile(
            r'^(?=.*?[a-z])(?=.*?[A-Z])(?=.*?\d)\S{8,}$'
        )
        if pattern.search(password):
            return True
        return False

    def register(self, email: str, password: str):
        if not self.validate_email(email):
            raise BadRequest('incorrect email')
        if not self.validate_password(password):
            raise BadRequest('Simple password')

        user = User(email=email, password=generate_password_hash(password),
                    name='', surname='', favorite_genre_id=None)
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
        try:
            user = self.dao.get_by_email(email)
        except SQLAlchemyError:
            raise BadRequest("Invalid user email")

        if user is None:
            raise BadRequest("Email not found")

        if not compose_passwords(user.password, password):
            raise BadRequest("Invalid user password")

        return self.generate_tokens(user)

    def refresh(self, refresh_token):
        jwt_data = jwt.decode(jwt=refresh_token, key=current_app.config['SECRET_KEY'],
                              algorithms=[current_app.config['TOKEN_ALGORITHM']])
        user_email = jwt_data.get('email')

        try:
            user = self.dao.get_by_email(user_email)
        except SQLAlchemyError:
            raise BadRequest("Invalid user email")

        if user is None:
            raise BadRequest("Email not found")

        return self.generate_tokens(user)
