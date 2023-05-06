from typing import Optional, List

from project.dao import MoviesDAO
from project.dao.models import Movie
from project.services.base import BaseService


class MoviesService(BaseService[MoviesDAO]):

    def get_all(self, page: Optional[int] = None, status: Optional[str] = None) -> List[Movie]:
        movies = self.dao.get_all(page=page, status=status)
        return movies

    def get_by_user(self, user_id: str, page: Optional[int] = None) -> List[Movie]:
        movies = self.dao.get_by_user(user_id=user_id, page=page)
        return movies
