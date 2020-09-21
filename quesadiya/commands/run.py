import click

from quesadiya.errors import ProjectNotExistError
from quesadiya.errors import AuthenticationError
from quesadiya.errors import ProjectRunningError

from quesadiya.db import factory
from quesadiya import utils
import quesadiya

import os


def operator(project_name):
    admin_interface = factory.get_admindb_interface()
    if not admin_interface.check_project_exists(project_name):
        raise ProjectNotExistError(project_name)
    if admin_interface.is_project_running(project_name):
        raise ProjectRunningError(project_name, "`quesadiya run`")
    if not utils.admin_auth(admin_interface, project_name):
        raise AuthenticationError(project_name)
    project_dir = os.path.join(quesadiya.get_projects_path(), project_name)
    projectdb_interface = factory.get_projectdb_interface(project_dir)
    triplets = projectdb_interface.get_triplets()
    count = 0
    for t in triplets:
        click.echo([t.time_changed.strftime("%m/%d/%Y"), t.status.name])
        count += 1
    click.echo('Project ({}) has {} rows'.format(project_name, count))
