import click

from quesadiya.errors import ProjectNotExistError
from quesadiya.errors import ProjectRunningError
from quesadiya.errors import AuthenticationError

from quesadiya.db import factory
from quesadiya import utils
import quesadiya

import shutil
import os
import sys


def operator(project_name):
    admin_interface = factory.get_admindb_interface()
    if not admin_interface.check_project_exists(project_name):
        raise ProjectNotExistError(project_name)
    if admin_interface.is_project_running(project_name):
        raise ProjectRunningError(project_name, "`quesadiya delete`")
    if not utils.admin_auth(project_name):
        raise AuthenticationError(project_name)
    conf = click.confirm("Are you sure you want to continue?")
    if conf:
        click.echo("Successfully deleted project '{}'".format(project_name))
        # delete directory first
        shutil.rmtree(
            os.path.join(quesadiya.get_projects_path(), project_name)
        )
        # then, delete row in admin.db
        admin_interface.delete_project(project_name)
    else:
        click.echo("Stop deleting {}".format(project_name))
