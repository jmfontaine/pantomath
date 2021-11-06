"""Elements shared by providers."""
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Callable, Iterable

from aiostream import operator, stream
from sqlalchemy.ext.asyncio.engine import AsyncEngine

from pantomath.registry import CachedRegistry

providers = CachedRegistry()


def to_sqlalchemy(*args, **kwargs) -> Callable:
    """Aiostream operator that loads records into the database."""

    @operator(pipable=True)
    def _to_sqlalchemy(source, conn, table, chunk_size: int = 1000):
        async def run(chunk):
            await conn.execute(table.insert(), chunk)

        return stream.action(stream.chunks(source, chunk_size), run)

    # KLUDGE: Trick to avoid the need for calling the pipe method in the pipeline.
    # to_sqlalchemy.pipe(arg1, arg2) becomes to_sqlalchemy(arg1, arg2)
    return _to_sqlalchemy.pipe(*args, **kwargs)


@dataclass(frozen=True)  # type: ignore
class Provider(ABC):
    """Interact with the data sources for a provider.

    :param config: Block from the configuration file that is specific to the provider.
    :param db_engine: Database engine to be used to load data into the database.
    :param log_level: Log level.
    """

    config: dict = field(default_factory={})  # type: ignore
    db_engine: AsyncEngine = None
    log_level: int = field(default=logging.ERROR)

    def __post_init__(self):
        """Set some fields after the class initialization."""
        logging.getLogger("asyncio").setLevel(self.log_level)
        logging.getLogger("sqlalchemy").setLevel(self.log_level)

    @abstractmethod
    async def collect(self):
        """Extract, transforms and loads from the provider data sources into the database."""  # noqa: E501
        pass


class AsyncIteratorWrapper:
    """Allow to asyncronously iterate a synchronous iterator."""

    def __init__(self, iterable: Iterable):
        """Initialize the object.

        :param iterable: Iterable to iterate over
        """
        self._iterable = iter(iterable)

    def __aiter__(self):
        """Implement __aiter__."""
        return self

    async def __anext__(self):
        """Implement __anext__."""
        try:
            return next(self._iterable)
        except StopIteration as ex:
            raise StopAsyncIteration() from ex


# These imports must be at the end of the file to avoid dependency issues
from pantomath.provider import aws  # noqa: E402,F401
