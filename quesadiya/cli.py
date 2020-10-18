import click

import os

import quesadiya
import quesadiya.commands.create
import quesadiya.commands.run
import quesadiya.commands.inspect
import quesadiya.commands.delete
import quesadiya.commands.export
import quesadiya.commands.modify


@click.group()
@click.version_option()
def cli():
    """A delicious mexican dish."""
    pass


@cli.command()
def path():
    """Print path to this package."""
    click.echo("quesadiya resides @ {}".format(
        quesadiya.get_base_path()
    ))


@cli.command()
@click.argument(
    "project_name",
    metavar="PROJECT"
)
@click.argument(
    "admin_name",
    metavar="ADMIN",
)
@click.argument(
    "input_data_path",
    metavar="DATAPATH"
)
@click.option(
    "-d",
    "--project-description",
    type=click.STRING,
    default="No description",
    help="Description of a project to create."
)
@click.option(
    "-c",
    "--contact",
    type=click.STRING,
    default="No contact",
    help="Contact to admin user."
)
@click.option(
    "-a",
    "--add-collaborators",
    type=click.STRING,
    help="Add collaboratos from a jsonl file. Each row in the file must "
         "follow the following format: "
         "{'name': str, 'password': str, 'contact': str}. "
         "Note that `contact` field can be empty."
)
def create(
    project_name,
    admin_name,
    input_data_path,
    project_description,
    contact,
    add_collaborators
):
    """Create a data annotation project."""
    quesadiya.commands.create.operator(
        project_name=project_name,
        project_description=project_description,
        input_data_path=input_data_path,
        admin_name=admin_name,
        admin_contact=contact,
        collaborator_input_path=add_collaborators
    )


@cli.command()
@click.option(
    "-p",
    "--port",
    default=1133,
    help="Select a port number to run quesadiya. The default port for "
         "quesadiya is 1133."
)
def run(port):
    """Run annotation project indicated by project name."""
    quesadiya.commands.run.operator(port)


@cli.command()
@click.argument(
    "project_name",
    metavar="PROJECT"
)
@click.option(
    "-s",
    "--show-collaborators",
    is_flag=True,
    default=False,
    help="Show all collaborators associated with a project. "
         "This operation requires admin authentication."
)
def inspect(project_name, show_collaborators):
    """Show project information indicated by project name."""
    quesadiya.commands.inspect.operator(
        project_name=project_name,
        show_collaborators=show_collaborators
    )


@cli.command()
@click.argument(
    "project_name",
    metavar="PROJECT"
)
@click.option(
    "-e",
    "--edit",
    type=click.Choice(["contact", "description"], case_sensitive=True),
    help="Edit `admin contact` or `project description` of a project."
)
@click.option(
    "-t",
    "--transfer-ownership",
    is_flag=True,
    default=False,
    help="Change `admin name` and `admin password` of a project."
)
@click.option(
    "-a",
    "--add-collaborators",
    type=click.STRING,
    help="Add collaboratos from a jsonl file. Each row in the file must "
         "follow the following format: "
         "{'name': str, 'password': str, 'contact': str}. "
         "Note that `contact` field can be empty."
)
def modify(
    project_name,
    edit,
    transfer_ownership,
    add_collaborators
):
    """Modify a project indicated by project name. Note that it exectues one
    operation per run.
    """
    quesadiya.commands.modify.operator(
        project_name=project_name,
        edit=edit,
        transfer_ownership=transfer_ownership,
        collaborator_input_path=add_collaborators
    )


@cli.command()
@click.argument(
    "project_name",
    metavar="PROJECT"
)
def delete(project_name):
    """Delete project indicated by project name. Note that this operation
    will delete all data associated with a project."""
    quesadiya.commands.delete.operator(project_name=project_name)


@cli.command()
@click.argument(
    "project_name",
    metavar="PROJECT"
)
@click.argument("output_path")
@click.option(
    "-i",
    "--include-text",
    is_flag=True,
    default=False,
    help="Include text field assocaited with sample ids into output file."
)
def export(project_name, output_path, include_text):
    """Export data associated with a project indicated by project name."""
    quesadiya.commands.export.operator(
        project_name=project_name,
        output_path=output_path,
        include_text=include_text
    )
