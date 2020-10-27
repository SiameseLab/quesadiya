0.3 (10-24-2020)
================

Bugs
----
* Updated ``Edit Collaborators`` tab so the admin can delete collaborators.
* Fixed ``Add New`` button's issue where there was no button to confirm the
  operation.
* Issue: when the admin deletes a collaborator, a sample assigned to the
  collaborator is still assigned to the collaborator.
  Solution: add lines in ``quesadiya/django_tool/tool/views.py`` to assign -1
  to ``username`` whose value is identical with the deleted collaborator.

Enhancements
------------
* Added an option in ``Discarded`` tab so the admin can view the bodies of
  discarded samples.
* Modified help message of ``quesadiya run``.

Notes
-----
* Beta release.

0.2.2 (10-20-2020)
==================

Bugs
----
* Fixed an ``quesadiya run`` issue by making subprocess executable.
* Fixed a typo in ``setup.py`` so it downloads django package when being
  donwloaded by pip install.

0.2.1 (10-19-2020)
==================

Notes
-----
* Formatted readme.

0.2 (10-19-2020)
================

Bugs
----
* Fixed an upgrading issue: when upgrading ``quesadiya``, ``admin.db`` was removed as well.
  In the new version, ``admin.db`` and project folder are created after installing a package.

Notes
-----
* Beta release.

0.1 (10-19-2020)
================

Notes
-----
* Initial release (beta).
