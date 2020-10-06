import pytest

from click.testing import CliRunner

from quesadiya.cli import create
from quesadiya.cli import delete
from quesadiya.cli import modify
from quesadiya.cli import inspect

from quesadiya.errors import ProjectNotExistError
from quesadiya.errors import ProjectRunningError
from quesadiya.errors import AuthenticationError
from quesadiya.errors import NotJSONLFileError

from quesadiya.db.schema import Project, ProjectStatusEnum
from quesadiya.db import factory

import quesadiya as q
import os
import jsonlines

from prettytable import PrettyTable
from datetime import date


# TODO: add test for invalid file path
class TestModify:

    runner = CliRunner()

    def test_edit(self):
        """Test edit command in modify command."""
        # create a dummy project
        r = self.runner.invoke(create,
                                ["test1", "me",
                                "data/sample_triplets.jsonl",
                                "-c", "awesome@legendary.com",
                                "-d", "this is a test"],
                                input="1234\n1234\n")
        assert r.exception is None
        # edit description
        r = self.runner.invoke(
            modify, ["test1", "-e", "description"],
            input="me\n1234\nlegen ..wait for it... daryy!\n"
        )
        assert r.exception is None
        # get current description in admin.db
        admin_interface = factory.get_admindb_interface()
        with admin_interface.session_context_manager(expire_on_commit=False) as session:
            resp = session.query(Project)\
                        .filter(Project.project_name == "test1")\
                        .first()
        assert resp.project_description == "legen ..wait for it... daryy!"
        # edit contact
        r = self.runner.invoke(
            modify, ["test1", "-e", "contact"],
            input="me\n1234\nducky@tie.com\n"
        )
        assert r.exception is None
        # get current contact in admin.db
        admin_interface = factory.get_admindb_interface()
        with admin_interface.session_context_manager(expire_on_commit=False) as session:
            resp = session.query(Project)\
                        .filter(Project.project_name == "test1")\
                        .first()
        assert resp.admin_contact == "ducky@tie.com"
        r = self.runner.invoke(delete, ["test1"], input="me\n1234\ny\n")
        assert r.exception is None

    def test_transfer_ownership(self):
        """Test --transfer-ownership option."""
        r = self.runner.invoke(create,
                                ["test1", "me", "data/sample_triplets.jsonl"],
                                input="1234\n1234\n")
        assert r.exception is None
        # transfer ownership
        r = self.runner.invoke(
            modify, ["test1", "-t"],
            input="me\n1234\nnew_admin\n5678\n5678\nme/test1\n"
        )
        assert r.exception is None
        # delete the dummy project with new admin auth
        r = self.runner.invoke(delete, ["test1"], input="new_admin\n5678\ny\n")
        assert r.exception is None

    def test_add_collaborators(self):
        """Test --add-collaborators option."""
        # create dummy project with empty collaborators
        r = self.runner.invoke(create,
                                ["test1", "me", "data/sample_triplets.jsonl"],
                                input="1234\n1234\n")
        assert r.exception is None
        # add collaborators
        r = self.runner.invoke(
            modify, ["test1", "-a", "data/sample_collaborators1.jsonl"],
            input="me\n1234\n"
        )
        assert r.exception is None
        # test input with inspect command
        # project deafult info
        expected1 = PrettyTable(field_names=["Project Name", "Admin Contact",
                                             "Description", "Date Created",
                                             "Status"])
        expected1.add_row([
            "test1", "No contact", "No description",
            date.today(), "not_running"
        ])
        # collaborator info
        expected2 = PrettyTable(field_names=["Collaborator Name", "Contact"])
        expected2.add_row(["a", "a@1"])
        expected2.add_row(["b", "b@2"])
        expected2.add_row(["c", "c@3"])
        expected = str(expected1) + '\n' + str(expected2) + '\n'
        r = self.runner.invoke(inspect, ["test1", "-s"], input="me\n1234\n")
        assert r.exception is None
        assert expected == '\n'.join(r.output.split('\n')[2:])
        # add more collabortors
        # this should throw warnings for duplicate data (there is supposed to be one duplicate)
        with pytest.warns(RuntimeWarning):
            r = self.runner.invoke(
                modify, ["test1", "-a", "data/sample_collaborators2.jsonl"],
                input="me\n1234\n"
            )
        assert r.exception is None
        # test input with inspect command
        expected2.add_row(["d", "d@4"])
        expected2.add_row(["e", "e@5"])
        new_expected = str(expected1) + '\n' + str(expected2) + '\n'
        r = self.runner.invoke(inspect, ["test1", "-s"], input="me\n1234\n")
        assert r.exception is None
        assert new_expected == '\n'.join(r.output.split('\n')[2:])
        # delete dummy project
        r = self.runner.invoke(delete, ["test1"], input="me\n1234\ny\n")
        assert r.exception is None

    def test_bad_input(self):
        """Test exception handling for bad inputs."""
        # create a dummy project
        r = self.runner.invoke(create,
                                ["test1", "me", "data/sample_triplets.jsonl"],
                                input="1234\n1234\n")
        assert r.exception is None
        # incorrect project name
        r = self.runner.invoke(modify, ["lol"])
        assert isinstance(r.exception, ProjectNotExistError)
        # incorrect password
        r = self.runner.invoke(
            modify, ["test1", "-e", "contact"],
            input="me\n333\n"
        )
        assert isinstance(r.exception, AuthenticationError)
        # incorrect username
        r = self.runner.invoke(
            modify, ["test1", "-e", "contact"],
            input="ny\n1234\n"
        )
        assert isinstance(r.exception, AuthenticationError)
        # make project status running
        admin_interface = factory.get_admindb_interface()
        with admin_interface.session_context_manager(expire_on_commit=True) as session:
            session.query(Project)\
                .filter(Project.project_name == "test1")\
                .update({"status": ProjectStatusEnum.running})
        # can't modify running project
        r = self.runner.invoke(
            modify, ["test1", "-e", "contact"],
            input="ny\n1234\n"
        )
        assert isinstance(r.exception, ProjectRunningError)
        # make project not running
        with admin_interface.session_context_manager(expire_on_commit=True) as session:
            session.query(Project)\
                .filter(Project.project_name == "test1")\
                .update({"status": ProjectStatusEnum.not_running})
        # this should go through
        r = self.runner.invoke(
            modify, ["test1", "-e", "contact"],
            input="me\n1234\nducky@tie.com\n"
        )
        assert r.exception is None
        # collaborator path must be valid file name and jsonl file
        r = self.runner.invoke(
            modify, ["test1", "-a", "data/bluh.jsonl"],
            input="me\n1234\n"
        )
        assert isinstance(r.exception, FileNotFoundError)
        r = self.runner.invoke(
            modify, ["test1", "-a", "data/sample_collaborators2.js"],
            input="me\n1234\n"
        )
        assert isinstance(r.exception, NotJSONLFileError)
        # this should go thorugh
        r = self.runner.invoke(
            modify, ["test1", "-a", "data/sample_collaborators2.jsonl"],
            input="me\n1234\n"
        )
        assert r.exception is None
        # clean dummy project
        r = self.runner.invoke(delete, ["test1"], input="me\n1234\ny\n")
        assert r.exception is None
