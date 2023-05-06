from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from project.dao import FavouriteMoviesDAO
from project.dao.models import Movie
from project.exceptions import BaseServiceError
from project.services.base import BaseService
from typing import Optional, List


class FavouriteMoviesService(BaseService[FavouriteMoviesDAO]):
    def get_all(self, user_id: str, page: Optional[int] = None) -> List[Movie]:
        movies = self.dao.get_all(user_id=user_id, page=page)
        return movies

    def create(self, data: dict) -> None:
        try:
            self.dao.create(self.dao.__model__(**data))
        except IntegrityError:
            raise BaseServiceError("Something went wrong")
        except SQLAlchemyError:
            raise BaseServiceError()

    def delete(self, pk: tuple[int, int]) -> None:
        movie = self.get_item(pk)
        self.dao.delete(movie)
