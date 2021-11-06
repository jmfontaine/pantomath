"""Elements shared by data sources."""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Callable, List, Union

import sqlalchemy


@dataclass(frozen=True)
class DataSourceColumn:
    """Hold the information for a column in a data source.

    :param name: The column name.
    :param description: The column description.
    :param hydrate: A JMESPath expression or a callable to be used to populate the column.
    :param index: Whether or not to create an index for the column.
    :param transform: An optional callable to transform the column values.
    :param type: The database type for the column.
    """  # noqa: E501

    name: str
    description: str
    hydrate: Union[str, Callable]
    index: bool = False
    transform: Union[Callable, None] = None
    type: sqlalchemy.types.TypeEngine = sqlalchemy.Text  # noqa A003


@dataclass(frozen=True)  # type: ignore
class DataSource(ABC):
    """Interact with a data source.

    :param columns: List of columns for the data source.
    :param excluded_default_columns: List of default columns to be omitted.
    """

    columns: List[DataSourceColumn] = field(default=False, init=False)  # type: ignore
    excluded_default_columns: List[str] = field(default=False, init=False)  # type: ignore # noqa: E501

    @abstractmethod
    async def extract(self):
        """Extract raw data from the data source."""
        pass

    async def transform(self, item):
        """Refine raw data from the data source."""
        yield item
