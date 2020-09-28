import click

from quesadiya.db.schema import TripletStatusEnum
from quesadiya.db import factory
import quesadiya

from datetime import datetime
from tqdm import tqdm
from collections import defaultdict

import os
import jsonlines


PARAGRAPH_DELIM = ' <end_of_paragraph> '


def get_now():
    return datetime.now()


def print_time(start_time, operation):
    delta = get_now() - start_time
    click.echo("{} took {}m {}s".format(
        operation, delta.seconds//60, delta.seconds%60
    ))


def check_file_path(path):
    if not os.path.exists(path):
        raise FileNotFoundError("No such file or directory: {}".format(path))


def concat_paragraphs(paragraps):
    """Convert list of strings into one big string by concatenating each string
    by `PARAGRAPH_DELIM`.

    Parameters
    ----------
    paragraps : list of str
        A list of string

    Returns
    -------
    str
        A string where each string in `paragraps` is concatenated by
        PARAGRAPH_DELIM.
    """
    return PARAGRAPH_DELIM.join(paragraps)


def split_text_into_paragraphs(text):
    """Split text into paragraphs by `PARAGRAPH_DELIM`.

    Parameters
    ----------
    text : str
        A string to split into paragraphs.

    Returns
    -------
    list of str
        A list of paragraphs where each paragraph is a string.
    """
    return text.split(PARAGRAPH_DELIM)


def ask_admin_info():
    admin_name = click.prompt("Admin name", type=click.STRING)
    admin_password = click.prompt("Password", hide_input=True, type=click.STRING)
    return admin_name, admin_password


def admin_auth(project_name):
    project_dir = os.path.join(quesadiya.get_projects_path(), project_name)
    db_interface = factory.get_projectdb_interface(project_dir)
    admin_name, admin_password = ask_admin_info()
    auth = db_interface.admin_authentication(
        admin_name=admin_name,
        admin_password=admin_password
    )
    return auth


def load_format_collaborators(input_path):
    """Load collabortors from input file and format them to be added to
    `collabortos` table in `admin.db`.

    Parameters
    ----------
    input_path : str
        Input path to jsonl file that contains collabortos. Each row must follow
        the following format:
        {
            'name': str,
            'password': str,
            'contact': str
        }

    Returns
    -------
    collabortos : list of dict
        A list of collaborators in the json format.
    """
    collaborators = []
    with jsonlines.open(input_path, mode="r") as jsonl:
        for row in jsonl:
            collaborator = {
                "name": row["name"],
                "password": row["password"],
                "contact": row["contact"]
            }
            collaborators.append(collaborator)
    return collaborators


def load_format_dataset(input_path):
    """Load triplets from input file and format them to be added to
    `triplet_dataset` table in `project.db`.

    Parameters
    ----------
    project_id : str
        The id of a project which collabortos are affilicated with.
    input_path : str
        Input path to jsonl file that contains collabortos. Each row must follow
        the following format:
        {
            "anchor_sample_id": str,
            "anchor_sample_text": list of str,
            "anchor_sample_title": str,
            "candidate_group_id": str,
            "candidates": [
                cand = {
                    "candidate_sample_id": str,
                    "candidate_sample_text": list of str,
                    "candidate_sample_title": str
                }
            ]
        }

    Returns
    -------
    (triplets, candidates,  sample_text): (list of dict)*3
        A list of triplets, candidate groups, and sample texts in the json
        format. Please refer to `quesadiya.db.schema.py` for the fields of each
        json objects.
    """
    candidates, triplets = [], []
    sample_text_lookup = defaultdict()
    with jsonlines.open(input_path, mode="r") as jsonl_reader:
        for row in tqdm(jsonl_reader, desc="Loading input data", unit=" row"):
            # create row for triplet_dataset
            triplet = {
                "anchor_sample_id": row["anchor_sample_id"],
                "candidate_group_id": row["candidate_group_id"],
                "status": TripletStatusEnum.unfinished,
                "time_changed": get_now(),
                "positive_sample_id": -1,
                "negative_sample_id": -1
            }
            triplets.append(triplet)
            # insert id-metadata pair into lookup table
            sample_text_lookup[row["anchor_sample_id"]] = \
                {
                    "text": concat_paragraphs(row["anchor_sample_text"]),
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
                        "text": concat_paragraphs(cand["candidate_sample_text"]),
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
