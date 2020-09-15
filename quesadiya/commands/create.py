import click

from quesadiya.db import factory


def operator(project_name, admin_name, admin_password):
    interface = factory.get_interface()
    interface.insert_project(project_name, admin_name, admin_password)
    click.echo('{} created'.format(project_name))
