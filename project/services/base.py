from typing import Optional, TypeVar, Generic, Union, Tuple

from project.dao.base import BaseDAO
from project.exceptions import ItemNotFound
from project.setup.db.models import Base

T = TypeVar('T', bound=BaseDAO)


class BaseService(Generic[T]):
    def __init__(self, dao: T) -> None:
        self.dao = dao

    def get_item(self, pk: Union[int, Tuple[int, int]]) -> Base:
        if instance := self.dao.get_by_id(pk):
            return instance
        raise ItemNotFound(f'{self.__class__.__name__} with pk={pk} not exists.')

    def get_all(self, page: Optional[int] = None) -> list[Base]:
        instances = self.dao.get_all(page=page)
        return instances
