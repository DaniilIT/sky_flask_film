from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from project.dao import FavouriteMoviesDAO
from project.exceptions import BaseServiceError
from project.services.base import BaseService


class FavouriteMoviesService(BaseService[FavouriteMoviesDAO]):
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
