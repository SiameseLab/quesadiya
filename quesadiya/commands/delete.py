import click

from quesadiya.db import factory
from quesadiya import utils
import quesadiya

import shutil
import os
import sys


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
    conf = click.confirm("Are you sure you want to continue?")
    if conf:
        admin_interface.delete_project(project_name)
        click.echo('successfully deleted {}'.format(project_name))
        shutil.rmtree(
            os.path.join(quesadiya.get_projects_path(), project_name)
        )
    else:
        click.echo("stop deleting {}".format(project_name))
