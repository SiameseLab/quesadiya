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
    if not utils.admin_auth(admin_interface, project_name):
        raise AuthenticationError(project_name)
    conf = click.confirm("Are you sure you want to continue?")
    if conf:
        admin_interface.delete_project(project_name)
        click.echo("Successfully deleted {}".format(project_name))
        shutil.rmtree(
            os.path.join(quesadiya.get_projects_path(), project_name)
        )
    else:
        click.echo("Stop deleting {}".format(project_name))
