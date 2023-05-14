from project.dao import GenresDAO, DirectorsDAO, MoviesDAO, UsersDAO, FavouriteMoviesDAO

from project.services import GenresService, DirectorsService, MoviesService, UsersService, FavouriteMoviesService
from project.setup.db import db

# DAO
genre_dao = GenresDAO(db.session)
director_dao = DirectorsDAO(db.session)
movie_dao = MoviesDAO(db.session)
user_dao = UsersDAO(db.session)
favourite_movie_dao = FavouriteMoviesDAO(db.session)

# Services
genre_service = GenresService(dao=genre_dao)
director_service = DirectorsService(dao=director_dao)
movie_service = MoviesService(dao=movie_dao)
user_service = UsersService(dao=user_dao)
favourite_movie_service = FavouriteMoviesService(dao=favourite_movie_dao)
