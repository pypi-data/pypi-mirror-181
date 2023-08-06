"""Namespace subcommand cli."""
import click
import rich

import ikcli.utils.rich

from .core import Namespaces

# Click choice on organization visibility
# TODO: move this on core file
visibility_choice = click.Choice(["PRIVATE", "TEAM"], case_sensitive=False)


# A decorator to give Namespaces object to commands
pass_namespaces = click.make_pass_decorator(Namespaces)


@click.group(name="namespace")
@click.pass_context
def cli_namespace(ctx):
    """Manage namespaces."""
    ctx.obj = Namespaces(ctx.obj)


@cli_namespace.command(name="ls")
@click.option("--name", help="Filter namespaces by name")
@click.option("--limit", type=int, default=20, help="Specify how many rows to display")
@pass_namespaces
def cli_namespace_list(namespaces, name, limit):
    """List namespaces."""
    ikcli.utils.rich.table(
        namespaces.list(name=name).limit(limit),
        "Namespaces",
        ["name", "path", "visibility"],
    )


@cli_namespace.command(name="add")
@click.argument("namespace")
@click.argument("name")
@click.option("--visibility", type=visibility_choice, help="Filter organizations by visibility")
@pass_namespaces
def cli_namespace_add(namespaces, namespace, name, visibility):
    """Add namespaces NAME to NAMESPACE."""
    # Get parent namespace
    ns = namespaces.get(name=namespace)

    # Add sub namespace
    subns = ns.namespaces.create(name=name, visibility=visibility)
    rich.print(subns)


@cli_namespace.command(name="delete")
@click.argument("name")
@pass_namespaces
def cli_namespace_delete(namespaces, name):
    """Delete namespace NAME."""
    ikcli.utils.rich.delete(namespaces.get(name=name))
