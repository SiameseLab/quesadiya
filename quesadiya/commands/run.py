import click

from quesadiya.errors import ProjectNotExistError
from quesadiya.errors import ProjectRunningError

from quesadiya.db import factory
from quesadiya import utils
import quesadiya

import os
import subprocess


def operator():
    admin_interface = factory.get_admindb_interface()
    run_path = os.path.join(quesadiya.get_base_path(), 'django_tool', 'manage.py')
    subprocess.call([run_path, "runserver"], shell=True)
