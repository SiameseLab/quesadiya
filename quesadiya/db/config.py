import os
import quesadiya


# for more configurations:
# https://docs.sqlalchemy.org/en/13/core/engines.html#sqlalchemy.create_engine
CONFIG_ADMINDB = {
    "echo": False,
    "encoding": "utf-8",
    "pool_pre_ping": True # turn on pessimistic disconnect handling
}


ADMIN_PATH = os.path.join(quesadiya.get_projects_path(), "admin.db")
