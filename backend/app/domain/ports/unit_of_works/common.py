import abc
from typing import Any, Self


class BaseUnitOfWorkInterface(abc.ABC):
    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        *args: list[Any],
    ) -> None:
        self.rollback()

    def commit(self) -> None:
        self._commit()
        self.publish_events()

    @abc.abstractmethod
    def publish_events(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def _commit(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self) -> None:
        raise NotImplementedError
