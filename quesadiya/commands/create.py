import click
import click_spinner

from quesadiya.errors import NotJSONLFileError
from quesadiya.errors import ProjectExistsError

from quesadiya.db.schema import TripletStatusEnum
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
    admin_contact
):
    if input_data_path[-6:] != ".jsonl":
        raise NotJSONLFileError("`DATAPATH`", input_data_path)
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
    triplets, candidates, sample_text = _load_format_input(input_data_path)
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
    # insert bulk data into database
    click.echo("Finish creating {}".format(project_name))


def _load_format_input(input_data_path):
    candidates, triplets = [], []
    sample_text_lookup = defaultdict()
    with jsonlines.open(input_data_path, mode="r") as jsonl_reader:
        for row in tqdm(jsonl_reader, desc="Loading input data", unit=" row"):
            # create row for triplet_dataset
            triplet = {
                "anchor_sample_id": row["anchor_sample_id"],
                "candidate_group_id": row["candidate_group_id"],
                "status": TripletStatusEnum.unfinished,
                "time_changed": utils.get_now(),
                "positive_sample_id": -1,
                "negative_sample_id": -1
            }
            triplets.append(triplet)
            # insert id-metadata pair into lookup table
            sample_text_lookup[row["anchor_sample_id"]] = \
                {
                    "text": PARAGRAPH_DELIM.join(row["anchor_sample_text"]),
                    "title": row["anchor_sample_title"]
                }
            # create row for articles and add id-text pairs
            for cand in row["candidates"]:
                candidates.append({
                    "candidate_group_id": row["candidate_group_id"],
                    "candidate_sample_id": cand["candidate_sample_id"]
                })
                # insert id-metadata pair into lookup table
                sample_text_lookup[cand["candidate_sample_id"]] = \
                    {
                        "text": utils.concat_paragraphs(
                            cand["candidate_sample_text"]
                        ),
                        "title": cand["candidate_sample_title"]
                    }
    # convert lookup table into list of dicts (json objects)
    sample_text = [
        {
            "sample_id": id,
            "sample_body": metadata["text"],
            "sample_title": metadata["title"]
        } for id, metadata in sample_text_lookup.items()
    ]
    return triplets, candidates, sample_text
