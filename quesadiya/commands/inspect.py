import click

from quesadiya.db import factory


def operator(project_name):
    interface = factory.get_interface()
    if project_name == "all":
        projects = interface.get_all_project()
        click.echo('Project list:')
        for p in projects:
            click.echo(p)
