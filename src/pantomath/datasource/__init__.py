from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Union

import sqlalchemy


@dataclass(frozen=True)
class DataSourceColumn:
    name: str
    description: str
    hydrate: Union[str, callable]
    type: sqlalchemy.types.TypeEngine = sqlalchemy.Text
    index: bool = False
    transform: callable = None


@dataclass(frozen=True)
class DataSource(ABC):
    columns: List[DataSourceColumn] = field(default=False, init=False)
    excluded_default_columns: List[str] = field(default=False, init=False)

    @abstractmethod
    async def extract(self):
        pass

    async def transform(self, item):
        yield item
