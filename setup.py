from __future__ import print_function

import os
import sys
import glob
import sqlite3

from setuptools import setup, find_packages


def get_include_files(directory):
    dir_root = os.path.join(directory, "**/*")
    files = glob.iglob(dir_root, recursive=True)
    return [os.path.join("..", path) for path in files]


__version__ = "0.3"


with open(os.path.join(os.path.dirname(__file__), "README.rst"), "r") as f:
    long_description = f.read()


# base path for initializing folder and database file
# ../quesadiya/quesadiya
base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'quesadiya')
# get all non python files to include
api_files = get_include_files(os.path.join('quesadiya', 'django_tool'))
# check sqlite version
if sqlite3.sqlite_version_info < (3, 6):
    sys.exit(
        "`sqlite >= 3.6` is required for quesadiya (but got sqlite={}). "
        "Please upgrade sqlite and "
        "try installing again.".format(sqlite3.sqlite_version)
    )


setup(
    name="quesadiya",
    version=__version__,
    author="SiameseLab",
    author_email="underkey256@gmail.com",
    description="data annotation platform for siamese models",
    long_description=long_description,
    url="https://github.com/SiameseLab/quesadiya",
    keywords=[
        "natural language processing",
        "siamese deep neural network",
        "data annotation"
    ],
    install_requires=[
        "click>=7.1",
        "click-spinner>=0.1.10",
        "django>=3.1",
        "sqlalchemy>=1.3.12",
        "prettytable>=0.7",
        "jsonlines>=1.2",
        "tqdm>=4.48",
        "argon2-cffi==20.1"
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
    packages=find_packages(),
    zip_safe=False,
)
