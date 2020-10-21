import click

import quesadiya

import os
import sys
import subprocess


def operator(port_number):
    run_path = os.path.join(quesadiya.get_base_path(), 'django_tool', 'manage.py')
    child = subprocess.Popen(
        [
            sys.executable,
            run_path,
            "runserver",
            "localhost:{}".format(port_number),
            "--insecure"
        ], # insert stdout=subprocess.PIPE to turn off django outputs
        stdin=subprocess.PIPE,
        universal_newlines=True
    )
    child.communicate()
