"""Root cli."""
import logging
import sys

import click
import rich
import rich.padding
import rich.panel
import rich.traceback
from rich.logging import RichHandler

import ikcli.utils.rich

from .algo.cli import cli_algo
from .namespaces.cli import cli_namespace
from .net.http import http
from .organizations.cli import cli_organization
from .projects.cli import cli_project
from .users.core import Account

# Click context settings
CONTEXT_SETTINGS = dict(help_option_names=["--help", "-h"])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option()
@click.option(
    "--url",
    envvar="IKOMIA_URL",
    default="",
    help="Ikomia HUB url.",
)
@click.option(
    "--username",
    envvar="IKOMIA_USER",
    help="Ikomia API user name.",
)
@click.option(
    "--password",
    envvar="IKOMIA_PWD",
    help="Ikomia API password.",
)
@click.option("--debug/--no-debug", default=False)
@click.pass_context
def cli_cli(ctx, url, username, password, debug=False):
    """Ikomia command line interface."""
    # Configure logger
    level = logging.INFO
    if debug:
        level = logging.DEBUG
        rich.traceback.install(show_locals=True, suppress=[click])
    logging.basicConfig(level=level, datefmt="[%X]", handlers=[RichHandler()])

    # Setup HTTP request
    ctx.obj = http(url, username=username, password=password)


# @cli_cli.command(name="register")
# @click.option("--username", prompt="Username")
# @click.option("--email", prompt="Email")
# @click.password_option()
# @click.pass_context
# def cli_register(ctx, username, email, password):
#     """Register a new user."""
#     rich.print(f"Register user {username}")
#     account = Account(ctx.obj)
#     user = account.register(username, email, password)
#     rich.print(f"[green] {user}")
#
#
# @cli_cli.command(name="login")
# @click.option("--username", prompt="Username")
# @click.option(
#    "--password",
#    prompt=True,
#    hide_input=True,
# )
# @click.pass_context
# def cli_login(ctx, username, password):
#    """Log in user."""
#    Account(ctx.obj).login(username, password)


def cli():
    """
    Call click and catch all Exceptions to display them properly.

    :raises Exception: If debug is enabled and something wrong happen
    """
    try:
        # Call click
        cli_cli()
    except Exception as e:
        # If debug enable, let exception raise (and rich display traceback)
        if logging.root.level == logging.DEBUG:
            raise

        # Otherwise try to display it properly
        ikcli.utils.rich.exception(e)
        sys.exit(1)


cli_cli.add_command(cli_algo)
# cli_cli.add_command(cli_namespace)
# cli_cli.add_command(cli_organization)
# cli_cli.add_command(cli_project)

if __name__ == "__main__":
    cli()
