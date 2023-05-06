from flask_restx import Namespace, Resource

from project.container import user_service, movie_service, favourite_movie_service
from project.setup.api.models import movie
from project.setup.api.parsers import page_parser, status_parser
from project.tools.token_required import token_required

api = Namespace('favorites/movies', description='Понравившееся фильмы')


@api.route('/')
class FavouriteMoviesView(Resource):
    @api.expect(page_parser)
    @api.response(400, 'Bad request')
    @api.response(401, 'Unauthorized')
    @api.marshal_with(movie, as_list=True, code=200, description='OK')
    @token_required
    def get(self, user_email):
        """
        Get favourite movies.
        """
        user = user_service.get_by_email(user_email)
        favourite_movies = movie_service.get_by_user(
            user.id,
            **page_parser.parse_args()
        )
        return favourite_movies


@api.route('/<int:movie_id>/')
class FavouriteMovieView(Resource):
    @api.response(400, 'Bad request')
    @api.response(401, 'Unauthorized')
    @api.doc(responses={201: 'OK'})
    @token_required
    def post(self, user_email, movie_id: int):
        """
        Add favourite movie.
        """
        current_user = user_service.get_by_email(user_email)
        current_movie = movie_service.get_item(movie_id)
        favourite_movie_service.create({
            'user_id': current_user.id,
            'movie_id': current_movie.id,
        })
        return 'OK', 201

    @api.response(400, 'Bad request')
    @api.response(401, 'Unauthorized')
    @api.doc(responses={204: 'NO CONTENT'})
    @token_required
    def delete(self, user_email, movie_id: int):
        """
        Delete favourite movie.
        """
        current_user = user_service.get_by_email(user_email)
        current_movie = movie_service.get_item(movie_id)
        favourite_movie_service.delete((current_user.id, current_movie.id))
        return 'NO CONTENT', 204
