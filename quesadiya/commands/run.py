import click

from quesadiya.db import factory
from quesadiya import utils
import quesadiya

import os


def operator(project_name):
    admin_interface = factory.get_admindb_interface()
    if not admin_interface.check_project_exists(project_name):
        click.echo(
            "project ({}) doesn't exist. check all project names by "
            "'quesadiya inspect all'".format(project_name)
        )
        return
    if not utils.admin_auth(admin_interface, project_name):
        sys.exit("invalid name or password for {}".format(project_name))
    project_dir = os.path.join(quesadiya.get_projects_path(), project_name)
    projectdb_interface = factory.get_projectdb_interface(project_dir)
    triplets = projectdb_interface.get_triplets()
    for t in triplets:
        click.echo(t)
    click.echo('project ({}) has {} rows'.format(project_name, len(triplets)))
