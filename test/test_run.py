import pytest

from click.testing import CliRunner

from quesadiya.cli import run

import multiprocessing as mp


runner = CliRunner()


def run_project():
    print('start running')
    r = runner.invoke(run)
    print('finished running')
    assert r.exception is None


def run_project_on_4000():
    print('start running')
    r = runner.invoke(run, ['-p', '4000'])
    print('finished running')
    assert r.exception is None


class TestRun:
    """
    [Source]
    https://stackoverflow.com/questions/14920384/stop-code-after-time-period
    """

    def test_default_port(self):
        """Test the command to run a project."""
        p = mp.Process(target=run_project)
        p.start()
        p.join(3)
        if p.is_alive():
            p.terminate()
            p.join()

    def test_port_option(self):
        """Run quesdiya at different port."""
        p = mp.Process(target=run_project_on_4000)
        p.start()
        p.join(3)
        if p.is_alive():
            p.terminate()
            p.join()
