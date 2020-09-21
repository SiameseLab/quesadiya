import click
import click_spinner

from quesadiya.errors import NotJSONLFileError
from quesadiya.errors import ProjectExistsError
from quesadiya.errors import QuesadiyaCommandError

from quesadiya.db.schema import ProjectStatusEnum
from quesadiya.db import factory

from quesadiya import utils
import quesadiya

from datetime import datetime
from tqdm import tqdm
from collections import defaultdict

import jsonlines
import os


def operator(
    project_name,
    project_description,
    admin_name,
    admin_password,
    input_data_path,
    admin_contact,
    collaborator_input_path
):
    if input_data_path[-6:] != ".jsonl":
        raise NotJSONLFileError("`DATAPATH`", input_data_path)
    if (collaborator_input_path is not None) and \
        (collaborator_input_path[-6:] != ".jsonl"):
        raise NotJSONLFileError("`--add-collabortos`", collaborator_input_path)
    if project_name == "all":
        raise QuesadiyaCommandError("`all` is reserved for use by Quesadiya.")
    admin_interface = factory.get_admindb_interface()
    # create folder for project inside `projects` dir and insert project.db in it
    project_dir = os.path.join(quesadiya.get_projects_path(), project_name)
    # TODO: create a custom exception
    if admin_interface.check_project_exists(project_name):
        raise ProjectExistsError(project_name)
    try:
        os.mkdir(project_dir)
    except PermissionError:
        raise PermissionError(
            "Permission is denied to create a project folder under {}. "
            "Make sure you have the right permission to create folder under "
            "the directory.".format(quesadiya.get_projects_path())
        )
    # create project.db
    factory.init_projectdb(project_dir)
    # get interface
    projectdb_interface = factory.get_projectdb_interface(project_dir)
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
            admin_name=admin_name,
            admin_password=admin_password,
            admin_contact=admin_contact,
            status=ProjectStatusEnum.not_running
        )
        if collaborator_input_path is not None:
            _add_collaborators(interface=admin_interface,
                               project_name=project_name,
                               input_path=collaborator_input_path)
    # insert bulk data into database
    click.echo("Finish creating {}".format(project_name))


def _add_collaborators(interface, project_name, input_path):
    project_id = interface.get_project_id(project_name)
    collaboratos = utils.load_format_collaborators(project_id=project_id,
                                                   input_path=input_path)
    interface.collaborators_bulk_insert(collaboratos)
