import click

from prettytable import PrettyTable

from quesadiya.db import factory
from quesadiya import utils


# TODO: add show_user option with admin auth later
def operator(project_name):
    admin_interface = factory.get_admindb_interface()
    result = PrettyTable(field_names=["project name",
                                      "admin name",
                                      "project description"])
    if project_name == "all":
        projects = admin_interface.get_all_projects()
        for p in projects:
            result.add_row([
                p.project_name,
                p.admin_name,
                p.project_description
            ])
    else:
        if not admin_interface.check_project_exists(project_name):
            click.echo(
                "project ({}) doesn't exist. check all project names by "
                "'quesadiya inspect all'".format(project_name)
            )
            return
        p = admin_interface.get_project(project_name)
        result.add_row([
            p.project_name,
            p.admin_name,
            p.project_description
        ])
    click.echo(result)
