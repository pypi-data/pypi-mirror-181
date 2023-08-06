"""Organization subcommand cli."""
import click
import rich

import ikcli.utils.rich
from ikcli.users.core import Users

from .core import Organizations

# Click choice on organization visibility
visibility_choice = click.Choice(["PUBLIC", "TEAM"], case_sensitive=False)

# Click choice on member roles
role_choice = click.Choice(["OWNER", "MANAGER", "MEMBER", "PARTNER"], case_sensitive=False)

# A decorator to give Organizations object to commands
pass_organizations = click.make_pass_decorator(Organizations)


@click.group(name="organization")
@click.pass_context
def cli_organization(ctx):
    """Manage organizations."""
    ctx.obj = Organizations(ctx.obj)


@cli_organization.command(name="ls")
@click.option("--name", help="Filter organizations by name")
@click.option("--visibility", type=visibility_choice, help="Filter organizations by visibility")
@click.option("--limit", type=int, default=20, help="Specify how many rows to display")
@pass_organizations
def cli_organization_list(organizations, name, visibility, limit):
    """List organizations."""
    ikcli.utils.rich.table(
        organizations.list(name=name, visibility=visibility).limit(limit),
        "Organizations",
        ["name", "visibility"],
    )


@cli_organization.command(name="add")
@click.option("--visibility", type=visibility_choice, help="Organization visibility")
@click.argument("name")
@pass_organizations
def cli_organization_add(organizations, name, visibility):
    """Add organization NAME."""
    ikcli.utils.rich.create(f"Add Organization '{name}'", organizations, name=name, visibility=visibility)


@cli_organization.command(name="show")
@click.argument("name")
@pass_organizations
def cli_organization_show(organizations, name):
    """Show organization NAME."""
    rich.print_json(data=organizations.get(name=name)._data)


@cli_organization.command(name="delete")
@click.argument("name")
@pass_organizations
def cli_organization_delete(organizations, name):
    """Delete organization NAME."""
    ikcli.utils.rich.delete(organizations.get(name=name))


#
#   Members
#
@cli_organization.group(name="member")
def cli_organization_member():
    """Manage organization members."""
    pass


@cli_organization_member.command(name="ls")
@click.argument("organization_name")
@click.option("--username", help="Filter organization members by name")
@click.option("--role", type=role_choice, help="Filter organization members by role")
@pass_organizations
def cli_organization_member_list(organizations, organization_name, username, role):
    """List organizaton members."""
    # Get organization and members
    organization = organizations.get(name=organization_name)
    members = organization.members.list(username=username, role=role)

    # Display on table
    ikcli.utils.rich.table(members, "Members", ["username", "role"])


@cli_organization_member.command(name="add")
@click.argument("organization_name")
@click.argument("username")
@click.argument("role", type=role_choice)
@pass_organizations
def cli_organization_member_add(organizations, organization_name, username, role):
    """Add organizaton members."""
    # Get organization and user
    organization = organizations.get(name=organization_name)
    user = Users(organizations._http).get(username=username)
    ikcli.utils.rich.create(
        f"Add '{username}' as {organization_name}'s {role}",
        organization.members,
        user=user,
        role=role,
    )


@cli_organization_member.command(name="delete")
@click.argument("organization_name")
@click.argument("username")
@pass_organizations
def cli_organization_member_delete(organizations, organization_name, username):
    """Remove organizaton member."""
    # Get organization and member
    organization = organizations.get(name=organization_name)
    ikcli.utils.rich.delete(organization.members.get(username=username))
