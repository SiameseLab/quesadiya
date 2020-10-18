.. _admin:

Login
=====

The admin user can login to a project by opening browser and typing **<ip_address>:<port>**.
For example, http://localhost:1133/.
The admin user can run the quesadiya server by

.. code-block:: bash

  $ quesadiya run

The code above runs the server at port 1133. You can specify the port by

.. code-block:: bash

  $ quesadiya run -p 8000

Once you get to the login page, select your project and enter admin name and password.

.. image:: ../images/login.png
  :width: 400
  :align: center
  :alt: Login

Project Status
==============

Admin can view the current progress of a project in **View Status** tab.
This page shows the progress of each collaborator.

.. image:: ../images/status.png
  :width: 600
  :align: center
  :alt: Project Status

Discarded Samples
=================

Admin can view all discarded samples. To view sample, you can simply click
anchor sample id. If you'd like to push a sample back to the project, you can do so
by clicking **undo** button. Once a sample is pushed back, quesadiya randomly assigns the sample to
a collaborator.

.. image:: ../images/discarded.png
  :width: 600
  :align: center
  :alt: Discarded Samples

Manage Collaborators
====================

Admin can also manage collaborators in **Edit User** tab. You can either add a new
collaborator or remove an existing collaborator in your project.

.. image:: ../images/edit_collaborator.png
  :width: 600
  :align: center
  :alt: Edit Collaborator
