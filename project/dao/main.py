from project.dao.base import BaseDAO
from project.dao.models import Genre


class GenresDAO(BaseDAO[Genre]):
    __model__ = Genre
