import pytest

from click.testing import CliRunner

from quesadiya.cli import create
from quesadiya.cli import delete

from quesadiya.errors import NotJSONLFileError
from quesadiya.errors import ProjectExistsError
from quesadiya.errors import QuesadiyaCommandError

import quesadiya as q
import os


class TestCreate:

    runner = CliRunner()

    def test_default_action(self):
        """Test the command create a project."""
        r = self.runner.invoke(create, ["test1", "me", "1234",
                                        "data/sample_triplets.jsonl"])
        assert r.exception is None
        # check the existence of project folder
        assert os.path.exists(os.path.join(q.get_projects_path(), "test1"))
        # check the existence of db file
        assert os.path.exists(os.path.join(q.get_projects_path(), "test1", "project.db"))
        # clean dummy project
        r = self.runner.invoke(delete, ["test1"], input="me\n1234\ny\n")
        assert r.exception is None

    def test_bad_input(self):
        """create command only accepts jsonl file."""
        # the following should raise an error
        r = self.runner.invoke(create, ["test1", "me",
                                        "1234", "data/sample_triplets.j"])
        assert isinstance(r.exception, NotJSONLFileError)
        # the following should pass
        r = self.runner.invoke(create, ["test1", "me", "1234",
                                        "data/sample_triplets.jsonl"])
        assert r.exception is None
        # the following should raise an error
        r = self.runner.invoke(create, ["test2", "me", "1234",
                                        "data/sample_triplets.jsonl",
                                        "-a", "data/sample_collaborators1.j"])
        assert isinstance(r.exception, NotJSONLFileError)
        # the following should pass
        r = self.runner.invoke(create, ["test2", "me", "1234",
                                        "data/sample_triplets.jsonl",
                                        "-a", "data/sample_collaborators1.jsonl"])
        assert r.exception is None
        # `all` is reserved for internal use
        r = self.runner.invoke(create, ["all", "me", "1234",
                                        "data/sample_triplets.jsonl"])
        assert isinstance(r.exception, QuesadiyaCommandError)
        # clean dummy projects
        r = self.runner.invoke(delete, ["test1"], input="me\n1234\ny\n")
        assert r.exception is None
        r = self.runner.invoke(delete, ["test2"], input="me\n1234\ny\n")
        assert r.exception is None

    def test_project_exists(self):
        """Quesadiya should reject create if project already exists."""
        # create a dummy project
        r = self.runner.invoke(create, ["test1", "me", "1234",
                                        "data/sample_triplets.jsonl"])
        assert r.exception is None
        # this shouldn't go trough
        r = self.runner.invoke(create, ["test1", "me", "1234",
                                        "data/sample_triplets.jsonl"])
        assert isinstance(r.exception, ProjectExistsError)
        # clean dummy projects
        r = self.runner.invoke(delete, ["test1"], input="me\n1234\ny\n")
        assert r.exception is None

    # TODO: add code to test data in admin.db and project.db
