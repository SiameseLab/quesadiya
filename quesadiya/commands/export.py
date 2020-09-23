import click
import click_spinner

from quesadiya.errors import NotJSONLFileError
from quesadiya.errors import ProjectRunningError
from quesadiya.errors import ProjectNotExistError
from quesadiya.errors import AuthenticationError

from quesadiya.db import factory
from quesadiya import utils
import quesadiya

import jsonlines
import os


def operator(project_name, output_path, include_text):
    if output_path[-6:] != ".jsonl":
        raise NotJSONLFileError("`OUTPUT_PATH`", output_path)
    admin_interface = factory.get_admindb_interface()
    if not admin_interface.check_project_exists(project_name):
        raise ProjectNotExistError(project_name)
    if admin_interface.is_project_running(project_name):
        raise ProjectRunningError(project_name, "`quesadiya export`")
    if not utils.admin_auth(admin_interface, project_name):
        raise AuthenticationError(project_name)
    # fetch triplets whose status is finished in a project
    click.echo("Exporting data...")
    with click_spinner.spinner():
        project_dir = os.path.join(quesadiya.get_projects_path(), project_name)
        projectdb_interface = factory.get_projectdb_interface(project_dir)
        triplets = []
        # if `include_text` is True, it includes text data in json object
        if include_text:
            rows = projectdb_interface.get_annotated_triplets_with_text()
            for row in rows:
                triplet = {
                    "anchor_sample_id": row.anchor_sample_id,
                    "positive_sample_id": row.positive_sample_id,
                    "negative_sample_id": row.negative_sample_id,
                    # split text into paragraps
                    "anchor_sample_text": utils.split_text_into_paragraphs(
                        row.anchor_sample_text
                    ),
                    "positive_sample_text": utils.split_text_into_paragraphs(
                        row.positive_sample_text
                    ),
                    "negative_sample_text": utils.split_text_into_paragraphs(
                        row.negative_sample_text
                    )
                }
                triplets.append(triplet)
        else:
            rows = projectdb_interface.get_annotated_triplets()
            for row in rows:
                triplet = {
                    "anchor_sample_id": row.anchor_sample_id,
                    "positive_sample_id": row.positive_sample_id,
                    "negative_sample_id": row.negative_sample_id
                }
                triplets.append(triplet)
        with jsonlines.open(output_path, mode="w") as jsonl:
            for t in triplets:
                jsonl.write(t)
    click.echo(
        "{} samples in project '{}' is exported "
        "to '{}'".format(len(triplets), project_name, output_path)
    )
