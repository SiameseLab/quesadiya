import click

from prettytable import PrettyTable

from quesadiya.db import factory
from quesadiya import utils


class DefaultTable:

    def __init__(self):
        self.default_table = PrettyTable(field_names=["Project Name",
                                                      "Admin Contact",
                                                      "Description",
                                                      "Date Created",
                                                      "Status"])
    def add_row(self, project):
        self.default_table.add_row([
            project.project_name,
            project.admin_contact,
            project.project_description,
            project.date_created,
            project.status.name
        ])

    def get_table(self):
        return self.default_table


# TODO: add function to print common error message
def operator(project_name, show_collaborators):
    if (project_name == "all") and show_collaborators:
        raise AssertionError(
            "`--show-collaborators` option is not supported for "
            "`quesadiya inspect all`"
        )
    if project_name == "all":
        _show_all()
    else:
        _show_project(project_name, show_collaborators)


def _format_collaborators(collaborators):
    table = PrettyTable(field_names=["Collaborator Name",
                                     "Password",
                                     "Contact"])
    for coll in collaborators:
        table.add_row(
            coll.collaborator_name,
            coll.collaborator_password,
            coll.collaborator_contact
        )
    return table


def _show_all():
    admin_interface = factory.get_admindb_interface()
    projects = admin_interface.get_all_projects()
    default_table = DefaultTable()
    for p in projects:
        default_table.add_row(p)
    click.echo(default_table.get_table())


def _show_project(project_name, show_collaborators):
    admin_interface = factory.get_admindb_interface()
    if not admin_interface.check_project_exists(project_name):
        click.echo(
            "Project ({}) doesn't exist. Check all project names by "
            "'quesadiya inspect all'".format(project_name)
        )
        return
    p = admin_interface.get_project(project_name)
    default_table = DefaultTable()
    default_table.add_row(p)
    if show_collaborators:
        if not utils.admin_auth(admin_interface, project_name):
            click.echo("Invalid name or password for {}".format(project_name))
            return
        click.echo(default_table.get_table())
        collaborators = admin_interface.get_collaborators(project_name)
        click.echo(_format_collaborators(collaborators))
    else:
        click.echo(default_table.get_table())
