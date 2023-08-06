from abc import ABC, abstractmethod
from typing import Iterable

from assimilator.core.database.specifications import Specification


class BaseRepository(ABC):
    def __init__(self, session):
        self.session = session

    @abstractmethod
    def get_initial_query(self):
        raise NotImplementedError("get_initial_query() must be implemented")

    def apply_specifications(self, specifications):
        query = self.get_initial_query()

        for specification in specifications:
            query = specification(query)

        return query

    @abstractmethod
    def get(self, *specifications: Specification, lazy: bool = False):
        raise NotImplementedError("get() is not implemented()")

    @abstractmethod
    def filter(self, *specifications: Specification, lazy: bool = False):
        raise NotImplementedError("filter() is not implemented()")

    @abstractmethod
    def save(self, obj):
        raise NotImplementedError("save() is not implemented in the repository")

    @abstractmethod
    def update_many(self, specifications: Iterable[Specification], updated_fields: dict):
        raise NotImplementedError("update_many() is not implemented in the repository")

    @abstractmethod
    def delete(self, obj):
        raise NotImplementedError("delete() is not implemented in the repository")

    @abstractmethod
    def update(self, obj):
        raise NotImplementedError("update() is not implemented in the repository")

    @abstractmethod
    def is_modified(self, obj):
        raise NotImplementedError("is_modified() is not implemented in the repository")

    @abstractmethod
    def refresh(self, obj):
        raise NotImplementedError("refresh() is not implemented in the repository")
