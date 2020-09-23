import pytest

from click.testing import CliRunner

from quesadiya.cli import create
from quesadiya.cli import delete

from quesadiya.errors import ProjectNotExistError
from quesadiya.errors import ProjectRunningError
from quesadiya.errors import AuthenticationError

from quesadiya.db import factory
from quesadiya.db.schema import Project, ProjectStatusEnum

import quesadiya as q
import os


class TestDelete:

    runner = CliRunner()

    def test_default_action(self):
        """Test the command deletes a project."""
        # create dummy project
        r = self.runner.invoke(create, ["test1", "me", "1234",
                                        "data/sample_triplets.jsonl"])
        assert r.exception is None
        # check the existence of project folder
        assert os.path.exists(os.path.join(q.get_projects_path(), "test1"))
        # check admin.db has the record
        admin_interface = factory.get_admindb_interface()
        assert admin_interface.check_project_exists("test1")
        # delete the project
        r = self.runner.invoke(delete, ["test1"], input="me\n1234\ny\n")
        assert r.exception is None
        # make sure it deletes project folder
        assert not os.path.exists(os.path.join(q.get_projects_path(), "test1"))
        # make sure record doesn't exist in admin.db
        assert not admin_interface.check_project_exists("test1")

    def test_bad_input(self):
        """Test exception handling for bad inputs."""
        r = self.runner.invoke(create, ["test1", "me", "1234",
                                        "data/sample_triplets.jsonl"])
        assert r.exception is None
        # incorrect project name
        r = self.runner.invoke(delete, ["lol"], input="me\n1234\ny\n")
        assert isinstance(r.exception, ProjectNotExistError)
        # incorrect password
        r = self.runner.invoke(delete, ["test1"], input="me\n333\ny\n")
        assert isinstance(r.exception, AuthenticationError)
        # incorrect username
        r = self.runner.invoke(delete, ["test1"], input="ny\n1234\ny\n")
        assert isinstance(r.exception, AuthenticationError)
        # make project status running
        admin_interface = factory.get_admindb_interface()
        with admin_interface.session_context_manager(expire_on_commit=True) as session:
            session.query(Project)\
                .filter(Project.project_name == "test1")\
                .update({"status": ProjectStatusEnum.running})
        # can't modify running project
        r = self.runner.invoke(delete, ["test1"], input="ny\n1234\ny\n")
        assert isinstance(r.exception, ProjectRunningError)
        # make project not running
        with admin_interface.session_context_manager(expire_on_commit=True) as session:
            session.query(Project)\
                .filter(Project.project_name == "test1")\
                .update({"status": ProjectStatusEnum.not_running})
        # this should go through
        r = self.runner.invoke(delete, ["test1"], input="me\n1234\ny\n")
        assert r.exception is None
