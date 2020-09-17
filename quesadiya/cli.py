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
    """print path to this package."""
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
    help="description of a project to create"
)
def create(
    project_name,
    admin_name,
    admin_password,
    input_data_path,
    project_description
):
    """create annotation project."""
    quesadiya.commands.create.operator(
        project_name=project_name,
        project_description=project_description,
        input_data_path=input_data_path,
        admin_name=admin_name,
        admin_password=admin_password,
    )


@cli.command()
@click.argument(
    "project_name",
    metavar="PROJECT"
)
def run(project_name):
    """run annotation project indicated by project name."""
    quesadiya.commands.run.operator(project_name=project_name)


@cli.command()
@click.argument(
    "project_name",
    metavar="PROJECT"
)
def inspect(project_name):
    """show project information indicated by project name."""
    quesadiya.commands.inspect.operator(project_name=project_name)


@cli.command()
@click.argument(
    "project_name",
    metavar="PROJECT"
)
def modify(project_name):
    """modify project indicated by project name."""
    quesadiya.commands.modify.operator(project_name=project_name)


@cli.command()
@click.argument(
    "project_name",
    metavar="PROJECT"
)
def delete(project_name):
    """delete project indicated by project name."""
    quesadiya.commands.delete.operator(project_name=project_name)


@cli.command()
@click.argument(
    "project_name",
    metavar="PROJECT"
)
def export(project_name):
    """export data associated with project indicated by project name."""
    quesadiya.commands.export.operator(project_name=project_name)
