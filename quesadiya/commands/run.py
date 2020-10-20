import click

from quesadiya.errors import ProjectNotExistError
from quesadiya.errors import ProjectRunningError

from quesadiya.db import factory
from quesadiya import utils
import quesadiya

import os
import subprocess


def operator(port_number):
    admin_interface = factory.get_admindb_interface()
    run_path = os.path.join(quesadiya.get_base_path(), 'django_tool', 'manage.py')
    subprocess.Popen(
        [
            run_path,
            "runserver",
            "localhost:{}".format(port_number),
            "--insecure"
        ], shell=True
    )
