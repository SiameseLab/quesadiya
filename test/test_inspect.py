import pytest

from click.testing import CliRunner

from quesadiya.cli import create
from quesadiya.cli import delete
from quesadiya.cli import inspect

from quesadiya.errors import QuesadiyaCommandError
from quesadiya.errors import ProjectNotExistError
from quesadiya.errors import AuthenticationError

from prettytable import PrettyTable
from datetime import date


class TestInspect:

    runner = CliRunner()

    def test_default_action(self):
        """Test the command shows project info."""
        # create a dummy project
        r = self.runner.invoke(create,
                                ["test1", "me", "data/sample_triplets.jsonl"],
                                input="1234\n1234\n")
        assert r.exception is None
        # get default info
        r = self.runner.invoke(inspect, ["test1"])
        assert r.exception is None
        # check the output
        expected = PrettyTable(field_names=["Project Name", "Admin Contact",
                                            "Description", "Date Created",
                                            "Status"])
        expected.add_row([
            "test1", "No contact", "No description",
            date.today(), "not_running"
        ])
        assert str(expected) + '\n' == r.output
        # clean dummy project
        r = self.runner.invoke(delete, ["test1"], input="me\n1234\ny\n")
        assert r.exception is None
        # test project description and admin contact
        r = self.runner.invoke(create,
                                ["test2", "me",
                                 "data/sample_triplets.jsonl",
                                 "-d", "this is a test",
                                 "-c", "awesome@legendary.com"],
                                 input="1234\n1234\n")
        assert r.exception is None
        expected = PrettyTable(field_names=["Project Name", "Admin Contact",
                                            "Description", "Date Created",
                                            "Status"])
        expected.add_row([
            "test2", "awesome@legendary.com", "this is a test",
            date.today(), "not_running"
        ])
        r = self.runner.invoke(inspect, ["test2"])
        assert r.exception is None
        assert str(expected) + '\n' == r.output
        # clean dummy project
        r = self.runner.invoke(delete, ["test2"], input="me\n1234\ny\n")
        assert r.exception is None

    def test_collaborators_info(self):
        """Test output of collaboratos."""
        # create dummy project with dummy collaborators
        r = self.runner.invoke(create,
                                ["test1", "me",
                                 "data/sample_triplets.jsonl",
                                 "-a", "data/sample_collaborators1.jsonl"],
                                 input="1234\n1234\n")
        assert r.exception is None
        # this command should show collaborator info
        r = self.runner.invoke(inspect, ["test1", "-s"], input="me\n1234\ny\n")
        assert r.exception is None
        # project deafult info
        expected1 = PrettyTable(field_names=["Project Name", "Admin Contact",
                                             "Description", "Date Created",
                                             "Status"])
        expected1.add_row([
            "test1", "No contact", "No description",
            date.today(), "not_running"
        ])
        # collaborator info
        expected2 = PrettyTable(field_names=["Collaborator Name",
                                             "Password", "Contact"])
        expected2.add_row(["a", "1", "a@1"])
        expected2.add_row(["b", "2", "b@2"])
        expected2.add_row(["c", "3", "c@3"])
        expected = str(expected1) + '\n' + str(expected2) + '\n'
        # fomrat r.output bc it somehow returns Admin ...\nPassword\n<table>
        assert expected == '\n'.join(r.output.split('\n')[2:])
        r = self.runner.invoke(delete, ["test1"], input="me\n1234\ny\n")
        assert r.exception is None

    def test_bad_input(self):
        """Test exception handling for bad inputs."""
        # create a dummy project
        r = self.runner.invoke(create,
                                ["test1", "me", "data/sample_triplets.jsonl"],
                                input="1234\n1234\n")
        assert r.exception is None
        # --show-collaborators is not supported for `all`
        r = self.runner.invoke(inspect, ["all", "-s"])
        assert isinstance(r.exception, QuesadiyaCommandError)
        # incorrect project name
        r = self.runner.invoke(inspect, ["lol"])
        assert isinstance(r.exception, ProjectNotExistError)
        # incorrect password
        r = self.runner.invoke(inspect, ["test1", "-s"], input="me\n333\n")
        assert isinstance(r.exception, AuthenticationError)
        # incorrect username
        r = self.runner.invoke(inspect, ["test1", "-s"], input="ny\n1234\n")
        assert isinstance(r.exception, AuthenticationError)
        # this should go through
        r = self.runner.invoke(inspect, ["test1", "-s"], input="me\n1234\n")
        assert r.exception is None
        # clean dummy project
        r = self.runner.invoke(delete, ["test1"], input="me\n1234\ny\n")
        assert r.exception is None
