# Data Annotation Project Management Tool

[![TravisCI](https://travis-ci.com/SiameseLab/quesadiya.svg?branch=master)](https://travis-ci.com/SiameseLab/quesadiya)

Quesdadiya is a data annotation platform where users can easily manage
data annotation projects to create data sets for developing Siamese models.
It provides a web UI to ease the burden of annotation. It also provides tools
that allows the data annotation project organizer to manage multiple annotators.

# How to install

1. Quesadiya requires `sqlalchemy>=1.3.12"`. Install the package by `pip install sqlalchemy>=1.3.12`.
1. `git clone` this repo
1. `cd quesadiya`
1. open your python environment
1. run `python setup.py develop`
1. check installation by running `quesadiya` on your terminal

# Commands

Try the following commands to play with quesadiya!

* show version info: `quesadiya --version`
* show help: `quesadiya --help`
* create project: `quesadiya create <project_name>`
* show `create`'s help" `quesadiya create --help`
* inspect project: `quesadiya inspect <project_name>`
* show `inspect`'s help" `quesadiya inspect --help`
* delete project: `quesadiya delete <project_name>`
* show `delete`'s help" `quesadiya delete --help`
* modify project: `quesadiya modify <project_name>`
* show `modify`'s help" `quesadiya modify --help`
* run project: `quesadiya run <project_name>`
* show `run`'s help" `quesadiya run --help`
* export data from project: `quesadiya export <project_name>`
* show `export`'s help" `quesadiya export --help`
