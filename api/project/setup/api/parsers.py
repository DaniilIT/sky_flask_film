from flask_restx.reqparse import RequestParser

page_parser: RequestParser = RequestParser()
page_parser.add_argument(name='page', type=int, location='args', required=False)

status_parser: RequestParser = RequestParser()
status_parser.add_argument(name='status', choices=('new',), location='args', required=False)
