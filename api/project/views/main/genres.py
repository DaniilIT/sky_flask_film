from flask_restx import Namespace, Resource

from project.container import genre_service
from project.exceptions import BaseServiceError
from project.setup.api.models import genre
from project.setup.api.parsers import page_parser

api = Namespace('genres', description='Жанры')


@api.route('/')
class GenresView(Resource):
    @api.expect(page_parser)
    @api.marshal_with(genre, as_list=True, code=200, description='OK')
    def get(self):
        """
        Get all genres.
        """
        # page = request.args.get('page')
        genres = genre_service.get_all(**page_parser.parse_args())
        return genres


@api.route('/<int:genre_id>/')
class GenreView(Resource):
    @api.response(404, 'Not Found')
    @api.marshal_with(genre, code=200, description='OK')
    def get(self, genre_id: int):
        """
        Get genre by id.
        """
        try:
            current_genre = genre_service.get_item(genre_id)
        except BaseServiceError:
            raise
        return current_genre
