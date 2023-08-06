"""Algorithm subcommand cli."""
import click
import rich
import ikcli.utils.rich
from .core import Algos

# Click choice on Qt framework
qt_choice = click.Choice(["pyqt", "pyside"], case_sensitive=False)

# A decorator to give Projects object to commands
pass_algos = click.make_pass_decorator(Algos)


@click.group(name="algo")
@click.pass_context
def cli_algo(ctx):
    """Manage algorithm."""
    # Retrieve username and password from context
    ctx.obj = Algos(str(ctx.obj.url), ctx.obj.auth.username, ctx.obj.auth.password)


@cli_algo.command(name="ls")
@pass_algos
def cli_algo_list(algos):
    """List local algorithms."""
    algo_list, columns = algos.get_list()
    rtable = rich.table.Table()
    rtable.title = f"Algorithms ({len(algo_list)})"

    for column in columns:
        rtable.add_column(column, justify="left")

    for algo in algo_list:
        rtable.add_row(*algo)

    rich.print(rtable)


@cli_algo.command(name="create")
@click.argument("name")
@click.option("--base_class", type=str, default="CWorkflowTask", help="Algorithm base class from Ikomia API")
@click.option("--widget_class", type=str, default="CWorkflowTaskWidget", help="Widget base class from Ikomia API")
@click.option("--qt", type=qt_choice, default="pyqt", help="Python Qt framework for widget")
@pass_algos
def cli_algo_create(algos, name, base_class, widget_class, qt):
    """Create local algorithm NAME."""
    console = rich.console.Console()
    with console.status(f"[cyan]Creating {name} ..."):
        algo_dir = algos.create(name, base_class, widget_class, qt)

    console.print(f"[green] {name} successfully created.")
    console.print(f"[green]Source code here: {algo_dir}")


@cli_algo.command(name="publish")
@click.argument("name")
@pass_algos
def cli_algo_publish(algos, name):
    """Publish algorithm NAME."""
    # Check credentials
    if not algos.is_logged():
        ikcli.utils.rich.auth_panel_info()
        username = click.prompt("Login", type=str)
        password = click.prompt("Password", type=str, hide_input=True)
        algos.login(username, password)

    console = rich.console.Console()
    console.print(f"[cyan]Publishing {name} to Ikomia HUB...")
    algos.publish(name)
    console.print(f"[green] {name} successfully published.")
