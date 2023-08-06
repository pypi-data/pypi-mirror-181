"""Some shortcuts to display rich interface on ikcli."""
from typing import List

import rich
import rich.align
import rich.console
import rich.prompt
import rich.table
from PIL import ImageShow

import ikcli.net.api
import ikcli.net.http.exceptions
from ikcli.net.api.pagination import LimitedPagination, Pagination


def table(pagination: Pagination, title: str, columns: List[str]):
    """
    Display API object in a table.

    :param pagination: Pagination object
    :param title: Table title
    :param columns: Column name to display
    """
    # Define table
    rtable = rich.table.Table()
    for column in columns:
        rtable.add_column(column.title(), justify="right")

    # Add row per organization
    for row in pagination:
        args = [row[column] for column in columns]
        rtable.add_row(*args)

    # If it remains object in pagination, display it
    if isinstance(pagination, LimitedPagination) and pagination.remaining() > 0:
        rtable.add_section()
        rtable.add_row(f"[bold] ... and {pagination.remaining()} remaining")

    # Craft title
    rtable.title = f"{title.title()} ({len(pagination)})"

    # Print table
    rich.print(rtable)


def menu(title: str, options: dict, prompt: str = "Please choose an option", default=None, none: bool = False):
    """
    Display a menu and ask to user to choose an entry.

    :param title: A menu title
    :param options: Dict that contains a key to return if chosen and a string to display
    :param prompt: Prompt to display
    :param default: A default value
    :param none: Add a 'None of them' entry to meny
    :return: Selected option key
    """
    # Craft choice list
    choices = sorted(options, key=options.get)
    prompt_choices = [format(i + 1) for i in range(0, len(choices))]
    default_choice = None

    # Define beaufiful padding according to options length
    padding = 1
    if len(choices) >= 10:
        padding = 2
    elif len(choices) >= 100:
        padding = 3

    # Create table menu
    table_menu = rich.table.Table(box=rich.box.MINIMAL_DOUBLE_HEAD)
    table_menu.add_column(title)
    for counter, option in enumerate(choices):
        value = f"{counter+1:{padding}} - {options[option]}"
        if default == option:
            value = "[prompt.default]" + value
            default_choice = counter + 1
        table_menu.add_row(value)

    # If none (of them) is defined, add special entries
    if none:
        options[None] = None
        prompt_choices.append("0")
        choices.append(None)
        table_menu.add_row(f"[bright_black]{0:{padding}} - None of them")

    # Display table and prompt choice
    rich.print(rich.padding.Padding(table_menu, (0, 1)))
    intprompt = rich.prompt.IntPrompt(f" > {prompt}", choices=prompt_choices, show_choices=False)
    intprompt.prompt_suffix = " : "
    index = intprompt(default=default_choice)

    # Return value
    return choices[index - 1]


def create(title: str, api_list: ikcli.net.api.List, *args, **kwargs) -> ikcli.net.api.Object:
    """
    Display spinners and infos about object creation.

    :param title: A title to display behind spinner
    :param api_list: An API list object
    :param args: Args to create object
    :param kwargs: Kwargs to create object
    :return: A newly created object
    """
    console = rich.console.Console()
    with console.status(f"[cyan]{title} ..."):
        api_object = api_list.create(*args, **kwargs)
    console.print(f"[green] {api_object}")
    return api_object


def delete(api_object: ikcli.net.api.Object):
    """
    Prompt for object deletion.

    :param api_object: API Object to delete
    """
    console = rich.console.Console()
    if not rich.prompt.Confirm.ask(f"Do you really want to delete [red]'{api_object}'[/red] ?"):
        console.print("[orange3]Aborted by user")
        return

    with console.status(f"[cyan]Deleting {api_object} ..."):
        api_object.delete()
    console.print(f"[orange3]{api_object.__class__.__name__} deleted")


def exception(e: Exception):
    """
    Try to properly display exception.

    :param e: Exception to display
    """
    # Process some well known exceptions
    if isinstance(e, ikcli.net.http.exceptions.HTTPBadCodeError):
        title = e.__class__.__name__
        lines = []
        data = e.data()
        if e.code == 401:
            lines.append(
                "\U0001F449 If you want to avoid be prompted for credentials,"
                " may you have to define username and password as follow:"
            )
            lines.append(
                rich.padding.Padding(
                    "$> export IKOMIA_USER='my-user-name'\n$> export IKOMIA_PWD='4-v3ry-s3cr3t-p4ssw0rd!'",
                    (1, 2),
                    style="green on grey11",
                    expand=False,
                ),
            )
        elif isinstance(data, str):
            lines.append(f"\U0001F449 {data}")
        elif "detail" in data:
            lines.append(f"\U0001F449 {data['detail']}")
        elif "message" in data:
            lines.append(f"\U0001F449 {data['message']}")
        else:
            for field, messages in e.data().items():
                lines.append(f"\U0001F449 [bright_white]{field}[/bright_white]:")
                for message in messages:
                    lines.append(f" - {message}")
                lines.append("")

            # Remove last line return
            lines.pop()
    elif isinstance(e, ikcli.net.api.exceptions.ObjectNotFoundException):
        title = f"{e.object_class.__name__} not found"
        lines = [f"\U0001F449 {e.object_class.__name__} that match :"]
        lines += [f"  - {k}: '{v}'" for k, v in e.kwargs.items()]
        lines.append("  was not found.")
    elif isinstance(e, ikcli.net.api.exceptions.NotUniqueObjectException):
        title = f"Not unique {e.object_class.__name__} found"
        lines = [f"\U0001F449 {len(e.pagination)} {e.object_class.__name__}(s) that match :"]
        lines += [f"  - {k}: '{v}'" for k, v in e.kwargs.items()]
        lines.append("  were found.")
    else:
        # Common case exception
        title = e.__class__.__name__
        lines = ["\U0001F449 " + str(arg) for arg in e.args]

    # Finally display
    rich.print(
        rich.panel.Panel(
            rich.padding.Padding(rich.console.Group(*lines), (1, 1), style="white"),
            title=title,
            width=80,
            border_style="bold red",
        )
    )


def show_image(path: str, title: str = None, **options) -> bool:
    """
    Use PIL ImageShow to display existing image without convert nor temporary save it.

    :param path: A path to image to display
    :param title: A title to give to image display (not well supported)
    :param **options: Other options to give to ImageShow
    :return: True if image was displayed, False otherwise
    """
    for viewer in ImageShow._viewers:
        if viewer.show_file(path, title=title, **options):
            return True
    return False


def auth_panel_info():
    lines = []
    lines.append(
        "\U0001F449 If you want to avoid being prompted for your credentials,"
        " you may define username and password as follow:"
    )
    lines.append(
        rich.padding.Padding(
            "$> export IKOMIA_USER='my-user-name'\n$> export IKOMIA_PWD='4-v3ry-s3cr3t-p4ssw0rd!'",
            (1, 2),
            style="green on grey11",
            expand=False,
        ),
    )
    rich.print(
        rich.panel.Panel(
            rich.padding.Padding(rich.console.Group(*lines), (1, 1), style="white"),
            title="Authentication information",
            width=80,
            border_style="cyan",
        )
    )
