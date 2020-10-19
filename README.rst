=========
Quesadiya
=========

.. image:: https://travis-ci.com/SiameseLab/quesadiya.svg?branch=master
    :target: https://travis-ci.com/SiameseLab/quesadiya
    :alt: Build Status
    
.. image:: https://img.shields.io/badge/python-3.6%20%7C%203.7%20%7C%203.8-success
    :target: https://github.com/SiameseLab/quesadiya
    :alt: Supported Python Version

.. image:: https://img.shields.io/badge/docs-available-informational
    :target: https://siameselab.github.io/quesadiya/
    :alt: Docs

Quesdadiya is a data annotation project management platform where you can manage a
project through `Command Line Interface (CLI) <https://siameselab.github.io/quesadiya/build/html/cli.html#cli>`__ and annotate data on
`Web GUI <https://siameselab.github.io/quesadiya/build/html/collaborator.html#collaborator>`__ to generate a triplet data set for developing Siamese models.

Quickstart
==========

Installation
------------
Quesadiya requires `sqlalchemy>=1.3.12`. Install the package by

.. code-block:: bash

  $ pip install sqlalchemy

After installing `sqlalchemy`, run

.. code-block:: bash

  $ pip install quesadiya

Check installation by

.. code-block:: bash

  $ quesadiya --help

Installation from Source
------------------------
#. Make sure your environment has `sqlalchemy>=1.3.12`.
#. `git clone` this repo.
#. `cd quesadiya`.
#. run `pip install .`.
#. check installation by running `quesadiya` on your terminal.

Project Management
==================

Quesadiya provides the command-line interface (CLI) to manage data annotation projects.

Create Project
--------------
You can create a data annotation project by

.. code-block:: bash

  $ quesadiya create <project_name> <admin_name> <datapath> [OPTIONS]

For example,

.. code-block:: bash

  $ quesadiya create queso me data/sample_triplets.jsonl
  Loading input data: 5 row [00:00, 1495.40 row/s]
  Admin password:
  Repeat for confirmation:
  Inserting data. This may take a while...
  Finish creating a new project 'queso'

**Caution**:
`<datapath>` must be a jsonline file, where each row must follow the format below:

.. code-block:: javascript

  {
    "anchor_sample_id": "string (max 100 char)",
    "anchor_sample_text": "list of text", # each element is a paragraph
    "anchor_sample_title": "text (nullable)",
    "candidate_group_id": "string (max 100 char)",
    "candidates": [
      "item": {
        "candidate_sample_id": "string (max 100 char)",
        "candidate_sample_text": "list of text", # each element is a paragraph
        "candidate_sample_title": "text (nullable)"
      }
    ]
  }

`anchor` is the sample you want to compare to the positive sample and the negative sample.
`candidates` is a list of candidates for a positive and a negative sample. The sample collaborator
selects is recorded as a positive sample and `quesadiya` chooses a negative sample from the rest.

**Tips**: You can add collaborators from a jsonline file when you create a project by

.. code-block:: bash

  $ quesadiya create queso me data/triplets.jsonl -a data/collaborators.jsonl

Note that `<collaborator_path>` must be a jsonline file, where each row must follow the format below:

.. code-block:: javascript

  {
    'name': "string (max 150 char)",
    'password': "string (max 128 char)",
    'contact': "string (max 254 char)"
  }

See `Command Line Interface Guide <https://siameselab.github.io/quesadiya/build/html/cli.html#cli>`__ for more details.

Run Project
-----------

You can annotate a data set by running quesadiya:

.. code-block:: bash

  $ quesadiya run [OPTION]

You can specify the port number to run the quesadiya server by option. For example,

.. code-block:: bash

  $ quesadiya run -p 4000

Quesadiya's default port number is `1133`.

Once you run a project, open your browser and access http://localhost:1133/.

Then, select a project and type admin name and password.

This leads you to the admin page. In the admin page, you can do the followings:
  * view discarded samples
  * view progress of each collaborator
  * edit collaborators

**Tips**: Admin user cannot annotate data. If you're the admin and like to annotate
samples, make a collaborator account for yourself and login with the account.

See `Admin Guide <https://siameselab.github.io/quesadiya/build/html/admin.html#admin>`__ for more details.

Data Annotation
---------------

Data annotation is very simple and intuitive in Quesadiya. **Anchor text** is shown
on the left hand side of the screen and **Candidates** are on the right. Collaborators
can either `select` positive sample among candidates or **discard** a sample if the sample is corrupted for some reason.
Admin can view discarded samples and push a sample back to the project in the admin page.

Export Data
-----------

You can export a snapshot of annotated data set by

.. code-block:: bash

  $ quesadiya export <project_name> <output_path>

The output path must be a jsonline file. Each row follows the format below:

.. code-block:: javascript

  {
    "anchor_sample_id": "text",
    "positive_sample_id": "text",
    "negative_sample_id": "text"
  }


Note that this operation requires the admin privilege.

The operation above only generates a triplet data set with samples ids.
If you'd like to include text for each sample, add **-i** option. For example,

.. code-block:: bash

  $ quesadiya export queso data.jsonl -i

This will generate a jsonline file, where each row follows:

.. code-block:: javascript

  {
      "anchor_sample_id": "text",
      "positive_sample_id": "text",
      "negative_sample_id": "text",
      "anchor_sample_text": "list of text" // each element is a paragraph,
      "positive_sample_text": "list of text",
      "negative_sample_text": "list of text"
  }

Security
========

A disclaimer: **Quesadiya** and its contributors take no responsibility for protecting your data.
That said, we encrypt password using  `argon2 <https://pypi.org/project/argon2-cffi/>`__ to encrypt admin password.

If you'd like to prohibit any other user from accessing your data, we encourage you to change the accessibility of
project folder. You can see the path to the quesadiya root by

.. code-block:: bash

  $ quesadiya path

This command shows the absolute path to your project folder.
