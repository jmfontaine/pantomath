from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Callable, List, Union

import sqlalchemy


@dataclass(frozen=True)
class DataSourceColumn:
    name: str
    description: str
    hydrate: Union[str, Callable]
    type: sqlalchemy.types.TypeEngine = sqlalchemy.Text
    index: bool = False
    transform: Union[Callable, None] = None


@dataclass(frozen=True)  # type: ignore
class DataSource(ABC):
    columns: List[DataSourceColumn] = field(default=False, init=False)  # type: ignore
    excluded_default_columns: List[str] = field(default=False, init=False)  # type: ignore # noqa: E501

    @abstractmethod
    async def extract(self):
        pass

    async def transform(self, item):
        yield item
