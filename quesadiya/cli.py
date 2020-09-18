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
    """Delicious mexican pizza."""
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
    metavar="ADMIN"
)
@click.argument(
    "admin_password",
    metavar="PASSWORD"
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
def create(
    project_name,
    admin_name,
    admin_password,
    input_data_path,
    project_description,
    contact
):
    """Create a data annotation project."""
    quesadiya.commands.create.operator(
        project_name=project_name,
        project_description=project_description,
        input_data_path=input_data_path,
        admin_name=admin_name,
        admin_password=admin_password,
        admin_contact=contact
    )


@cli.command()
@click.argument(
    "project_name",
    metavar="PROJECT"
)
def run(project_name):
    """Run annotation project indicated by project name."""
    quesadiya.commands.run.operator(project_name=project_name)


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
def modify(project_name):
    """Modify project indicated by project name."""
    quesadiya.commands.modify.operator(project_name=project_name)


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
    help="Include text field assocaited with sample ids in output file."
)
def export(project_name, output_path, include_text):
    """Export data associated with a project indicated by project name."""
    quesadiya.commands.export.operator(
        project_name=project_name,
        output_path=output_path,
        include_text=include_text
    )
