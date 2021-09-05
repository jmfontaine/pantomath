import logging
import sys

import click
from loguru import logger
from rich.traceback import install

from pantomath import Pantomath, __version__


class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


logging.basicConfig(handlers=[InterceptHandler()], level=0)

install(show_locals=True)


@click.group()
@click.option(
    "-c",
    "--config",
    "config_path",
    default="pantomath.yaml",
    help="Set configuration file path.",
    show_default=True,
)
@click.option("-v", "--verbose", "verbosity", count=True)
@click.pass_context
def cli(ctx, config_path, verbosity) -> None:
    """
    Easily collect, analyze, and explore FinOps data.

    Written by Jean-Marc Fontaine (jm@jmfontaine.net).
    """  # noqa: E501
    ctx.ensure_object(dict)

    ctx.obj["config_path"] = config_path

    if verbosity == 0:
        level = logging.ERROR
    elif verbosity == 1:
        level = logging.WARNING
    elif verbosity == 2:
        level = logging.INFO
    elif verbosity > 2:
        level = logging.DEBUG
    logger.remove()
    logger.add(
        sys.stderr,
        colorize=True,
        format="<level>{level}</level> - <cyan>{name}</cyan> - {message}",
        level=level,
    )
    ctx.obj["log_level"] = level


@cli.command()
@click.pass_context
def collect(ctx) -> None:
    """Extract, transform and load from data sources into the database."""
    pantomath = Pantomath(
        config_path=ctx.obj["config_path"],
        log_level=ctx.obj["log_level"],
    )
    pantomath.collect()


@cli.command()
def version() -> None:
    """Display version."""
    print(__version__)
