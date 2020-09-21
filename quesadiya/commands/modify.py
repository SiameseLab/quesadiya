import click

from quesadiya.errors import ProjectNotExistError
from quesadiya.errors import ProjectRunningError
from quesadiya.errors import AuthenticationError
from quesadiya.errors import NotJSONLFileError

from quesadiya.db import factory
from quesadiya import utils
import quesadiya

import os


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
    if not utils.admin_auth(admin_interface, project_name):
        raise AuthenticationError(project_name)
    # start operation
    if (edit == "contact") or (edit == "description"):
        _edit_data(field=edit,
                   interface=admin_interface,
                   project_name=project_name)
    elif transfer_ownership:
        _transfer_ownership(interface=admin_interface,
                            project_name=project_name)
    elif collaborator_input_path is not None:
        if collaborator_input_path[-6:] != ".jsonl":
            raise NotJSONLFileError("`--add-collaborators`",
                                    collaborator_input_path)
        _update_collaborators(interface=admin_interface,
                              project_name=project_name,
                              input_path=collaborator_input_path)


def _edit_data(field, interface, project_name):
    new_value = click.prompt("New {}".format(field))
    if field == "contact":
        interface.update_admin_contact(project_name=project_name,
                                       new_contact=new_value)
    elif field == "description":
        interface.update_project_description(project_name=project_name,
                                             new_description=new_value)


def _transfer_ownership(interface, project_name):
    # get new values
    new_admin = click.prompt("New admin name")
    new_password = click.prompt("New password", hide_input=True)
    # confirm the operation
    admin_name = interface.get_project(project_name).admin_name
    expected = admin_name + "/" + project_name
    user_input = click.prompt("Type `{}` to confirm".format(expected))
    if user_input != expected:
        click.echo("Input doesn't match {}. Stop this operation.".format(expected))
    else:
        interface.change_admin_name(project_name=project_name,
                                    new_admin=new_admin)
        interface.change_admin_password(project_name=project_name,
                                        new_password=new_password)
        click.echo("The ownership of '{}' is transferred to new admin: {}".format(
            project_name, new_admin
        ))


def _update_collaborators(interface, project_name, input_path):
    project_id = interface.get_project_id(project_name)
    collaborators = utils.load_format_collaborators(project_id=project_id,
                                                   input_path=input_path)
    num_added = interface.collaborators_bulk_update(collaborators, project_id)
    click.echo("Added {} collaborators to project '{}'".format(
        num_added, project_name
    ))
