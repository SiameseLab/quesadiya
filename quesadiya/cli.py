import click

import quesadiya.commands.create
import quesadiya.commands.run
import quesadiya.commands.inspect
import quesadiya.commands.delete
import quesadiya.commands.export
import quesadiya.commands.modify


@click.group()
@click.version_option()
def cli():
    """delicious mexican pizza."""
    pass


@cli.command()
@click.argument(
    "name",
    metavar="PROJECT"
)
def create(name):
    """create annotation project."""
    quesadiya.commands.create.operator(project_name=name)


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
def delete(name):
    """delete project indicated by project name."""
    quesadiya.commands.delete.operator(project_name=project_name)


@cli.command()
@click.argument(
    "project_name",
    metavar="PROJECT"
)
def export(name):
    """export data associated with project indicated by project name."""
    quesadiya.commands.export.operator(project_name=project_name)
