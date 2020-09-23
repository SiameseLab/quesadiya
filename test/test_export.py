import pytest

from click.testing import CliRunner

from quesadiya.cli import create
from quesadiya.cli import delete
from quesadiya.cli import export

from quesadiya.errors import ProjectNotExistError
from quesadiya.errors import ProjectRunningError
from quesadiya.errors import AuthenticationError
from quesadiya.errors import NotJSONLFileError

from quesadiya.db.schema import TripletDataset, TripletStatusEnum
from quesadiya.db.schema import Project, ProjectStatusEnum
from quesadiya.db import factory

import quesadiya as q
import os
import jsonlines


class TestExport:

    runner = CliRunner()
    dummy_positive_sample = "5ed93d5fd98c5b4207f0b64e"
    dummy_negative_sample = "5ed92a18d98c5b4207effb48"
    this_dir = os.path.dirname(__file__)

    def test_default_action(self):
        """Test command exports output file w/ or w/o text."""
        # create a dummy project
        r = self.runner.invoke(create, ["test1", "me", "1234",
                                        "data/sample_triplets.jsonl"])
        assert r.exception is None
        # insert dummy samples and set status finished for testing export
        project_dir = os.path.join(q.get_projects_path(), "test1")
        projectdb_interface = factory.get_projectdb_interface(project_dir)
        with projectdb_interface.session_context_manager(expire_on_commit=True) as session:
            session.query(TripletDataset)\
                .update({"status": TripletStatusEnum.finished})
            session.query(TripletDataset)\
                .update({"positive_sample_id": self.dummy_positive_sample})
            session.query(TripletDataset)\
                .update({"negative_sample_id": self.dummy_negative_sample})
        # export data
        output_path = os.path.join(self.this_dir, "output.jsonl")
        assert not os.path.exists(output_path)
        r = self.runner.invoke(export, ["test1", output_path], input="me\n1234\ny\n")
        assert r.exception is None
        assert os.path.exists(output_path)
        # import output and check its data
        expected_file_path = os.path.join(self.this_dir, "expected_output.jsonl")
        expected = [x for x in jsonlines.open(expected_file_path)]
        output = [x for x in jsonlines.open(output_path)]
        for x, y in zip(expected, output):
            assert x == y
        # remove output file
        os.remove(output_path)
        output_with_text_path = os.path.join(self.this_dir, "output_with_text.jsonl")
        assert not os.path.exists(output_with_text_path)
        # export project with text
        r = self.runner.invoke(export, ["test1", output_with_text_path, "-i"],
                               input="me\n1234\ny\n")
        assert r.exception is None
        assert os.path.exists(output_with_text_path)
        # import output and check its data
        expected_file_path = os.path.join(self.this_dir, "expected_output_with_text.jsonl")
        expected_with_text = [x for x in jsonlines.open(expected_file_path)]
        output_with_text = [x for x in jsonlines.open(output_with_text_path)]
        for x, y in zip(expected_with_text, output_with_text):
            assert x == y
        # remove file and delete project
        os.remove(output_with_text_path)
        r = self.runner.invoke(delete, ["test1"], input="me\n1234\ny\n")
        assert r.exception is None

    def test_bad_input(self):
        """Test exception handling for bad inputs."""
        # create a dummy project
        r = self.runner.invoke(create, ["test1", "me", "1234",
                                        "data/sample_triplets.jsonl"])
        assert r.exception is None
        # output_path must be jsonl
        r = self.runner.invoke(export, ["test1", "output.j"])
        assert isinstance(r.exception, NotJSONLFileError)
        # incorrect project name
        r = self.runner.invoke(export, ["lol", "output.jsonl"])
        assert isinstance(r.exception, ProjectNotExistError)
        # incorrect password
        r = self.runner.invoke(export, ["test1", "out.jsonl"], input="me\n333\ny\n")
        assert isinstance(r.exception, AuthenticationError)
        # incorrect username
        r = self.runner.invoke(export, ["test1", "out.jsonl"], input="ny\n1234\ny\n")
        assert isinstance(r.exception, AuthenticationError)
        # make project status running
        admin_interface = factory.get_admindb_interface()
        with admin_interface.session_context_manager(expire_on_commit=True) as session:
            session.query(Project)\
                .filter(Project.project_name == "test1")\
                .update({"status": ProjectStatusEnum.running})
        # can't modify running project
        r = self.runner.invoke(export, ["test1", "out.jsonl"], input="ny\n1234\ny\n")
        assert isinstance(r.exception, ProjectRunningError)
        # make project not running
        with admin_interface.session_context_manager(expire_on_commit=True) as session:
            session.query(Project)\
                .filter(Project.project_name == "test1")\
                .update({"status": ProjectStatusEnum.not_running})
        # this should go through
        r = self.runner.invoke(export, ["test1", "output.jsonl"], input="me\n1234\ny\n")
        assert r.exception is None
        # remove file and delete project
        os.remove("output.jsonl")
        r = self.runner.invoke(delete, ["test1"], input="me\n1234\ny\n")
        assert r.exception is None
