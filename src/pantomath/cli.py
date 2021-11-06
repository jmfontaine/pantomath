"""CLI commands."""
import logging
import sys

import click
from loguru import logger
from rich.traceback import install

from pantomath import Pantomath, __version__


class _InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name  # noqa: SC200
        except ValueError:
            level = record.levelno  # type: ignore # noqa: SC200

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2  # noqa: SC200
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back  # type: ignore
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(  # noqa: SC200
            level, record.getMessage()
        )


logging.basicConfig(handlers=[_InterceptHandler()], level=0)

install(show_locals=True)

# We use "help" and "short_help" parameters to document the CLI
# without impacting the API documentation that is auto-generated from the docstrings.
@click.group(  # noqa: E302
    help="""Easily collect, analyze, and explore FinOps data.

Written by Jean-Marc Fontaine (jm@jmfontaine.net).
"""
)
@click.option(
    "-c",
    "--config",
    "config_path",
    default="pantomath.yaml",
    help="Set configuration file path.",
    show_default=True,
)
@click.option(
    "-v",
    "--verbose",
    "verbosity",
    count=True,
    help="Set output verbosity. Can be passed multiple times to increase verbosity.",
)
@click.pass_context
def cli(ctx: click.Context, config_path: str, verbosity: int) -> None:
    """Root group for the CLI commands.

    Initializes some settings based on the provided options.
    """
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


@cli.command(
    short_help="Extract, transform and load from data sources into the database."
)
@click.pass_context
def collect(ctx: click.Context) -> None:
    """Wrap the :meth:`pantomath.Pantomath.collect` function."""
    pantomath = Pantomath(
        config_path=ctx.obj["config_path"],
        log_level=ctx.obj["log_level"],
    )
    pantomath.collect()


@cli.command()
def version() -> None:
    """Display Pantomath version."""
    print(__version__)
