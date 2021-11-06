"""Base elements."""
import asyncio
import json
import logging

import click
import confuse
import pkg_resources
from sqlalchemy.ext.asyncio import create_async_engine

from pantomath.provider import providers

__version__ = pkg_resources.get_distribution(__name__).version


class Pantomath:
    """Main class that coordinates all the other classes."""

    def __init__(self, config_path: str, log_level: int = None) -> None:
        """Initialize the object.

        :param config_path: Path to the configuration file
        :param log_level: Log level. Default is ERROR.
        """
        if log_level is None:
            log_level = logging.ERROR

        self._config = self._load_configuration(config_path)
        self.log_level = log_level

    def _load_configuration(self, config_path: str) -> confuse.templates.AttrDict:
        config = confuse.Configuration("pantomath")
        config.set_file(config_path)

        template = {
            "version": str,
            "db": {
                "host": confuse.Optional("localhost"),
                "port": confuse.Optional(5432),
                "user": confuse.Optional("pantomath"),
                "password": confuse.Optional(""),
                "name": str,
            },
            "providers": {
                "aws": confuse.Optional(
                    {
                        "settings": {
                            "accounts": confuse.Sequence(
                                {
                                    "assume_role": confuse.Optional(None),
                                    "profile": str,
                                }
                            ),
                        },
                        "sources": list,
                    }
                ),
            },
        }
        try:
            return config.get(template)
        except confuse.ConfigError as err:
            raise click.UsageError(err)

    def _get_db_dsn(self) -> str:
        return "postgresql+asyncpg://{user}:{password}@{host}:{port}/{name}".format(
            **self._config["db"]
        )

    async def _async_collect(self) -> None:
        def serialize_to_json(obj):
            # To avoid empty values being serialized as the string "null"
            if obj is None:
                return None

            return json.dumps(obj, indent=1, sort_keys=True, default=str)

        dsn = self._get_db_dsn()
        engine = create_async_engine(dsn, echo=False, json_serializer=serialize_to_json)

        for provider_name, provider_config in self._config["providers"].items():
            provider = providers.get(
                provider_name,
                config=provider_config,
                db_engine=engine,
                log_level=self.log_level,
            )
            await provider.collect()

    def collect(self) -> None:
        """Extract, transform and load from data sources into the database."""
        asyncio.run(self._async_collect())
