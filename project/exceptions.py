from werkzeug.exceptions import HTTPException


class BaseServiceError(HTTPException):
    code = 500


class ItemNotFound(BaseServiceError):
    code = 404


class BadRequest(BaseServiceError):
    code = 400
