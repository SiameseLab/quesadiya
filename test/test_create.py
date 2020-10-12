import pytest

from click.testing import CliRunner

from quesadiya.cli import create
from quesadiya.cli import delete

from quesadiya.errors import NotJSONLFileError
from quesadiya.errors import ProjectExistsError
from quesadiya.errors import QuesadiyaCommandError

from quesadiya.db import factory
import quesadiya as q
import os


class TestCreate:

    runner = CliRunner()

    def test_default_action(self):
        """Test the command creates a project."""
        r = self.runner.invoke(create,
                               ["test1", "me", "data/sample_triplets.jsonl"],
                               input='1234\n1234\n')
        assert r.exception is None
        # check the existence of project folder
        assert os.path.exists(os.path.join(q.get_projects_path(), "test1"))
        # check the existence of db file
        assert os.path.exists(os.path.join(q.get_projects_path(), "test1", "project.db"))
        # make sure project info is in admin.db
        admin_interface = factory.get_admindb_interface()
        assert admin_interface.check_project_exists("test1")
        # clean dummy project
        r = self.runner.invoke(delete, ["test1"], input="me\n1234\ny\n")
        assert r.exception is None

    def test_bad_input(self):
        """Test exception handling for bad inputs."""
        # data file must be jsonl
        r = self.runner.invoke(create,
                               ["test1", "me", "data/sample_triplets.j"],
                               input="1234\n1234\n")
        assert isinstance(r.exception, NotJSONLFileError)
        # the following should pass
        r = self.runner.invoke(create,
                               ["test1", "me", "data/sample_triplets.jsonl"],
                               input="1234\n1234\n")
        assert r.exception is None
        # collaborator input must be jsonl
        r = self.runner.invoke(create,
                              ["test2", "me", "data/sample_triplets.jsonl",
                               "-a", "data/sample_collaborators1.j"],
                               input="1234\n1234\n")
        assert isinstance(r.exception, NotJSONLFileError)
        # if a data file doesn't follow quesadiya format, it should give KeyError
        r = self.runner.invoke(create,
                              ["test2", "me", "data/sample_collaborators1.jsonl"],
                               input="1234\n1234\n")
        assert isinstance(r.exception, KeyError)
        # the following should pass
        r = self.runner.invoke(create,
                              ["test2", "me", "data/sample_triplets.jsonl",
                               "-a", "data/sample_collaborators1.jsonl"],
                               input="1234\n1234\n")
        assert r.exception is None
        # if input file doesn't exist, it doesn't create project folder and
        # row in admin.db
        r = self.runner.invoke(create,
                                ["test3", "me", "data/bluh.jsonl",],
                                input="1234\n1234\n")
        assert isinstance(r.exception, FileNotFoundError)
        assert not os.path.exists(os.path.join(q.get_projects_path(), "test3"))
        # `all` is reserved for internal use
        r = self.runner.invoke(create,
                                ["all", "me", "data/sample_triplets.jsonl"],
                                input="1234\n1234\n")
        assert isinstance(r.exception, QuesadiyaCommandError)
        # `admin` is reserved for internal use
        r = self.runner.invoke(create,
                                ["admin", "me", "data/sample_triplets.jsonl"],
                                input="1234\n1234\n")
        assert isinstance(r.exception, QuesadiyaCommandError)
        # clean dummy projects
        r = self.runner.invoke(delete, ["test1"], input="me\n1234\ny\n")
        assert r.exception is None
        r = self.runner.invoke(delete, ["test2"], input="me\n1234\ny\n")
        assert r.exception is None

    def test_project_exists(self):
        """Quesadiya should reject create if project already exists."""
        # create a dummy project
        r = self.runner.invoke(create,
                                ["test1", "me", "data/sample_triplets.jsonl"],
                                input="1234\n1234\n")
        assert r.exception is None
        # this shouldn't go trough
        r = self.runner.invoke(create,
                                ["test1", "me", "data/sample_triplets.jsonl"],
                                input="1234\n1234\n")
        assert isinstance(r.exception, ProjectExistsError)
        # clean dummy projects
        r = self.runner.invoke(delete, ["test1"], input="me\n1234\ny\n")
        assert r.exception is None

    # TODO: add code to test data (collaborator, project metadata) in admin.db, project.db and django.db
