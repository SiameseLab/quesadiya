import click
import click_spinner

from quesadiya.errors import NotJSONLFileError
from quesadiya.errors import ProjectExistsError
from quesadiya.errors import QuesadiyaCommandError

from quesadiya.db.schema import ProjectStatusEnum
from quesadiya.db import factory
from quesadiya.django_tool.database import (
    create_django_tables,
    insert_admin,
    insert_collaborator
)

from quesadiya import utils
import quesadiya

from django.contrib.auth.hashers import make_password

from datetime import datetime
from tqdm import tqdm
from collections import defaultdict

import jsonlines
import os


def operator(
    project_name,
    project_description,
    admin_name,
    input_data_path,
    admin_contact,
    collaborator_input_path
):
    # initial checks
    if input_data_path[-6:] != ".jsonl":
        raise NotJSONLFileError("`DATAPATH`", input_data_path)
    if (collaborator_input_path is not None) and \
        (collaborator_input_path[-6:] != ".jsonl"):
        raise NotJSONLFileError("`--add-collabortos`", collaborator_input_path)
    if project_name == "all":
        raise QuesadiyaCommandError("`all` is reserved for use by Quesadiya.")
    utils.check_file_path(input_data_path)
    if collaborator_input_path is not None:
        utils.check_file_path(collaborator_input_path)
    admin_interface = factory.get_admindb_interface()
    project_dir = os.path.join(quesadiya.get_projects_path(), project_name)
    if admin_interface.check_project_exists(project_name):
        raise ProjectExistsError(project_name)
    # create folder for project inside `projects` dir and insert project.db in it
    try:
        os.mkdir(project_dir)
    except PermissionError:
        raise PermissionError(
            "Permission is denied to create a project folder under {}. "
            "Make sure you have the right permission to create folder under "
            "the directory.".format(quesadiya.get_projects_path())
        )
    # ask admin password
    admin_password = click.prompt("Admin password",
                                  hide_input=True,
                                  confirmation_prompt=True)
    # create project.db
    factory.init_projectdb(project_dir)
    # get interface
    projectdb_interface = factory.get_projectdb_interface(project_name)
    # load data and format it to be inserted into project.db
    triplets, candidates, sample_text = \
        utils.load_format_dataset(input_path=input_data_path)
    # start inserting rows into tables in project.db
    click.echo("Inserting data. This may take a while...".format(project_name))
    # showing spinner
    with click_spinner.spinner():
        projectdb_interface.triplets_bulk_insert(triplets)
        projectdb_interface.candidate_groups_bulk_insert(candidates)
        projectdb_interface.sample_text_bulk_insert(sample_text)
        # insert project into admin.db
        admin_interface.insert_project(
            project_name=project_name,
            project_description=project_description,
            admin_contact=admin_contact,
            status=ProjectStatusEnum.not_running
        )
        # create django tables in project.db and insert values
        with projectdb_interface.engine.connect() as con:
            create_django_tables(con)
            # encode password
            # encoded_password = make_password(admin_password)
            insert_admin(
                con=con,
                # password=encoded_password,
                password=admin_password,
                admin_name=admin_name,
                date_time=datetime.now()
            )
        if collaborator_input_path is not None:
            add_collaborators(
                engine=projectdb_interface.engine,
                project_name=project_name,
                input_path=collaborator_input_path
            )
    # insert bulk data into database
    click.echo("Finish creating {}".format(project_name))


def add_collaborators(engine, project_name, input_path):
    collaborators = utils.load_format_collaborators(input_path=input_path)
    with engine.connect() as con:
        for collaborator in collaborators:
            insert_collaborator(
                con=con,
                password=collaborator["password"],
                collaborator_name=collaborator["name"],
                date_time=datetime.now(),
                contact=collaborator["contact"]
            )
