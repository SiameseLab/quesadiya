import os
import quesadiya


# for more configurations:
# https://docs.sqlalchemy.org/en/13/core/engines.html#sqlalchemy.create_engine
CONFIG_ADMINDB = {
    "echo": False,
    "encoding": "utf-8",
    "pool_pre_ping": True # turn on pessimistic disconnect handling
}
# NOTE: make config customizable in the future
CONFIG_PROJECTDB = {
    "echo": False,
    "encoding": "utf-8",
    "pool_pre_ping": True # turn on pessimistic disconnect handling
}


# path to admin.db
ADMIN_PATH = os.path.join(quesadiya.get_projects_path(), "admin.db")
# project database name
PROJECTDB_NAME = "project.db"
