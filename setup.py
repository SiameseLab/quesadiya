from __future__ import print_function

import os
import sys
import glob
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

from setuptools import setup, find_packages


# sqlalchemy base for table
Base = declarative_base()
MAX_PROJECT_NAME_CHAR = 30
MAX_USER_NAME_CHAR = 30
MAX_PASSWORD_CHAR = 30


# table schemas for admin.db
class Projects(Base):
    """Table schema for `projects` table in `admin.db`."""
    __tablename__ = "projects"
    project_id = Column(Integer, index=True, primary_key=True)
    project_name = Column(String(MAX_PROJECT_NAME_CHAR), nullable=False)
    owner_name = Column(String(MAX_USER_NAME_CHAR), nullable=False)
    owner_password = Column(String(MAX_PASSWORD_CHAR), nullable=False)
    date_created = Column(Date(), nullable=False)


class Collaborators(Base):
    """Table schema for `collaborators` table in `admin.db`."""
    __tablename__ = "collaborators"
    # set foregin key to projects table
    project_id =  Column(
        Integer, ForeignKey("projects.project_id"), nullable=False
    )
    collaborator_name = Column(String(MAX_USER_NAME_CHAR), nullable=False)
    collaborator_password = Column(String(MAX_PASSWORD_CHAR), nullable=False)
    # set project_id and collaborator_name primary key
    __table_args__ = (
        PrimaryKeyConstraint('project_id', 'collaborator_name'),
        {}
    )


def get_include_files(directory):
    dir_root = os.path.join(directory, "**/*")
    files = glob.iglob(dir_root, recursive=True)
    return [os.path.join("..", path) for path in files]


__version__ = "0.1"


with open(os.path.join(os.path.dirname(__file__), "README.md"), "r") as f:
    long_description = f.read()


# check sqlite version
sqlite_version = tuple([int(x) for x in sqlite3.sqlite_version.split(".")])
if sqlite_version < (3, 3):
    sys.exit(
        "sqlite >= 3.3 is required for quesadiya (but got sqlite={}), "
        "please upgrade sqlite and "
        "try installing again.".format(sqlite3.sqlite_version)
    )
# base path for initializing folder and database file
# ../quesadiya/quesadiya
base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'quesadiya')
# get all non python files to include
api_files = get_include_files(os.path.join('quesadiya', 'django_tool'))
# ../quesadiya/quesadiya/projects
projects_dir = os.path.join(base_dir, "projects")
# create `projects` folder
if not os.path.exists(projects_dir):
    try:
        os.mkdir(projects_dir)
    except PermissionError:
        raise PermissionError(
            "permission is denied to create a project folder under {}. "
            "make sure you have the right permission to create folder, or "
            "try `pip install . --user`".format(base_dir)
        )
# create admin database file and define schema
db_uri = 'sqlite:///' + os.path.join(projects_dir, "admin.db")
engine = create_engine(db_uri, echo=True, encoding="utf-8")
Base.metadata.create_all(engine)


setup(
    name="quesadiya",
    version=__version__,
    author="SiameseLab",
    author_email="underkey256@gmail.com",
    description="data annotation platform for siamese models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SiameseLab/quesadiya",
    keywords=[
        "natural language processing",
        "siamese deep neural network",
        "data annotation"
    ],
    install_requires=[
        "click>=7.1",
        "django>=3.1",
        "sqlalchemy>=1.3.12"
    ],
    tests_require=["pytest>=5.4"],
    entry_points="""
        [console_scripts]
        quesadiya=quesadiya.cli:cli
    """,
    license="Apache License 2.0",
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    package_data={"quesadiya": ["projects/admin.db"] + api_files},
    packages=find_packages(exclude=["test"]),
    zip_safe=False,
)
