from flask_restx import Namespace, Resource

from project.container import movie_service
from project.setup.api.models import movie
from project.setup.api.parsers import page_parser, status_parser

api = Namespace('movies', description='Фильмы')


@api.route('/')
class MoviesView(Resource):
    @api.expect(page_parser, status_parser)
    @api.marshal_with(movie, as_list=True, code=200, description='OK')
    def get(self):
        """
        Get all movies.
        """
        # status = request.args.get('status')
        movies = movie_service.get_all(**page_parser.parse_args(),
                                       **status_parser.parse_args())
        return movies


@api.route('/<int:movie_id>/')
class MovieView(Resource):
    @api.response(404, 'Not Found')
    @api.marshal_with(movie, code=200, description='OK')
    def get(self, movie_id: int):
        """
        Get movie by id.
        """
        current_movie = movie_service.get_item(movie_id)
        return current_movie
