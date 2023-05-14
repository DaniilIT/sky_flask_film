from project.dao.base import BaseDAO
from project.dao.models.favourite_movie import FavouriteMovie


class FavouriteMoviesDAO(BaseDAO[FavouriteMovie]):
    __model__ = FavouriteMovie
