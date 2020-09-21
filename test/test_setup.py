import pytest

import os
import subprocess
import sqlite3

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Date,
    PrimaryKeyConstraint
)
from sqlalchemy.ext.declarative.api import DeclarativeMeta


class TestFileOps:
    """Test file operations in `setup.py`"""

    # ../quesadiya/test
    root_dir = os.path.dirname(os.path.abspath(__file__))

    def test_version_check(self):
        """Check the version of sqlite3."""
        # convert sqlite3 version info to tuples
        sqlite_version = tuple([int(x) for x in sqlite3.sqlite_version.split(".")])
        # make sure version info is correct
        # sqlite3 v-4. is not released yet (9/13/2020)
        assert sqlite_version > (2, 40)
        assert sqlite_version > (3, 3)
        assert sqlite_version < (4, 1)

    def test_mkdir(self):
        """Test mkdir to create `projects` folder under the root directory of
        this package.
        """
        # create a directory named projects
        dir_path = os.path.join(self.root_dir, "projects")
        assert not os.path.exists(dir_path)
        if not os.path.exists(dir_path):
            try:
                os.mkdir(dir_path)
            except PermissionError:
                raise PermissionError(
                    "permission is denied to create a project folder under {}. "
                    "make sure you have the right permission to create folder, or "
                    "try `pip install --user quesadiya` or "
                    "`python setup.py install --user`".format(base_dir)
                )
        # make sure the path exists
        assert os.path.exists(dir_path)
        # remove the directory
        os.rmdir(dir_path)


class TestSQLQuery:
    """Test sql queries in `setup.py`"""

    Base = declarative_base()

    class Projects(Base):
        """Table schema for `projects` table in `admin.db`."""
        __tablename__ = "projects"
        project_id = Column(Integer, index=True, primary_key=True)
        project_name = Column(String(30), nullable=False)
        owner_name = Column(String(30), nullable=False)
        owner_password = Column(String(30), nullable=False)
        date_created = Column(Date(), nullable=False)


    class Collaborators(Base):
        """Table schema for `collaborators` table in `admin.db`."""
        __tablename__ = "collaborators"
        # set foregin key to projects table
        project_id =  Column(
            Integer, ForeignKey("projects.project_id"), nullable=False
        )
        collaborator_name = Column(String(30), nullable=False)
        collaborator_password = Column(String(30), nullable=False)
        # set project_id and collaborator_name primary key
        __table_args__ = (
            PrimaryKeyConstraint('project_id', 'collaborator_name'),
            {}
        )

    # ../quesadiya/test
    root_dir = os.path.dirname(os.path.abspath(__file__))

    def test_create_db_in_root(self):
        """Create db file under the root directory of this package."""
        # make sure db file exists
        db_uri = 'sqlite:///' + os.path.join(self.root_dir, "test.db")
        engine = create_engine(db_uri, echo=True, encoding="utf-8")
        self.Base.metadata.create_all(engine)
        assert os.path.exists(os.path.join(self.root_dir, "test.db"))
        os.remove(os.path.join(self.root_dir, "test.db"))

    def test_create_table(self):
        """Create table in test database file."""
        # query to create projects table
        db_uri = 'sqlite:///' + os.path.join(self.root_dir, "test.db")
        engine = create_engine(db_uri, echo=True, encoding="utf-8")
        self.Base.metadata.create_all(engine)
        # get all tables in test.db and make sure names are correct
        engine = create_engine(db_uri, echo=True, encoding="utf-8")
        # print(engine.table_names())
        count = 0
        expected = set(['projects', 'collaborators'])
        assert set(engine.table_names()) == expected
        os.remove(os.path.join(self.root_dir, "test.db"))


class TestImport:

    # ../quesadiya
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def test_import(self):
        """Test loading module from file path."""
        import importlib.util
        schema_path = os.path.join(self.root_dir, "quesadiya", "db", "schema.py")
        spec = importlib.util.spec_from_file_location('queso', schema_path)
        queso = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(queso)
        # make sure module path is correct
        assert queso.__file__ == schema_path
        # make sure datatypes are correct
        assert isinstance(queso.AdminDB.Base, DeclarativeMeta)
        assert isinstance(queso.Project, DeclarativeMeta)
        assert isinstance(queso.Collaborator, DeclarativeMeta)



class TestInstall:
    """Test setup.py by calling it from subprocess.

    CAUTION: this class uninstalls quesadiya package when it runs.
    """

    # ../quesadiya
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def test_install(self):
        """Run `python setup.py install` to make sure it initializes files
        in the correct locations.
        """
        # run setup.py
        subprocess.call("pip install {} --no-cache-dir".format(
            self.root_dir), shell=True)
        # check existence of `projects` folder
        import quesadiya
        assert os.path.exists(
            os.path.join(quesadiya.get_base_path(), 'projects')
        )
        # check existince of `admin.db`
        db_path = os.path.join(quesadiya.get_base_path(), 'projects', 'admin.db')
        assert os.path.exists(db_path)
        # make sure db file contains correct tables
        expected = set(['projects', 'collaborators'])
        engine = create_engine('sqlite:///' + db_path, echo=True, encoding="utf-8")
        assert set(engine.table_names()) == expected
        # make sure setup.py installs django apis (non python modules)
        non_python_dirs = \
            ['apps', 'root', 'Sample data', 'static', 'templates', 'tool']
        queso_dirs = \
            os.listdir(os.path.join(quesadiya.get_base_path(), 'django_tool'))
        for x in non_python_dirs:
            assert x in queso_dirs
        subprocess.call("pip uninstall quesadiya", shell=True)
