import click

from quesadiya.errors import ProjectNotExistError
from quesadiya.errors import ProjectRunningError
from quesadiya.errors import AuthenticationError
from quesadiya.errors import NotJSONLFileError

from quesadiya.db import factory
from quesadiya.django_tool.database import insert_collaborator

from quesadiya import utils
import quesadiya

import os
import warnings
from datetime import datetime


def operator(
    project_name,
    edit,
    transfer_ownership,
    collaborator_input_path
):
    # check validitity of this operation
    admin_interface = factory.get_admindb_interface()
    if not admin_interface.check_project_exists(project_name):
        raise ProjectNotExistError(project_name)
    if admin_interface.is_project_running(project_name):
        raise ProjectRunningError(project_name, "`quesadiya modify`")
    if collaborator_input_path is not None:
        if collaborator_input_path[-6:] != ".jsonl":
            raise NotJSONLFileError("`--add-collaborators`",
                                    collaborator_input_path)
        utils.check_file_path(collaborator_input_path)
    if not utils.admin_auth(project_name):
        raise AuthenticationError(project_name)
    # start operation
    if (edit == "contact") or (edit == "description"):
        _edit_data(field=edit,
                   interface=admin_interface,
                   project_name=project_name)
    elif transfer_ownership:
        _transfer_ownership(project_name=project_name)
    elif collaborator_input_path is not None:
        _update_collaborators(project_name=project_name,
                              input_path=collaborator_input_path)


def _edit_data(field, interface, project_name):
    new_value = click.prompt("New {}".format(field))
    if field == "contact":
        interface.update_admin_contact(project_name=project_name,
                                       new_contact=new_value)
    elif field == "description":
        interface.update_project_description(project_name=project_name,
                                             new_description=new_value)


def _transfer_ownership(project_name):
    # get new values
    new_admin = click.prompt("New admin name")
    new_password = click.prompt("New password",
                                hide_input=True,
                                confirmation_prompt=True)
    # confirm the operation
    projectdb_interface = factory.get_projectdb_interface(project_name)
    admin = projectdb_interface.get_admin_info()
    expected = admin["username"] + "/" + project_name
    user_input = click.prompt("Type `{}` to confirm".format(expected))
    if user_input != expected:
        click.echo("Input doesn't match {}. Stop this operation.".format(expected))
    else:
        projectdb_interface.change_admin_name(new_admin=new_admin)
        projectdb_interface.change_admin_password(new_password=new_password)
        click.echo("The ownership of '{}' is transferred to user: {}".format(
            project_name, new_admin
        ))


def _update_collaborators(project_name, input_path):
    # load new collaborators
    new_cs = utils.load_format_collaborators(input_path=input_path)
    # get exisitng collaborators
    projectdb_interface = factory.get_projectdb_interface(project_name)
    current_cs = projectdb_interface.get_collaborators()
    # create a set of collaborator names to check exisitance of collaborator
    cs_names = set([x["collaborator_name"] for x in current_cs])
    num_added = 0
    warned = False
    with projectdb_interface.engine.connect() as con:
        for cs in new_cs:
            if cs["name"] not in cs_names:
                insert_collaborator(
                    con=con,
                    password=cs["password"],
                    collaborator_name=cs["name"],
                    date_time=datetime.now(),
                    contact=cs["contact"]
                )
                num_added += 1
            elif not warned:
                warnings.warn(
                    "Duplicate collaborator name found during inserting "
                    "new collabortors. Quesadiya skips duplicate "
                    "collaborators in the new file.", RuntimeWarning
                )
                warned = True
    click.echo("Added {} collaborators to project '{}'".format(
        num_added, project_name
    ))
