.. _cli:

Command Line Interface
======================

The Quesadiya command-line interface (CLI) is used to manage your projects.
With the Quesadiya CIL, you can **run**, **create**, **delete**, **inspect**, **modify**
your data annotation projects and **export** annotated data sets . To list
available commands, either run ``quesadiya`` or ``quesadiya --help``.

.. code-block:: bash

  $ quesadiya --help
  Usage: quesadiya [OPTIONS] COMMAND [ARGS]...

    A delicious mexican dish.

  Options:
    --version  Show the version and exit.
    --help     Show this message and exit.

  Commands:
    create   Create a data annotation project.
    delete   Delete project indicated by project name.
    export   Export data associated with a project indicated by project name.
    inspect  Show project information indicated by project name.
    modify   Modify a project indicated by project name.
    path     Print path to this package.
    run      Run annotation project indicated by project name.

.. click:: quesadiya.cli:cli
  :prog: quesadiya
  :show-nested:
