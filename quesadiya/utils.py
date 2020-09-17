import click

from quesadiya.db.schema import DataStatusEnum
from quesadiya.db.schema import PARAGRAPH_DELIM

from datetime import datetime
from tqdm import tqdm
from collections import defaultdict

import jsonlines
import sys


def get_now():
    return datetime.now()


def print_time(start_time, operation):
    delta = get_now() - start_time
    click.echo('{} took {}.{} seconds'.format(
        operation, delta.seconds, delte.microseconds
    ))


def format_input(input_data_path):
    candidates, triplets = [], []
    sample_text_lookup = defaultdict()
    with jsonlines.open(input_data_path, mode="r") as jsonl_reader:
        for row in tqdm(jsonl_reader, desc="Loading input data", unit=" row"):
            # create row for triplet_dataset
            triplet = {
                "anchor_sample_id": row["anchor_sample_id"],
                "candidate_group_id": row["candidate_group_id"],
                "status": DataStatusEnum.unfinished,
                "time_changed": get_now(),
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
                        "text": PARAGRAPH_DELIM.join(
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


def ask_admin_info():
    admin_name = click.prompt("Type admin name")
    admin_password = click.prompt("Type password", hide_input=True)
    return admin_name, admin_password


def admin_auth(db_interface, project_name):
    admin_name, admin_password = ask_admin_info()
    auth = db_interface.admin_authentication(
        project_name=project_name,
        admin_name=admin_name,
        admin_password=admin_password
    )
    return auth
