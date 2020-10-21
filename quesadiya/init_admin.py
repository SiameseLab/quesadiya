from sqlalchemy import create_engine

from quesadiya.db.schema import AdminDB
from quesadiya.django_tool.database import django_database

import quesadiya as q
import os


def init_admin():
    # create `projects` folder
    if not os.path.exists(q.get_projects_path()):
        try:
            os.mkdir(q.get_projects_path())
        except PermissionError:
            raise PermissionError(
                "Permission is denied to create a project folder under {}. "
                "Make sure you have the right permission to create folder, or "
                "try `pip install . --user`".format(base_dir)
            )
    # create admin database file and define schema
    db_uri = 'sqlite:///' + os.path.join(q.get_projects_path(), "admin.db")
    engine = create_engine(db_uri, echo=False, encoding="utf-8")
    # creates admin db tables inside
    AdminDB.Base.metadata.create_all(engine)
    # import django table from file
    # create django tables in admin.db
    with engine.connect() as con:
        django_database.create_django_tables(con)
