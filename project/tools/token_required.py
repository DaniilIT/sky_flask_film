from functools import wraps

import jwt
from flask import request, current_app
from flask_restx import abort


def token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "Authorization" not in request.headers:
            abort(401)  # Unauthorized

        data = request.headers['Authorization']
        token = data.split("Bearer ")[-1]

        try:
            jwt_data = jwt.decode(jwt=token, key=current_app.config['SECRET_KEY'],
                                  algorithms=[current_app.config['TOKEN_ALGORITHM']])
            user_email = jwt_data['email']
            kwargs.update({'user_email': user_email})
        except (jwt.exceptions.PyJWTError, KeyError):
            abort(401)  # Unauthorized

        return func(*args, **kwargs)

    return wrapper
