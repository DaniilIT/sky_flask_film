from project.dao.base import BaseDAO
from project.dao.models import Director


class DirectorsDAO(BaseDAO[Director]):
    __model__ = Director
